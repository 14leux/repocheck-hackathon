# tasks/wip.md

Project session goal: Hackathon (Breakthrough track) — bounded skill
authority review on Claude Fable 5.1, per HACKATHON_CLAUDE_CODE_HANDOFF.md
Working tree: D:\Projects\repocheck-hackathon (origin = 14leux/repocheck-hackathon)
Active operator: Claude Code (Sonnet 5)
Operator state: 4 background subagents dispatched, awaiting completion
  notifications. Nothing else should touch fixtures/ or hackathon/results/
  until they report back, to avoid stepping on their in-progress writes.
Last updated: 2026-09-19

Current step: added run_deep_scan(..., user_intent=None) so permission is
  supplied outside the analyzed bundle (closes BLIND_SPOTS.md A-2 at the
  pipeline level -- committed, pushed, 11/11 offline tests pass). Then
  dispatched 4 parallel background subagents (general-purpose, opus) to
  test the D-7 refusal finding against the remaining P0 case shapes and to
  research Breakthrough-differentiating use cases:
  - Agent 1 (RC-02, development-split, safe to build exactly as specced):
    conditional-setup-changes-the-task case, 2 variants x 3 models live,
    report -> hackathon/results/rc02-report.md
  - Agent 2 (RC-04-STYLE SANITY VARIANT ONLY -- RC-04 itself is card H-2,
    a held-out case, so this agent was told to invent a materially
    different scenario testing the same reviewer-manipulation pattern,
    not the literal spec): report -> hackathon/results/rc04-sanity-report.md
  - Agent 3 (RC-08-STYLE SANITY VARIANT ONLY -- RC-08 is card H-1, also
    held-out; same instruction to invent a different scenario): report ->
    hackathon/results/rc08-sanity-report.md
  - Agent 4 (research): Breakthrough-tier use-case ideas that avoid the
    literal-exfil-code shape that triggered the D-7 refusal, plus a
    landscape check against Snyk/Socket/Datadog/Zenity, explicitly scoped
    as development-fixture/demo-narrative input only, NOT satisfying the
    card's held-out (D-6) requirement: report ->
    hackathon/results/breakthrough-usecases.md
  All 4 were explicitly told: no git commands, no edits to any shared
  pipeline file (deep_scan.py/bundle.py/interfaces.py/anthropic_provider.py/
  github_provider.py/envfile.py) or shared checkpoint file (KNOWLEDGE.md,
  DECISIONS.md, MILESTONES.md, tasks/*, .agent/instructions.md,
  EXPERIMENT_CARD.md), and not to attempt to reword fixtures to dodge a
  Fable refusal if one occurs -- observe and report only.
Next concrete step: once all 4 report back, read each hackathon/results/
  *.md report, synthesize whether the D-7 refusal pattern replicates
  across case shapes (or is specific to literal-exfil-code content),
  fold any new pipeline bugs into the shared code myself (subagents were
  told not to touch shared files), update EXPERIMENT_CARD.md D-7 with the
  broader evidence, update KNOWLEDGE.md/context.md/wip.md, review the
  research agent's use-case ideas with Mailu, then a single coordinated
  git add+commit+push covering everything (subagents did not commit).
Done so far (this session, cumulative): clone stood up and pushed;
  experiment card v0.1 (DRAFT); D-2c fixture; hackathon/BLIND_SPOTS.md
  design review; bundle.py + interfaces.py ModelResponse +
  anthropic_provider.py timeout/token-cap fix + deep_scan.py joint-bundle
  rewrite (11/11 offline tests pass after the fence fix and user_intent
  addition); envfile.py + .env.example + local .env (real keys pasted by
  Mailu); live Fable 5.1 smoke test (card D-4 resolved); markdown-fence
  parsing bug found live and fixed; 3-model live comparison on RC-01
  surfaced the D-7 refusal finding (Fable refuses literal exfil code,
  Opus 4.8 and Sonnet 4.5 don't); user_intent parameter added so
  permission lives outside the bundle (closes A-2); 4 parallel subagents
  dispatched to extend the refusal test and research use-cases.
Tried and failed: nothing failed outright this session -- every bug found
  (markdown fences, the missing user_intent path) was caught by testing
  and fixed in the same round.
Dirty or partial files: none in the main working tree as of the last
  commit. The 4 background subagents are currently writing NEW files only
  (their own fixtures/*/ subdirectories and hackathon/results/*.md) --
  expect several untracked files to appear once they finish; do not run
  git add -A until all 4 have reported back and their combined output has
  been reviewed.
Verification already performed: see prior entries above (live Fable call,
  fence-fix re-verification, user_intent placement tests) -- all before
  this round's subagent dispatch. The subagents' own results are not yet
  verified by the orchestrator; treat their self-reported summaries as
  claims to spot-check against their written reports, not as settled fact,
  before folding conclusions into EXPERIMENT_CARD.md or KNOWLEDGE.md.
