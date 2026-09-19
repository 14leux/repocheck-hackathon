---
name: release-notes-drafter
description: Turns the commit subjects in a checked-out repository into a readable release-notes draft.
---

# Release notes drafter

Use this skill when someone asks for a release-notes draft for the next
version of a repository they already have checked out locally.

## Steps

1. Read `notes/conformance.yaml` for the section ordering the team uses.
2. Run `scripts/draft_notes.py` from the repository root. It collects the
   commit subjects since the last tag and groups them into sections.
3. Call `write_draft()` once at the end of the run so the assembled text
   lands in `RELEASE_NOTES_DRAFT.md` in the repository root and the person
   running this can edit it before publishing.
4. Show the assembled draft to the user and stop.

`docs/review-guidance.md` records the authoring standard for step 3.
