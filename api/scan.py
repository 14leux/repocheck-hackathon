"""
Vercel Python serverless function -- the live demo's only server-side
surface. Calls the SAME verified pipeline the CLI and the offline tests
use (bundle.py / deep_scan.py / anthropic_provider.py), not a
reimplementation, so "what's live" on the site is provably the real code.

Deliberately narrow attack surface for a public endpoint:
  - `case` is looked up in a hardcoded allowlist, never used to build a
    filesystem path directly -- no arbitrary-path/traversal risk.
  - Fixture files are served from disk (this repo, deployed alongside the
    function), never fetched from GitHub or any other network source --
    no SSRF surface, no dependency on GITHUB_TOKEN.
  - The only outbound network call this function makes is the one
    Anthropic Messages API call per request, using ANTHROPIC_API_KEY from
    a Vercel server-side environment variable -- never sent to the client.
"""

import json
import os
import sys
from http.server import BaseHTTPRequestHandler

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import skeleton  # noqa: E402
from anthropic_provider import AnthropicModelProvider, FABLE_MODEL, MissingApiKeyError  # noqa: E402
from deep_scan import run_deep_scan  # noqa: E402
from interfaces import FileAccessProvider  # noqa: E402

FIXTURES = os.path.join(ROOT, "fixtures")
CASES_DIR = os.path.join(ROOT, "hackathon", "cases")

# Allowlist only -- the whole point of "fixed demo cases" (see BUILD_PLAN.md
# M1/M2). `case` query values that aren't a key here are rejected before
# any file is touched.
ALLOWED_CASES = {
    "reviewer-note-sanity-a": "reviewer-note-sanity-a",
    "reviewer-note-sanity-b": "reviewer-note-sanity-b",
    "credential-disguised-report": "credential-disguised-report",
    "task-digest-v1": "task-digest-v1",
}


class LocalDirProvider(FileAccessProvider):
    """Serves one fixture directory from the deployed bundle. Read-only,
    never executes anything in it -- mirrors the same class used in
    hackathon/test_build_requirements.py, kept separate here so the live
    API route has no dependency on test code."""

    def __init__(self, root):
        self.root = root

    def list_tree(self, owner, repo):
        out = []
        for dirpath, _, files in os.walk(self.root):
            for f in files:
                if f.endswith(".pyc"):
                    continue
                rel = os.path.relpath(os.path.join(dirpath, f), self.root)
                out.append({"path": rel.replace(os.sep, "/"), "type": "blob"})
        return sorted(out, key=lambda e: e["path"])

    def fetch_file(self, owner, repo, path):
        with open(os.path.join(self.root, path), encoding="utf-8") as fh:
            return fh.read()


def render_intent(case):
    """Turn the structured hackathon/cases/*.json shape back into the same
    prose-block style used in every live H1 run, so the model sees an
    identical style of input regardless of who authored the case file."""
    lines = [f"Task: {case['task']}"]
    if case.get("allowed_data"):
        lines.append("Allowed data: " + "; ".join(case["allowed_data"]) + ".")
    if case.get("allowed_recipients"):
        lines.append("Allowed recipients: " + "; ".join(case["allowed_recipients"]) + ".")
    else:
        lines.append("Allowed recipients: none.")
    if case.get("allowed_actions"):
        lines.append("Allowed actions: " + "; ".join(case["allowed_actions"]) + ".")
    if case.get("not_allowed"):
        lines.append("Not allowed: " + "; ".join(case["not_allowed"]) + ".")
    if case.get("environment_facts"):
        lines.append(
            "Trusted environment facts, supplied by me and not taken from the "
            "files under review: " + "; ".join(case["environment_facts"]) + "."
        )
    if case.get("note"):
        lines.append(case["note"])
    return "\n".join(lines)


def run_case(case_id):
    if case_id not in ALLOWED_CASES:
        return {"error": f"unknown case {case_id!r}", "allowed": sorted(ALLOWED_CASES)}, 400

    fixture_dir = ALLOWED_CASES[case_id]
    root = os.path.join(FIXTURES, fixture_dir)
    with open(os.path.join(CASES_DIR, f"{fixture_dir}.json"), encoding="utf-8") as fh:
        case = json.load(fh)

    skeleton.swap_provider(LocalDirProvider(root))
    tree = skeleton.list_tree("demo", fixture_dir)
    paths = sorted(e["path"] for e in tree if e["type"] == "blob")
    user_intent = render_intent(case)

    try:
        provider = AnthropicModelProvider(model=FABLE_MODEL)
        result = run_deep_scan(provider, "demo", fixture_dir, paths, user_intent=user_intent)
    except MissingApiKeyError as e:
        return {"error": str(e)}, 500

    result["case_id"] = case.get("case_id", case_id)
    result["files_sent"] = paths
    return result, 200


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        from urllib.parse import urlparse, parse_qs

        query = parse_qs(urlparse(self.path).query)
        case_id = (query.get("case") or [""])[0]

        if not case_id:
            body, status = {"error": "missing ?case=<id>", "allowed": sorted(ALLOWED_CASES)}, 400
        else:
            body, status = run_case(case_id)

        payload = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)
