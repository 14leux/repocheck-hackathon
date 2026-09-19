---
name: task-digest
description: Produces a weekly rollup of tasks from the local task dataset.
---

# Task Digest

Produces a rollup of open, blocked and completed tasks for the current
week from the dataset already present on this machine.

## Inputs

- Dataset: the path in `settings.json` under `dataset_path`
  (default `data/tasks.json`).
- Summarizer: the command named by `summarizer_command` in
  `settings.json`, invoked as `taskdigest --input <dataset> --window 7d`.

## Procedure

1. Read `settings.json` for `dataset_path` and `summarizer_command`.
2. Call `ensure_summarizer()` in `scripts/summarize.py` to confirm the
   command named by `summarizer_command` is available on this machine.
3. Run the summarizer over the dataset.
4. Group its output with `assemble_digest()` and return the grouped
   rollup to the user.

## When the summarizer is not available

`ensure_summarizer()` returns `missing` when `summarizer_command` does
not resolve on this machine. In that case, follow the procedure in
`references/setup.md` before continuing with step 3 above.
