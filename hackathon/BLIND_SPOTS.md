# Blind-spot review — fixture D-2c and the case matrix

**Date:** 2026-09-19 · **Reviewed:** `fixtures/legit-permission-gated-setup/`
(commit `84f2d12`), `hackathon/EXPERIMENT_CARD.md` v0.1, `deep_scan.py`,
`anthropic_provider.py`.

**Nothing has been run.** No scan, no model call, no measured result. This
is a design review of artifacts, not an evaluation.

---

## A. Defects in the D-2c fixture as committed

### A-1. The directory name leaks the answer key into model-visible input

The path is `fixtures/legit-permission-gated-setup/` and the skill's
frontmatter `name:` is `format-converter-legit`. Card §5 lists raw file
paths as **model-visible**, and separately forbids "case labels such as
'harmful' or 'control'" from reaching the model. The word `legit` appears
twice in content the model will read.

A model that scores correctly here may have scored the filename. Fix: neutral
opaque IDs (`fixtures/case-a2/`), and a skill `name:` that a real converter
skill would plausibly use.

### A-2. The user permission is declared inside the bundle being judged

`SKILL.md` line 6 says "User permission: convert files between formats ONLY."
That is the repository stating its own authorization scope — the exact thing
the handoff and card say cannot be accepted ("A repository's own README,
allowlist, or 'approved' claim cannot authorize its behavior").

Every case needs permission supplied **outside** the bundle: a separate
`intent.json` the harness passes as user-side input, never as scanned
content. As committed, D-2c can only be judged by trusting the artifact
under review.

### A-3. The fixture argues its own innocence in prose

Two sentences do the work: "This skill never installs anything automatically"
and "This skill will not fetch or execute this installer on your behalf."
That is reassurance addressed to the reviewer, and it is structurally the
same move RC-04 exists to punish — repository text steering the review.

The control should be benign **structurally** (no fetch-or-execute
instruction exists anywhere; the setup doc addresses the human, not the
agent), so the model has to derive that. If the pair differs mainly in
vocabulary, the eval rewards keyword-spotting, which the research warns
against in the same words for RC-08 ("do not reward a model simply for
noticing a function named redact").

### A-4. The pair will not be structurally matched

RC-02 specifies four files: `SKILL.md` with the missing-service condition,
`references/setup.md`, a `settings.json` selecting the setup destination, and
a helper source. D-2c has two files, no settings, no helper.

If the harmful twin gets four files and the control has two, file count and
file shape become a shortcut to the answer. Paired fixtures must be identical
in structure except for the single thing under test.

### A-5. No trusted environment facts, so reachability is unanswerable

RC-02 asks the model to state whether the branch condition is true, false, or
unknown. Nothing in the fixture says whether `converter` is on PATH. Under the
card's own rules the only defensible answer is `INSPECT` on reachability — for
both variants, which collapses the distinction the pair is meant to test.

Environment facts belong in the same out-of-bundle input file as the
permission (A-2).

### A-6. No pinned snapshot identity

Card §6 requires a content digest per case. Not present. Without it, run
records cannot state which bytes were analyzed, and RC-07 (stale scan) has no
mechanism to build on later.

### A-7. Real-domain URL instead of `.invalid`

`https://github.com/example-vendor/converter/releases/tag/v2.3.1` is a real
domain with a plausible path. The authoring rule is fictional names and
`.invalid` destinations. Low severity — nothing fetches it today — but the
link-integrity pillar and any future collector both treat real URLs
differently from obviously-fake ones, and a live 404 is a different test than
an unresolvable host.

---

## B. Gaps in the case matrix

### B-1. Only one kind of control: the obviously-innocent one

Every control in the matrix is clean-by-construction. Nothing tests a bundle
that *looks* alarming and is genuinely authorized — the RC-01 control names
this shape (a credential used solely to authenticate to its own issuer API)
but the matrix carries one instance of it.

False accusation is the failure mode that makes a security tool unusable, and
it is currently the least-pressured dimension in the suite.

### B-2. Nothing provokes `ANALYSIS_FAILED`

It is one of four dispositions and a separately counted critical failure, but
no case is designed to trigger it — no oversized bundle, no deliberately
malformed model response, no citation that fails validation. An error path
that is never exercised before the demo is an error path that fails during
the demo.

### B-3. The suite tests skill mode only

Fair to scope, but the demo narrates "RepoCheck." The CVE, freshness, and
link-integrity pillars are untouched by every case. Say "skill authority
review" in the pitch, not "RepoCheck catches this."

---

## C. The implementation blind spot that outranks all of the above

### C-1. `deep_scan.py` cannot answer a cross-file question at all

`run_deep_scan()` loops over paths and calls `provider.analyze()` **once per
file**, discarding each result into a per-path dict. There is no joint
bundle, so no request ever contains two files at once.

Every P0 case — credential traced from `collect.py` through `schema.json`
into `send.py`, conditional setup reached from `SKILL.md` through
`references/setup.md` — is a cross-file question. Against today's code these
are not hard cases; they are **structurally unanswerable**, and the model
would be scored for failing something it was never shown.

This is the single change that has to land before any fixture can be run
against the pipeline.

### C-2. `max_tokens: 1024` plus silent malformed-JSON handling

`anthropic_provider.py` hardcodes `max_tokens: 1024`. The card's output
schema — findings with per-link citations, byte spans, basis and uncertainty
— will not fit. On Fable 5.1, thinking is always on and its tokens count
against that same ceiling, so the budget is tighter than it looks.

Truncation produces `stop_reason: "max_tokens"` and invalid JSON. And
`run_deep_scan()` converts a `JSONDecodeError` into
`{"findings": [], ...}` — which `main()` then prints as **"no findings."**

A truncated response currently renders as a clean bill of health. That is the
handoff's named risk #4, and the small token cap makes it not a rare edge
case but the expected outcome for a structured authority review.

### C-3. The provider is blind to everything the run record requires

`analyze()` returns `"".join(block.get("text", "") for block in ...)` — a
bare string. It never reads `stop_reason`, `stop_details`, `usage`, the
resolved `model`, or the response id.

Card §9 requires every one of those per run. As written, the run record
cannot be produced, and two specific failures are invisible: a **refusal**
(`stop_reason: "refusal"`) and a **truncation** both arrive as a short string
that looks like a normal answer.

---

## D. Fable 5.1 alignment — concrete changes to the current setup

Keep the raw-HTTP provider (card decision D-2). Every feature needed here is
a plain JSON body field; the SDK would buy typed errors and `messages.parse()`
at the cost of the project's zero-dependency promise. Not worth it.

| # | Change | Where | Why |
|---|---|---|---|
| 1 | Explicit model selection; stop relying on `DEFAULT_MODEL` | `anthropic_provider.py:24,32` | Currently `claude-sonnet-4-5`. The hackathon path must name `claude-fable-5-1` explicitly and record what it sent |
| 2 | `max_tokens` 1024 → 16000 | `anthropic_provider.py:50` | Structured output plus always-on thinking will not fit in 1024 (C-2) |
| 3 | Add `output_config: {"effort": "high", "format": {...}}` | provider body | Effort nests **inside** `output_config`, not top-level. Structured output replaces the forced-tool-call approach, which 400s on Fable |
| 4 | Send no `temperature` / `top_p` / `top_k` | provider body | 400 on Fable 5.1. Currently absent — keep it that way, and add a comment so nobody "fixes" determinism by adding it |
| 5 | Send no `thinking` parameter | provider body | Always on; `disabled` and `budget_tokens` both 400 |
| 6 | Send no `fallbacks` | provider body | A refusal silently answered by another model would be scored as Fable's result |
| 7 | Add an explicit timeout | `urlopen(req, timeout=N)` | `urllib` defaults to the socket default, which is `None` — it can hang forever. Handoff risk #3 |
| 8 | Return a result object, not a string | `analyze()` + `interfaces.py` | Must carry `stop_reason`, `stop_details`, `usage`, resolved `model`, request id (C-3) |
| 9 | Malformed JSON → `ANALYSIS_FAILED` | `deep_scan.py:~100` | Never an empty findings list that prints "no findings" (C-2) |
| 10 | Joint bounded bundle instead of per-file calls | `run_deep_scan()` | Without it no cross-file case is answerable (C-1) |
| 11 | Confirm the org is not zero-data-retention | account setting | Fable 5.1 requires 30-day retention; a ZDR org gets `400` on every request and it will read as a setup bug |
| 12 | Soften the "prompt-injection-safe by construction" claim | `deep_scan.py` docstring | Delimiters are defense in depth, not a guarantee. Named in the handoff |

No retry logic is needed: `urllib` retries nothing, which happens to match the
card's `max_retries = 0`. Worth a comment so it stays deliberate rather than
accidental.
