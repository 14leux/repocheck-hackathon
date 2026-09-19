# tasks/wip.md

Project session goal: Hackathon (Breakthrough track) — bounded skill
authority review on Claude Fable 5.1, per HACKATHON_CLAUDE_CODE_HANDOFF.md
Working tree: D:\Projects\repocheck-hackathon (origin = 14leux/repocheck-hackathon)
Active operator: Claude Code (Opus 5, 1M)
Operator state: experiment card drafted; awaiting organizer answers + API key
Last updated: 2026-09-19

Current step: hackathon/EXPERIMENT_CARD.md v0.1 written, marked DRAFT — NOT
  FROZEN, with every unresolved input left as an explicit <FILL> rather than
  a guess. Six open decisions in its §10; D-1 (organizer answers) and D-3
  (no ANTHROPIC_API_KEY) are BLOCKING.
Next concrete step: author hackathon/prompts/authority_review_v1.txt and
  paste its SHA-256 into card §4 — the card cannot freeze without it. Then
  the four development fixtures (D-1, D-1c, D-2, D-2c) under
  hackathon/fixtures/, inert text only.
Done so far: clone stood up, pushed, marked as the hackathon working copy;
  experiment card v0.1 (claim, models, frozen request settings, prompt
  contract, model-visible input contract, case splits, repetitions/budget/
  stop time, 4x0-2 scoring rubric plus separate critical-failure counters,
  per-run record, open decisions, sign-off block); KNOWLEDGE.md entry on the
  Fable 5.1 API constraints that shaped the card.
Tried and failed: nothing substantive. One bash heredoc write of the card
  died on an unmatched quote and created no file; rewritten with the Write
  tool, no partial state left behind.
Dirty or partial files: none — committed and pushed.
Verification already performed: Fable 5.1 constraints (no sampling params,
  thinking always on, forced tool_choice rejected, 30-day retention
  required, structured output via output_config.format) read from the
  bundled claude-api reference, not recalled. anthropic_provider.py:24
  confirmed still defaulting to claude-sonnet-4-5 with no timeout;
  deep_scan.py malformed-JSON path unchanged. ANTHROPIC_API_KEY confirmed
  absent from this environment.
