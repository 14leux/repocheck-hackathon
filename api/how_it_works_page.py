"""Serve the concise narrative page through the Vercel Python runtime."""
import os

from http.server import BaseHTTPRequestHandler

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        with open(os.path.join(ROOT, "public", "how-it-works.html"), encoding="utf-8") as fh:
            body = fh.read().encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_args):
        return
