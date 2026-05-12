# Calibration Set — Methodology

A calibration set is the small, curated collection of pre-scored diffs that defines what "spotting the seven signatures" actually means at your organization. Without one, the workshop produces reviewers who agree with the seven signatures in the abstract but disagree on what the signatures look like in practice.

This file is the framework — how to build, score, rotate, and use a calibration set. The actual diffs are not shipped in this repo, and they should not be: every organization's slop has its own accent, drawn from its own codebase, languages, and prior incidents. A calibration set borrowed from another team is a calibration set that calibrates to that team, not yours.

Per Ch 22 §22.4:

> A junior reviewer who can spot the seven AI-slop signatures is more valuable than a senior who rubber-stamps.

The calibration set is the artifact that makes "spot the signatures" measurable, not aspirational.

## What a calibration set is

A calibration set is **20 real-world diffs**, scored independently by the most senior reviewer on the team (or, ideally, by two seniors who norm against each other). For each diff, the senior records:

- The actual change being made (the issue, the PR description)
- Which of the seven signatures (S1-S7) are present, and at what severity
- Which "smells" are absent but the diff might trick a less-experienced reviewer into flagging
- The reference set of review comments — what the experienced reviewer would have written

The 20 diffs are split:

| Subset | Diffs | Use |
|---|---|---|
| Workshop training | 5 | Used during the 90-minute workshop. Trainees see these alongside the walkthrough. |
| L2 certification | 5 | Used to evaluate L2 readiness. Rotated quarterly. |
| Pair-review practice | 5 | Used for 1:1 pair-reviewing between trainee and senior, between workshops. |
| Recertification | 5 | Used for annual recert (Ch 44 §44.2). Held back; trainees should not see these during onboarding. |

Twenty is the working minimum. A larger set is better; a smaller set risks calibration trainees who memorize the answers.

## What makes a good calibration diff

### Good: real diffs from real PRs

Synthetic diffs are useful for the workshop walkthrough (the worked examples in [`ai-code-smell-checklist.md`](ai-code-smell-checklist.md)). They are not enough for calibration. Real diffs have the texture of real engineering — the imperfect commit messages, the off-by-one in line numbers, the comment that's almost relevant but not quite, the test that's mostly behavior-asserting but has one mock that shouldn't be there. Trainees who only ever see synthetic diffs spot synthetic-shaped smells.

Source for real diffs:

- **Incident postmortems.** Per [`../incident-postmortem-templates/`](../incident-postmortem-templates/), every AI-related incident produces a categorized diff with a known signature. These are gold. Use them.
- **Caught-in-review PRs.** PRs where a senior reviewer caught a smell before merge. The author's draft is the calibration material; the reviewer's comment is the reference.
- **Near-misses.** PRs that merged with the smell, surfaced in production, but didn't escalate to a postmortem. The "we got lucky" PRs are excellent calibration.

### Good: span all seven signatures

The 20-diff set should have at least two diffs primarily exhibiting each of S1-S7. Many diffs will exhibit multiple signatures. The distribution should reflect the team's actual incident corpus — if your team's postmortems show S5 (removed security checks) in 40% of incidents, your calibration set should overweight S5.

### Good: include "clean" diffs

3-5 of the 20 should be PRs with no slop signatures present. A reviewer who flags smells in clean diffs has high recall and low precision — the false-positive end of the spectrum. The calibration set must distinguish "spots the smells" from "is suspicious of everything."

### Good: vary by language, by domain, by author

A calibration set that's 100% Python backend PRs trains reviewers to spot Python backend smells. If the team also reviews TypeScript frontend, infrastructure-as-code, or SQL migrations, those should be represented. Per Ch 22 §22.2, the signatures are language-agnostic; the calibration material should reflect that.

### Good: redacted but realistic

Real diffs from production code have proprietary content. Redact carefully — variable names matter for the realism, but customer-specific identifiers and trade-secret algorithms don't. Replace specific business logic with semantically equivalent placeholders.

### Bad: synthetic-perfect

A diff where every line is suspicious and every smell is screaming. Real PRs are mostly fine, with the smell hidden in 3-5 lines. The calibration material should match.

### Bad: trick diffs

A diff that looks like S1 but isn't actually a mock-implementation pattern (it's a behavior assertion that happens to use a Mock). Or a diff that looks like S6 but is actually a justified abstraction. These exist; they're useful exactly once, to test whether the trainee distinguishes pattern from substance. Use sparingly. A calibration set full of trick diffs trains trainees to second-guess themselves into not flagging real smells.

### Bad: outdated

A diff that exhibits a smell pattern from an older model version that current models no longer produce. The seven signatures are durable; the specific way they manifest evolves. Refresh the calibration set when model behavior changes meaningfully (typically annually, or after a major model release).

## How diffs are selected

The selector is a senior reviewer who has caught slop incidents personally and who has read [`ai-code-smell-checklist.md`](ai-code-smell-checklist.md) cover to cover. The selector's process:

1. **Source the candidate pool.** Pull 50-100 candidate PRs from the last 6 months: AI-authored PRs (tagged `[AI-authored]` per Ch 2 §2.4), incident-linked PRs, and senior-caught-in-review PRs.
2. **First-pass score.** For each candidate, identify which signatures are present, at what severity (1-3 scale: subtle, clear, blatant). Discard PRs where no signature scores ≥ 2 unless the PR is a "clean" reference diff.
3. **Compose the set.** Aim for the distribution above: 20 diffs, signatures spread, languages/domains spread, 3-5 clean.
4. **Norm with a second senior.** A different senior scores the same 20 diffs independently. If the two scorers disagree on which signatures are present in > 4 diffs, the set is too ambiguous — refine or replace those diffs.
5. **Score the reference comments.** For each diff, write the comments an experienced reviewer would leave. These are the rubric anchors — what a 4-score articulation looks like for that specific diff.
6. **Publish to the calibration repo.** The set lives in a separate, access-restricted location. Trainees should not have read access; scorers and facilitators do.

## How to score against the calibration set

Per [`evaluation-rubric.md`](evaluation-rubric.md), the rubric is the scoring grid. The calibration set is the substrate.

Operationally:

1. Trainee receives the 5 calibration diffs for their cohort
2. Trainee submits review comments — same format they'd use on a real PR (inline comments, summary comment)
3. Scorer compares the trainee's comments to the reference comments
4. Scorer applies the 0-4 rubric per signature present in each diff
5. Scorer aggregates: total score across all 5 diffs, recall %, precision %, articulation distribution
6. Scorer writes a 3-5 sentence narrative for the trainee — what they did well, what they missed, where to focus next

Time budget: 30-60 minutes per trainee scoring. If it takes longer, the rubric isn't sharp enough or the calibration set is too ambiguous.

## How the set is rotated

### Quarterly rotation

The L2 certification subset of 5 diffs rotates every quarter. Trainees in adjacent cohorts will talk. The L2 calibration diffs for Q1 should not be the L2 calibration diffs for Q2.

The rotation is operationally a swap, not a full rebuild. Each quarter:

- Retire 2-3 of the previous quarter's L2 diffs to the "pair-review practice" subset
- Promote 2-3 from the "pair-review practice" subset to L2 calibration
- Add 2-3 new candidate diffs from the last quarter's PRs to the pair-review practice pool

The "recertification" subset rotates more slowly — once per year — because trainees only see those once per year by definition. The "workshop training" subset can be more stable, because those diffs are used as walkthroughs, not as evaluations.

### When to rebuild

The full set is rebuilt when:

- A new model version produces smells that the existing set doesn't represent
- An incident surfaces a signature manifestation that wasn't in the set
- The team's tech stack shifts significantly (e.g., a new primary language)
- The scoring data shows trainees consistently saturating the set (90%+ scores across cohorts — the set has become memorized or is too easy)

Per [`../evals-and-benchmarks-runbook/quarterly-model-lineup-review.md`](../evals-and-benchmarks-runbook/quarterly-model-lineup-review.md), quarterly model lineup review is the natural trigger for calibration-set review.

## Tie-in: the quality decay signals (Ch 31 §31.3)

Per Ch 31 §31.3, the Slop Detector heuristics that catch AI-driven quality decay early:

> Duplicated code block growth (GitClear-style, or via SonarQube/CodeClimate). Refactor ratio decline. Two-week churn rate above 7–8%. Test-to-code ratio declining. PR size distribution. Faros AI's data shows AI-using teams produce PRs that are 51–154% larger on average. Time-in-PR-review. Faros AI's 2026 dataset showed median time in PR review up 441%.

These are team-level metrics. The calibration set is the individual-reviewer-level metric. Both matter; they answer different questions:

| Question | Where to look |
|---|---|
| Are our reviewers catching slop on PRs? | Calibration scores, postmortem rate per AI-authored PR |
| Is the team's code base decaying? | Ch 31 §31.3 quality decay signals |
| Are individual engineers operating at their certified level? | Per-engineer slop incidents at their cert level |
| Has the calibration set itself decayed? | Cohort-aggregate scores trending up over time without workshop changes |

The calibration set is meaningful when its scoring data correlates with real outcomes. If trainees score 80% on calibration but the team's S5 incidents don't decline, the set isn't measuring the right thing — or it's measuring it but the team isn't acting on the results. Either way, the calibration set needs adjustment, and so does the team's response loop.

## Using the set for onboarding

A new engineer joining the team:

1. **Day 1-4** of the Ch 44 §44.1 onboarding week. Standard.
2. **Day 5** — runs through the workshop training subset (5 diffs) with their manager or onboarding buddy. Discusses each diff after they've written comments. Goal: pattern-recognition, not evaluation.
3. **30-60 days post-onboarding** — takes the L2 calibration set. Goal: evaluation. Output: pass/fail/close-call per [`evaluation-rubric.md`](evaluation-rubric.md).
4. **Quarterly** — informal pair-review with a senior using the practice subset. Goal: maintenance.
5. **Annually** — recertification using the recert subset. Goal: drift check.

A new engineer who can't pass the L2 calibration in 60-90 days is not failing onboarding. The book's framing (Ch 43 §43.3): "after a year, the engineer either has it or they don't." 60-90 days is the early indicator, not the final word.

## Using the set for ongoing recalibration

Engineers drift. Per Ch 44 §44.2:

> Certifications expire. Review yearly. The drift is real, and it is asymmetric: people drift up, never down, unless you actively re-certify.

The recertification subset is the operational discipline. Once a year, every L2+ engineer runs through 5 fresh diffs. Their score determines:

- Cert renewed (≥ 75%, no diff under 60%): standard renewal
- Cert renewed with note (60-74%): renewed, but the manager flags the missed signatures for focused practice
- Cert reset (< 60%): per [`../agent-autonomy-levels/certification-gates.md`](../agent-autonomy-levels/certification-gates.md), cert resets are not punitive; they're discipline. The engineer re-takes the workshop; re-earns the cert in 30-60 days.

For engineers involved in slop incidents at their certified level, recertification is triggered immediately, not at the annual cadence.

## Anti-patterns

### Trainees with read access to the calibration set

If the calibration set is in the team wiki, anyone on the team can read the answers. Trainees who study the answers in advance score artificially high.

**Mitigation:** the calibration set lives in a restricted location. Workshop facilitators have read access. Scorers have read access. Trainees do not, until the moment of evaluation.

### Calibration set never rotates

The first quarter's calibration set persists for two years. Trainees in cohort 8 see the same diffs cohort 1 saw. The signal degrades to noise.

**Mitigation:** quarterly rotation, scheduled and owned. Per [`../agent-autonomy-levels/autonomy-drift-monitoring.md`](../agent-autonomy-levels/autonomy-drift-monitoring.md), the rotation discipline is part of the team's harness maintenance.

### Calibration set built from one person's intuition

A single senior's intuition becomes the team's standard. If the senior's intuition skews — they overweight S5, they underweight S6 — the whole team's calibration skews with them.

**Mitigation:** the dual-scorer norming process during construction. A second senior independently scores the candidate diffs; disagreements force the set to be sharpened or the disagreed-on diffs to be discarded.

### Calibration scores not acted on

Trainees score, get a number, and nothing changes. The score becomes a checkbox; the workshop becomes a ritual.

**Mitigation:** per [`../failed-one-shot-triage/closing-the-loop.md`](../failed-one-shot-triage/closing-the-loop.md), the loop closes with action. Scores below the L2 bar trigger pair-reviewing; cohort-wide misses trigger workshop revision; team-wide drift triggers calibration-set rebuild.

### Calibration set is itself slop

A junior facilitator builds the calibration set without senior calibration. The set is plausible but doesn't actually test the seven signatures. Trainees who score high on this set still ship slop.

**Mitigation:** the construction process above is non-optional. Two seniors, real diffs, norming, reference comments. If you can't afford the time to build it right, you can't afford to rely on the scores it produces.

## Starting from zero — first calibration set

A team that doesn't have a calibration set yet, building from scratch:

1. **Week 1:** the senior facilitator pulls 50-100 candidate PRs from the last 6 months. Tags them with present-signatures.
2. **Week 2:** facilitator narrows to 20 diffs across the four subsets. Writes reference comments.
3. **Week 3:** second senior reviews and norms. Sharpen the set.
4. **Week 4:** dry-run the workshop training subset on a willing senior who hasn't seen the set. Verify the diffs work as walkthroughs. Adjust.
5. **Month 2:** run the first cohort with the set. Score. Refine based on first-cohort results.

The first quarter's calibration set is the v1. By v3 (quarter 3), the set is mature. The team's first-cohort scores will be lower than the team's third-cohort scores, but not because the trainees are better — because the set is sharper. Track that.

## Companion artifacts

- [`ai-code-smell-checklist.md`](ai-code-smell-checklist.md) — the signatures the set is built around
- [`evaluation-rubric.md`](evaluation-rubric.md) — how the set is scored against
- [`facilitator-guide.md`](facilitator-guide.md) — how the set is used in the workshop
- [`../incident-postmortem-templates/`](../incident-postmortem-templates/) — source material for real diffs
- [`../agent-autonomy-levels/certification-gates.md`](../agent-autonomy-levels/certification-gates.md) — the cert gate this set feeds
- [`../failed-one-shot-triage/closing-the-loop.md`](../failed-one-shot-triage/closing-the-loop.md) — the action loop the scores trigger
- [`../evals-and-benchmarks-runbook/`](../evals-and-benchmarks-runbook/) — adjacent (eval discipline for AI-reviewer subagents)
- Ch 22 §22.2, Ch 31 §31.3, Ch 44 §44.2 — sources
