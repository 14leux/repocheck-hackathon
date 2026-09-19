# tasks/context.md

**Status:** IN PROGRESS

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
