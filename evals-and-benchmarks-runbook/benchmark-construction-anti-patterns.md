# Benchmark Construction Anti-Patterns

Common failure modes when teams build internal evals. Each anti-pattern has a mitigation; many have similar surface symptoms (the benchmark seems healthy but the data isn't actionable).

## Anti-pattern 1 — The benchmark uses public data

The team's "internal benchmark" is a curated set of HumanEval / SWE-bench / Aider Polyglot tasks.

**Why it's wrong:** these tasks are in training data for current models. Performance is inflated. Public benchmarks measure general capability, not the team's specific work.

**Mitigation:** internal benchmark uses tasks from the team's own backlog and history. Public benchmarks can be a sanity check, not the basis.

## Anti-pattern 2 — The benchmark is too small

The team uses 10-15 tasks. Run-to-run variance is high; results don't reproduce.

**Why it's wrong:** at small N, statistical noise dominates. A model that scores 70% on 10 tasks and 75% on 10 tasks aren't significantly different.

**Mitigation:** 30-100 tasks per [`internal-benchmark-construction.md`](internal-benchmark-construction.md). 50-60 is the sweet spot.

## Anti-pattern 3 — The benchmark is too easy

Every candidate model passes every task. No signal between models.

**Why it's wrong:** if every model scores 95%+, the benchmark isn't differentiating. The team can't tell which model is actually better for their work.

**Mitigation:** include T3 (architecting) tasks deliberately. The benchmark should have failures; that's where the signal lives.

## Anti-pattern 4 — The benchmark is all T2

The team only includes "fair" tasks — well-specified, bounded, mid-complexity. T1 (trivial) and T3 (hard) tasks are excluded.

**Why it's wrong:** the benchmark doesn't reflect the team's actual work distribution. It tests one slice of capability.

**Mitigation:** include all three tiers per the distribution in [`internal-benchmark-construction.md`](internal-benchmark-construction.md).

## Anti-pattern 5 — Tasks succeed only with team-specific knowledge

Tasks reference internal jargon, undocumented patterns, tribal knowledge. Models that don't know the team's specific context fail; models with more general knowledge appear to fail equivalently.

**Why it's wrong:** the benchmark is testing whether the model has team-specific context, not whether the model can do the work given the same context all engineers have.

**Mitigation:** task includes the same context an engineer would have (CLAUDE.md, AGENTS.md, relevant skills, fixtures). The benchmark tests the model + harness, not the model alone.

## Anti-pattern 6 — Inconsistent scoring

Two reviewers grade the same task differently. Pass/Partial/Fail decisions vary.

**Why it's wrong:** the benchmark's results aren't reproducible. Comparing models becomes comparing reviewers.

**Mitigation:** explicit rubric for what counts as Pass/Partial/Fail. Two reviewers grade the same set; check inter-reviewer agreement; if agreement is below ~80%, refine the rubric.

## Anti-pattern 7 — One reviewer for all tasks

A single platform engineer grades the whole benchmark. Their biases (favoring specific code styles, weighting certain failure modes) become the benchmark's biases.

**Why it's wrong:** the benchmark reflects one person's judgment, not the team's.

**Mitigation:** rotate reviewers across tasks. For high-stakes decisions (primary model switch), have at least 2 reviewers grade independently.

## Anti-pattern 8 — Tasks aren't refreshed

The benchmark has the same 50 tasks for 18 months. Models trained on data from before the benchmark's creation may have effectively memorized the tasks.

**Why it's wrong:** scores climb over time not because models improved on this work but because models trained on this work.

**Mitigation:** retire 5-10 tasks per quarter; replace with new ones. Per [`internal-benchmark-construction.md`](internal-benchmark-construction.md).

## Anti-pattern 9 — The benchmark is run only at quarterly review

Between reviews, no benchmark runs. The team has no signal on month-to-month drift.

**Why it's wrong:** model behavior changes between releases. Vendor-side changes (model versions, system prompt changes, API changes) can shift benchmark results without a release announcement.

**Mitigation:** the full benchmark runs quarterly; a smaller subset (10-20 tasks) runs monthly to catch drift.

## Anti-pattern 10 — Score chasing without root cause

The team sees a 4-point drop in benchmark score. They don't investigate; they just lower the threshold or add tasks the model handles well.

**Why it's wrong:** the score drop was signal. Investigation might surface a real regression that needs vendor escalation or a routing change.

**Mitigation:** any benchmark score change >2 points triggers investigation. What's driving it? Is it a specific category? Did vendor change something?

## Anti-pattern 11 — Cost and capability conflated

The benchmark scores models on capability only. Cost is a separate consideration.

**Why it's wrong:** routing decisions need both. A model that scores 5 points higher at 3× the cost is a different decision than one that scores 5 higher at the same cost.

**Mitigation:** report capability and cost together. Per [`when-to-switch-primary-model.md`](when-to-switch-primary-model.md), both feed the decision.

## Anti-pattern 12 — Benchmark designed once, never reviewed

The benchmark structure (categories, weights, scoring) was set in 2025 and hasn't been re-examined. The team's work has shifted; the benchmark hasn't kept up.

**Why it's wrong:** the benchmark may not reflect current work. Decisions made on stale benchmark data are stale decisions.

**Mitigation:** annual review of benchmark structure (not just task refresh). Are the categories right? Are the weights right? Has team work shifted?

## Anti-pattern 13 — Single-model design

The benchmark was designed when the team had one model in the lineup. As the lineup grew (specialized models, mixed routing), the benchmark didn't adapt.

**Why it's wrong:** the benchmark gives an aggregate score that's not meaningful when different models handle different work types.

**Mitigation:** benchmark is per-category. The aggregate is informational; the per-category scores drive decisions.

## Anti-pattern 14 — Edge cases dominate

The benchmark is heavy on edge cases (the 5% of work that's tricky), light on routine work (the 80% of work that's normal).

**Why it's wrong:** the team's productivity is dominated by routine work. A model that's great at edge cases but mediocre at routine work isn't actually better for the team.

**Mitigation:** distribution matches the team's actual work. Edge cases get 5-10%, not 30%.

## Anti-pattern 15 — Benchmarks run by an isolated platform team

The platform team runs the benchmark; nobody else sees the results. Engineers don't know how their model was selected.

**Why it's wrong:** lack of transparency erodes trust. Engineers route around the benchmark's decisions.

**Mitigation:** benchmark results are published internally. Per [`quarterly-model-lineup-review.md`](quarterly-model-lineup-review.md), tech leads attend the review.

## Anti-pattern 16 — Vendor-supplied benchmark

A vendor supplies a benchmark suite "tuned to your team's work." It looks comprehensive.

**Why it's wrong:** vendor-supplied benchmarks favor the vendor's models. The vendor isn't malicious; the benchmark is just selected from the vendor's strengths.

**Mitigation:** team builds the benchmark internally. Vendor-supplied tools are useful for scoring infrastructure (running tasks, capturing results); the task set should be the team's.

## Anti-pattern 17 — Benchmark depends on production data

Tasks reference real customer data. The benchmark can't be run in non-production environments; data exposure risk.

**Why it's wrong:** the benchmark becomes a privacy / security concern. Running it requires production access.

**Mitigation:** task fixtures use synthetic data that mirrors production patterns. Anonymization or synthetic generation; never real customer data.

## Anti-pattern 18 — Benchmark fragility

A small change to CLAUDE.md or a skill update breaks the benchmark. Results aren't comparable across runs.

**Why it's wrong:** the benchmark is supposed to test the model + harness; if minor harness changes invalidate results, the benchmark is too fragile.

**Mitigation:** benchmark uses a stable harness configuration version. Changes to the production harness don't immediately propagate to the benchmark.

## Anti-pattern 19 — All-or-nothing scoring

Pass/Fail only; no Partial. A task that's 80% there scores the same as a task that's 0% there.

**Why it's wrong:** loses signal. A model improving from 0%-correct to 80%-correct on a task isn't visible.

**Mitigation:** Pass/Partial/Fail per [`internal-benchmark-construction.md`](internal-benchmark-construction.md), with explicit rubric for Partial.

## Anti-pattern 20 — Benchmark used as engineer evaluation

Engineers' work is compared to the benchmark's expected outcomes. Engineers feel surveilled.

**Why it's wrong:** the benchmark exists to evaluate models, not engineers. Conflating the two destroys trust.

**Mitigation:** explicit boundary. Benchmark results are operational data for routing decisions; not input to performance reviews.

## How to know if your benchmark is good

A good internal benchmark:
- Reproduces (same model, same tasks, same scores within ~2 points)
- Discriminates (different models score meaningfully differently)
- Reflects work (the task distribution matches what the team actually does)
- Refreshes (tasks rotate; rubric is reviewed)
- Informs decisions (the team has changed routing based on benchmark data at least once)

If any of these isn't true, the benchmark needs work.

## Companion artifacts

- [`internal-benchmark-construction.md`](internal-benchmark-construction.md) — the construction guide
- [`when-to-switch-primary-model.md`](when-to-switch-primary-model.md) — the decision framework
- [`quarterly-model-lineup-review.md`](quarterly-model-lineup-review.md) — when this is exercised
- Ch 26 §26.5 — source
