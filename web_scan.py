"""Small web adapter around the CLI's structured JSON output.

The web endpoint must use the same scanner as the CLI.  Keeping this adapter
separate makes that contract explicit while avoiding a second scan
implementation in the serverless function.
"""

import io
import json
import re
import threading
from contextlib import redirect_stderr, redirect_stdout
from urllib.parse import urlparse

from verdict import repo_verdict, skill_verdict


_SCAN_LOCK = threading.Lock()
_OWNER_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38}[A-Za-z0-9])?$")
_REPO_RE = re.compile(r"^[A-Za-z0-9_.-]{1,100}$")


class InvalidTarget(ValueError):
    pass


def parse_github_target(raw):
    """Return ``{mode, owner, repo, path}`` for one public GitHub target."""
    if not isinstance(raw, str) or len(raw.strip()) > 2048:
        raise InvalidTarget("paste a GitHub repository or SKILL.md URL")
    value = raw.strip()
    if not value:
        raise InvalidTarget("paste a GitHub repository or SKILL.md URL")

    if "://" not in value and "/" in value:
        parts = value.rstrip("/").split("/")
        if len(parts) != 2:
            raise InvalidTarget("use owner/repo or a GitHub URL")
        owner, repo = parts
        path = None
    else:
        parsed = urlparse(value)
        if parsed.scheme != "https" or parsed.netloc.lower() != "github.com":
            raise InvalidTarget("only public https://github.com targets are supported")
        if parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise InvalidTarget("the GitHub URL must not contain credentials or query parameters")
        parts = [p for p in parsed.path.split("/") if p]
        if len(parts) == 2:
            owner, repo = parts
            path = None
        elif len(parts) >= 5 and parts[2] == "blob":
            owner, repo = parts[:2]
            path = "/".join(parts[4:])
            if not path or path.split("/")[-1].lower() != "skill.md":
                raise InvalidTarget("skill mode requires a GitHub URL ending in SKILL.md")
            if any(piece in (".", "..") for piece in path.split("/")):
                raise InvalidTarget("skill paths may not contain traversal segments")
        else:
            raise InvalidTarget("use a repository URL or a GitHub SKILL.md URL")

    if not _OWNER_RE.fullmatch(owner) or not _REPO_RE.fullmatch(repo):
        raise InvalidTarget("the GitHub owner or repository name is invalid")
    return {"mode": "skill" if path else "repo", "owner": owner, "repo": repo, "path": path}


def scan_target(target):
    """Run the existing CLI scanner and return its JSON report.

    The scanner historically prints JSON as its CLI contract.  Capture that
    output under a process lock so the web adapter still uses the exact same
    pipeline without duplicating security logic.
    """
    parsed = parse_github_target(target)
    stdout, stderr = io.StringIO(), io.StringIO()
    with _SCAN_LOCK, redirect_stdout(stdout), redirect_stderr(stderr):
        if parsed["mode"] == "skill":
            completed = skill_verdict(parsed["owner"], parsed["repo"], parsed["path"], True)
        else:
            completed = repo_verdict(parsed["owner"], parsed["repo"], True)
    try:
        report = json.loads(stdout.getvalue())
    except json.JSONDecodeError as exc:
        raise RuntimeError("the scanner returned an invalid report") from exc
    report["target"] = parsed
    report["scan_status"] = "COMPLETE" if completed and not report.get("degraded") else "INCOMPLETE"
    if report.get("verdict") == "UNKNOWN":
        report["scan_status"] = "INCOMPLETE"
    return report
