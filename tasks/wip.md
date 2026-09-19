# tasks/wip.md

Project session goal: Hackathon (Breakthrough track) — bounded skill
authority review on Claude Fable 5.1, per HACKATHON_CLAUDE_CODE_HANDOFF.md
Working tree: D:\Projects\repocheck-hackathon (origin = 14leux/repocheck-hackathon)
Active operator: Claude Code (Sonnet 5)
Operator state: bundle collection fixed and verified offline; awaiting API key + organizer answers
Last updated: 2026-09-19

Current step: fixed the top implementation blind spot from
  hackathon/BLIND_SPOTS.md (C-1) — deep_scan.py called the model once per
  file, so no cross-file case was answerable. New bundle.py collects a
  bounded, delimited, deterministic joint bundle; interfaces.py gained
  ModelResponse + analyze_detailed() so stop_reason/usage/model are no
  longer discarded; anthropic_provider.py's max_tokens went 1024->16000
  plus a real timeout; deep_scan.py's run_deep_scan() now makes one joint
  request, validates every citation against the exact bytes sent, and
  maps malformed JSON/refusal/truncation to ANALYSIS_FAILED instead of an
  empty findings list.
Next concrete step: get ANTHROPIC_API_KEY into this environment and run
  verify_deep_scan.py for real -- the two live-call acceptance criteria
  (injection resistance, a real detection win) are still unverified;
  offline tests prove the plumbing, not the model's actual behavior.
  Then: author hackathon/prompts/authority_review_v1.txt and hash it into
  EXPERIMENT_CARD.md section 4; get organizer answers into section 9;
  re-cut fixtures/legit-permission-gated-setup (D-2c) with neutral naming
  and out-of-bundle permission per BLIND_SPOTS.md section A, then build
  its harmful twin D-2.
Done so far: clone stood up, pushed, marked as the hackathon working copy;
  experiment card v0.1 (DRAFT, not frozen); D-2c fixture committed;
  hackathon/BLIND_SPOTS.md design review (7 fixture defects, 3 case-matrix
  gaps, 3 implementation blind spots); bundle.py + interfaces.py
  ModelResponse + anthropic_provider.py timeout/token-cap fix +
  deep_scan.py joint-bundle rewrite; test_deep_scan_bundle.py (7 cases,
  offline, all pass); KNOWLEDGE.md entries for the Fable 5.1 API
  constraints and for this session's fix; .agent/instructions.md OI-020
  row refreshed (still OPEN, description updated to match current code).
Tried and failed: nothing substantive this round.
Dirty or partial files: none once this commit lands -- bundle.py,
  interfaces.py, anthropic_provider.py, deep_scan.py,
  test_deep_scan_bundle.py, KNOWLEDGE.md, .agent/instructions.md,
  tasks/context.md, tasks/wip.md all staged together.
Verification already performed: test_deep_scan_bundle.py's 7 cases all
  pass (joint single-call bundling; truncation/refusal/malformed-JSON/
  bad-citation -> ANALYSIS_FAILED; fetch failure -> coverage gap, not
  silent drop; bundle digest stable across two independent runs despite
  the per-run random nonce). test_provider_swap.py re-run unmodified,
  still passes -- FileAccessProvider contract untouched. Confirmed
  analyze() still returns a bare string (mocked analyze_detailed) so
  verify_deep_scan.py's existing string-based checks are not broken by
  the refactor, though verify_deep_scan.py itself was not re-run (still
  needs a real ANTHROPIC_API_KEY, absent from this environment). All
  touched files py_compile clean.
