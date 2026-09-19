# tasks/codebase_map.md

| Path | Status | Purpose |
|------|--------|---------|
| `README.md` | active | Project overview, install/usage, glossary — rewritten for real usage at M12 |
| `CLAUDE.md` | active | Agent entry point, non-negotiables (4) |
| `CONTRIBUTING.md` | active | M12 — red-flag-rule contribution process per DECISIONS.md #006 |
| `LICENSE` | active | MIT license (DECISIONS.md #005) |
| `.gitignore` | active | Python/secrets/OS ignores |
| `.agent/instructions.md` | active | Boot/close sequence, Open Items table (OI-001–OI-021) |
| `DECISIONS.md` | active | Decision log — 28 entries (027/028 added hackathon session H1: joint-bundle collection, out-of-band `user_intent` authorization) |
| `MILESTONES.md` | active | 12 milestones; M9 still IN PROGRESS despite a self-contradictory "ALL COMPLETE" line — corrected in-place, hackathon session H1, do not read that line at face value without checking the correction directly below it |
| `KNOWLEDGE.md` | active | Confirmed learnings — validation traces, 2 rounds of independent QA, all post-M12 open-item fixes, plus a substantial hackathon session H1 block (Fable 5.1 API constraints, the joint-bundle fix, D-7 refusal-pattern evidence and decision, the `.env` secrets fix, the parallel-Opus-subagent usage-cap incident) |
| `council-transcript-20260807T000000.md` | active | 8-advisor llm-council run on v1 scope (session 1) |
| `council-transcript-20260919T201238.md` | active | 8-advisor llm-council pressure test on the hackathon plan (main-project session 5, inherited by this fork) |
| `HACKATHON_CLAUDE_CODE_HANDOFF.md` | active | Consolidated hackathon brief (Breakthrough track). Amended hackathon session H1 with a "Session H1 update" section (D-7 decision, revised claims lists, revised demo script) — original text preserved, update is additive |
| `research/hackathon-edge-cases-2026-09-19.md` | active | Sourced case research and evaluation protocol behind the case specs below (main-project session 5) |
| `research/hackathon-case-specs-2026-09-19.json` | active | Machine-readable case specifications (RC-01…RC-08) — ground truth for fixture design; case IDs must never appear in model-visible bytes |
| `hackathon/EXPERIMENT_CARD.md` | active | The frozen-when-ready experiment design — claim, models, request settings, input contract, case splits, scoring, open decisions (D-1 is the sole remaining blocker as of hackathon session H1 close) |
| `hackathon/BLIND_SPOTS.md` | active | Design review of the first fixture (D-2c) and the collection pipeline — findings A-1…A-7 (fixture defects) and C-1…C-3 (pipeline defects, now fixed per DECISIONS 027/028) |
| `hackathon/results/` | active | Per-case live-test reports (`rc02-report.md`, `rc04-sanity-report.md`, `rc08-sanity-report.md`) and the differentiation research pass (`breakthrough-usecases.md`), plus 2 raw-JSON scratch files recovered from a subagent crash. All exploratory — none are measured runs under a frozen card |
| `bundle.py` | active | Bounded, delimited, deterministic multi-file bundle builder for deep_scan.py — DECISION 027 |
| `envfile.py` | active | Stdlib-only `.env` loader (no `python-dotenv` dependency) — `anthropic_provider.py`/`github_provider.py` fall back to a local git-ignored `.env` file when the real environment lacks the key |
| `.env.example` | active | Tracked template documenting `ANTHROPIC_API_KEY`/`GITHUB_TOKEN` — no real values; the real `.env` is git-ignored and never tracked |
| `test_deep_scan_bundle.py` | active | Offline proof of the joint-bundle pipeline (bundle.py + deep_scan.py + interfaces.py), zero network calls — 11 cases, all pass |
| `test_fixtures.py` | active | Differential harness over the STATIC pillars (code_scan/skill_scan), the counterpart to `test_deep_scan_bundle.py`'s deep-scan coverage. Asserts both directions — malicious fixtures must fire, legitimate counterparts must stay clean — plus 4 `KNOWN_GAP` rows recording the single-file co-occurrence limitation, and reports a gap that closes rather than silently asserting "still broken" |
| `fixtures/` | active | Hand-built and live-tested fixture bundles: `legit-permission-gated-setup` (D-2c, known-defective per BLIND_SPOTS.md §A, superseded in practice), `task-digest-v1`/`-v2` (RC-02), `reviewer-note-sanity-a`/`-b` (RC-04-style, not the official held-out instance), `test-digest-relay-sanity-a`/`-a2`/`-b` (RC-08-style, not the official held-out instance) . Also `legit-aggregate-report`/`malicious-aggregate-report`/`malicious-single-file` — the static-pillar differential set driving `test_fixtures.py` (handoff research pattern #2), inert by construction: nothing executes at import, every endpoint uses the reserved `.test` TLD |
| `tasks/context.md` | active | Live session checkpoint |
| `tasks/wip.md` | active | Crash-recovery pad |
| `tasks/todo.md` | active | Task board |
| `tasks/codebase_map.md` | active | This file |
| `skeleton.py` | active | Core: CVE lookup via OSV.dev, manifest parsing (PyPI/npm/Go), `parse_repo_arg` (hardened against malformed input), `resolve_package_versions` (npm caret/tilde resolution), `strip_invisible_characters` (shared Unicode-evasion fix), module-level `list_tree`/`fetch_file`/`fetch_all_files` delegating to the active `FileAccessProvider` |
| `skill_scan.py` | active | Skill-mode instruction scan — credential-exfil (incl. env-var-shaped secrets), instruction-override (broadened guard), shell-pipe-execute (incl. xargs/download-then-execute), fetch-and-follow caveat |
| `code_scan.py` | active | Repo-mode code red-flag scan — obfuscation (co-occurrence-gated), credential-harvesting (multi-language/library), suspicious network calls (private-IP-excluded), install-time scripts. Scans `.ps1` too |
| `freshness_scan.py` | active | Dependency freshness — PyPI, npm, and Go (case-encoded module proxy), concurrent lookups |
| `verdict.py` | active | Severity model + humanized verdict — both modes, `--json`, degraded-state handling, suppression, reproducibility metadata, concurrent + bulk-fetch pillars, "about this repo/skill" summary (DECISIONS.md #025) |
| `link_scan.py` | active | Fifth pillar, README link-integrity scan — link-text-domain-mismatch (critical, forces DANGER) and the downloadable-binary caveat (DECISIONS.md #026). **Was tracked in git but had no row in this map at all until the hackathon session H1 reconcile found it by direct file-list comparison** — a real gap this file's own reconcile step exists to catch, not merely a hackathon-session omission |
| `interfaces.py` | active | `FileAccessProvider` (extracted, proven swappable, `fetch_all_files` bulk-fetch method, `fetch_repo_description` default-None hook) and `ModelProvider` (forward-defined for M9). Hackathon session H1: added `ModelResponse` (`stop_reason`/`stop_details`/`usage`/`model`/`request_id`/`latency_ms`) and `analyze_detailed()`, so a refusal/truncation is distinguishable from a normal answer — DECISION 028 |
| `github_provider.py` | active | `GitHubFileAccessProvider` — per-file contents API plus `fetch_all_files` (one tarball download, graceful per-file fallback verified with a real simulated failure) and `fetch_repo_description` (GitHub's own repo `description` field) |
| `semver_resolve.py` | active | npm caret/tilde range resolution against the live registry, no third-party semver lib |
| `suppression.py` | active | `.repocheck-allow.json` suppression mechanism, category+path matching, type-validated |
| `concurrency.py` | active | Shared thread-pool helper (`parallel_map`), ~9x measured speedup, used by verdict.py/freshness_scan.py/skeleton.py |
| `test_provider_swap.py` | active | Proves `FileAccessProvider` swap works with zero changes to calling code, using a fake in-memory provider |
| `repocheck.py` | active | CLI entry point — zero scan logic, auto-detects repo/skill mode, exits non-zero on a failed/degraded scan |
| `anthropic_provider.py` | active | `AnthropicModelProvider` — raw HTTP (no SDK dep), specific missing-key error. Hackathon session H1: `max_tokens` 1024→16000, a real request timeout, `analyze_detailed()` reads real `stop_reason`/`usage`/`model`/`request-id`, falls back to local `.env` via `envfile.py` |
| `deep_scan.py` | active | Opt-in deep scan — collects ONE bounded joint multi-file bundle per scan (`bundle.py`, DECISION 027) instead of one request per file; `user_intent` supplies authorization from outside the bundle (DECISION 028); malformed JSON/refusal/truncation/bad citation all map to `ANALYSIS_FAILED`, never an empty findings list; a markdown-fence wrapper is stripped before parsing. Extensively live-tested hackathon session H1 across `claude-fable-5-1`/`claude-opus-4-8`/`claude-sonnet-4-5` (see `hackathon/results/`) — but OI-020's two named acceptance criteria still need re-running through this pipeline specifically (see `verify_deep_scan.py` row) |
| `verify_deep_scan.py` | active | Live-verification script for deep_scan.py's 2 acceptance criteria (OI-020). Run for real hackathon session H1 (both PASS) — but against the older single-file `analyze()` interface on `claude-sonnet-4-5` (its hardcoded default model), not the new joint-bundle pipeline on Fable 5.1. Still needs updating to call `run_deep_scan()` with an explicit `claude-fable-5-1` model to close OI-020 as originally scoped |
| `skills/repocheck/SKILL.md` | active | RepoCheck's own Claude Code skill wrapper — scans clean under its own instruction-scan (dogfooding found and fixed a real false positive); now also instructs leading with the about-summary and never auto-installing after the report (DECISIONS.md #025). Mirrored at `~/.claude/skills/repocheck/SKILL.md` (user-wide install, session 3) — keep both in sync |

**Main-project status inherited into this fork (unverified as a live
claim by this fork — see the MILESTONES.md correction above):** repo is
public at github.com/14leux/repocheck, default branch `main`. M9 is
IN PROGRESS pending OI-020's two named criteria being re-run through
the joint-bundle pipeline (this fork gathered extensive live evidence
this session but via a materially different pipeline than OI-020 names).
OI-021 (proximity-based obfuscation matching) remains deferred, larger
scope than a pattern fix.

**Reconcile note (main-project session, historical):** `git ls-files`
compared against this map — all 30 tracked files accounted for at that
time, no mapped-but-deleted entries. Fixed two staleness issues found
during reconcile: a broken markdown table (a stray blank line had split
it into two separate tables) and three descriptions that still described
pre-fix state (`code_scan.py`/`freshness_scan.py` referencing OI-017/
OI-018 as open when both are now closed). Also consolidated three
function-level rows that had been added ad hoc back into their parent
file's single row — the map's granularity is files, not functions
within already-mapped files.

**Reconcile note (hackathon session H1 close, 2026-09-19):** `git
ls-files` now returns 77 tracked files in this fork (up from the 30 the
prior note counted), reflecting the hackathon work — fixture directories,
`hackathon/results/`, `bundle.py`/`envfile.py`, and the two new
`DECISIONS.md` entries. All new files added to this map above, at the
directory level for `fixtures/` and `hackathon/results/` (many small,
similarly-purposed files — a per-file row would exceed the map's stated
granularity value for this kind of content). Three stale rows fixed in
place rather than just flagged: `MILESTONES.md`'s self-contradictory
"ALL COMPLETE" claim (corrected directly in that file), `deep_scan.py`'s
row (rewritten — no longer accurate after DECISIONS 027/028), and
`verify_deep_scan.py`'s row (its PASS this session used a different code
path than OI-020 actually names, now stated explicitly rather than
implied). One real pre-existing gap found by direct comparison and
fixed, not just flagged: `link_scan.py` was tracked in git and had been
for at least one prior session (it implements DECISION 026) but had no
row in this map at all — added. No other mapped-but-deleted entries
found; every row in this file now corresponds to a real, current path.
