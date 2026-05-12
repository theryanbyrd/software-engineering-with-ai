# Facilitator Guide — 90-Minute Workshop

A run-of-show for the Code Review Craft workshop. Direct companion to Ch 2 §2.4 ("train reviewers on the seven signatures — a 30-minute session per quarter beats a 60-page style guide") and Ch 43 §43.3 ("code review craft. Mandatory. One review per week with a senior, talking through the cues.").

Per Ch 22 §22.4:

> A junior reviewer who can spot the seven AI-slop signatures is more valuable than a senior who rubber-stamps.

This workshop is how juniors become that valuable reviewer. The book's 30-minute quarterly cadence is the minimum; this 90-minute version is the onboarding format. Run it once per cohort; refresh quarterly with the shorter version.

## Who runs this

A senior or staff engineer who has personally caught at least three slop incidents in code review and has read [`ai-code-smell-checklist.md`](ai-code-smell-checklist.md) cover to cover. If the facilitator hasn't done both, recruit a co-facilitator who has.

This is a facilitator's role, not a presenter's. The format is hands-on; the facilitator's job is to provoke the right realizations, not to deliver content.

## Who attends

- **Required**: every engineer at L1 certification or below per [`../agent-autonomy-levels/certification-gates.md`](../agent-autonomy-levels/certification-gates.md). L2 requires demonstrated ability to spot the seven signatures.
- **Recommended**: every engineer who reviews PRs, regardless of seniority. Seniors miss signatures too; the workshop is calibration for them as well.
- **Optional**: PMs who write specs for AI-assisted work. Useful for the "what does a reviewable PR look like" framing.

Cap the room at 12. Larger rooms make the diff-review exercises unworkable.

## Prep — 1 week before

| Item | Owner | Notes |
|---|---|---|
| Confirm attendee list and roles | facilitator | If half the attendees are seniors, swap the exercises for the harder calibration diffs |
| Print [`reviewer-cheatsheet.md`](reviewer-cheatsheet.md) one per attendee | facilitator | One-sided; readable at arm's length |
| Pick 4 exercises from [`exercises/`](exercises/) | facilitator | Two single-smell, two multi-smell. Match attendee experience. |
| Prep the AI-reviewer demo | facilitator | Open a real PR; the agent runs [`review-prompts/general-review.md`](review-prompts/general-review.md) live |
| Confirm room with projector or large monitor | facilitator | Diff review benefits from a shared screen for debrief |
| Send pre-read | facilitator | One day before: link [`ai-code-smell-checklist.md`](ai-code-smell-checklist.md). 20 minutes of reading. Don't make it optional. |

## Prep — day of

- 30 minutes early: room set up, screen tested, exercises queued, cheatsheets at each seat
- 10 minutes early: facilitator's own copy of the cheatsheet annotated with the exercises' planted smells (don't leak this; use it to refer to during debrief)
- 5 minutes early: open the room. Engineers who arrive early are the engineers who care; talk to them

## Run-of-show

### 0:00–0:05 — Opening framing

Stand. Don't sit. The frame matters; deliver it with weight.

> "Generation is cheap. Review is not. The book's claim — Ch 2 — is that AI slop is the dominant failure mode of AI-assisted development, and the only thing that catches it is a reviewer trained to recognize the seven signatures on sight. Today we're going to drill those seven. By the end of 90 minutes, you should be able to look at a diff and pattern-match it the way a senior reviews production code.
>
> Three rules:
>
> One — there are no stupid questions in this room. The signatures are subtle. If you don't see what I'm pointing at, that's not a failure; that's the workshop working.
>
> Two — when we hit the exercises, don't shout out the answer. Write your review comments first, then we discuss. The signatures are a pattern library; you build the library by seeing them yourself, not by hearing them from someone else.
>
> Three — none of this is about blame. The AI authored the slop. Our job is to catch it before it ships. The author of the slop is not in the room and is not the point.

If you have new hires in the room, name them: "Welcome. The vocabulary in this room is the vocabulary the team uses. Ask if anything isn't familiar."

### 0:05–0:35 — Seven signatures walkthrough

The goal: every attendee leaves with a working mental model of all seven signatures. They will not master them in 30 minutes. They will be able to recognize them when they see them.

Pace: ~4 minutes per signature. Slides optional; better to walk through [`ai-code-smell-checklist.md`](ai-code-smell-checklist.md) on the shared screen.

For each signature:

1. **The name and the one-line definition** (read from the cheatsheet)
2. **Why the model produces it** (30 seconds — the model's incentive, framed simply)
3. **The before/after diff from the checklist** (60 seconds — show on screen)
4. **The catch heuristic** (30 seconds — what the reviewer does to spot it)
5. **Brief Q&A** (60 seconds — if no question, move on)

If you run long on one signature, run shorter on the next. The walkthrough is calibration, not mastery. The exercises are where mastery starts.

#### Signature-specific facilitator notes

| Signature | Watch for in the room |
|---|---|
| S1 (mocked tests) | The "but mocks are normal" objection. Acknowledge — yes, mocks have a place. The problem isn't mocking; it's mocking the function under test. Pivot to the "does this test fail if the implementation is wrong?" question. |
| S2 (deleted edge cases) | Engineers want to see the *new* code. Force the habit: open the *old* code in a side pane. The discipline is comparing branches before reading new logic. |
| S3 (swallowed errors) | Attendees often confuse "handles errors" with "swallows errors." The catch is whether anyone downstream learns about the failure. If no one learns, it's swallowed. |
| S4 (weakened validation) | The "but the test was failing" reframe: when a test fails because validation rejects an input, sometimes the *input is wrong*, not the validation. The signal is whether the PR description articulates *why* the loosening is safe. |
| S5 (removed security checks) | Watch for "but the old endpoint had the check" thinking. The agent built a *new* endpoint; the check is *missing*, not removed. The diff doesn't show a deletion. This is the trickiest of the seven. |
| S6 (unnecessary abstractions) | Engineers trained in heavy-OOP curricula push back. Their reflex is "this is good design." The catch: rule of three. If one concrete case exists today and no dated plan for a second, the abstraction is premature. |
| S7 (diff bloat) | The room nods because everyone agrees in principle. The discipline is enforcing the line-count cap mechanically (Ch 2 §2.4: ~400-600 lines, ~8-10 files). |

### 0:35–1:15 — Live diff exercises

Four exercises, 10 minutes each. Two single-smell, two multi-smell. Each exercise:

1. **2 minutes**: facilitator shows the exercise. Reads the issue and the diff aloud. No interpretation.
2. **5 minutes**: attendees review silently and write down the comments they would leave. Pen and paper, not laptops — attendees who type get distracted; pen-and-paper forces focus.
3. **3 minutes**: facilitator polls the room. "Who spotted [smell X]?" Hands. "Who else spotted something I haven't named?" Hands. Then walks the planted smells aloud, and surfaces any *correct but unplanted* findings as bonus material.

Pick from [`exercises/`](exercises/). Suggested progression:

| Order | Exercise | Why |
|---|---|---|
| 1 | [`exercises/01-mocked-impl.md`](exercises/01-mocked-impl.md) | Pure S1. Builds confidence — most attendees spot at least part of it. |
| 2 | [`exercises/02-deleted-edge-cases.md`](exercises/02-deleted-edge-cases.md) | Pure S2. Drills the "open the original" habit. |
| 3 | [`exercises/03-multi-smell.md`](exercises/03-multi-smell.md) | S4 + S5 + S7. Hard. By this point the room is warmed up and ready. |
| 4 | (instructor's choice) | If the calibration set has a recent real incident's diff, use that. Real beats synthetic every time. |

#### Common derailments and how to handle them

| Derailment | What to say |
|---|---|
| "My agent doesn't do that — Sonnet 4.6 / Opus 4.7 is better than this." | "Per Ch 1 §1.3, agent quality is bounded by harness quality, not model version. The signatures still appear at the latest model — sometimes worse, because the code reads more confidently. The METR 2025 finding (Ch 1 §1.1) — senior engineers in mature repos got 19% slower with AI tooling — is the cautionary tale. Better models don't fix this; trained reviewers do." |
| "We don't have time to review at this depth on every PR." | "Per Ch 22 §22.3, the AI-reviewer subagent is the floor — it catches the mechanical cases. Humans are the ceiling for the structural cases. The 90-minute investment up front saves the incident-postmortem and re-review time. See [`../reviewer-burnout-mitigation/`](../reviewer-burnout-mitigation/) for the operational tooling." |
| "This is just normal bad code; it's not AI-specific." | "True for some signatures — humans write bad mocks too. The AI-specific part is the *volume*: agents produce these patterns *consistently*, not occasionally. The training is for the volume, not the rarity." |
| "Won't the agent get better and make this obsolete?" | "Ch 1 §1.3 — 'models will subsume the harness' is hype, not reality. The harness is where 20+ ranking positions of capability live (LangChain Terminal-Bench). Better models reduce some signatures; they introduce new ones. The pattern library transfers; the specific patterns evolve." |
| Engineer who didn't pre-read tries to participate without the vocabulary | Be kind but firm: "Catch up at break — the cheatsheet is in front of you. The exercises are easier with the vocabulary." Don't slow the room for one person. |
| Senior engineer dominates the room | "I'd love to hear from someone who hasn't spoken yet." Or, more direct: "Let's let [junior name] take this one first." |
| Room is silent and nothing is being spotted | The exercise is too hard for this cohort, or pre-read didn't happen. Pause. Spend 3 minutes walking the planted smells aloud on the first exercise, then start over with the next one. The point of the workshop is reps, not pride. |

### 1:15–1:25 — Debrief

Sit. Switch tone. This part is reflection.

Three questions, in this order:

1. **"What did you spot today that you wouldn't have spotted before this workshop?"** (Round-robin; each attendee answers in one sentence. No skipping.)
2. **"What's still fuzzy? Which signature would you fail to spot in production?"** (Round-robin again. The honest answers go in the post-workshop notes.)
3. **"What's your commitment for the next two weeks?"** (Round-robin. Examples: "I'll catch S1 in my own PRs before I open them"; "I'll print the cheatsheet and tape it to my monitor"; "I'll review one PR per day specifically scanning for S5.")

Capture the answers. The fuzzy-signature data becomes the next quarter's exercise focus. The commitments become the 1:1 follow-up — managers ask in the next 1:1, "you said you'd do X; how's it going?"

### 1:25–1:30 — Evaluation

Per [`evaluation-rubric.md`](evaluation-rubric.md), the workshop has an evaluation component. Either:

- **Same-day calibration**: each attendee reviews one diff from the calibration set independently in the final 5 minutes; facilitator scores afterward.
- **Within-week calibration**: attendees take home a calibration packet; submit comments within 5 business days; facilitator scores against the rubric.

Same-day is faster; within-week catches engineers who do better with thinking time. Run same-day for first-cohort or onboarding; within-week for refresher workshops where attendees have been doing this for a while.

The evaluation is not punitive. It's the data that feeds the L2 certification gate (see Ch 44 §44.2 and [`../agent-autonomy-levels/certification-gates.md`](../agent-autonomy-levels/certification-gates.md)). An engineer who can spot 5 of 7 signatures consistently is at the bar.

## After the workshop

### Within 24 hours

- Score evaluations against [`evaluation-rubric.md`](evaluation-rubric.md)
- Send each attendee a short note: their score, the signatures they spotted, the ones they missed
- Update the team's certification record (see [`../agent-autonomy-levels/certification-gates.md`](../agent-autonomy-levels/certification-gates.md))

### Within 1 week

- Run a refresher 1:1 with anyone scoring below the L2 bar
- If three or more attendees missed the same signature, that's a workshop signal: revisit the walkthrough for that signature next cohort
- Add findings to the [`calibration-set.md`](calibration-set.md) — fuzzy signatures get more exercise coverage

### Quarterly

- Re-run the workshop with a refreshed exercise set. The calibration set rotates; engineers who attended the first workshop see new diffs. Skill stays sharp.
- Per Ch 43 §43.3: "after a year, the engineer either has it or they don't." The quarterly cadence is the year-long calibration.
- Per [`../failed-one-shot-triage/`](../failed-one-shot-triage/), the slop signatures that surface in retros become workshop fuel. Real failures > synthetic ones.

## Common workshop failure modes

### The "demo" failure

Facilitator turns the workshop into a presentation. Talks for 80 minutes. The room nods along. Nobody learns to spot signatures because nobody practiced.

**Mitigation:** the run-of-show above is 30 minutes of walkthrough, 40 minutes of exercises. Stick to it. If you're 50 minutes into walkthrough, you're running it wrong.

### The "expert" failure

Senior engineers in the room treat the workshop as below them. They dominate, derail, or check out.

**Mitigation:** assign them facilitator duty for the next cohort. The act of teaching is its own calibration. If a senior consistently checks out, the cert gate (see Ch 44 §44.2) catches it — an L3-certified engineer who can't articulate the seven signatures is operating beyond their actual skill, and that's a recert conversation.

### The "agreement" failure

Everyone agrees with the seven signatures in the abstract. Nobody can spot one in the exercise. The workshop produces zero behavior change.

**Mitigation:** the exercises are the test, not the walkthrough. If exercise scores are flat, the workshop didn't work. Run more exercises in the next session. Cut walkthrough time if needed.

### The "checklist" failure

Attendees treat the seven signatures as a literal checklist. They run through it linearly on every PR, find nothing because they're pattern-matching instead of reading the code, and approve.

**Mitigation:** the cheatsheet is for cuing pattern-recognition, not for substituting for it. Drill this in the debrief: "the goal isn't to check seven boxes; the goal is to *see* the patterns when they're there. The seven names are the vocabulary." Per [`reviewer-cheatsheet.md`](reviewer-cheatsheet.md), the final question — "if this ships and breaks production at 3am, which line is the broken one?" — is the test of whether you actually read the code.

### The "AI will catch it" failure

The room concludes "we should rely on the AI reviewer." That's the opposite of the message.

**Mitigation:** Ch 22 §22.3 — "AI reviewers are a floor. Humans are the ceiling. Never let an AI-only review approve a merge to main." The AI reviewer catches the mechanical cases; humans catch the structural cases. The workshop is *human* training.

## Facilitator's own preparation

Before facilitating for the first time:

1. Read [`ai-code-smell-checklist.md`](ai-code-smell-checklist.md) cover to cover. Twice if it's been a while.
2. Run yourself through [`exercises/01-mocked-impl.md`](exercises/01-mocked-impl.md) cold. If you don't spot all the planted smells, you're not ready to facilitate.
3. Co-facilitate at least once with someone who has. Co-facilitation is not optional for the first round.
4. Run a postmortem on your own first session within 48 hours. What worked? What didn't? Update this guide; it's a living document.

## Variants

| Variant | When to use |
|---|---|
| 30-minute refresher | Quarterly, for engineers who've already done the 90-minute. Two exercises, no walkthrough, debrief only. |
| 2-hour deep dive | For platform/DevEx teams building the team's review infrastructure. Adds time on the harness pieces — hooks, [`review-prompts/`](review-prompts/), the AI-reviewer subagent. |
| Async (self-paced) | For distributed teams. Attendees work through the checklist + exercises individually; facilitator schedules a 30-minute 1:1 to debrief per attendee. Slower but works. Doesn't replace the in-person version for first-cohort onboarding. |
| New-hire bundle | Day 4 of the [`../agent-autonomy-levels/`](../agent-autonomy-levels/) onboarding week (Ch 44 §44.1). Run the workshop with the new hire and their manager. The manager's presence is part of the L1 certification path. |

## Companion artifacts

- [`ai-code-smell-checklist.md`](ai-code-smell-checklist.md) — the deep reference for the walkthrough
- [`reviewer-cheatsheet.md`](reviewer-cheatsheet.md) — printable, one per attendee
- [`exercises/`](exercises/) — the diff exercises
- [`evaluation-rubric.md`](evaluation-rubric.md) — how the workshop is evaluated
- [`calibration-set.md`](calibration-set.md) — methodology for the calibration diffs
- [`review-prompts/`](review-prompts/) — for the AI-reviewer demo
- [`../agent-autonomy-levels/certification-gates.md`](../agent-autonomy-levels/certification-gates.md) — what the workshop output feeds
- [`../reviewer-burnout-mitigation/`](../reviewer-burnout-mitigation/) — adjacent (the operational counter)
- Ch 2 §2.4, Ch 22, Ch 43 §43.3, Ch 44 §44.1–§44.2 — sources
