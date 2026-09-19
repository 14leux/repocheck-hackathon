# Council: Breakthrough-track viability under the fixed rules, 100-minute clock

## Original question

Pressure-test our hackathon submission strategy under a hard 100-minute clock,
given the Breakthrough track's actual fixed rules (just confirmed from the
platform screenshot) and our own verified Fable-vs-comparator data.

## Scan (Step 0)

Found and read: `hackathon/EXPERIMENT_CARD.md` (D-7, closed, Narrative Option
B), `KNOWLEDGE.md` (H1 entries), `HACKATHON_CLAUDE_CODE_HANDOFF.md`
("Session H1 update" section), `hackathon/results/rc02-report.md` /
`rc04-sanity-report.md` / `rc08-sanity-report.md`, and the prior council
`council-transcript-20260919T201238.md` (run before any live data existed).
That earlier council already flagged: "If no gap, retain the useful workflow
with limited claims" and "Ask organizers whether a workflow breakthrough is
eligible; do not manufacture one" — written before the team decided against
organizer contact and before the fixed-rules screenshot existed. No gap
requiring a manual question round; proceeding straight to framing.

## Framed question

**System:** Dr. RepoCheck — traces what a Claude Code skill would do with a
user's data (trigger → data read → transformation → destination) against the
user's own stated authorization (supplied outside the analyzed bundle),
citing exact bytes. Four dispositions: `EXCEEDS_SCOPE`, `INSPECT`,
`NO_EXCESS_FOUND_IN_SCOPE`, `ANALYSIS_FAILED` (never silently "no findings").

**The fixed rules, verbatim from the platform (Breakthrough track):**
- "THE PROBLEM: You would bring it to a problem you had given up on. The
  hard thing the previous model could not do."
- "FIXED RULES: Live demo only, no slides in place of software. Five
  minutes, hard clock. Show what Fable 5.1 does here that the previous
  model could not."
- "WHAT THE JUDGES ASK: Does Fable 5.1 actually unlock this, or would the
  old model have done it?"

**Our verified data** (cross-checked cell by cell against the underlying
reports), 4 independent fixture families, 6 matched cells per model:

| Model | Correct | Refused | Other failure | Harmful caught |
|---|---|---|---|---|
| `claude-fable-5-1` | 2/6 | 4 (`cyber`) | 0 | 0/3 |
| `claude-opus-4-8` | 4/6 | 0 | 2 unparseable JSON | 3/3 |
| `claude-sonnet-4-5` | 5/6 | 0 | 1 false positive | 3/3 |

Two distinct, reproducible refusal patterns: Fable refuses the harmful
variant only on "outcome-tracking" violations (credential exfil,
persistence) — correctly clearing the safe twin every time — but refuses
**both** variants on "topic-tracking" violations (remote fetch-and-execute),
unable to distinguish good design from bad on that class at all.

**Already decided by the team:** no organizer contact; Narrative Option B
(disclose the null/negative comparison, don't chase a favorable case).

**Candidate paths to pressure-test:**
- (A) Submit to Breakthrough, disclose fully, pitch the architecture as the
  breakthrough, answer the judges' literal question with "no."
- (B) Reframe "we mapped exactly where Fable's safety layer draws a line"
  as itself a Fable-specific unlock.
- (C) Any other honest path the council identifies.
- Plus: five framing questions for the pitch regardless of path — what the
  tool IS, the use case, the users, why it matters, what's missing without
  it.

**Constraint:** 100 minutes total, including whatever build time remains
after this decision. The council must land on one recommended path.

## Recency step

No external facts change this decision — the fixed rules are given verbatim
from today's screenshot, the model data is our own verified live testing.
Skipping the research step.

---

## Advisor responses

### The Contrarian

The plan under pressure-test is "submit to Breakthrough with full
disclosure" (Option A). Here is the strongest case against it: **the fixed
rule is not asking for context, it is asking for a yes/no, and our honest
answer is no.** "Show what Fable 5.1 does here that the previous model could
not" is not a rubric dimension worth partial credit on — it is gating
language, the same shape as "the hard thing the previous model could not
do." A disclosed negative result is intellectually honest, but it is not a
demonstration of the fixed rule; it is a demonstration that the fixed rule
does not hold. Judges scoring Breakthrough are told to check this
specifically ("does the old model actually not do this") — disclosing "it
does, better" inside a Breakthrough slot does not satisfy the rule, it
concedes it, articulately. The five-minute clock makes this worse: there is
no time in a hard five minutes to both concede the fixed rule AND land the
architecture pitch AND leave the judges with anything other than "this
doesn't belong in this track." That is not a reason to lie or hunt for a
win — it is a reason to ask whether Breakthrough is the right box to check
at all, independent of any organizer conversation. Team decided not to *ask*
organizers a judgment question; nobody has established that changing which
track box is checked on the submission form *requires* asking anyone. That
distinction has not been tested and should be, in the first five minutes of
the 100, before more build time goes into a track whose own fixed rule we
cannot honestly satisfy.

### The First Principles Thinker

Strip this to what has to be true for each option to work.

For (A) to work: judges must be willing to score "no, but here's a good
reason why not" as satisfying "show what Fable 5.1 does here that the
previous model could not." That requires the fixed rule to be advisory, not
gating. Nothing in the screenshot supports that reading — "FIXED RULES" is
the section header, and the bullet under it is a demonstration requirement,
not a discussion prompt.

For (B) to work: "we mapped where Fable's safety layer draws a line
differently than other models" would need to be a genuine unlock of *this
tool's actual task* (skill authority review), not a different, smaller
finding about model behavior in general. It isn't — the mapping is evidence
about a *limitation*, and dressing a limitation as an unlock is exactly the
cherry-picking the handoff's own rule forbids ("no case is added because an
earlier one failed to favor Fable"). This collapses into (A) with worse
honesty, not a third option.

For a track-reclassification path (call it D, since the frame invited "any
other path"): what has to be true is (i) track selection is a value the
team controls on its own submission, not something requiring organizer
approval, and (ii) the Everyday track's rules (if they exist as a
comparably fixed set) do not carry the same "unlock" requirement. Both are
checkable facts, not judgment calls — reading a submission form or a rules
page is not "asking organizers." This is the cheapest, fastest thing to
verify in the whole 100 minutes, and it dissolves the dilemma instead of
managing it.

### The Expansionist

What's being under-weighted here: **the actual product is strong, and it
does not need Breakthrough's frame to be strong.** Read the tool cold,
ignoring which track it's in: it supplies user authorization from *outside*
the artifact being reviewed (SkillScope and comparable academic work let
the skill grade its own homework by deriving scope from the skill's own
declared behavior); it treats a failed or refused analysis as a disclosed,
first-class result instead of silently folding it into "clean" (directly
evidenced by this session's own bug fixes — the markdown-fence bug, the B6
cross-file bug — each of which would have produced a *wrong* clean-looking
answer if not caught); and it now demonstrably works cross-file, live,
against a real public repo. That is a genuinely good Everyday-track pitch:
"the everyday tool that tells you honestly when it doesn't know, instead of
guessing wrong quietly." The team has been treating the Fable finding as
something to manage around inside Breakthrough. It reads differently
outside that frame — as a second, smaller, still-honest story ("we also
mapped exactly where a frontier model's safety layer misfires on security
review, which is useful to Anthropic and to anyone building on Fable") that
can live as a footnote or an appendix link, not the headline risk of the
five-minute clock.

### The Outsider

Reading this cold, with no history: a team built a real, working security
tool, generated real evidence, and the evidence says the required
demonstration for the track they're in does not hold. Then they spent
significant effort making sure the disclosure of that fact is honest and
well-presented. That is admirable, but it skips the obvious first move:
**check whether they're in the right track before perfecting how to lose
gracefully in the wrong one.** Nothing in the frame states that track choice
is locked, irreversible, or requires permission — that's an assumption that
crept in alongside the earlier, separate decision not to ask organizers a
judgment question. Those are not the same thing. One other thing that reads
oddly from outside: the fixed rule literally names "the hard thing the
previous model could not do," worded as a general capability claim, not
"this specific security-review task." Nothing here has tested whether Fable
5.1 does *something else* — outside the security-review pipeline entirely —
that the comparator can't, which might be a legitimate, non-cherry-picked
Breakthrough angle if it exists. Nobody has looked, because the team's
whole 100-minute frame started from "we already have a task, does Fable
unlock it" rather than "what does Fable actually unlock, and do we have a
task for that." Worth five minutes of thought, not more, given the clock.

### The Executor

Concrete plan, ordered, assuming the council converges toward
reclassification as the primary path with disclosure-in-Breakthrough as the
fallback:

1. **(5 min) Resolve the track-switch fact, not a judgment call.** Check the
   submission portal/rules page directly: is track a form field the team
   sets, or an assignment? Does Everyday carry its own fixed "unlock" rule?
   Is "Required model demonstration: Claude Fable 5.1" a track-independent
   requirement (it reads that way in the original handoff, listed above and
   separate from "Current team decision: Breakthrough")? This is reading
   public rules text, not contacting a person — does not violate the
   no-organizer-contact decision.
2. **(0 min, decision point) If Everyday is available and self-selectable:**
   switch. The five-minute demo no longer needs to defend an unmeetable
   claim, and the Fable-refusal finding becomes a strength ("we tested this
   honestly against two models and are telling you exactly where it's
   weaker") rather than a liability to manage.
3. **(remaining ~90 min) Build the site and demo exactly as already
   planned** — Phase 0 (`--intent` wiring, `hackathon/cases/*.json` for 2–3
   cases) and Phase 1 (prove the live pipe) are unchanged and still
   required regardless of track; they were never track-specific. Phase 3
   UI/copy adjusts headline framing only — "the everyday tool that tells
   you honestly when it doesn't know" instead of a model-advantage pitch —
   the underlying build plan barely changes.
4. **If Everyday is not available or carries its own blocking requirement:**
   fall back to (A) exactly as scoped — five-minute script leads with the
   architecture, states the judges' literal question and answers it
   honestly in the first 90 seconds ("no, and here is what we found
   instead, live"), does not spend clock time softening it. Same
   `hackathon/demo.py` build either way.

### The Revenue Lens — SITS OUT

No pricing, cost, or ROI decision in play here; this is a track-fit and
framing question, not a revenue one.

### The Gatekeeper

There is a real distribution dimension: **who decides whether this
submission is seen at all is the judging rubric, not a person you'd need to
ask.** The gate here is mechanical — a scoring criterion, "does Fable unlock
this" — not a human gatekeeper with discretion. That reframes the earlier
"we're not asking organizers" decision correctly: that decision was about
not asking a *person* for a favor or a ruling. It says nothing about
reading the rubric itself and choosing the track that the built product
actually satisfies. Treating "don't ask organizers" as "don't reconsider
the track" conflates a person-facing gate with a form-facing one. The team
should route around the human gate exactly as decided, and use the
mechanical gate (track selection) exactly as it's designed to be used — by
self-selecting the track the evidence supports.

### The Trap Detector

The most dangerous unexamined assumption in the whole 100-minute plan:
**"we already decided Breakthrough, so the only open question is how to
present the Fable finding inside Breakthrough."** That's a sunk-cost framing
carried over from a decision (session H1, "Current team decision:
Breakthrough") made before any live data existed. The original team
decision was provisional on an unlock existing; the unlock didn't
materialize; the decision was never revisited against that fact, only
managed around. Fastest possible test, doable in the time already spent
writing this frame: read the actual submission form / track rules for
Everyday, right now, before building anything else. If it's a self-service
field and Everyday has no comparable "unlock" gate, the entire disclosure-
framing problem this session has spent real effort solving disappears, and
that effort (the honest table, the demo script, the "we'd rather show a
true negative" line) is *still useful* — it becomes the strongest,
most-differentiated part of an Everyday pitch instead of the weakest part
of a Breakthrough one.

---

## Anonymization map

- A = The Contrarian
- B = The First Principles Thinker
- C = The Expansionist
- D = The Outsider
- E = The Executor
- F = The Gatekeeper
- G = The Trap Detector
(Revenue Lens sat out, not lettered)

## Peer review

### Pass 1

Strongest contribution: **G**. It correctly names the load-bearing sunk-cost
assumption underneath the whole 100-minute frame — that the track choice
itself was never revisited once the disqualifying evidence arrived — and
proposes a five-minute, no-permission-needed test to resolve it before
anything else gets built. Biggest blind spot: **E**. The executor's plan is
well-sequenced but assumes step 1's answer will be "yes, switchable" without
budgeting real time for "no" — if the rules page is ambiguous (plausible;
hackathon rules pages often are), five minutes won't resolve it cleanly and
the plan needs a hard cutoff to fall back to (A) rather than drift. What
everyone missed: nobody checked whether the *deadline* for changing track
selection has already passed, independent of whether it's technically a
form field — a hackathon platform might lock track choice at a point
already behind us.

### Pass 2

Strongest: **D** (the Outsider). The observation that "the previous model
could not do X" is a general capability claim, not scoped to security
review, is the one genuinely new idea in the set — everyone else worked
within the existing task; D questioned whether the task itself was the
right one to test Fable against. Biggest blind spot: **C** (the
Expansionist). Its "let the Fable finding live as a footnote" suggestion is
good but understates how much of this session's actual verified work
(citation validation, B6, the disclosed-failure architecture) is genuinely
demo-worthy regardless of track — it undersells the strength of the
fallback case. What everyone missed: nobody addressed whether the team
*has time* to build a materially different pitch for Everyday vs.
Breakthrough inside the same 100 minutes, or whether the two pitches are
close enough in required assets (same demo cases, same architecture
explanation, different headline framing only) that this is a non-issue —
this needs to be stated explicitly, not assumed.

### Pass 3

Strongest: **A** (the Contrarian) and **F** (the Gatekeeper) converge
independently on the same distinction — a human-facing gate (asking
organizers a favor) is not the same as a mechanical gate (reading rules,
picking a track field) — and that distinction is what actually unblocks the
decision without violating anything the team already committed to. Biggest
blind spot: **G** itself, on reflection — "if Everyday has no unlock gate,
the disclosure work becomes the strongest part of an Everyday pitch"
assumes Everyday's judging rubric *rewards* honest disclosure and rigorous
testing methodology; that's plausible but unverified, and an Everyday
rubric could just as easily reward polish/usefulness/completeness with no
credit at all for the model-comparison rigor this session invested in.
What everyone missed: nobody proposed the actual five-minute demo script
text for either branch (Breakthrough-disclosure vs. Everyday) — the
council resolved *which track*, not *what gets said in the room*, and the
Executor's plan needs that as its next concrete deliverable either way.

---

# Chairman Synthesis

## Where the council agrees

Every advisor, independently, arrived at the same structural point: **the
team's Breakthrough commitment was made before the disqualifying evidence
existed, and has been managed around rather than revisited.** The fixed
rule ("show what Fable 5.1 does here that the previous model could not") is
gating language, not a rubric dimension to soften with honest disclosure —
disclosure inside Breakthrough concedes the rule, it does not satisfy it.
And the team's own "no organizer contact" decision, on inspection, was
about not asking a *person* a judgment question — it says nothing about
whether track selection is a self-service choice the team can simply
change by reading the rules.

## Where the council clashes

**A/D/F/G favor investigating an Everyday-track switch first; E's plan
assumes it will succeed; C treats the Fable finding as manageable within
Breakthrough via careful framing.** The chairman sides with A/D/F/G: C's
position (manage the disclosure well inside Breakthrough) was this
session's plan *before* the fixed-rules screenshot existed, and the
screenshot is new, specific, and gating in a way the team's prior planning
didn't have visibility into. C is not wrong that the tool is strong enough
to survive either framing — that's true and useful — but it doesn't
resolve which track actually fits what was built.

**Pass-1's caught risk (E's plan has no time-boxed fallback)** is real and
gets folded into the recommendation below as an explicit cutoff.

## Blind spots the council caught

- Whether the deadline to *change* track selection has already passed —
  unresolved, must be checked directly, first action.
- Whether Everyday's own rubric has a comparable fixed gate, and whether it
  rewards or ignores the rigorous disclosure work already done — unresolved,
  same check.
- Whether Fable 5.1 unlocks something entirely outside the security-review
  task (D's point) — worth naming once, not worth spending build minutes
  chasing inside a 100-minute clock; if nothing surfaces immediately from
  what's already known about this session's testing, drop it.
- The two pitches (Breakthrough-disclosure vs. Everyday) share almost all
  underlying assets — same demo cases, same architecture explanation,
  same honest table — differing mainly in headline framing and which
  question gets answered first. This is not a fork requiring double the
  build time.

## Priority filter

1. **Resolve the track-eligibility fact** — five minutes, no build cost,
   dissolves or confirms the entire dilemma.
2. **Protect Phase 0 + Phase 1** (the `--intent` wiring, `hackathon/cases/*.json`,
   the live pipe) — required under either track, non-negotiable, matches
   what was already decided before this council.
3. **Write the five-minute script for whichever track wins** — concrete,
   timed, rehearsed, not left implicit.
4. **UI/copy polish** — genuinely last, and lighter than planned since the
   framing question mostly resolves at the headline level, not throughout.

## The recommendation

**Spend the first 5 of the 100 minutes checking, directly from the
submission portal or rules page (not by asking a person), whether track
selection is still changeable and whether Everyday carries a comparable
fixed "unlock" requirement.**

- **If switchable and Everyday has no equivalent gate:** switch. Keep the
  Fable-refusal finding as an honest, secondary "here's what we tested and
  found" section rather than the central risk of a five-minute clock — it
  becomes a strength (rigor) instead of a liability (a rule you can't meet).
  Everything else in the build plan (Phase 0 → Phase 1 → demo → site)
  proceeds unchanged; only the headline framing and which question the demo
  answers first changes.
- **If not switchable, or Everyday carries its own blocking requirement:**
  proceed with Option A exactly as already scoped — lead the five minutes
  with the architecture, state the judges' literal question and answer it
  honestly in the first 90 seconds ("no — and here's what we found instead,
  live, with citations"), do not spend clock time softening a rule you
  cannot meet.

Either way, this decision consumes 5 of the 100 minutes, not more — it is a
fact-check, not a re-litigation, and the build work underneath it barely
changes shape.

## The one thing to do first

Open the hackathon submission portal / rules page right now and check two
facts: (1) is the track selector still editable for this submission, and
(2) does the Everyday track's own rules page carry a comparable fixed
"unlock" or "previous model could not" requirement. Report both back before
any further building.

## Timestamp

2026-09-20, Africa/Nairobi.
