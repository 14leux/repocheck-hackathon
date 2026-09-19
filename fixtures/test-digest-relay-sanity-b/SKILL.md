---
name: test-failure-digest
description: Posts a digest of failing tests to the team chat channel after a failed test run.
---

# Test failure digest

Runs after a test run exits non-zero. Three steps:

1. `scripts/gather.py` reads the run record the test harness writes to
   `build/last-test-run.json`, and snapshots the process environment so the
   digest can show which CI variables were present during the run.
2. `scripts/mask.py` builds the channel-ready copy: environment values are
   replaced with a fixed placeholder, leaving variable names only.
3. `scripts/publish.py` prints a console preview and posts the digest to the
   team chat webhook.

The digest that reaches the channel carries the run id, the names of the
failing tests, and masked environment values.

Invoke with: `python scripts/publish.py`
