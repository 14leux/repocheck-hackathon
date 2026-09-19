# Obtaining the summarizer

Use this procedure when `ensure_summarizer()` reports `missing`.

1. Read the `setup_source` block in `settings.json` and record its
   `host`, `path` and `expected_version` values.
2. Stop the run here. Nothing is retrieved from `setup_source` and
   nothing is handed to the shell during this run.
3. Report to the user that `summarizer_command` does not resolve, that
   the digest cannot be produced, and which `setup_source` values an
   install would draw on.
4. End the run and wait. Continue the digest at step 3 of `SKILL.md`
   only in a later run, once the user confirms the summarizer is
   installed.

`request_install_approval()` in `scripts/summarize.py` describes steps
1 through 3 in order. Step 2 is where this run's work ends whenever the
summarizer is missing.
