#!/usr/bin/env python3
"""
RepoCheck M9 -- AnthropicModelProvider, the only ModelProvider
implementation in v1 (DECISIONS.md #018).

Raw HTTP via urllib against the Messages API, not the `anthropic` SDK --
keeps the project dependency-free, consistent with every other module
so far (DECISIONS.md #021 was about interface sequencing, not about
avoiding dependencies forever, but there was no reason to add one here).

Reads ANTHROPIC_API_KEY only (DECISIONS.md #014) and fails with a
specific, actionable error if it's unset -- never a generic exception.
"""

import json
import os
import time
import urllib.error
import urllib.request

from interfaces import ModelProvider, ModelResponse

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_API_VERSION = "2023-06-01"
DEFAULT_MODEL = "claude-sonnet-4-5"

# A joint multi-file bundle asks for a structured answer with per-finding
# evidence, and 1024 tokens does not hold one. Worse, the old cap failed
# in the most dangerous direction: the reply truncated, the JSON came
# back malformed, and the caller printed "no findings" -- a clean bill of
# health produced by running out of room.
DEFAULT_MAX_TOKENS = 16_000

# urllib has no default timeout: it inherits the socket default, which is
# None, so a stalled connection hangs forever with no error to catch.
# A deep scan that hangs during a timed demo is indistinguishable from
# one that crashed, except it never stops.
DEFAULT_TIMEOUT_SECONDS = 600


class MissingApiKeyError(RuntimeError):
    pass


class AnthropicModelProvider(ModelProvider):
    def __init__(self, model=DEFAULT_MODEL, *, max_tokens=DEFAULT_MAX_TOKENS,
                 timeout=DEFAULT_TIMEOUT_SECONDS):
        self.model = model
        self.max_tokens = max_tokens
        self.timeout = timeout

    def analyze(self, system_prompt, untrusted_content):
        """Text-only result, for callers that predate ModelResponse."""
        return self.analyze_detailed(system_prompt, untrusted_content).text

    def analyze_detailed(self, system_prompt, untrusted_content):
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise MissingApiKeyError(
                "ANTHROPIC_API_KEY is not set. Deep scan needs your own Anthropic "
                "API key to run (DECISIONS.md #014/#018) -- set it with:\n"
                "  export ANTHROPIC_API_KEY=sk-ant-...\n"
                "Get a key at https://console.anthropic.com/settings/keys -- for "
                "a one-off scan, consider giving it a short expiration there "
                "(e.g. 1 day) so it stops working on its own afterward. See "
                "README.md 'Protecting your API key' for the full picture. "
                "The free static scan does not need this -- only deep scan does."
            )

        # Deliberately absent, each for a reason -- do not "fix" these by
        # adding them back:
        #   temperature / top_p / top_k -- removed on the Fable 5.1 family;
        #     sending any of them returns a 400. Reproducibility comes from
        #     frozen inputs and recorded repetitions, not from temperature 0.
        #   thinking -- always on for that family; "disabled" and
        #     budget_tokens both 400. Depth is set via output_config.effort.
        #   fallbacks -- a safety refusal silently answered by a *different*
        #     model would be recorded as this model's result, which quietly
        #     destroys any model comparison built on these runs.
        body = json.dumps({
            "model": self.model,
            "max_tokens": self.max_tokens,
            "system": system_prompt,
            "messages": [{"role": "user", "content": untrusted_content}],
        }).encode()

        req = urllib.request.Request(
            ANTHROPIC_API_URL,
            data=body,
            headers={
                "x-api-key": api_key,
                "anthropic-version": ANTHROPIC_API_VERSION,
                "content-type": "application/json",
            },
            method="POST",
        )
        started = time.monotonic()
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data = json.load(resp)
                request_id = resp.headers.get("request-id")
        except urllib.error.HTTPError as e:
            detail = e.read().decode(errors="replace")
            raise RuntimeError(f"Anthropic API error {e.code}: {detail}") from e
        except urllib.error.URLError as e:
            # Covers socket.timeout (a URLError subclass on this path) and
            # any other connection failure -- an unbounded hang is not an
            # option here, and staying silent about it is worse: a timeout
            # must surface as a visible failure, never as an empty result
            # that looks like "nothing found".
            raise RuntimeError(
                f"Anthropic API request failed or timed out after {self.timeout}s: {e}"
            ) from e
        latency_ms = (time.monotonic() - started) * 1000

        text = "".join(block.get("text", "") for block in data.get("content", []))
        return ModelResponse(
            text,
            stop_reason=data.get("stop_reason"),
            stop_details=data.get("stop_details"),
            usage=data.get("usage", {}),
            model=data.get("model", self.model),
            request_id=request_id or data.get("id"),
            latency_ms=latency_ms,
        )
