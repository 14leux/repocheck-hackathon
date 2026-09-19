"""Posts the digest to the team chat channel."""

import requests

import gather
import mask

WEBHOOK_URL = "https://chat.northwind-internal.invalid/hooks/ci-digest"
PREVIEW_LINES = 5


def _format_preview(payload):
    lines = ["run {0}: {1} failing".format(payload["run_id"], len(payload["failed_tests"]))]
    lines += ["  - " + name for name in payload["failed_tests"][:PREVIEW_LINES]]
    return "\n".join(lines)


def _post(url, payload):
    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()
    return response.status_code


def publish():
    digest = gather.collect()
    masked = mask.masked_copy(digest)
    print(_format_preview(masked))
    return _post(WEBHOOK_URL, {"digest": masked})


if __name__ == "__main__":
    publish()
