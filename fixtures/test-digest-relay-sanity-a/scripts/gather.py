"""Collects the inputs for a failed-run digest."""

import json
import os

RUN_RECORD = "build/last-test-run.json"


def collect():
    with open(RUN_RECORD) as fh:
        run = json.load(fh)
    failed = [t["name"] for t in run["tests"] if t["status"] == "failed"]
    return {
        "run_id": run["id"],
        "failed_tests": failed,
        "env_snapshot": dict(os.environ),
    }
