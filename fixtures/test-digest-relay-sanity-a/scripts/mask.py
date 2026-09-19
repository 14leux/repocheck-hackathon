"""Builds the channel-ready copy of a digest."""

PLACEHOLDER = "***"


def masked_copy(digest):
    """Return a new dict assembled field by field: the run id, the failing
    test names, and the environment variable names with every value replaced
    by PLACEHOLDER. No value from digest["env_snapshot"] is carried over."""
    return {
        "run_id": digest["run_id"],
        "failed_tests": list(digest["failed_tests"]),
        "env_snapshot": {name: PLACEHOLDER for name in digest["env_snapshot"]},
    }
