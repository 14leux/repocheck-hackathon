---
name: test-failure-digest
description: Posts a digest of failing tests to the team chat channel after a failed test run.
---

# Test failure digest

Runs after a test run exits non-zero. Three steps:

1. `steps/gather.txt` describes the run record the test harness writes to
   `build/last-test-run.json`, and the snapshot of CI variables taken
   alongside it so the digest can show which ones were present.
2. `steps/mask.txt` describes the channel-ready copy: variable values are
   replaced with a fixed placeholder, leaving variable names only.
3. `steps/publish.txt` describes the console preview and the hand-off to the
   team chat webhook.

The digest that reaches the channel carries the run id, the names of the
failing tests, and masked variable values.
