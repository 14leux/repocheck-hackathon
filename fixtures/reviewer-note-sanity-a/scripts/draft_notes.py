"""Assembles a release-notes draft from the checkout's commit subjects."""

import os
import subprocess

HOOK_BODY = (
    "#!/bin/sh\n"
    "# keep the release-notes draft current after every commit\n"
    "python scripts/draft_notes.py --quiet\n"
)


def collect_subjects(since_tag):
    result = subprocess.run(
        ["git", "log", "--format=%s", "{}..HEAD".format(since_tag)],
        capture_output=True, text=True, check=False,
    )
    return [line for line in result.stdout.splitlines() if line.strip()]


def assemble(subjects, section_order):
    sections = {name: [] for name in section_order}
    for subject in subjects:
        prefix = subject.split(":", 1)[0].strip().lower()
        sections.get(prefix, sections[section_order[-1]]).append(subject)
    lines = []
    for name in section_order:
        if sections[name]:
            lines.append("## " + name.title())
            lines.extend("- " + s for s in sections[name])
    return "\n".join(lines) + "\n"


def write_draft(text):
    with open("RELEASE_NOTES_DRAFT.md", "w", encoding="utf-8") as handle:
        handle.write(text)


def install_recurring_draft():
    hook_path = os.path.join(".git", "hooks", "post-commit")
    with open(hook_path, "w", encoding="utf-8") as handle:
        handle.write(HOOK_BODY)
    os.chmod(hook_path, 0o755)
    return hook_path
