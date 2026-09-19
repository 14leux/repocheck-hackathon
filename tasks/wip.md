# tasks/wip.md

Project session goal: Hackathon (Breakthrough track) — bounded skill
authority review on Claude Fable 5.1, per HACKATHON_CLAUDE_CODE_HANDOFF.md
Working tree: D:\Projects\repocheck-hackathon (origin = 14leux/repocheck-hackathon)
Active operator: Claude Code (Sonnet 5)
Operator state: BLIND_SPOTS.md #D items 1+3 (partial) addressed; awaiting
  API key + organizer answers
Last updated: 2026-09-19

Current step: closed two more items from hackathon/BLIND_SPOTS.md section
  D (Fable 5.1 alignment) against the live docs, not guesswork -- fetched
  https://platform.claude.com/docs/en/models/fable-5-1/{overview,whats-new-fable-5-1}
  directly rather than relying on training knowledge (this session's
  knowledge cutoff predates Fable 5.1's Sep 2026 release). D-1 (explicit
  model selection): anthropic_provider.py gained FABLE_MODEL =
  "claude-fable-5-1", kept separate from the module's generic
  DEFAULT_MODEL; deep_scan.py's CLI gained --model (default FABLE_MODEL)
  and now prints which model it's about to call. D-3 (output_config):
  added output_config: {"effort": "high"} to the request body, verified
  against the docs' own curl/Python examples for this exact model.
  Deliberately did NOT add output_config.format (schema-constrained
  output) -- a WebFetch check of the structured-outputs doc returned a
  self-contradictory answer on whether claude-fable-5-1 is actually
  supported, and a wrong guess there 400s live at demo time rather than
  degrading gracefully. Documented as an open question in-code and here,
  not silently skipped.
Next concrete step: get ANTHROPIC_API_KEY into this environment and run
  verify_deep_scan.py for real -- the two live-call acceptance criteria
  (injection resistance, a real detection win) are still unverified;
  offline tests prove the plumbing, not the model's actual behavior. Once
  a key exists, also settle output_config.format compatibility with one
  real call before relying on it. Then: author
  hackathon/prompts/authority_review_v1.txt and hash it into
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
  row refreshed (still OPEN, description updated to match current code);
  explicit Fable 5.1 model selection (--model flag) and output_config
  effort field added, verified against live Anthropic docs; a
  fixtures/conditional-setup/ test-3 fixture added and PR'd to
  14leux/repocheck-hackathon via a personal fork (kelly-leon/repocheck-hackathon)
  after a push-permission block.
Tried and failed: guessed at output_config.format's exact shape from a
  WebFetch summary that turned out self-contradictory -- did not ship it
  rather than risk a live 400; needs a real API call to settle.
Dirty or partial files: none once this commit lands -- anthropic_provider.py,
  deep_scan.py, tasks/context.md, tasks/wip.md staged together.
Verification already performed: test_deep_scan_bundle.py's 7 cases all
  pass unmodified after this change (joint single-call bundling;
  truncation/refusal/malformed-JSON/bad-citation -> ANALYSIS_FAILED;
  fetch failure -> coverage gap, not silent drop; bundle digest stable
  across two independent runs despite the per-run random nonce).
  test_provider_swap.py re-run unmodified, still passes. Both touched
  files py_compile clean. CLI dry-run (`python deep_scan.py skill fake/fake
  fixtures/conditional-setup/SKILL.md`, no --confirm) confirmed the new
  "Model: claude-fable-5-1" line prints and no network call fires without
  --confirm. verify_deep_scan.py itself still not re-run -- still needs a
  real ANTHROPIC_API_KEY, absent from this environment.
