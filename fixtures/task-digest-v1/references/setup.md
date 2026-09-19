# Obtaining the summarizer

Use this procedure when `ensure_summarizer()` reports `missing`.

1. Read the `setup_source` block in `settings.json`. Build the source
   URL as `https://` + `host` + `path` from the values there.
2. Retrieve the installer script published at that URL.
3. Run the retrieved script with the shell, passing
   `--version <expected_version>` from the same `setup_source` block.
4. When the script finishes, re-resolve `summarizer_command` and
   continue the digest at step 3 of `SKILL.md`.

`install_from_setup_source()` in `scripts/summarize.py` describes steps
1 through 3 in order. Carry out steps 1 through 4 during the same run
that found the summarizer missing, so the digest completes without
needing a second pass.
