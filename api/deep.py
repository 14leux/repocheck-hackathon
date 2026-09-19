"""Anthropic-only deep scope review with request-scoped BYOK keys.

The endpoint is deliberately separate from the free static checker.  A key
is accepted only for a single request, never placed in a URL, and never
returned to the browser.  Durable abuse controls should be added before
opening this route to unrestricted public traffic.
"""

import json
import os
import sys
import time
from http.server import BaseHTTPRequestHandler

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from anthropic_provider import AnthropicModelProvider
from deep_scan import run_deep_scan, select_high_risk_files_repo, select_skill_bundle_files
from skeleton import fetch_all_files, list_tree
from web_scan import InvalidTarget, parse_github_target


MAX_BODY = 12_000
MAX_INTENT_CHARS = 8_000
MAX_KEY_CHARS = 512
_deep_hits = {}
_DEEP_WINDOW_SECONDS = 600
_DEEP_MAX_REQUESTS = 1


def _json(handler, body, status):
    payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Cache-Control", "no-store")
    handler.send_header("X-Content-Type-Options", "nosniff")
    handler.send_header("Content-Length", str(len(payload)))
    handler.end_headers()
    handler.wfile.write(payload)


def _text(value, label):
    if value is None:
        return ""
    if not isinstance(value, str) or len(value) > MAX_INTENT_CHARS:
        raise ValueError(f"{label} is too long")
    return value.strip()


def _list(value, label):
    if value is None:
        return []
    if not isinstance(value, list) or len(value) > 20:
        raise ValueError(f"{label} must be a short list")
    out = []
    for item in value:
        if not isinstance(item, str) or len(item) > 500:
            raise ValueError(f"{label} contains an invalid item")
        out.append(item.strip())
    return [item for item in out if item]


def _intent(body):
    task = _text(body.get("task"), "task")
    if not task:
        raise ValueError("describe the task before requesting a deep review")
    lines = [f"Task: {task}"]
    for key, label in (("allowed_data", "Allowed data"), ("allowed_recipients", "Allowed recipients"), ("allowed_actions", "Allowed actions"), ("not_allowed", "Not allowed")):
        values = _list(body.get(key), label)
        lines.append(f"{label}: " + ("; ".join(values) if values else "none") + ".")
    return "\n".join(lines)


def _allowed(handler):
    key = (handler.headers.get("x-forwarded-for") or "local").split(",")[0].strip()[:80]
    now = time.time()
    recent = [t for t in _deep_hits.get(key, []) if now - t < _DEEP_WINDOW_SECONDS]
    if len(recent) >= _DEEP_MAX_REQUESTS:
        _deep_hits[key] = recent
        return False
    recent.append(now)
    _deep_hits[key] = recent
    return True


def _paths(parsed):
    tree = list_tree(parsed["owner"], parsed["repo"])
    if parsed["mode"] == "skill":
        available = {entry["path"] for entry in tree if entry.get("type") == "blob"}
        if parsed["path"] not in available:
            raise ValueError("the requested SKILL.md was not found in the public snapshot")
        paths = select_skill_bundle_files(parsed["owner"], parsed["repo"], tree, parsed["path"])
    else:
        paths = select_high_risk_files_repo(parsed["owner"], parsed["repo"], tree)
    return tree, paths


def _preflight(parsed, paths):
    fetched = fetch_all_files(parsed["owner"], parsed["repo"], paths)
    included = []
    omitted = []
    total = 0
    for path in paths:
        content = fetched.get(path)
        if isinstance(content, Exception):
            omitted.append({"path": path, "reason": "could not fetch file"})
            continue
        size = len(content.encode("utf-8"))
        total += size
        included.append({"path": path, "bytes": size})
    return {
        "files": included,
        "omitted": omitted,
        "file_count": len(included),
        "bytes": total,
        "estimated_input_tokens": max(1, total // 4),
        "model": os.environ.get("REPOCHECK_WEB_MODEL", "claude-sonnet-4-5"),
        "note": "Estimate only; Anthropic charges apply to your key.",
    }


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get("content-length", "0"))
        except (TypeError, ValueError):
            return _json(self, {"error": "invalid request size"}, 400)
        if length <= 0 or length > MAX_BODY:
            return _json(self, {"error": "request is empty or too large"}, 413)
        try:
            body = json.loads(self.rfile.read(length))
            if body.get("operation", "plan") == "run" and not _allowed(self):
                return _json(self, {"error": "deep-review rate limit reached; try again later"}, 429)
            parsed = parse_github_target(body.get("target"))
            _, paths = _paths(parsed)
            plan = _preflight(parsed, paths)
            if body.get("operation", "plan") == "plan":
                return _json(self, {"target": parsed, "plan": plan}, 200)

            key = body.get("api_key")
            if not isinstance(key, str) or not (20 <= len(key) <= MAX_KEY_CHARS) or any(c in key for c in "\r\n"):
                return _json(self, {"error": "provide a valid Anthropic API key for this review"}, 400)
            intent = _intent(body)
            model = os.environ.get("REPOCHECK_WEB_MODEL", "claude-sonnet-4-5")
            provider = AnthropicModelProvider(model=model, api_key=key, timeout=180, max_tokens=16000)
            result = run_deep_scan(provider, parsed["owner"], parsed["repo"], paths, user_intent=intent)
            # Never return raw model text; it is unnecessary after validation.
            result.pop("raw_response_truncated", None)
            result["target"] = parsed
            result["files_sent"] = paths
            result["model"] = model
            return _json(self, result, 200)
        except (ValueError, TypeError, json.JSONDecodeError, InvalidTarget) as exc:
            return _json(self, {"error": str(exc) or "invalid request"}, 400)
        except Exception:
            # In particular, do not expose Anthropic error bodies or paths.
            return _json(self, {"error": "deep review could not complete"}, 503)

    def log_message(self, *_args):
        return
