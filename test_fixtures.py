#!/usr/bin/env python3
"""
RepoCheck -- differential fixture harness.

Runs the static scanners over matched fixture pairs and asserts BOTH
directions: a malicious fixture must fire, and its legitimate
counterpart must stay clean. A scanner that flags everything and a
scanner that flags nothing both pass a one-sided test; only the pair
tells you the rules actually discriminate.

Three expectations, deliberately distinct:

  DETECTED   -- must produce at least one finding. A regression here
                means a detection rule stopped working.
  CLEAN      -- must produce zero findings. A regression here is a
                false positive, which is just as damaging: a scanner
                nobody trusts is a scanner nobody runs.
  KNOWN_GAP  -- currently produces zero findings, and that is a real
                limitation, recorded rather than hidden. Both pillars
                gate on credential-access and network-send co-occurring
                inside a SINGLE file (code_scan.py's sensitive_hits/
                network_hits check, and the equivalent in skill_scan.py).
                Split the same behaviour across collect.py / schema.json
                / send.py and nothing fires. This is not a tuning
                problem -- a single-file rule structurally cannot see
                across a file boundary.

                If a KNOWN_GAP case ever starts firing, this harness
                reports it as progress and tells you to reclassify it.

All fixtures are inert test data: nothing here is executed by the
harness or by RepoCheck itself (CLAUDE.md non-negotiable), the malicious
ones define functions but run nothing at import, and every endpoint uses
the reserved .test TLD (RFC 2606), which cannot resolve.

Usage:
    python test_fixtures.py
"""

import pathlib
import sys

from code_scan import RULESET_VERSION as CODE_SCAN_VERSION
from code_scan import scan_file_content
from skill_scan import RULESET_VERSION as SKILL_SCAN_VERSION
from skill_scan import scan_skill_content

FIXTURES = pathlib.Path(__file__).parent / "fixtures"

DETECTED = "DETECTED"
CLEAN = "CLEAN"
KNOWN_GAP = "KNOWN_GAP"

# (fixture dir, filename, expectation, why this case exists)
CASES = [
    # --- control: the rules DO work when everything is in one file ---
    ("malicious-single-file", "collect_and_send.py", DETECTED,
     "credential read + network send in the same file"),
    ("malicious-single-file", "SKILL.md", DETECTED,
     "SKILL.md prose naming a credential path and an exfil destination"),

    # --- the legitimate counterpart: must not be flagged ---
    ("legit-aggregate-report", "SKILL.md", CLEAN,
     "same skill shape, no credential anywhere"),
    ("legit-aggregate-report", "collect.py", CLEAN,
     "collects only OS, version, command count"),
    ("legit-aggregate-report", "send.py", CLEAN,
     "posts a report, touches no secret"),
    ("legit-aggregate-report", "schema.json", CLEAN,
     "field map with a benign endpoint"),

    # --- the gap: identical attack, split across files ---
    ("malicious-aggregate-report", "SKILL.md", KNOWN_GAP,
     "delegates to helpers; prose alone names nothing sensitive"),
    ("malicious-aggregate-report", "collect.py", KNOWN_GAP,
     "reads ~/.aws/credentials but has no network call in this file"),
    ("malicious-aggregate-report", "send.py", KNOWN_GAP,
     "network call, but the credential is not named in this file"),
    ("malicious-aggregate-report", "schema.json", KNOWN_GAP,
     "maps the credential into a report field -- never even fetched, "
     "code_scan's SOURCE_EXTENSIONS is code-only"),
]


def scan(fixture_dir, filename):
    """Route a fixture file to the pillar that would see it in a real
    scan: SKILL.md through the skill-mode instruction scan, everything
    else through the repo-mode code scan."""
    path = FIXTURES / fixture_dir / filename
    content = path.read_text()
    if filename == "SKILL.md":
        findings, caveats = scan_skill_content(content)
        return list(findings) + list(caveats)
    return scan_file_content(f"{fixture_dir}/{filename}", content)


def main():
    if not FIXTURES.is_dir():
        print(f"FAIL -- no fixtures directory at {FIXTURES}")
        sys.exit(1)

    print(f"rulesets: {SKILL_SCAN_VERSION} | {CODE_SCAN_VERSION}\n")

    failures = []
    promoted = []

    for fixture_dir, filename, expected, why in CASES:
        findings = scan(fixture_dir, filename)
        fired = bool(findings)

        if expected == DETECTED:
            ok = fired
        elif expected == CLEAN:
            ok = not fired
        else:  # KNOWN_GAP -- documented as currently undetected
            ok = not fired
            if fired:
                promoted.append((fixture_dir, filename))

        status = "ok" if ok else "FAIL"
        print(f"[{status:>4}] {expected:<9} {fixture_dir}/{filename}")
        print(f"              {why}")
        for f in findings:
            print(f"              -> {f}")
        if not ok:
            failures.append((fixture_dir, filename, expected, findings))

    print()
    if promoted:
        # not a failure -- the gap closed. But the harness must not keep
        # silently asserting "still broken" once it isn't.
        print("GAP CLOSED -- these now produce findings and should be "
              "reclassified as DETECTED:")
        for d, f in promoted:
            print(f"  {d}/{f}")
        print()

    if failures:
        print(f"FAIL -- {len(failures)} case(s) did not match expectation")
        for fixture_dir, filename, expected, findings in failures:
            print(f"  {fixture_dir}/{filename}: expected {expected}, "
                  f"got {len(findings)} finding(s)")
        sys.exit(1)

    detected = sum(1 for c in CASES if c[2] == DETECTED)
    clean = sum(1 for c in CASES if c[2] == CLEAN)
    gaps = sum(1 for c in CASES if c[2] == KNOWN_GAP)
    print(f"PASS -- {detected} detected, {clean} clean (no false positives), "
          f"{gaps} known gap(s) still open")


if __name__ == "__main__":
    main()
