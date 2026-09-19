# tasks/wip.md

Project session goal: Hackathon (Breakthrough track) — bounded skill
authority review on Claude Fable 5.1, per HACKATHON_CLAUDE_CODE_HANDOFF.md
Working tree: D:\Projects\repocheck-hackathon (origin = 14leux/repocheck-hackathon)
Active operator: Claude Code (Sonnet 5)
Operator state: D-7 decided (Narrative Option B); D-1 organizer answers is
  now the sole blocker before the card can freeze
Last updated: 2026-09-19

Current step: Mailu chose Narrative Option B ("disclose it as a
  limitation and ask the organizers") over Option A. Updated three
  documents to carry the decision: HACKATHON_CLAUDE_CODE_HANDOFF.md (new
  "Session H1 update" section right after "Purpose of this file",
  documenting the D-7 evidence, the SkillScope differentiation risk, and
  the decision; revised "Two-minute demo" step 8 to state the finding
  honestly instead of "show the result if supported"; revised both Honest/
  Unsafe claims lists — three new safe claims, two new unsafe claims,
  original text preserved, update is additive and dated, not a rewrite);
  hackathon/EXPERIMENT_CARD.md (§1 now states the secondary claim is
  abandoned per its own rule, not massaged; D-7 row changed OPEN -> CLOSED
  with the decided framing; §9 gained a fourth organizer question specific
  to how they weigh a disclosed null/negative model result against the
  track's requirement); KNOWLEDGE.md (decision entry).
Next concrete step: get organizer answers into card §9 -- now the only
  blocking item before freeze (eligibility, comparator, evidence standard,
  plus the new disclosure-framing question). Then author
  hackathon/prompts/authority_review_v1.txt and hash it into card §4.
  Then decide whether to build the official held-out H-1/H-2 (RC-08/RC-04)
  instances now that their sanity variants already characterized the
  refusal boundary, or defer per the card's original held-out timing.
  Then start on the demo narrative around the architecture claim alone,
  since the secondary Fable-advantage claim is no longer part of the
  pitch.
Done so far (this session, cumulative): clone stood up and pushed;
  experiment card v0.1 (DRAFT, now with D-3/D-4/D-7 resolved, D-1 the sole
  blocker); D-2c fixture (known-defective per BLIND_SPOTS.md, superseded
  in practice by four cleaner fixture families built this session);
  hackathon/BLIND_SPOTS.md design review; bundle.py + interfaces.py
  ModelResponse + anthropic_provider.py timeout/token-cap fix +
  deep_scan.py joint-bundle rewrite + user_intent parameter (11/11 offline
  tests pass); envfile.py + .env.example + local .env (real keys pasted
  by Mailu); live Fable 5.1 smoke test (card D-4 resolved); markdown-fence
  parsing bug found live and fixed; D-7 refusal finding confirmed across 4
  independent fixture families with two distinct patterns identified
  (outcome-tracking vs topic-tracking); a genuine Sonnet-4-5 false
  positive found; a recurring Opus-4-8 JSON-parse issue on safe variants
  found (2/2); a serious differentiation risk found via research
  (SkillScope, CCS '26); one operational incident (4 parallel Opus-tier
  subagents hit an account usage cap) survived without losing real work;
  a durable process correction adopted (Sonnet instructs, Haiku/direct
  execution does mechanical work) and saved to persistent memory; D-7
  decided as Narrative Option B, three documents updated to carry it.
Tried and failed: the 4-parallel-Opus-tier-subagent approach hit a real
  account usage limit and got killed mid-run -- not a dead end (results
  were salvageable and the remaining work was cheap to finish directly),
  but a real cost/time lesson already corrected.
Dirty or partial files: none once this commit lands.
Verification already performed: every disposition/stop_reason/citation
  claim in this session's reports was read directly from real API
  responses (either live-observed by the orchestrator or recovered raw
  JSON from a subagent's scratch directory, cross-checked against the
  actual fixture file contents on disk) -- none of it is a subagent's
  self-reported summary taken on faith. The .env key was independently
  retested after the account cap incident and confirmed fully functional
  again before any further live calls were made. The D-7 decision itself
  (Option B) is a direct instruction from Mailu, not an inference --
  quoted verbatim in the KNOWLEDGE.md decision entry.
