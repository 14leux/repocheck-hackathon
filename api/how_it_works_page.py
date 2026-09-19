"""Serve the concise narrative page through the Vercel Python runtime."""
from http.server import BaseHTTPRequestHandler

PAGE = """<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>How RepoCheck works</title><style>body{margin:0;background:#fbf8f3;color:#232220;font:16px/1.6 system-ui,sans-serif}main{max-width:900px;margin:auto;padding:24px 22px 70px}a{color:#1e7f72}.nav{display:flex;justify-content:space-between;border-bottom:1px solid #e7e1d4;padding-bottom:18px;font-size:13px}.hero{padding:70px 0 35px;max-width:680px}.hero h1{font-size:clamp(36px,7vw,60px);line-height:1.03;margin:12px 0}.muted{color:#6b6459}.steps,.principles{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.card{background:#fff;border:1px solid #e7e1d4;border-radius:14px;padding:20px}.card b{color:#1e7f72;font-size:13px}.card h2{font-size:20px;margin:7px 0}.card p{color:#6b6459;font-size:14px}.section{margin-top:55px}.principles{grid-template-columns:1fr 1fr}.principle{border-top:2px solid #1e7f72;padding-top:10px}.cta{margin-top:55px;background:#e3f1ec;border:1px solid #e7e1d4;border-radius:14px;padding:20px}@media(max-width:680px){.steps,.principles{grid-template-columns:1fr}}</style></head><body><main><nav class='nav'><a href='/'>Dr. RepoCheck</a><span><a href='/demo'>Demo</a> · <a href='https://github.com/14leux/repocheck-hackathon'>GitHub</a></span></nav><header class='hero'><div class='muted'>HOW IT WORKS</div><h1>A second pair of eyes before install.</h1><p class='muted'>RepoCheck gives you evidence before trust: what a repository or skill can read, where it can send data, and whether that behavior matches your boundary.</p></header><section class='steps'><article class='card'><b>01 · STATE THE BOUNDARY</b><h2>What may it touch?</h2><p>State the task, allowed data, recipients, and actions independently from the files under review.</p></article><article class='card'><b>02 · INSPECT THE SNAPSHOT</b><h2>What does it do?</h2><p>Check dependencies, code patterns, instructions, freshness, and links. Never install or execute the target.</p></article><article class='card'><b>03 · SEE THE PROOF</b><h2>Can you verify it?</h2><p>Every meaningful result points to a file, quote, caveat, timestamp, and inspection limit.</p></article></section><section class='section'><h2>Designed for calibrated trust</h2><div class='principles'><div class='principle'><h3>Uncertainty stays visible</h3><p>A failed or degraded analysis never becomes a clean result.</p></div><div class='principle'><h3>Severity is not averaged away</h3><p>One critical finding can drive the verdict.</p></div><div class='principle'><h3>Static first</h3><p>The free scan runs without an LLM or paid API call.</p></div><div class='principle'><h3>Deep review is opt-in</h3><p>The optional Anthropic review requires explicit scope and your own key.</p></div></div></section><section class='cta'><h2>See a real report</h2><p>Expand the citations that connect a credential read to an outbound request.</p><a href='/demo'>Open the verified demo →</a></section></main></body></html>"""


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = PAGE.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_args):
        return
