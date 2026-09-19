#!/usr/bin/env python3
"""
RepoCheck hackathon -- bounded joint bundle collection.

Why this module exists: deep_scan.py used to call the model once per
file and keep each answer in its own dict entry. Every question the
skill-authority review actually asks is a cross-file question -- a
credential read in one file, renamed in a second, and sent from a
third; a setup branch in SKILL.md that only becomes reachable through
a referenced doc. One file per request makes those questions not hard
but *unanswerable*, and scoring a model for missing a connection it was
never shown is measuring nothing.

So: one request, many files, with hard bounds and an explicit record of
everything the bounds left out.

Three properties this module is responsible for:

1. **Bounded.** Caps on file count, per-file bytes and total bytes. A
   scan that hits a cap says so -- an omitted or truncated file is a
   recorded coverage gap, never a silent absence. "We did not look" and
   "we looked and found nothing" are different claims and the output
   keeps them apart.

2. **Deterministic.** Files are sorted by path and the manifest is
   canonical, so the same snapshot produces the same bundle bytes and
   the same digest on every run. That digest is the snapshot identity
   the experiment card records per run; without it a result cannot say
   which bytes it describes.

3. **Delimiter-spoof resistant.** Boundaries carry a per-bundle random
   nonce. A multi-file bundle makes plain fixed tags meaningfully worse
   than they were for one file: a file can contain text that looks like
   a closing tag and an opening tag for another path, and try to
   impersonate a different file's content or escape the data region
   entirely. A nonce the content cannot predict removes the forgery,
   and file bytes stay exact -- nothing is escaped or rewritten, because
   citation validation later has to match the bytes the model saw.

Note on (3): this is defence in depth, not a proof. A delimiter makes
forging a boundary impractical; it does not make the model immune to
instruction-shaped text sitting legitimately inside the data region.
The system prompt still has to say that content is data, and findings
still have to be read as claims about the input rather than commands
from it.
"""

import hashlib
import json
import secrets

# Defaults chosen for a bounded review pass, not for exhaustive coverage.
# A repo bigger than this is meant to hit the cap and report it.
MAX_FILES = 25
MAX_FILE_BYTES = 40_000
MAX_TOTAL_BYTES = 200_000

# Below this, a truncated tail is more misleading than useful -- an
# almost-empty fragment reads as "we looked at this file" when we did
# not meaningfully look at it. Omit it and say so instead.
MIN_USEFUL_BYTES = 1_024


class BundleFile:
    """One file as it appears in the bundle: what was included, what the
    original was, and whether those differ."""

    def __init__(self, path, content, sha256, original_bytes, included_bytes, truncated):
        self.path = path
        self.content = content
        self.sha256 = sha256
        self.original_bytes = original_bytes
        self.included_bytes = included_bytes
        self.truncated = truncated

    def manifest_entry(self):
        return {
            "path": self.path,
            "sha256": self.sha256,
            "original_bytes": self.original_bytes,
            "included_bytes": self.included_bytes,
            "truncated": self.truncated,
        }


class Bundle:
    """The assembled bundle plus everything needed to defend a result
    that came out of it."""

    def __init__(self, nonce, text, files, coverage_gaps, limits):
        self.nonce = nonce
        self.text = text
        self.files = files
        self.coverage_gaps = coverage_gaps
        self.limits = limits

    @property
    def manifest(self):
        return [f.manifest_entry() for f in self.files]

    @property
    def digest(self):
        """Snapshot identity. Computed over the canonical manifest, not
        over the bundle text, so it is stable across the random nonce --
        two runs of the same files agree, which is the whole point of
        recording it."""
        canonical = json.dumps(self.manifest, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def file_by_path(self, path):
        for f in self.files:
            if f.path == path:
                return f
        return None


def _sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _truncate_to_bytes(text, limit):
    """Cut to at most `limit` UTF-8 bytes without splitting a character."""
    encoded = text.encode("utf-8")
    if len(encoded) <= limit:
        return text, False
    return encoded[:limit].decode("utf-8", errors="ignore"), True


def _pick_nonce(contents):
    """A nonce no supplied content already contains. Collision odds on
    16 random hex chars are negligible; checking anyway costs nothing
    and turns 'negligible' into 'none'."""
    for _ in range(8):
        nonce = secrets.token_hex(8)
        if not any(nonce in c for c in contents):
            return nonce
    raise RuntimeError("could not generate a bundle nonce absent from the content")


def build_bundle(
    files,
    *,
    max_files=MAX_FILES,
    max_file_bytes=MAX_FILE_BYTES,
    max_total_bytes=MAX_TOTAL_BYTES,
    fetch_errors=None,
):
    """
    Assemble a bounded, delimited, deterministic multi-file bundle.

    `files` is any iterable of (path, content) pairs; content must
    already be text. `fetch_errors` is an optional iterable of
    (path, reason) for files the caller could not retrieve -- they
    become coverage gaps, because a file that failed to download is a
    hole in the analysis and has to be visible as one.
    """
    entries = sorted(files, key=lambda pair: pair[0])
    coverage_gaps = []

    for path, reason in (fetch_errors or []):
        coverage_gaps.append({
            "path": path,
            "reason": "fetch-failed",
            "detail": str(reason),
        })

    if len(entries) > max_files:
        for path, _ in entries[max_files:]:
            coverage_gaps.append({
                "path": path,
                "reason": "file-count-cap",
                "detail": f"bundle is capped at {max_files} files",
            })
        entries = entries[:max_files]

    nonce = _pick_nonce([content for _, content in entries])

    included = []
    total_used = 0
    for path, content in entries:
        remaining = max_total_bytes - total_used
        allowed = min(max_file_bytes, remaining)
        if allowed < MIN_USEFUL_BYTES:
            coverage_gaps.append({
                "path": path,
                "reason": "total-byte-cap",
                "detail": f"bundle byte budget ({max_total_bytes}) exhausted before this file",
            })
            continue

        original_bytes = len(content.encode("utf-8"))
        body, truncated = _truncate_to_bytes(content, allowed)
        included_bytes = len(body.encode("utf-8"))
        total_used += included_bytes

        included.append(BundleFile(
            path=path,
            content=body,
            sha256=_sha256_text(content),  # hash of the ORIGINAL, not the cut
            original_bytes=original_bytes,
            included_bytes=included_bytes,
            truncated=truncated,
        ))

        if truncated:
            coverage_gaps.append({
                "path": path,
                "reason": "file-byte-cap",
                "detail": (
                    f"included first {included_bytes} of {original_bytes} bytes; "
                    "the remainder was not analyzed"
                ),
            })

    text = _render(nonce, included)
    limits = {
        "max_files": max_files,
        "max_file_bytes": max_file_bytes,
        "max_total_bytes": max_total_bytes,
        "total_bytes_used": total_used,
    }
    return Bundle(nonce, text, included, coverage_gaps, limits)


def _render(nonce, files):
    open_tag = f"<repocheck-data-{nonce}>"
    close_tag = f"</repocheck-data-{nonce}>"
    parts = [open_tag]
    for index, f in enumerate(files, start=1):
        parts.append(
            f'<file-{nonce} index="{index}" path="{f.path}" sha256="{f.sha256}" '
            f'bytes="{f.included_bytes}" truncated="{str(f.truncated).lower()}">'
        )
        parts.append(f.content)
        parts.append(f"</file-{nonce}>")
    parts.append(close_tag)
    return "\n".join(parts)


def describe_gaps(bundle):
    """One line per gap, for the human-readable report. A scan that
    looked at part of something says which part."""
    return [f"{g['path']}: {g['reason']} -- {g['detail']}" for g in bundle.coverage_gaps]
