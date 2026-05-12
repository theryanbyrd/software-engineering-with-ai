# Exercises — Diffs to Spot the Signatures In

The exercises drill the seven signatures from Ch 2 §2.2 against synthetic-but-realistic diffs. Each exercise plants one or more smells; the trainee reviews the diff and writes the comments they would leave on the PR.

The exercises are for **practice**, not for evaluation. The evaluation set is the calibration set per [`../calibration-set.md`](../calibration-set.md). The two should not overlap — a trainee who's seen an exercise is no longer being evaluated cold on it.

Per Ch 22 §22.4:

> A junior reviewer who can spot the seven AI-slop signatures is more valuable than a senior who rubber-stamps.

Spotting is a built skill, not an innate one. The exercises are the reps.

## How to use these

### Solo

1. Pick an exercise. Read the scenario.
2. Read the diff. Write down the review comments you would leave. Pen and paper, no shortcuts.
3. Read the instructor key. Compare your comments to the planted smells.
4. Score yourself loosely against the [`../evaluation-rubric.md`](../evaluation-rubric.md). Don't game it; honest self-assessment matters more than the number.

Solo practice is fine for maintenance. It is not a substitute for the workshop and the pair-review reps.

### In the workshop

Per [`../facilitator-guide.md`](../facilitator-guide.md), the facilitator picks 3-4 exercises to run live, with the workshop pacing (2 min present, 5 min review, 3 min debrief). The exercises here are calibrated to that pacing.

### In pair review

Trainee and senior reviewer pick an exercise. Trainee reviews first; senior reads the same diff and adds anything missed. The senior's reads are the calibration — and the senior often learns something too.

## Exercise catalog

| # | File | Smells planted | Difficulty |
|---|---|---|---|
| 01 | [`01-mocked-impl.md`](01-mocked-impl.md) | S1 (primary) | Easy. Single-smell. Good for first-cohort. |
| 02 | [`02-deleted-edge-cases.md`](02-deleted-edge-cases.md) | S2 (primary), S3 (secondary) | Medium. Drills the "open the original" habit. |
| 03 | [`03-multi-smell.md`](03-multi-smell.md) | S4, S5, S7 (all planted) | Hard. Multi-smell. For trainees past the first walkthrough. |
| 04 | (slot reserved) | (TBD) | (TBD) |
| 05 | (slot reserved) | (TBD) | (TBD) |

Exercises are added in batches as field-tested versions land. See [`../calibration-set.md`](../calibration-set.md) for how the team's own incident corpus becomes the next batch.

## Exercise format

Each exercise file has four sections:

1. **Scenario** — the issue/ticket the PR claims to address. Read this first.
2. **The diff** — synthetic but realistic. Patch format or before/after blocks.
3. **Trainee task** — what to do with the diff. Always: "review this diff; write the comments you would leave."
4. **Instructor key** — the planted smells with the reference comments. Don't read this until you've written your own comments.

The "instructor key" name is intentional. The exercises are facilitator-led; the trainee reviews without the key. If you're working solo, cover the key with your hand until you've written your comments.

## What the exercises won't teach

- **Real-codebase context.** The exercises are stripped of the surrounding files, the team's CLAUDE.md, the project's architecture. Real PRs have context the exercises don't. The signatures are spottable from the diff alone; the rest of review benefits from context.
- **Disagreement handling.** Real PRs include back-and-forth with the author. The exercises don't simulate that. For that, pair-review on real PRs.
- **Time pressure.** Real PRs come in batches; reviewer attention is finite. The exercises let you take as long as you want. For time-pressure practice, the workshop's 5-minute review window is the closest analog.

## Difficulty progression

For a new trainee:

1. Start with 01 (single smell, easy). Build confidence.
2. Move to 02 (single primary, secondary smell). Drill the "open the original" habit.
3. Attempt 03 (multi-smell). Expect to miss something. The miss is the data.
4. Run the next exercises in the batch (when published) at this trajectory.

For an experienced reviewer at recert:

Jump straight to multi-smell. The single-smell exercises are calibration for trainees who don't yet have the vocabulary; experienced reviewers have it and need the harder reps.

## Common workshop misuses

### Treating the exercise as a test

Trainee feels bad about missing a smell. Facilitator reinforces the failure narrative.

The exercises are not a test. The calibration set is the test. The exercises are the practice. Per [`../facilitator-guide.md`](../facilitator-guide.md), the workshop's debrief explicitly names this: "if you missed something, that's the workshop working."

### Reading the key before reviewing

Trainee glances at the key "to see what to look for." Now they can't unsee it. The exercise is burned.

**Discipline:** write your comments first. Even if you only spot one smell, write that one down. Then read the key. The act of generating comments is what builds the skill; reading the key without generating is reading, not practicing.

### Over-explaining the smell

Trainee writes a 200-word comment for a single S3. Per the articulation guide in [`../evaluation-rubric.md`](../evaluation-rubric.md), the bar is "specific and actionable," not "comprehensive." Real review comments are tight.

### Memorizing the exercises

A trainee runs the exercises five times "to get good at them." On exercise 5, they spot every smell. They're now good at *these exercises*, not at review.

**Mitigation:** practice on real PRs in pair-review. The exercises are a starting point; they are not the destination.

## What's outside the seven

Some exercises include code that isn't slop but might trick a less-experienced reviewer into flagging. These are intentional — the precision dimension in [`../evaluation-rubric.md`](../evaluation-rubric.md) tests whether the trainee distinguishes "smell" from "code I don't love."

When the instructor key says "trainee may have flagged X — that's not actually a smell," the trainee gets a small precision penalty if they flagged it. Real review tolerates style preferences; the seven signatures are about correctness, not aesthetics.

## Companion artifacts

- [`../ai-code-smell-checklist.md`](../ai-code-smell-checklist.md) — the deep reference for each signature
- [`../reviewer-cheatsheet.md`](../reviewer-cheatsheet.md) — the single-page summary
- [`../facilitator-guide.md`](../facilitator-guide.md) — how to use these in the workshop
- [`../evaluation-rubric.md`](../evaluation-rubric.md) — how scoring works
- [`../calibration-set.md`](../calibration-set.md) — distinct from these (evaluation, not practice)
- Ch 22 §22.2, Ch 43 §43.3 — sources
