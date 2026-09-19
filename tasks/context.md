# tasks/context.md

**Status:** IN PROGRESS

## Hackathon session H1 — Fable 5.1 model selection + output_config added, verified against live docs; first-hour gate still open

**Working copy:** `D:\Projects\repocheck-hackathon` (clone of the main
project at commit `667e669`). `origin` = `14leux/repocheck-hackathon`
(public), `upstream` = `14leux/repocheck`. Main project untouched.

**Goal:** Execute `HACKATHON_CLAUDE_CODE_HANDOFF.md` — Breakthrough
track, bounded skill authority review, demonstrated on Claude Fable 5.1.

**Current step:** the top implementation blind spot from
`hackathon/BLIND_SPOTS.md` (C-1: one-file-at-a-time API calls, unable to
answer any cross-file case) is fixed. New `bundle.py` builds one bounded,
delimited, deterministic multi-file bundle; `interfaces.py` gained
`ModelResponse`/`analyze_detailed()` so `stop_reason`/`usage`/`model` are
no longer thrown away; `anthropic_provider.py`'s `max_tokens` went
1024→16000 and got a real timeout; `deep_scan.py`'s `run_deep_scan()`
makes one joint request instead of one per file, validates every
citation against the exact bundle bytes sent, and maps malformed
JSON/refusal/truncation to `ANALYSIS_FAILED` instead of an empty
findings list. Verified offline with a new 7-case suite
(`test_deep_scan_bundle.py`, scripted provider, zero network calls) —
all pass. `test_provider_swap.py` re-run unmodified, still passes.

**This session's addition:** two more BLIND_SPOTS.md §D items closed
against the live Anthropic docs (fetched directly, not from training
knowledge — this model's cutoff predates Fable 5.1's Sep 2026 release):
`anthropic_provider.py` now has an explicit `FABLE_MODEL` constant and
sends `output_config: {"effort": "high"}`, verified against the docs'
own request examples for `claude-fable-5-1`; `deep_scan.py` gained a
`--model` flag (default `claude-fable-5-1`) and prints which model it's
about to call, so the subject model is never silently inherited from
the provider's generic default. Deliberately did NOT add
`output_config.format` (schema-constrained output) — a doc-compatibility
check for this exact model came back self-contradictory, and a wrong
guess there risks a live 400 at demo time. Flagged as an open question,
not shipped. Re-verified `test_deep_scan_bundle.py` (7/7) and
`test_provider_swap.py` unmodified after the change; both pass.

Also this session: a `fixtures/conditional-setup/` test-3 fixture was
added and opened as a PR against `14leux/repocheck-hackathon` via a
personal fork (`kelly-leon/repocheck-hackathon`), after discovering the
`kelly` branch's push permissions were denied on the shared repo. The
rebase onto the fork also surfaced that `main` had moved 4 commits ahead
of what this session's boot read (the team's own bundle-collection fix,
`test 4` fixture, blind-spot review, and a draft experiment card) — now
reconciled.

**Not yet done:** `hackathon/EXPERIMENT_CARD.md` v0.1 is still DRAFT —
NOT FROZEN (six open decisions in its §10; D-1 organizer answers and D-3
no `ANTHROPIC_API_KEY` are BLOCKING). No prompt file authored yet, no
live API call made, no fixtures built beyond D-2c (which
`hackathon/BLIND_SPOTS.md` section A found real defects in — untouched
by this session's fix, since those are fixture-authoring issues, not
collection-pipeline issues). `output_config.format` compatibility with
Fable 5.1 unresolved (see above). No UI. The hard first-hour gate is
still open — everything above is plumbing verified against a fake, not
a demonstrated live capability.

**Next concrete step:** (1) get `ANTHROPIC_API_KEY` into this
environment and run `verify_deep_scan.py` for real — the two live-call
acceptance criteria (injection resistance, a real detection win) are
still unverified, offline tests don't substitute for them; while a real
key is available, also settle `output_config.format` compatibility with
one real call; (2) author `hackathon/prompts/authority_review_v1.txt`
and hash it into card §4; (3) get organizer answers into card §9; (4)
re-cut D-2c with neutral naming and out-of-bundle permission, then build
its harmful twin D-2.

**Known blockers:**
- `ANTHROPIC_API_KEY` is not set in this environment — blocks the Fable
  smoke test and OI-020's live deep-scan verification (unchanged; the
  offline suite added this session does not resolve this blocker, it
  only proves the surrounding plumbing is correct given some response).
- Organizer comparator and eligibility rules are still unconfirmed
  (carried over from main-project session 5).

**Milestone status (inherited, unverified in this clone):** M1–M8, M10,
M11, M12 DONE; M9 IN PROGRESS pending OI-020 (status text refreshed this
session in `.agent/instructions.md`'s Open Items table — not closed);
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
