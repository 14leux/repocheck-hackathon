# tasks/wip.md

Project session goal: Hackathon (Breakthrough track) — bounded skill
authority review on Claude Fable 5.1, per HACKATHON_CLAUDE_CODE_HANDOFF.md
Working tree: D:\Projects\repocheck-hackathon (origin = 14leux/repocheck-hackathon)
Active operator: Claude Code (Sonnet 5)
Operator state: first live Fable 5.1 results in hand; awaiting Mailu's
  direction on the D-7 refusal finding before continuing fixture work
Last updated: 2026-09-19

Current step: real ANTHROPIC_API_KEY/GITHUB_TOKEN now in .env (pasted by
  Mailu). Hard-first-hour-gate step 2 done for real. Ran the joint-bundle
  pipeline live against claude-fable-5-1, claude-opus-4-8, and
  claude-sonnet-4-5 on an RC-01-shaped fixture plus its legitimate
  counterpart. Found and fixed a real bug (markdown-fenced JSON breaking
  the parser). Surfaced a real, unresolved finding: Fable 5.1 hard-refused
  the credential-exfil fixture while the other two models analyzed it
  correctly; the legit counterpart did not trigger the refusal on Fable.
  Recorded as EXPERIMENT_CARD.md D-7, open, must resolve before freeze.
Next concrete step: decide with Mailu how to handle D-7 — test the
  refusal against the remaining P0 fixture shapes (RC-02 conditional
  setup, RC-04 reviewer manipulation, RC-08 redaction) before drawing any
  conclusion about whether it's a pattern; author
  hackathon/prompts/authority_review_v1.txt and hash it into card §4; get
  organizer answers into card §9; re-cut D-2c with neutral naming and
  out-of-bundle permission, then build its harmful twin D-2 informed by
  what actually triggers a Fable refusal so that test isn't accidentally
  contaminated by an unrelated refusal.
Done so far: clone stood up and pushed; experiment card v0.1 (still
  DRAFT); D-2c fixture; hackathon/BLIND_SPOTS.md design review; bundle.py
  + interfaces.py ModelResponse + anthropic_provider.py timeout/token-cap
  fix + deep_scan.py joint-bundle rewrite (offline-verified, 7/7 then
  9/9 after this session's fence fix); envfile.py + .env.example + local
  .env; live Fable 5.1 smoke test (model/stop_reason/usage/request_id all
  correct, no ZDR 400 — card D-4 resolved); markdown-fence parsing bug
  found live and fixed, re-verified live and offline; 3-model live
  comparison on RC-01-shaped fixture surfaced the D-7 refusal finding;
  KNOWLEDGE.md, EXPERIMENT_CARD.md (D-3/D-4 resolved, D-7 added),
  context.md, .agent/instructions.md OI-020 all updated to match.
Tried and failed: nothing failed outright this round — the markdown-fence
  issue was a real bug caught by testing, not a dead end, and was fixed
  in the same round it was found.
Dirty or partial files: none once this commit lands. .env holds real
  secrets, confirmed git-ignored and absent from git status throughout.
Verification already performed: live Fable 5.1 call (model field, real
  usage, request_id, no ZDR 400). Live 3-model comparison on matched
  harmful/legitimate fixture pairs (fable refuses harmful only; opus-4-8
  and sonnet-4-5 both correct on harmful; all three would need re-running
  under frozen conditions once the card is actually frozen — these were
  exploratory, not measured, runs). Fence-stripping fix re-verified live
  (Sonnet 4.5's exact same fixture now parses to EXCEEDS_SCOPE) and
  offline (2 new tests, 9/9 total pass, including a check that fence-
  stripping does not launder genuinely malformed content into a pass).
  All touched files py_compile clean.
