# tasks/wip.md

Project session goal: Hackathon (Breakthrough track) — bounded skill
authority review on Claude Fable 5.1, per HACKATHON_CLAUDE_CODE_HANDOFF.md
Working tree: D:\Projects\repocheck-hackathon (origin = 14leux/repocheck-hackathon)
Active operator: Claude Code (Sonnet 5)
Operator state: local .env secrets wired up; waiting on Mailu to paste real
  ANTHROPIC_API_KEY (and optionally GITHUB_TOKEN) into .env
Last updated: 2026-09-19

Current step: added envfile.py (stdlib-only .env loader) so
  ANTHROPIC_API_KEY/GITHUB_TOKEN can be supplied via a local, git-ignored
  .env file instead of a shell export -- necessary because this harness's
  Bash/PowerShell tools spawn a fresh, non-persistent shell per call, so a
  shell-level export set in one tool call never reaches the next.
  anthropic_provider.py and github_provider.py each call load_env_file()
  right at their existing os.environ.get(...) call site. .env.example
  (tracked, no real values) documents the two variables; .env itself
  (real file, git-ignored, confirmed via `git check-ignore -v .env`) was
  created with both keys blank, waiting for Mailu to paste real values
  directly into the file with a text editor -- never through chat.
Next concrete step: once .env has a real ANTHROPIC_API_KEY, run
  verify_deep_scan.py for real -- the two live-call acceptance criteria
  (injection resistance, a real detection win) are still unverified;
  offline tests prove the plumbing, not the model's actual behavior. Then:
  author hackathon/prompts/authority_review_v1.txt and hash it into
  EXPERIMENT_CARD.md section 4; get organizer answers into section 9;
  re-cut fixtures/legit-permission-gated-setup (D-2c) with neutral naming
  and out-of-bundle permission per BLIND_SPOTS.md section A, then build
  its harmful twin D-2.
Done so far: clone stood up, pushed, marked as the hackathon working copy;
  experiment card v0.1 (DRAFT, not frozen); D-2c fixture committed;
  hackathon/BLIND_SPOTS.md design review (7 fixture defects, 3 case-matrix
  gaps, 3 implementation blind spots); bundle.py + interfaces.py
  ModelResponse + anthropic_provider.py timeout/token-cap fix +
  deep_scan.py joint-bundle rewrite (all verified offline,
  test_deep_scan_bundle.py, 7/7 pass); envfile.py + .env.example + local
  .env this round; KNOWLEDGE.md entries for the Fable 5.1 API constraints,
  the bundle-collection fix, and the .env loader; .agent/instructions.md
  OI-020 row refreshed (still OPEN, description matches current code).
Tried and failed: nothing substantive this round.
Dirty or partial files: .env exists locally with both keys still blank —
  git-ignored, never committed, not part of any commit. Everything else
  staged together in this session's commits.
Verification already performed: envfile.load_env_file() tested against an
  isolated temp file — parses KEY=VALUE/comments/blank lines/quoted
  values correctly, and confirmed a real env var already set is never
  overwritten by the file (setdefault, not assignment). Confirmed
  AnthropicModelProvider's MissingApiKeyError still fires correctly with
  an empty real .env at repo root, message now mentions .env.example.
  Confirmed .env is invisible to `git status` and matched by
  `git check-ignore -v .env` before anything was staged. Both offline
  suites (test_provider_swap.py, test_deep_scan_bundle.py) re-run clean
  after the envfile wiring. All touched files py_compile clean.
