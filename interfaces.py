#!/usr/bin/env python3
"""
RepoCheck M7 -- pluggable interfaces, extracted from M2-M6's working
code rather than designed in advance (DECISIONS.md #021).

FileAccessProvider is a real extraction: every one of skeleton.py,
skill_scan.py, code_scan.py, freshness_scan.py, and verdict.py already
depended on exactly two operations (list a repo's file tree, fetch one
file's content) via skeleton.py's module-level `list_tree`/`fetch_file`.
That existing chokepoint is what made this extraction cheap -- GitHub is
the only implementation shipped (DECISIONS.md #012), but the interface
now exists so a GitLab/Bitbucket implementation can be added later
without touching any calling code.

ModelProvider is forward-defined, not extracted -- M9 (opt-in deep
scan) hasn't been built yet, so there is no working code to extract it
from. Defined now so M9 can be written directly against the interface
(DECISIONS.md #018), but its "swap and prove nothing breaks" claim
can't be demonstrated the same way FileAccessProvider's can until M9
exists to call it.
"""

from abc import ABC, abstractmethod


class FileAccessProvider(ABC):
    @abstractmethod
    def list_tree(self, owner, repo):
        """Return a list of {"path": str, "type": "blob"|"tree", ...} entries
        for the repo's default branch, recursive."""
        raise NotImplementedError

    @abstractmethod
    def fetch_file(self, owner, repo, path):
        """Return the raw text content of one file."""
        raise NotImplementedError

    def fetch_all_files(self, owner, repo, paths):
        """
        Fetch many files at once. Default implementation is one
        fetch_file() call per path -- correct for any provider, but not
        the point of this method. A provider that can fetch a whole
        repo in one call (e.g. GitHub's tarball endpoint, see
        GithubFileAccessProvider -- OI-017's fix) should override this:
        the code red-flag pillar was costing up to 300 separate GitHub
        contents-API calls per scan, one per candidate file, which is a
        real scaling problem for very large repos independent of
        OI-019's wall-clock concurrency fix.

        Returns {path: content_or_Exception} -- a single path's failure
        must not raise and abort the whole batch, matching what callers
        already expect from a per-file fetch_file() try/except loop.
        """
        result = {}
        for path in paths:
            try:
                result[path] = self.fetch_file(owner, repo, path)
            except Exception as e:
                result[path] = e
        return result

    def fetch_repo_description(self, owner, repo):
        """
        Return the host's own one-line repo description (e.g. GitHub's
        "About" blurb), or None if unavailable. Default implementation
        returns None -- a provider that has no such metadata (or hasn't
        implemented this yet) degrades to verdict.py's README-paragraph
        fallback rather than raising.
        """
        return None


class ModelResponse:
    """
    One model call's result, including the parts that decide whether the
    text can be trusted at all.

    `text` alone is not enough. A response truncated at the token cap
    and a response that finished normally are the same string shape, and
    so is a safety refusal -- all three arrive as "some text". A caller
    that only looks at `text` reads a cut-off answer as a complete one,
    which for a security tool means reading "I did not finish" as "I
    found nothing". `stop_reason` is what separates them.

    `usage`, `model` and `request_id` are here because the experiment
    card requires them in every run record; a result that cannot say
    which model produced it, at what cost, is not evidence.
    """

    def __init__(self, text, *, stop_reason=None, stop_details=None,
                 usage=None, model=None, request_id=None, latency_ms=None):
        self.text = text
        self.stop_reason = stop_reason
        self.stop_details = stop_details
        self.usage = usage or {}
        self.model = model
        self.request_id = request_id
        self.latency_ms = latency_ms

    @property
    def truncated(self):
        return self.stop_reason == "max_tokens"

    @property
    def refused(self):
        return self.stop_reason == "refusal"

    def run_record(self):
        return {
            "model": self.model,
            "stop_reason": self.stop_reason,
            "stop_details": self.stop_details,
            "usage": self.usage,
            "request_id": self.request_id,
            "latency_ms": self.latency_ms,
        }


class ModelProvider(ABC):
    @abstractmethod
    def analyze(self, system_prompt, untrusted_content):
        """
        Run the deep-scan reasoning pass. `untrusted_content` must be
        structurally delimited by the caller so it is never interpreted
        as instructions (DECISIONS.md #016, non-negotiable) -- this
        method's job is to call the model, not to enforce that
        delimiting itself.

        Returns the response text only. Kept unchanged so existing
        callers and any other implementation keep working; new code that
        needs to tell a truncated answer from a complete one should call
        analyze_detailed() instead.
        """
        raise NotImplementedError

    def analyze_detailed(self, system_prompt, untrusted_content):
        """
        The same call, returning a ModelResponse instead of a bare
        string.

        The default implementation wraps analyze(), so a provider that
        has not been updated still works -- it just reports every field
        except the text as unknown. An implementation that can see the
        real stop reason and usage should override this. A
        `stop_reason` of None means "this provider cannot tell you",
        which a caller must treat as unverified rather than as success.
        """
        return ModelResponse(self.analyze(system_prompt, untrusted_content))
