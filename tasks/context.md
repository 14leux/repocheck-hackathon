# tasks/context.md

**Status:** CLOSED

## Full close, re-entry continuation (2026-09-20)

**Goal of this continuation:** reopen after finding another operator's
work on `main`, review 2 more community PRs against the live demo, and
close cleanly again.

**What was done:**
1. Re-entry: found 7 commits landed directly on `main` since the last
   close, all Mailu's own (free-tier arbitrary-repo scan, BYOK deep-scan
   path, narrative page split). Verified rather than assumed: all
   offline tests still pass, live site still 200s on all three routes.
2. Reviewed PR #3 ("ui changes") — actually a `claude-opus-4-8` →
   `claude-opus-5` comparator swap plus a genuinely good, separable
   defensive fix. Verified live on the PR branch: opus-5 refuses 2 of 4
   cached cases with Fable's own refusal category, which would have
   broken the site's flagship case panel and changed the disclosure
   table's central contrast. Took only the fix (`78bf909`, cache/model-
   mismatch guard); kept the comparator pinned (DECISIONS.md #031). PR
   closed with the reasoning explained in a comment.
3. Reviewed and merged whole PR #4 ("Say the verdict in plain words") —
   plain-language flag system. Verified by deploying the branch to an
   isolated throwaway Vercel project before merging, not just reading
   the diff: confirmed `ANALYSIS_FAILED` correctly maps to grey "NO
   RESULT", never green. Merged (`4b6f500`), deployed to production,
   confirmed live. PR closed. Throwaway preview project deleted.
4. Full codebase-map reconcile — caught a real bug in the reconcile
   method itself (a prose mention of `api/` was making every unmapped
   `api/*.py` file falsely appear covered); fixed the extraction to
   only count actual table rows, then found 6 genuinely undocumented
   files and 2 dead orphaned static files, all now in the map.

**Live result, unchanged in substance from the last close, verified
again:** `https://repocheck-hackathon.vercel.app` — comparator still
`claude-opus-4-8`, flagship credential-disguised-report case still
shows its compelling `EXCEEDS_SCOPE` finding, now with a plain-language
flag layer on top.

**Not done, carried forward (new this stretch):**
- OI-024: why `claude-opus-5` refuses the same 2 cases Fable refuses —
  deliberately not investigated, per direct instruction to present
  rather than dig, given the demo deadline.
- OI-025: `public/demo.html`/`public/how-it-works.html` are dead,
  unreferenced static files — not deleted, not this session's call.
- Everything carried forward from the previous close (OI-022/OI-023,
  the backup recording and rehearsal, the 17 open P0 acceptance-test
  items) is still open, untouched this stretch.

**Known blockers:** none blocking the live demo.

### Close Verification

- Project-session state: CLOSED — this file's header above
- Operator/WIP state: empty template — `tasks/wip.md` unchanged, already
  at empty template, verified before this close
- Acceptance criteria verified: `test_deep_scan_bundle.py` 11/11,
  `test_provider_swap.py`, `test_fixtures.py` all re-run and passing
  after PR #3/#4 changes; live site verified via Browser tool (PR #4's
  preview) and via curl (production, all 3 routes, all 4 case/model
  combos returning correct dispositions) — all re-run at close time
- Lessons updated: yes — `KNOWLEDGE.md`: the re-entry/another-operator
  lesson, the codebase-map reconcile's own extraction bug and fix, the
  PR #3/#4 review findings (opus-5 refusal pattern, the `vercel project
  rm` confirmation-prompt quirk)
- Decisions updated: yes — DECISIONS.md #031 (comparator pinned to
  claude-opus-4-8, PR #3's swap not taken, with rejected alternatives)
- Tasks/open items updated: yes — `tasks/todo.md` re-entry-continuation
  section added; OI-024 and OI-025 added to `.agent/instructions.md`
- Milestones updated: no — nothing this stretch changed M9/OI-020's
  status; MILESTONES.md's post-H1 addendum from the last close still
  accurate, not re-touched
- Structural map reconciled: yes — **found and fixed a real bug in the
  reconcile method itself** (prose mentions of a path were being
  counted as real table coverage), then re-ran the corrected check:
  119 tracked files, 0 unmapped. 6 genuinely undocumented files added
  with real descriptions (not placeholder rows); 2 dead orphaned static
  files found and flagged (not deleted)
- Resulting diff inspected: yes, every commit this stretch
- Tests/checks: see "Acceptance criteria verified" above
- Commits created: `78bf909`, `4b6f500`, plus this close's own commit
  (see below)
- Remote synchronization: pushed after each commit this stretch;
  `git log @{u}..HEAD` confirmed empty after each push, re-confirmed
  after this close's commit below
- External side effects verified: two GitHub PRs closed with
  explanatory comments (#3, #4); one Vercel preview project created and
  deleted for PR #4's review; production redeployed twice (after the
  cache-guard fix, after PR #4's merge), both confirmed live via curl
- Repository housekeeping: worktree clean (`pr4-review` worktree
  directory had a transient Windows file-lock on removal, unregistered
  from git regardless — see below). Four local-only PR-review branches
  now exist (`pr-1-kelly`, `pr-2-evarline`, `pr-3-steven`, `pr-4-steven`)
  — never pushed anywhere, all fully incorporated or deliberately
  excluded already, flagged not removed per the close protocol's own
  instruction not to remove unprompted
- Remaining risks or integration work: OI-024 (opus-5 refusal pattern,
  deliberately deferred) and OI-025 (dead static files) are new; the
  backup recording and rehearsal from the previous close are still the
  two items only Mailu can do

---


Reopened at Mailu's request. `git fetch` + `git log e36a326..HEAD` showed
7 commits landed on `origin/main` since this file's last close
(`e36a326`), from another operator/session, not this one:
`c4a1d31` (live static scan + Anthropic BYOK preview), `2f11370`,
`56a575d`, `0a6a7f3`, `c7bd446` (narrative/evidence-first page split),
`31350a4`, `c1e7585` (current HEAD). Local working tree was already in
sync with `origin/main` (0 ahead / 0 behind) before this session touched
anything — no merge or rebase was needed.

**What changed, read from the diff, not assumed:** two new public API
routes, `api/check.py` (free static scan of an arbitrary public GitHub
target, process-local per-IP rate limit, explicitly documented as a
"starter guard" needing a durable edge limiter before real public
traffic) and `api/deep.py` (Anthropic deep-scan on an arbitrary GitHub
target using a request-scoped, never-stored, never-URL'd BYOK key —
reuses this session's own `select_high_risk_files_repo`/
`select_skill_bundle_files`, not a reimplementation). Plus
`api/demo_page.py`/`api/how_it_works_page.py` and a narrative/evidence
page split, wired via new `vercel.json` rewrites for `/demo` and
`/how-it-works`.

**This reverses a decision made earlier this stretch**, not silently —
flagging it because BUILD_PLAN.md M2 explicitly chose "fixed demo cases
only" over "arbitrary user-submitted repos" as the safer scope for a
public site under a clock. That constraint no longer holds: arbitrary
GitHub targets are now scannable publicly (free static tier) and via
BYOK (paid/deep tier). Not reverted per the standing instruction to
treat an external change as deliberate rather than undo it — the new
code is careful about the things that matter (never executes scanned
code, key never stored/logged/URL'd, per-IP limiting present even if
acknowledged as not production-durable), consistent with `CLAUDE.md`'s
non-negotiables. Not independently security-reviewed by this session.

**Verified before reporting status, not assumed:** all new `api/*.py`
files `py_compile` clean; `test_deep_scan_bundle.py` 11/11,
`test_provider_swap.py`, `test_fixtures.py` (2 detected/4 clean/4
known-gap) all still pass unmodified; `hackathon/test_build_requirements.py`
unchanged at 49/74; live site returns 200 on `/`, `/demo`, and
`/how-it-works`.

**Next step:** search GitHub for open pull requests (Mailu's request,
in progress as of this checkpoint).

---

## Full close, post-H1 stretch (2026-09-20) — live Everyday-track demo shipped

**Goal of this stretch:** review and land two community PRs, review a
third party's submission guide, then pressure-test and execute the
remaining build against a hard clock — which turned into switching the
submission track and shipping a full live Vercel demo.

**What was done, end to end:**

1. Reviewed and partially merged `kelly-leon`'s PR #1 (Fable model
   selection landed, `7bb5885`; duplicate fixture left out; PR closed).
2. Reviewed and merged whole `Everline Mipata`'s PR #2 (differential
   static-pillar harness, `97320a1`; PR closed).
3. Reviewed Steven Kamau Muriu's submission guide: data table verified
   exact against source reports; its `git am` patch found not to apply
   cleanly (tested in an isolated worktree, not assumed); B6 (skill-mode
   CLI sending only `SKILL.md`) found and fixed (`49bdba3`) — the single
   most consequential bug caught this stretch, since it meant the
   documented CLI path could never have demonstrated cross-file tracing.
4. Ran an 8-advisor council against the platform's actual fixed
   Breakthrough-track rules (confirmed via screenshot) vs. the team's own
   verified Fable-vs-comparator data (`council-transcript-20260920T001404.md`).
   Recommendation: check track-switch eligibility (a rules-page read, not
   an organizer favor) before spending more build time managing
   disclosure inside a track whose fixed rule the evidence couldn't meet.
5. Switched track: Breakthrough → Everyday (DECISIONS.md #029).
6. Executed a full milestoned build (`hackathon/BUILD_PLAN.md` M0–M6):
   out-of-bundle intent files for 3 demo cases; a live Vercel Python
   pipe proven end-to-end against the real pipeline; cache-only public
   serving (DECISIONS.md #030) after discovering the deployed endpoint
   was public and uncapped; a real fixture bug found and fixed along the
   way (markdown-blockquote citation mismatch, confirmed on every model
   tested); a full demo page built and deployed live.

**Live result:** `https://repocheck-hackathon.vercel.app` — hero with a
named damage story, how-it-works diagram, 3 real case panels (client-side
fetch, server never makes a live call, serves committed cached-but-real
results), and an undodged Fable-vs-comparator disclosure table. Verified
working end to end via the Browser tool, both light and dark mode.

**Not done, carried forward (see `tasks/todo.md` and `.agent/instructions.md`
Open Items for the full list):**
- `hackathon/EXPERIMENT_CARD.md` and `HACKATHON_CLAUDE_CODE_HANDOFF.md`
  still read Breakthrough throughout — not updated for the track switch
  this stretch (OI-022). Read `DECISIONS.md` #029 alongside them.
- `credential-disguised-report`'s cached result carries a
  `reviewer_manipulation_detected: true` flag with no obvious textual
  basis — displayed as-is, not investigated under the clock (OI-023).
- 17 of 21 P0 items in `hackathon/test_build_requirements.py` remain open
  beyond what this stretch closed (B3, B8, B11, most fixture-hygiene
  checks on fixtures outside the demo path) — none block the live demo.
- Two things only Mailu can do: record the ~90s backup screen capture,
  run one timed rehearsal. Not done by this session, not automatable.

**Known blockers:** none blocking the live demo itself. D-1 (organizer
answers) is superseded, not resolved, by the track switch — no longer
the active blocker since a measured Breakthrough comparison is no longer
being pursued.

**Milestone status:** M1–M8, M10, M11, M12 DONE. M9 still IN PROGRESS —
OI-020's two named acceptance criteria remain unmet by `verify_deep_scan.py`
specifically, despite substantial further live-Fable evidence gathered
both in H1 and in this stretch's production demo (see MILESTONES.md's
post-H1 addendum).

### Close Verification

- Project-session state: CLOSED — verified in: this file's header above
- Operator/WIP state: empty template — verified: yes, `tasks/wip.md`
  reset below this block was applied
- Acceptance criteria verified: all touched Python files `py_compile`
  clean at every commit this stretch; `test_deep_scan_bundle.py` 11/11,
  `test_provider_swap.py`, and `test_fixtures.py` re-run and passing
  after every code change (not just at time of original authorship);
  `hackathon/test_build_requirements.py` re-run repeatedly, tracked
  36/59 → 39/74 → 45/74 → 49/74 as fixes landed; live site verified
  working end to end via the Browser tool (both theme modes)
- Lessons updated: yes — `KNOWLEDGE.md`: PR-review diff-against-merge-base
  discipline and `git am` patch fragility; the B6 CLI bug and why it was
  worse than first described; the markdown-blockquote citation-validation
  bug (confirmed model-agnostic, not Fable-specific); Vercel SSO-protection
  and stable-alias-vs-per-deploy-URL gotchas
- Decisions updated: yes — DECISIONS.md #029 (track switch, with rejected
  alternatives recorded) and #030 (cache-only public demo serving, with
  the rate-limiter alternative recorded as deferred not abandoned)
- Tasks/open items updated: yes — `tasks/todo.md` post-H1 section added;
  `.agent/instructions.md` OI-022 (EXPERIMENT_CARD.md/handoff not updated
  for track switch) and OI-023 (unexplained reviewer-manipulation flag)
  added; OI-020/OI-021 re-verified accurate, left unchanged deliberately
  rather than reflexively re-stamped
- Milestones updated: yes — MILESTONES.md post-H1 addendum recording
  further live-Fable evidence without closing OI-020 or M9
- Structural map reconciled: yes — direct `git ls-files` comparison (111
  files, up from 77), verified programmatically (0 of 111 unmapped, not
  eyeballed). One real pre-existing gap found and fixed: `fixtures/`'s
  row never mentioned `credential-disguised-report`, added mid-session
  and never reconciled until this close. `hackathon/EXPERIMENT_CARD.md`
  marked `stale (OI-022)` rather than left as `active`
- Resulting diff inspected: yes — `git status`/`git diff --cached`
  reviewed before every commit this stretch, including this close
- Tests/checks: see "Acceptance criteria verified" above — all re-run at
  close time, not assumed from earlier in the stretch
- Commits created: this stretch's commits are already individually
  pushed (see git log on `main`, `7bb5885` through `8674b5e` plus this
  close's own commits); `git log @{u}..HEAD` checked empty after every
  push this stretch, re-confirmed after this close commit below
- Remote synchronization: `origin` = `14leux/repocheck-hackathon`;
  confirmed empty `git log @{u}..HEAD` after this close's commit (see
  command output in the session transcript)
- External side effects verified: `.env` confirmed git-ignored and
  absent from every diff this stretch, including this close; a real
  API key was stored as a Vercel server-side environment variable
  (never echoed to any tool output — piped directly from `.env` via
  `grep`/`cut`, verified the CLI's own confirmation didn't echo the
  value); Vercel SSO deployment-protection was deliberately disabled to
  make the demo publicly reachable, and the public API surface was
  redesigned (DECISIONS.md #030) specifically because of that exposure
- Repository housekeeping: two PR review branches (`pr-1-kelly`,
  `pr-2-evarline`) and worktrees were created and removed during PR
  review — see worktree audit below for current state; no stray branches
  left on `origin`
- Remaining risks or integration work: see "Not done, carried forward"
  above — none block the live demo; the backup recording and rehearsal
  are the two items that must happen before judging regardless of what
  else changes

---

## Post-H1 ad-hoc follow-up (2026-09-19), continued — PR #2 reviewed and merged whole

**4. Reviewed and merged `Everline Mipata`'s PR #2** (`14leux/repocheck-hackathon#2`,
"Add differential harness for the static pillars", branch `Eve-static-harness`).
Unlike PR #1, this one was clean end to end: single commit, based on
`7bb5885` (nearly current), no duplicate/stale content. Adds
`test_fixtures.py` — a differential harness over the *static* pillars
(`code_scan.py`/`skill_scan.py`, no LLM call) asserting both directions on
matched fixture pairs (malicious must fire, legit twin must stay clean),
plus a third category, `KNOWN_GAP`, for a real, verified, previously-
undocumented limitation: the co-occurrence rule in both pillars only checks
credential-access and network-send *within a single file*, so the RC-01
pattern split across `collect.py`/`schema.json`/`send.py`
(`malicious-aggregate-report/`) is invisible to the free static scan —
confirmed by running it: 4/4 `KNOWN_GAP` cases correctly produce zero
findings. Complementary to (not a duplicate of) B6's fix, which addresses
the same underlying pattern but for the paid deep-scan/LLM pipeline
specifically. One real overlap noted and disclosed on the PR: its
`malicious-aggregate-report`/`legit-aggregate-report` fixtures and this
stretch's earlier `credential-disguised-report` fixture are the same RC-01
pattern (same field names, identical `send.py`), independently built from
the same handoff spec by two people — not a conflict since they exercise
different code paths, but flagged so it's not a surprise later.

Cherry-picked (`-x`) onto `main` as `97320a1`, preserving Everline's
authorship. Re-verified after merge: `test_fixtures.py` (2 detected, 4
clean, 4 known gaps, matches the PR's own numbers), `test_deep_scan_bundle.py`
11/11, `test_provider_swap.py` pass, `hackathon/test_build_requirements.py`
picked up the 3 new fixture directories automatically (59→74 checks, still
45/74 pass, no regressions). Posted a review comment explaining the merge
and the RC-01 overlap, then closed PR #2 on GitHub (now merged, unlike PR
#1 which is still open pending a decision — see below).

## Post-H1 ad-hoc follow-up (2026-09-19) — PR #1 reviewed and partially landed, submission-guide reviewed and partially landed, B6 fixed

No formal session was opened for this stretch (H1 is still the last formally
closed session below); real work happened in a follow-up conversation and is
checkpointed here per the discipline's "update at any natural pause" rule
rather than left to go stale.

**What happened, in order:**

1. **Reviewed `kelly-leon`'s PR #1** (`14leux/repocheck-hackathon#1`,
   "Add conditional-setup fixture"). Verified by diffing against its actual
   merge-base (not `main`, which falsely showed dozens of deletions since the
   branch predates most of H1) and by running its tests/CLI in an isolated
   worktree. Two genuinely separate changes were bundled: (a) explicit Fable
   5.1 model selection (`FABLE_MODEL` constant, `--model` CLI flag,
   `output_config.effort`) — real, closed a genuine gap (the CLI silently
   defaulted to Sonnet), ported by hand onto current `main` since the branch
   was ~12 commits behind; (b) a new `fixtures/conditional-setup/` fixture —
   safe but a near-duplicate of the already-tested `task-digest-v1`/`v2`
   pattern, not merged. Landed in commit `7bb5885`. Posted a review comment
   on the PR explaining the decision; PR left open pending a decision on
   whether to close it.
2. **Reviewed Steven Kamau Muriu's submission guide**
   (`RepoCheck_Submission_Guide_for_Mailu.md`, not in this repo). Its §1
   model-comparison table was cross-checked cell by cell against
   `hackathon/results/rc02-report.md`/`rc04-sanity-report.md`/
   `rc08-sanity-report.md` and confirmed exact. Its appendix (a 4-commit
   `git am` patch) was tested in an isolated worktree and found **not to
   apply cleanly** (fails at patch 3/4 on a context mismatch) even after
   fixing one transcription slip — the two useful pieces were reconstructed
   directly from the source document instead of via the broken patch:
   `fixtures/credential-disguised-report/` (a genuinely new, previously
   unfixtured RC-01-shaped case — RC-01 was tested live in H1 but never
   committed to disk) and `hackathon/test_build_requirements.py` (a new,
   non-duplicate offline acceptance test: 59 mechanical checks against the
   handoff/card/blind-spots requirements, distinct in scope from
   `test_deep_scan_bundle.py`). The guide's own B6 finding was verified and
   found more serious than believed: skill-mode deep scan sent only
   `[SKILL.md]`, so a **correct** model answer citing a helper file failed
   citation validation and silently became `ANALYSIS_FAILED` — reproduced
   live via the acceptance test before fixing it.
3. **Fixed B6**: added `select_skill_bundle_files()` to `deep_scan.py`
   (mirrors `select_high_risk_files_repo()`'s shape — lists the repo tree,
   selects every blob under the `SKILL.md`'s own folder, still bounded by
   `build_bundle()`'s existing caps), wired into `main()`'s skill mode.
   Verified live against `14leux/repocheck-hackathon`'s own
   `fixtures/task-digest-v1/`: preflight now lists all 4 files, not just
   `SKILL.md`. Acceptance test re-run after the fix: 39/59 pass (was 37/59
   before this stretch, 36/59 per the guide's own `origin/main`-only
   baseline), 15 P0 items open (was 18 per the guide, 17 after the PR #1
   model-selection fix alone). Landed in commit `49bdba3`.

**Not done, carried forward:** the guide's §1 recommendation to contact
organizers is moot — Mailu already decided against organizer contact this
stretch, which leaves the guide's own fallback (Option A framing, disclosed
honestly) as the live path, already aligned with H1's Narrative Option B
decision. 14 P0 acceptance-test items remain open beyond B6 (see
`hackathon/test_build_requirements.py` output for the current list — B3
`output_config.format`, B8 frozen-prompt-file, B11 card freeze, F6 case-spec
files under `hackathon/cases/` are the most structurally significant).
PR #1 closed on GitHub (2026-09-19, at Mailu's request) — model-selection
piece already landed in `7bb5885`, fixture and checkpoint-diff pieces left
unmerged per the review comment on the PR. Fixture directories
`fixtures/legit-permission-gated-setup`
and the RC-02-pattern duplicates remain untouched (out of scope for this
stretch). No formal session-close reconcile (KNOWLEDGE.md, DECISIONS.md,
MILESTONES.md, codebase_map.md) was performed for this stretch — do that at
the next formal close, not deferred indefinitely.

**Verification performed:** both commits' touched files py_compile clean;
`test_deep_scan_bundle.py` 11/11 and `test_provider_swap.py` re-run and
passing after both commits; live CLI dry-runs against the real
`14leux/repocheck-hackathon` GitHub repo (not just local fixtures) for both
the `--model` flag and the B6 fix; `git log @{u}..HEAD` empty after each
push.

---

## Hackathon session H1 — D-7 decided (Narrative Option B); D-1 organizer answers now the sole blocker

**Working copy:** `D:\Projects\repocheck-hackathon` (clone of the main
project at commit `667e669`). `origin` = `14leux/repocheck-hackathon`
(public), `upstream` = `14leux/repocheck`. Main project untouched.

**Goal:** Execute `HACKATHON_CLAUDE_CODE_HANDOFF.md` — Breakthrough
track, bounded skill authority review, demonstrated on Claude Fable 5.1.

**Current step:** the empirical question behind D-7 is now answered, in
more detail and with a more nuanced result than first suspected. Four
independent fixture families tested live against `claude-fable-5-1`,
`claude-opus-4-8`, `claude-sonnet-4-5` (all exploratory, not measured
runs under a frozen card): RC-01, a structurally distinct RC-04-style
sanity variant, a structurally distinct RC-08-style sanity variant, and
RC-02. Full reports: `hackathon/results/rc02-report.md`,
`rc04-sanity-report.md`, `rc08-sanity-report.md`,
`breakthrough-usecases.md`. Full synthesis: KNOWLEDGE.md (latest entry).

**Two distinct refusal patterns, not one:**
1. Outcome-tracking (RC-01, RC-04-sanity, RC-08-sanity): Fable refuses
   only the harmful variant, 3/3; correctly analyzes the safe
   counterpart, 3/3. Not mitigated by less-realistic/pseudocode framing
   (tested directly, still refused).
2. Topic-tracking (RC-02, fetch-and-execute): Fable refuses **both**
   variants, including the properly-guarded safe one. For this violation
   class Fable cannot currently distinguish good design from bad at all.

**Also found:** a genuine Sonnet-4-5 false positive on RC-02's safe
variant (verified citations, real reasoning error, not a fabrication);
Opus-4-8 producing unparseable JSON on the safe variant in 2/2 fixture
families tested (pattern, not yet a proven rate). The research agent's
report separately surfaced a serious differentiation risk: SkillScope
(ACM CCS '26, dated 2026-09-11) already does cross-file, task-conditioned,
evidence-cited scope analysis at scale — the handoff's "unsafe claims"
list needs "cross-file authorization-scope tracing is new" added to it.

**Operational incident this session:** 4 parallel background subagents
were dispatched on `model: "opus"` to run this testing faster. All 4 hit
a hard account usage cap mid-run and were killed. Two had already
produced complete results (salvaged, not rerun); one left usable fixtures
with no live results (rerun directly by the orchestrator in seconds, no
subagent needed); one (research) had already written its full report.
Retesting the `.env` key minutes later showed it fully functional again —
a burst-usage trip from 4 parallel Opus-tier agents, not a lasting
lockout, but real time was lost. **Mailu's explicit direction, effective
immediately: Sonnet gives clear instructions, Haiku or direct
orchestrator execution does mechanical work — no more parallel Opus-tier
subagent fleets for the remainder of this timed exercise.**

**D-7 decided: Narrative Option B.** Mailu chose disclosure over pursuing
a model-advantage claim. The secondary Breakthrough claim in card §1 is
now explicitly marked abandoned (not massaged) in the card itself.
Updated to carry this decision: `HACKATHON_CLAUDE_CODE_HANDOFF.md` (new
"Session H1 update" section, revised demo step 8, revised Honest/Unsafe
claims lists — original text preserved, update is additive and dated),
`hackathon/EXPERIMENT_CARD.md` (§1 status note, D-7 row now CLOSED with
the decision recorded, §9 gained a fourth organizer question specific to
this disclosure), `KNOWLEDGE.md` (decision entry).

**Not yet done:** `hackathon/EXPERIMENT_CARD.md` is still DRAFT — NOT
FROZEN. D-3/D-4/D-7 all resolved; **D-1 (organizer answers) is now the
sole blocking item.** No prompt file authored yet (§4). D-2c (the original
hand-built fixture) still has the answer-key-leak/in-bundle-permission
defects from `hackathon/BLIND_SPOTS.md` §A — untouched, since the four new
fixture families built this session are cleaner examples of correct
fixture design and can likely supersede it rather than needing a separate
fix. No UI. `verify_deep_scan.py` (Sonnet 4.5, single-file interface)
passed both its checks, but that's a different code path from the
joint-bundle pipeline this session exercised live four more times —
OI-020's "M9 verified" claim should attach to the joint-bundle evidence,
not just verify_deep_scan.py's older pass.

**Next concrete step:** (1) get organizer answers into card §9 — now the
only blocker before freeze, including the new disclosure-framing question;
(2) author `hackathon/prompts/authority_review_v1.txt` and hash it into
card §4; (3) decide whether to build the official held-out H-1/H-2
(RC-08/RC-04) instances now that their sanity variants have already
characterized the refusal boundary, or defer per the card's original
held-out timing; (4) start preparing the demo narrative around the
architecture claim, since the secondary claim is no longer part of the
pitch.

**Known blockers:**
- Organizer comparator and eligibility rules are still unconfirmed
  (carried over from main-project session 5) — card D-1, BLOCKING.
- `ANTHROPIC_API_KEY`/`GITHUB_TOKEN` (card D-3) resolved — both load from
  `.env` and work live, confirmed multiple times this session.

**Milestone status (inherited, unverified in this clone):** M1–M8, M10,
M11, M12 DONE; M9 still marked IN PROGRESS — see OI-020 gap noted above.

---

## Close, hackathon session H1 (2026-09-19)

**Reconciliation performed at close, beyond the summary above:**

- `DECISIONS.md` — two new entries added (027: joint-bundle collection;
  028: out-of-band `user_intent` authorization + the ANALYSIS_FAILED
  contract), matching the project's existing decision-log format. These
  are real architecture decisions this session made, not just bug
  fixes, and were previously recorded only in `KNOWLEDGE.md`.
- `tasks/todo.md` — hackathon session H1's own checklist section added,
  matching the file's existing per-session format. D-1 carried forward
  as the one open item.
- `tasks/codebase_map.md` — fully reconciled against `git ls-files`
  (77 tracked files, up from 30 at the last reconcile). All hackathon-
  session files added. Three stale rows fixed in place, not just
  flagged: `MILESTONES.md`'s self-contradictory "ALL COMPLETE" line
  (also corrected directly in that file), `deep_scan.py`'s row (rewrote
  — no longer accurate post-DECISIONS 027/028), `verify_deep_scan.py`'s
  row (its pass this session used a different code path than OI-020
  actually names). One real pre-existing gap found by direct
  comparison, not introduced this session: `link_scan.py` was tracked
  in git (implements DECISION 026) but had no map row at all — added.
- `MILESTONES.md` — corrected in place rather than left as a stale
  claim: the "ALL 12 MILESTONES COMPLETE" line contradicted its own
  next clause ("M9 partial") and OI-020's still-open status. A dated
  correction was appended directly below it.

**Acceptance criteria verified before close:** all touched Python files
(`bundle.py`, `interfaces.py`, `anthropic_provider.py`, `deep_scan.py`,
`envfile.py`, `github_provider.py`, `test_deep_scan_bundle.py`,
`test_provider_swap.py`) compile clean; both offline suites re-run and
pass (11/11 in `test_deep_scan_bundle.py`, `test_provider_swap.py`
unmodified and passing) after all reconcile edits.

**Lessons this close added beyond what's already in KNOWLEDGE.md:**
none new — the close's job was reconciling records to match sessions
already logged there, not discovering new lessons.

**Decisions this close added:** DECISIONS.md #027, #028 (see above) —
these formalize architecture choices already described informally in
KNOWLEDGE.md's hackathon entries; no new decision was made during the
close itself.

### Close Verification

- Project-session state: CLOSED — verified in: this file's header above
- Operator/WIP state: empty template — verified: yes, `tasks/wip.md`
  reset below this block was applied
- Acceptance criteria verified: all touched Python files py_compile
  clean; `test_deep_scan_bundle.py` 11/11 pass; `test_provider_swap.py`
  passes unmodified — both re-run at close time, not just at time of
  original authorship
- Lessons updated: none new at close — substantive lessons already
  recorded in `KNOWLEDGE.md` across this session's prior commits
- Decisions updated: DECISIONS.md #027 (joint-bundle collection), #028
  (out-of-band `user_intent` authorization + ANALYSIS_FAILED contract)
- Tasks/open items updated: `tasks/todo.md` hackathon session H1 section
  added; D-1 (organizer answers) carried forward as the sole open item
  in both `tasks/todo.md` and `hackathon/EXPERIMENT_CARD.md` §10
- Milestones updated: `MILESTONES.md`'s self-contradictory completion
  claim corrected in place; M9 status unchanged (still IN PROGRESS,
  correctly) — no milestone status was flipped at this close
- Structural map reconciled: yes — direct `git ls-files` comparison
  (77 files), all hackathon-session paths added, one pre-existing gap
  (`link_scan.py`) found and fixed, three stale rows corrected
- Resulting diff inspected: yes — `git status`/`git diff --cached`
  reviewed before every commit this session; no unexpected changes
- Tests/checks: `test_deep_scan_bundle.py` 11/11 PASS,
  `test_provider_swap.py` PASS, all touched `.py` files `py_compile`
  clean — all re-run at close time
- Commits created: this session's commits are already individually
  pushed (see git log on `main`); the close-reconciliation edits above
  will be committed and pushed as part of closing this session
- Remote synchronization: `origin` = `14leux/repocheck-hackathon`;
  `git log @{u}..HEAD` confirmed empty after every commit this session,
  re-confirmed after this close commit below
- External side effects verified: `.env` confirmed git-ignored and
  absent from every `git status`/staged diff this session, including
  this close commit; no secret material found in any diff
  (`git diff --cached | grep` checked before each push)
- Repository housekeeping: no stray worktrees or branches created this
  session; only `main` was used on `origin`; `upstream`
  (`14leux/repocheck`, the main project) was never touched
- Remaining risks or integration work: D-1 (organizer answers) is an
  external dependency, not resolvable by the agent — the sole blocker
  before `hackathon/EXPERIMENT_CARD.md` can freeze. `verify_deep_scan.py`
  still needs updating to call the joint-bundle pipeline with an
  explicit Fable 5.1 model to close OI-020 as originally scoped — noted,
  not fixed, since it's outside this session's actual task focus (D-7
  testing, not M9 closure). D-2c remains defective per
  `hackathon/BLIND_SPOTS.md` §A, superseded in practice by cleaner
  fixtures built this session, not deleted or fixed directly.
OI-021 deferred.

---

*History below is inherited from the main project up to commit `667e669`.*


## Session 5 — Hackathon handoff and intentional close

**Goal:** Consolidate the Breakthrough-track hackathon plan, council review,
researched edge cases, safe fixture specifications, and Claude Code starting
instructions into a durable handoff for continuation by Claude Code.

**What was done:** Created `HACKATHON_CLAUDE_CODE_HANDOFF.md`, the full
`council-transcript-20260919T201238.md`, and the `research/` casebook files.
The handoff records the user-confirmed Breakthrough track, Fable 5.1/API
requirement, four-person roles, hard first-hour capability gate, bounded
skill-authority-review scope, malformed-output risk, comparison protocol,
safe synthetic cases, source links, and the Claude Code starting prompt.
The attached context document said Everyday; the later user answer saying
Breakthrough was treated as authoritative.

**Next session starts with:** Open Claude Code in this repository, read
`HACKATHON_CLAUDE_CODE_HANDOFF.md` and the canonical project records, verify
the organizer-approved comparator and Fable model identifier, then execute
the handoff's one-page experiment card before building UI.

**Blockers:** the organizer's exact comparator and existing-project eligibility
were not available in this session. No code implementation or live Fable
comparison was performed here.

**Milestone status:** existing project status unchanged — M1–M8, M10, M11,
M12 DONE; M9 remains IN PROGRESS pending OI-020; OI-021 remains deferred.

Close Verification:
- KNOWLEDGE.md updated: no — no new implementation learning; research is captured in `research/` and the handoff
- DECISIONS.md updated: no — no architectural decision was made
- tasks/todo.md updated: no — no existing task items were completed; hackathon work is carried into the handoff
- Open Items table updated: no — OI-020 and OI-021 unchanged
- tasks/codebase_map.md updated: yes — added `link_scan.py` discrepancy and five new handoff/research paths
- tasks/wip.md reset to empty template: yes
- git commit created: pending close command
- git push completed: pending close command
- git worktree audit: pending close command

## Session 4 — About-summary in report output; never-auto-install skill guardrail

**Goal:** Two changes Mailu raised from real usage: (1) the report
should tell the user what the scanned repo/skill is actually for, not
just the security verdict; (2) a prior live session installed a scanned
skill immediately after reporting its verdict without asking — fix the
skill instructions so that never happens again.

**What was done:** Added a mechanical (no LLM call, keeps the static
scan free per DECISIONS.md #008/#009) "About this repo"/"About this
skill" summary to `verdict.py`'s repo- and skill-mode output, in both
text and `--json`. Repo mode: GitHub's own `description` field via a new
`fetch_repo_description()` on `FileAccessProvider`/`GitHubFileAccessProvider`
(default `None`, so `test_provider_swap.py` still passes untouched),
falling back to the README's first real paragraph. Skill mode: the
SKILL.md frontmatter's own `description:` field, falling back to the
body's first paragraph. Verified against real repos
(`pallets/itsdangerous`, the project's own `14leux/repocheck` SKILL.md)
and unit-tested the extraction helpers directly.

Fixed the auto-install gap in both `skills/repocheck/SKILL.md`
(project-local) and the user-wide install at
`~/.claude/skills/repocheck/SKILL.md` (outside this repo, not tracked
by git here, but the actual copy that ran the session where the bug
happened): report now explicitly ends at the verdict, with
install/copy/add-dependency called out as a separate step gated on the
user's explicit yes, added to both the workflow section and the
Non-negotiables list. Also confirmed (DECISIONS.md #017, pre-existing)
that the standalone CLI itself is already usable from Codex or any
other shell-capable agent with no changes needed — `SKILL.md` is a
Claude-Code-specific format Codex has no loader for, but
`repocheck.py` has zero Claude Code dependency.

**Next session starts with:** no milestones remain — all 12 are DONE.
Same two open items as before, neither touched this session: OI-020
(live deep-scan verification, needs a real ANTHROPIC_API_KEY) and OI-021
(proximity-based obfuscation matching, AST-level, deferred).

**Blockers:** none.

**Milestone status:** unchanged from session 3 close — M1–M8, M10, M11,
M12 DONE; M9 IN PROGRESS pending OI-020.

```
Close Verification:
- KNOWLEDGE.md updated: no -- nothing new this session (the design
  decisions made are architectural, captured in DECISIONS.md #025
  instead; no bugs or quirks discovered)
- DECISIONS.md updated: yes -- DECISION 025 (about-summary is
  mechanical/no-LLM; skill wrapper must never auto-install after
  reporting)
- tasks/todo.md updated: yes -- Session 4 section added, all items [x]
- Open Items table updated: no -- none touched this session (OI-020,
  OI-021 unchanged, still OPEN)
- tasks/codebase_map.md updated: yes -- verdict.py/interfaces.py/
  github_provider.py descriptions updated for the new
  fetch_repo_description/about-summary code; SKILL.md entry updated to
  note the never-auto-install instruction and the user-wide mirror.
  Full reconcile also run: `git ls-files` (30 files) diffed against the
  map, zero discrepancies (no tracked-but-unmapped, no
  mapped-but-deleted)
- tasks/wip.md reset to empty template: yes
- git commit created: yes -- commit 4fbfeb0, "Session 4 close:
  about-summary in report output, never-auto-install skill guardrail"
  (9 files changed, 274 insertions, 11 deletions)
- git push completed: yes -- 4fbfeb0 pushed to origin/main
  (b17a1d8..4fbfeb0); `git log @{u}..HEAD` returned empty output
- git worktree audit: clean -- single entry, D:/Projects/repocheck [main]
```

---

## Session 3 — Rebrand and humanized public-facing docs

**Goal:** Rename the tool's display name to "Dr. RepoCheck," rewrite the
README to explain the tool to a security-layman new to vibe coding using
plain psychology (why trust gets granted on autopilot, why that's riskier
with an AI agent driving), and add a full API-key-hygiene section
explaining why a key is requested and how to protect it.

**What was done:** README.md's intro rewritten around social proof /
optimism bias and the vibe-coding trust-speed gap; a "Protecting your API
key" section added (env vars, Anthropic Console expiring keys —
3h/1d/7d/30d/custom/never — workspace scoping, rotation, do/don't list,
sourced from Anthropic's own docs and the OWASP Secrets Management Cheat
Sheet via WebSearch, not invented); an explainer for why RepoCheck asks
for the user's own key rather than proxying one. Display name changed to
"Dr. RepoCheck" in README.md, `skills/repocheck/SKILL.md`'s heading, and
`repocheck.py`'s docstring banner — deliberately not touching the GitHub
repo name, module names, or CLI invocation (DECISIONS.md #024), which
would break existing clone/install commands for a cosmetic gain. Added
matching short key-hygiene pointers at the two places a user actually
hits the API-key ask: `anthropic_provider.py`'s `MissingApiKeyError` and
`deep_scan.py`'s `preflight()` output.

**Next session starts with:** no milestones remain — all 12 are DONE.
Same two open items as before, neither touched this session: OI-020
(live deep-scan verification, needs a real ANTHROPIC_API_KEY) and OI-021
(proximity-based obfuscation matching, AST-level, deferred).

**Blockers:** none.

**Milestone status:** unchanged from session 2 close — M1–M8, M10, M11,
M12 DONE; M9 IN PROGRESS pending OI-020.

```
Close Verification:
- KNOWLEDGE.md updated: no -- nothing new this session (content/docs
  work, no bugs found or design decisions requiring a learnings entry)
- DECISIONS.md updated: yes -- DECISION 024 (rebrand scope: display-only,
  technical identifiers unchanged, why)
- tasks/todo.md updated: yes -- Session 3 section added, all 4 items [x]
- Open Items table updated: no -- none touched this session (OI-020,
  OI-021 unchanged, still OPEN)
- tasks/codebase_map.md updated: no -- reconcile ran clean, no files
  added/removed/renamed this session (README.md/SKILL.md/anthropic_
  provider.py/deep_scan.py/repocheck.py all pre-existing mapped entries,
  edited in place, not moved)
- tasks/wip.md reset to empty template: yes
- git commit created: yes -- see below
- git push completed: yes -- see below, git log @{u}..HEAD checked empty
- git worktree audit: clean -- single entry, D:/Projects/repocheck [main]
```

---

## Session 2 — Build, hardening, public release, and open-item cleanup

**Goal:** Take RepoCheck from a validated-but-unbuilt scoping document
(session 1's output) to a real, working, tested, publicly released tool.

**What was done:**

Built all 8 V1 milestones (M2–M8): CVE lookup via OSV.dev, skill-mode
instruction scanning, repo-mode code red-flag scanning, dependency
freshness, a severity model + humanized traffic-light verdict, the
pluggable file-access interface (extracted from working code and
proven swappable with a real stub), and the CLI itself. Every pillar
was validated against real repos, not just synthetic tests — the
walking skeleton reproduced the session-1 manual trace exactly, then
exceeded it by finding two more real vulnerabilities the manual sample
missed.

Built Hardening (M9–M11) and Release (M12): opt-in deep scan (built and
mostly verified — two acceptance criteria need a live API call not
available in this environment, tracked as OI-020), the Claude Code
skill wrapper (dogfooding immediately found and fixed a real false
positive), degraded-state/reproducibility/suppression handling, and
full public-release polish (README rewritten, CONTRIBUTING.md, MIT
license, repository flipped private → public at
github.com/14leux/repocheck with the default branch renamed
master → main).

At Mailu's explicit request, dispatched independent adversarial QA
subagents against the Hardening work rather than relying on
self-testing. Two rounds found real bugs beyond what the building
session's own tests caught — most seriously, npm caret ranges
(`^4.1.9`) were being treated as exact pinned versions for both CVE
lookup and freshness classification, verified wrong (and the fix
verified *correct*, not just different) by cross-checking against
OSV.dev directly. Also found and fixed: two crash paths with no error
handling, an overfit false-positive guard, several detection evasions,
an obfuscation false positive, and a suppression-mechanism crash.

After M12, continued closing the remaining tracked open items with the
same real-verification discipline: OI-019 (concurrency, ~9x measured
speedup), OI-016 (sourced two real examples directly from Snyk's
ToxicSkills research rather than another synthetic test — found and
fixed two genuinely new gaps, a credential-shaped-environment-variable
exfiltration pattern and an invisible-Unicode-character evasion
technique), OI-018 (Go ecosystem freshness, verified against a real
uppercase-path module), and OI-017 (bulk tarball fetch replacing
per-file API calls, combined with OI-019 for an ~18x total improvement
on the same repo — 352s down to 19s).

This close's own reconcile step caught a real gap: OI-009, OI-010, and
OI-015 had all been genuinely resolved during earlier implementation
but were never marked CLOSED in the Open Items table, because fixing
the thing an item describes and closing the item are different actions
that both need a deliberate step. Fixed as part of this close, not
carried forward as more stale debt.

**Next session starts with:** no milestones remain — all 12 are DONE.
Two tracked open items remain, neither blocking: OI-020 (run
`verify_deep_scan.py` once a real `ANTHROPIC_API_KEY` is available,
then flip M9 fully DONE) and OI-021 (proximity-based obfuscation
matching — needs AST-level analysis, a genuinely larger undertaking
than a pattern tweak, deferred deliberately rather than rushed).

**Blockers:** none for further work; OI-020 specifically needs a live
API key this environment doesn't have.

**Milestone status:** M1–M8, M10, M11, M12 DONE. M9 IN PROGRESS (built,
3 of 5 acceptance criteria verified, 2 pending OI-020).

---

```
Close Verification:
- KNOWLEDGE.md updated: yes — entries: two rounds of independent QA (7 + 6 bugs found and fixed), OI-019 concurrency (measured, not assumed), OI-016 real Snyk examples (2 new gaps found and fixed), OI-018 Go freshness (verified with a real uppercase-path module), OI-017 bulk tarball fetch (measured, fallback tested for real), and this close's own reconcile catching 4 stale Open Items
- DECISIONS.md updated: no new entries this stretch — bug fixes and open-item closures are KNOWLEDGE.md territory, not new architectural decisions; DECISIONS.md already has 23 entries from earlier in the session (up to #023, M10's skill-wrapper decision)
- tasks/todo.md updated: yes — items closed: OI-019/016/018/017 fix batches, session-close reconcile (4 stale OIs found and closed, codebase map fixed) — carried forward: OI-020, OI-021
- Open Items table updated: yes — OIs touched: OI-009, OI-010, OI-014, OI-015 newly closed at this reconcile (previously stale-open despite being resolved); OI-016, OI-017, OI-018, OI-019 closed earlier this session with resolutions; OI-020, OI-021 remain OPEN with clear next steps
- tasks/codebase_map.md updated: yes — entries: fixed a broken markdown table (stray blank line had split it in two), corrected 3 stale descriptions (code_scan.py/freshness_scan.py referencing now-closed OI-017/OI-018 as open), consolidated 3 function-level rows into their parent file's entry, verified all 30 tracked files accounted for via git ls-files, no mapped-but-deleted entries
- tasks/wip.md reset to empty template: yes
- git commit created: yes — commit 9b10ed8, message: "Session 2 close: reconcile Open Items and codebase map, checkpoint" (6 files changed). Full session-2 work landed across three earlier commits this session: a838720 (V1, M1-M8), ec6a922 (M9-M12), 8995554 (OI-016/017/018/019 fixes), 9b10ed8 (this close)
- git push completed: yes — git log @{u}..HEAD returned no output, nothing sitting unpushed
- branch: main (renamed from master at M12), tracking origin/main
- git worktree audit: clean — single entry, D:/Projects/repocheck [main], no stray .claude/worktrees/* entries
```
