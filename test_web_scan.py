"""Offline checks for the public target parser and web adapter."""

import io
import json
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import patch

from web_scan import InvalidTarget, parse_github_target, scan_target


class WebScanTests(unittest.TestCase):
    def test_accepts_repo_and_skill_targets(self):
        self.assertEqual(parse_github_target("owner/repo")["mode"], "repo")
        parsed = parse_github_target("https://github.com/owner/repo/blob/main/skills/x/SKILL.md")
        self.assertEqual(parsed["mode"], "skill")
        self.assertEqual(parsed["path"], "skills/x/SKILL.md")

    def test_rejects_non_github_and_traversal(self):
        for target in ("https://example.com/owner/repo", "https://github.com/owner/repo?x=1", "https://github.com/owner/repo/blob/main/../SKILL.md", "owner/repo/extra"):
            with self.assertRaises(InvalidTarget):
                parse_github_target(target)

    def test_adapter_uses_cli_json_contract(self):
        def fake_repo(owner, repo, as_json):
            print(json.dumps({"repo": f"{owner}/{repo}", "mode": "repo", "verdict": "CLEAR", "findings": [], "degraded": [], "scan_timestamp": "test"}))
            return True

        with patch("web_scan.repo_verdict", fake_repo), patch("web_scan.skill_verdict") as skill:
            report = scan_target("owner/repo")
        self.assertEqual(report["scan_status"], "COMPLETE")
        self.assertEqual(report["target"]["owner"], "owner")
        skill.assert_not_called()


if __name__ == "__main__":
    unittest.main()
