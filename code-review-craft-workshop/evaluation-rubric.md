# Evaluation Rubric — Scoring a Reviewer Trainee

How to score a trainee on a calibration diff. Tied to the L2 certification gate per Ch 44 §44.2 (see [`../agent-autonomy-levels/certification-gates.md`](../agent-autonomy-levels/certification-gates.md)):

> Demonstrated ability to recognize the seven slop signatures (per Ch 22 §22.2) in code review.

The rubric is the operationalization of "demonstrated ability." Without it, "you can spot the seven signatures" is a vibe. With it, it's a documented score against a known calibration set.

## What the rubric scores

For each calibration diff, the trainee submits review comments. The rubric scores along four dimensions:

| Dimension | What it measures |
|---|---|
| **Recall** | Of the smells planted in the diff, how many did the trainee spot? |
| **Precision** | Of the smells the trainee flagged, how many were real? |
| **Articulation** | How specific and actionable were the comments? Vague vs. surgical. |
| **Calibration** | Did the trainee correctly identify which signature was present, or did they pattern-match incorrectly? |

A trainee can have high recall and low precision (sees smells everywhere; cries wolf). A trainee can have high precision and low recall (only flags the obvious cases; misses the subtle ones). The bar requires both.

## The scoring grid

Each diff is scored on a 0-4 scale per signature actually present.

| Score | Meaning |
|---|---|
| **4** | Identified the signature by name, articulated the specific concern, proposed a fix or asked the right diagnostic question |
| **3** | Identified the signature, articulated the concern accurately, didn't propose a fix |
| **2** | Identified that something was wrong in the right area, but didn't name the signature or articulate why |
| **1** | Vague concern that gestures at the right area ("this looks suspicious"; "are you sure?") |
| **0** | Missed entirely |

False positives are scored separately:

| FP score | Meaning |
|---|---|
| **0** | No false positives — every flagged item was a real concern |
| **−1** | One false positive that's at least plausible (e.g., flagged a real but tolerable abstraction as S6) |
| **−2** | One false positive that misreads the code (e.g., flagged a behavior-asserting test as S1) |
| **−3** | Multiple false positives, or one that would have created friction for the author |

## Comment quality — what's "specific vs. vague"

The articulation dimension is the one that distinguishes "spotted a smell" from "would actually catch it in real review." Examples:

| Vague (1-2 articulation) | Specific (3-4 articulation) |
|---|---|
| "This test looks weak." | "S1: this test mocks `payment_service._stripe_client` and asserts on the mock call. If the implementation were `pass`, this test would still pass. Suggest building a real customer fixture and asserting on `result.status` and a side effect on the ledger." |
| "Did you handle errors?" | "S3: line 47, `except Exception: pass` discards the original exception. When `fetchProfile` fails (network timeout, 500, permission denied), the function returns `nil` and the caller can't distinguish 'not found' from 'fetch failed.' Wrap with context and propagate." |
| "This regex looks too loose." | "S4: the regex was `^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$` and is now `^.+@.+$`. The new pattern accepts `\"@@@\"`, `\" @ \"`, and arbitrary whitespace-around-@. What incident or input motivated the loosening?" |
| "I don't love this abstraction." | "S6: `PaymentProcessorFactory` produces one concrete type (`StripePaymentProcessor`). Rule of three: introduce the abstraction at the third concrete case. Until then, inline the call." |
| "This PR is big." | "S7: issue scope is 'add `marketing_opt_in` field.' Diff includes that (25 lines), plus a rename of `full_name → display_name` (80 lines across 6 files), plus a reformat of `helpers/user_utils.py` (200 lines). Split the rename into its own PR; reject the reformat." |

The specific comments are what review actually looks like. The vague comments are what rubber-stamping looks like dressed up as engagement.

## Worked example — scoring a single diff

The diff is the worked example from [`exercises/03-multi-smell.md`](exercises/03-multi-smell.md): a refund handler refactor that plants S1, S4, S5, and S7.

Trainee submitted three comments:

1. "This PR is pretty large; was the rename necessary?"
2. "I notice you removed the `@require_auth` decorator on `refund_v2`. Was that intentional?"
3. "The test on line 142 mocks `stripe.refunds.create` and asserts the mock was called. Does this actually verify the refund happened?"

Scoring:

| Smell present | Score | Reasoning |
|---|---|---|
| S1 (mocked tests on `test_refund_creates_correctly`) | 4 | Identified by behavior, articulated the diagnostic question ("does this verify the refund happened?") |
| S4 (validation widened — `amount > 0` was `0 < amount <= 10000`) | 0 | Not spotted |
| S5 (`@require_auth` removed on the new endpoint) | 3 | Identified, articulated, didn't propose a fix |
| S7 (PR is 350 lines including unrelated rename) | 2 | Right area ("this PR is pretty large") but didn't name S7, didn't articulate the rename should be split |

False positives: 0 (all three comments were real concerns)

**Raw score**: 4 + 0 + 3 + 2 = 9 out of a possible 16
**FP adjustment**: 0
**Final**: 9 / 16 = 56%

This trainee spotted half the planted smells with mostly-good articulation. The miss on S4 is the diagnostic — they didn't open the original validation to compare. The S7 articulation could be sharper. They're not yet at the L2 bar but are within 1-2 workshops of it.

## Pass / fail thresholds

| Threshold | Score on calibration set | Implication |
|---|---|---|
| **L2 ready** | ≥ 75% on the 5-diff calibration set, with no diff under 60% | Bar for the Ch 44 §44.2 L2 certification. Senior signs off. |
| **L2 close** | 60-74% overall, or ≥ 75% with one diff under 60% | Re-run the workshop; target the missed signatures. Re-test in 4-6 weeks. |
| **Needs work** | < 60% overall | Pair with a senior reviewer for 4-6 weeks. Not blocked from L1 work; not eligible for L2. |
| **Calibration outlier** | > 95% on first attempt | Verify the trainee didn't see the calibration set in advance. If clean, consider them a candidate for workshop facilitator. |

**Calibration set composition.** Per [`calibration-set.md`](calibration-set.md), the 5-diff scoring set is rotated quarterly. Don't reuse the same diffs across cohorts; trainees in adjacent cohorts will talk.

## What the rubric is NOT for

### Not for performance review

Per Ch 31 §31.1, the book is explicit that AI-related metrics are not for individual performance evaluation:

> Track median (not mean) tokens per active developer per week, broken down by Opus/Sonnet/Haiku. Use this as a leading indicator of adoption and a cost-control input — never as a performance-evaluation metric.

The rubric is for the certification gate, not for the promotion conversation. A reviewer at 56% is not "underperforming"; they are pre-L2. The path to L2 is the workshop, the pair-reviewing, the reps — not the negative annual review.

### Not for hiring

The rubric is calibrated against engineers who have already onboarded. Using it to evaluate candidates produces noise — interview conditions are not review conditions, the candidate hasn't been pre-read on [`ai-code-smell-checklist.md`](ai-code-smell-checklist.md), the calibration set may not match the candidate's tech stack. For hiring, use the [`../people/`](../people/) interview rubrics.

### Not for AI-reviewer subagents

The calibration set and rubric are for *human* trainees. The AI-reviewer subagent uses the same vocabulary (see [`review-prompts/general-review.md`](review-prompts/general-review.md)) but its evaluation lives in [`../evals-and-benchmarks-runbook/`](../evals-and-benchmarks-runbook/) — the eval harness for prompt quality.

## Common scoring failure modes

### Grade inflation

Scorer wants the trainee to pass. Articulation scores creep up: a vague comment gets a 3 because "they were close." Over time, the L2 cert becomes meaningless.

**Mitigation:** the scorer is not the trainee's direct manager. Per [`../agent-autonomy-levels/certification-gates.md`](../agent-autonomy-levels/certification-gates.md), a senior who is not the manager signs off on L2. The scorer's incentive is preserving the bar, not protecting the trainee.

### Grade deflation

Scorer is a perfectionist senior who applies "I would have written this comment better." The trainee scores 40% and gets demoralized.

**Mitigation:** the scoring grid is the grid. A 3 means "identified and articulated"; it doesn't require the comment to read like a staff engineer's. If the comment names the signature, names the line, and articulates the concern, it's a 3. Calibration sessions between scorers (norming the grid against shared examples) are the fix.

### Trainee gaming the rubric

Trainee learns the planted smells in advance (from a teammate who took the workshop last cohort).

**Mitigation:** rotate the calibration set quarterly. Per [`calibration-set.md`](calibration-set.md), the rotation is operationally necessary. Don't let the same five diffs persist for two consecutive cohorts.

### Vague articulation slipping past

Trainee writes a lot of comments but none of them are surgical. They pattern-match "more comments = better reviewer." Articulation scoring should catch this; sometimes it doesn't.

**Mitigation:** the worked example above is the calibration. If a trainee's comments don't read like the "specific" column of the comparison table, they're 1-2 in articulation regardless of count. Quantity of comments is not the signal.

## How the rubric data is used

After scoring:

1. **Trainee gets the score**, the signatures they spotted, the ones they missed. Within 24 hours.
2. **The trainee's manager** gets a summary (score, pass/fail/close-call). Within 24 hours.
3. **The team's certification record** is updated if the trainee passed. Per [`../agent-autonomy-levels/certification-gates.md`](../agent-autonomy-levels/certification-gates.md), this is the operational state.
4. **The aggregate data** (across the cohort) goes back to the workshop facilitator. If 3+ trainees missed S4 in this cohort, S4 gets more time in the next workshop.

Per Ch 31 §31.5 and [`../failed-one-shot-triage/closing-the-loop.md`](../failed-one-shot-triage/closing-the-loop.md), the loop closes when the data informs the next cycle. A rubric that produces scores but doesn't change the workshop is decorative.

## Recertification (annual)

Per Ch 44 §44.2:

> Certifications expire. Review yearly. The drift is real, and it is asymmetric: people drift up, never down, unless you actively re-certify.

The annual recert uses the same rubric, with a fresh calibration set. An engineer who's been L2-certified for a year takes the recert; if they're still at ≥ 75%, the cert renews. If they're at 60-74%, the cert is reviewed (have they actually been doing L2 work? Has model evolution introduced signatures they haven't seen?). If they're below 60%, the cert is reset and they go through the workshop again.

Per [`../agent-autonomy-levels/certification-gates.md`](../agent-autonomy-levels/certification-gates.md):

> The annual review doesn't happen. Engineers retain L3 cert from 18 months ago; their actual operation has shifted; the cert is stale. Mitigation: annual review is on the calendar; tied to a specific person's responsibility (typically the engineering manager).

Calendar this. Don't let it slip.

## Companion artifacts

- [`ai-code-smell-checklist.md`](ai-code-smell-checklist.md) — the seven signatures the rubric scores against
- [`reviewer-cheatsheet.md`](reviewer-cheatsheet.md) — the one-pager trainees use
- [`exercises/`](exercises/) — the diffs trainees practice on (not the same as calibration)
- [`calibration-set.md`](calibration-set.md) — methodology for the calibration set
- [`facilitator-guide.md`](facilitator-guide.md) — workshop that produces calibration data
- [`../agent-autonomy-levels/certification-gates.md`](../agent-autonomy-levels/certification-gates.md) — the L2 gate this rubric feeds
- Ch 22 §22.2, Ch 31 §31.1, Ch 44 §44.2 — sources
