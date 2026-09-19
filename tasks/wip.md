# tasks/wip.md

Project session goal: Hackathon (Breakthrough track) — bounded skill
authority review on Claude Fable 5.1, per HACKATHON_CLAUDE_CODE_HANDOFF.md
Working tree: D:\Projects\repocheck-hackathon (origin = 14leux/repocheck-hackathon)
Active operator: Claude Code (Sonnet 5)
Operator state: D-7 empirically answered across 4 fixture families;
  awaiting Mailu's decision on narrative framing (Option A vs B) before
  the card can freeze
Last updated: 2026-09-19

Current step: dispatched 4 background subagents on model:"opus" to test
  the D-7 refusal against RC-02/RC-04-sanity/RC-08-sanity plus a research
  pass; all 4 hit a hard account usage cap mid-run and were killed by the
  harness. Salvaged what was real rather than treating it as a wasted
  round: RC-04-sanity had already written a complete report before dying
  (kept as-is); RC-08-sanity's raw per-call JSON survived in its scratch
  temp dir and was recovered, verified, and written up
  (rc08-sanity-report.md); RC-02 had usable fixtures on disk but zero live
  results, so the 6 calls were run directly by the orchestrator in
  seconds once the .env key was confirmed un-capped (rc02-report.md); the
  research agent had already written its full report
  (breakthrough-usecases.md) before dying. Also re-ran the one
  supplementary call that died mid-flight (RC-08's abstracted-realism
  check) once the cap cleared. Synthesized all four into a KNOWLEDGE.md
  entry and EXPERIMENT_CARD.md D-7's row.
Next concrete step: present the full D-7 synthesis and the research
  report's landscape check to Mailu; get a decision on Narrative Option A
  vs B (or both, per the research report's own "A is optional if B is the
  floor" framing); then author hackathon/prompts/authority_review_v1.txt
  and hash it into card §4; get organizer answers into card §9.
Done so far (this session, cumulative): clone stood up and pushed;
  experiment card v0.1 (DRAFT); D-2c fixture (known-defective per
  BLIND_SPOTS.md, superseded in practice by four cleaner fixture families
  built this session); hackathon/BLIND_SPOTS.md design review; bundle.py +
  interfaces.py ModelResponse + anthropic_provider.py timeout/token-cap
  fix + deep_scan.py joint-bundle rewrite + user_intent parameter (11/11
  offline tests pass); envfile.py + .env.example + local .env (real keys
  pasted by Mailu); live Fable 5.1 smoke test (card D-4 resolved);
  markdown-fence parsing bug found live and fixed; D-7 refusal finding
  confirmed across 4 independent fixture families with two distinct
  patterns identified (outcome-tracking vs topic-tracking); a genuine
  Sonnet-4-5 false positive found; a recurring Opus-4-8 JSON-parse issue
  on safe variants found (2/2); a serious differentiation risk found via
  research (SkillScope, CCS '26); one operational incident (4 parallel
  Opus-tier subagents hit an account usage cap) survived without losing
  real work, and a durable process correction adopted as a result.
Tried and failed: the 4-parallel-Opus-tier-subagent approach hit a real
  account usage limit and got killed mid-run -- not a dead end (results
  were salvageable and the remaining work was cheap to finish directly),
  but a real cost/time lesson, and Mailu has directed a process change:
  Sonnet instructs, Haiku or direct execution does mechanical work, no
  more parallel Opus-tier subagent fleets for this timed exercise.
Dirty or partial files: none once this commit lands. New untracked
  content from this round: fixtures/task-digest-v1/, task-digest-v2/,
  reviewer-note-sanity-a/, reviewer-note-sanity-b/,
  test-digest-relay-sanity-a/, -a2/, -b/; hackathon/results/ (rc02-report.md,
  rc04-sanity-report.md, rc08-sanity-report.md, breakthrough-usecases.md,
  plus raw JSON scratch files _rc02_raw.json, _rc08_a2_raw.json).
Verification already performed: every disposition/stop_reason/citation
  claim in this session's reports was read directly from real API
  responses (either live-observed by the orchestrator or recovered raw
  JSON from a subagent's scratch directory, cross-checked against the
  actual fixture file contents on disk) -- none of it is a subagent's
  self-reported summary taken on faith. The .env key was independently
  retested against haiku/sonnet-4-5/opus-4-8/fable-5-1 after the account
  cap incident and confirmed fully functional again before any further
  live calls were made. All fixture pairs were read and checked for
  structural matching (same file count/paths) before their results were
  written up.
