"""Public, bounded static-scan endpoint for the website.

This endpoint accepts public GitHub targets only and never executes or
downloads code from the target.  The process-local limiter is a conservative
starter guard; production traffic should put a durable edge limiter in front
of this function before enabling broad public use.
"""

import json
import os
import sys
import time
from http.server import BaseHTTPRequestHandler

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from web_scan import InvalidTarget, scan_target


MAX_BODY = 4096
WINDOW_SECONDS = 3600
MAX_REQUESTS_PER_WINDOW = 3
_hits = {}


def _client_key(handler):
    # Vercel supplies this header; fall back to a shared bucket locally.
    return (handler.headers.get("x-forwarded-for") or "local").split(",")[0].strip()[:80]


def _allowed(key):
    now = time.time()
    if len(_hits) > 10_000:
        for old_key, timestamps in list(_hits.items()):
            if not timestamps or now - timestamps[-1] >= WINDOW_SECONDS:
                _hits.pop(old_key, None)
    recent = [t for t in _hits.get(key, []) if now - t < WINDOW_SECONDS]
    if len(recent) >= MAX_REQUESTS_PER_WINDOW:
        _hits[key] = recent
        return False
    recent.append(now)
    _hits[key] = recent
    return True


def _json(handler, body, status):
    payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Cache-Control", "no-store")
    handler.send_header("X-Content-Type-Options", "nosniff")
    handler.send_header("Content-Length", str(len(payload)))
    handler.end_headers()
    handler.wfile.write(payload)


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get("content-length", "0"))
        except (TypeError, ValueError):
            return _json(self, {"error": "invalid request size"}, 400)
        if length <= 0 or length > MAX_BODY:
            return _json(self, {"error": "request is empty or too large"}, 413)
        if not _allowed(_client_key(self)):
            return _json(self, {"error": "rate limit reached; try again later"}, 429)
        try:
            body = json.loads(self.rfile.read(length))
            report = scan_target(body.get("target"))
        except (ValueError, TypeError, json.JSONDecodeError) as exc:
            return _json(self, {"error": str(exc) or "invalid request"}, 400)
        except Exception:
            # Do not return provider tracebacks, paths, or environment details.
            return _json(self, {"error": "scan could not complete"}, 503)
        return _json(self, report, 200)

    def log_message(self, *_args):
        # Avoid logging request bodies or target-controlled strings.
        return
