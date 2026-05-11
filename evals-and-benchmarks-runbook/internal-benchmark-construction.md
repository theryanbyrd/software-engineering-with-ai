# Internal Benchmark Construction

How to build the team's eval set from real work. This is the foundation of every other discipline in this folder — without an internal benchmark, model decisions are made on vibes or on public leaderboards (which Ch 26 §26.5 specifically warns against).

## What "internal benchmark" means here

A set of representative tasks, drawn from the team's actual work, that can be run against any model. The benchmark produces a score (or a set of scores) that lets you compare models on dimensions that matter to your team.

This is NOT:
- A public benchmark suite (SWE-bench, HumanEval, etc.) — those measure general capability
- A vibe check or one-off comparison — those don't reproduce
- A vendor's marketing demo — those are designed to look good

It IS:
- Real tasks from the team's backlog or recent history
- Reproducible (same inputs, same scoring, run again later)
- Specific to the team's codebase, conventions, and constraints
- Calibrated for the team's typical work, not edge cases or showcase work

## Sizing

A useful internal benchmark has 30-100 tasks. Below 30, statistical noise dominates; above 100, the eval cost becomes prohibitive (running 100 tasks across 3 candidate models is 300 invocations).

Most teams settle around 50-60 tasks. Calibrate to your team's eval budget.

## Task selection

Pull tasks from real history. For each, capture:

- **The original spec** (issue body, ticket text)
- **The expected outcome** (the merged PR, or the manual implementation if no AI was involved)
- **The category** (per [`task-taxonomy-rubric.md` in agent-autonomy-levels](../agent-autonomy-levels/task-taxonomy-rubric.md): AI-friendly, AI-cautious, AI-dangerous)
- **The tier** (per Ch 19 §19.5: T1 simple, T2 inspection, T3 architecting)
- **The actual model that did it** (if any) and how it went

### Distribution

Aim for a mix that matches your team's actual work distribution:

| Category | Suggested share | Notes |
|---|---|---|
| **Bug fixes** | 25-35% | Most teams' bread-and-butter work |
| **Small features** | 20-30% | Bounded new functionality |
| **Refactors** | 15-25% | Including some cross-cutting |
| **Test additions** | 5-15% | Including characterization tests |
| **Documentation** | 5-10% | Includes both reference docs and code comments |
| **Migrations / schema changes** | 5-10% | High-stakes work; small share but important |
| **Edge cases** | 5-10% | Things that famously go wrong |

Adjust to your team's reality. A platform team's mix differs from a feature team's.

### Tier distribution

Per Ch 19 §19.5, work falls into three tiers (T1 simple, T2 inspection, T3 architecting). The benchmark should include all three:

- **T1**: 20-30% — quick tasks the agent should one-shot reliably
- **T2**: 50-60% — the bulk of real work; agent should usually succeed with good spec
- **T3**: 15-25% — hard tasks; agent will not one-shot, but the quality of the plan matters

Don't skew to T2 only. T1 work tells you which model is fastest and cheapest for routine work; T3 work tells you which model can actually reason about hard problems.

### What NOT to include

- **Tasks that succeeded only because of unique team knowledge** — the benchmark should test the model, not the engineer's tribal knowledge transfer
- **Tasks where the spec was insufficient** — those are Train failures (per `failed-one-shot-triage/`), not model capability tests
- **Tasks that aren't reproducible** — if running the task again would produce a different result, it's not a benchmark
- **Recent work that's leaked into model training data** — newer tasks are sometimes better (less likely to be in training); use judgment

## Scoring

For each task in the benchmark, define what "success" means. The book's framing in §19.5 is the right vocabulary:

- **Score (success)**: agent produces a PR that passes verify, matches the spec, and would be merged with light review
- **Question (model can't)**: model demonstrably can't do this work; failure is in the model
- **Opportunity (harness gap)**: model could do it with better context; failure is in the harness
- **Train (spec failure)**: spec was insufficient; failure is in the input

For benchmarking purposes, only Score and Question are clean signals. Opportunity and Train depend on the harness and spec, not the model.

### Recommended scoring approach

Run each task through each candidate model with:

- The team's normal CLAUDE.md / AGENTS.md context
- The team's normal harness (skills, hooks, subagents)
- The team's normal verify command as the success gate

Score each result:

- **Pass**: produces a PR that passes verify and matches spec at quality the team would merge
- **Partial**: produces a PR with issues that would require rework but is on the right track
- **Fail**: produces a PR that's wrong, off-spec, or doesn't pass verify

Weights:
- Pass = 1.0
- Partial = 0.5
- Fail = 0.0

Aggregate: percentage of points earned across all tasks.

### Per-category scoring

Don't just aggregate. Score per category and per tier:

| Model | Bug fix | Small feature | Refactor | Test add | Docs | Migration | Total |
|---|---|---|---|---|---|---|---|
| Sonnet 4.6 | 88% | 75% | 67% | 92% | 95% | 60% | 79% |
| Opus 4.7 | 90% | 88% | 85% | 92% | 95% | 88% | 90% |
| Haiku 4.5 | 70% | 50% | 35% | 85% | 95% | 25% | 60% |

The per-category breakdown is what informs the routing rubric. Sonnet 4.6 ties Opus 4.7 on docs and tests but lags on refactors and migrations — which means routing migrations to Opus is the right call.

## Running the benchmark

### First-time

The first run is the most expensive. Plan for 1-2 weeks of platform team time:

- Week 1: task selection, scoring rubric definition, fixture preparation
- Week 2: running tasks against current model, recording baseline

After the first run, subsequent runs are much faster (the tasks and rubric exist).

### Recurring

Per [`quarterly-model-lineup-review.md`](quarterly-model-lineup-review.md), run quarterly. Each run takes 2-4 days of platform team time.

### When new models drop

Run the benchmark against the new model within 2-4 weeks of release. Don't wait for the quarterly cadence if a major model change is in the air.

## Maintaining the benchmark

### Refreshing tasks

Per quarter, retire 5-10 tasks and add 5-10 new ones. Reasons to retire:

- The task has been in training data for too long; results are inflated
- The task no longer represents current work (the team's scope has shifted)
- The task is too easy (every candidate model passes; no signal)

Reasons to add:
- New work patterns have emerged
- The team has shifted focus to a new technology / framework
- New edge cases have surfaced from production incidents

### Updating the rubric

The rubric (Pass/Partial/Fail criteria) can drift over time. Quarterly review of:
- Are pass/fail decisions consistent across reviewers?
- Are partial credit assignments reasonable?
- Have any tasks become ambiguous?

Update the rubric explicitly; document the change.

### Versioning

The benchmark has a version (e.g., `2026.q3.v1`). Each run is tagged with the version. When the benchmark changes substantively (tasks added/removed, rubric changed), bump the version.

This lets you compare apples to apples across time AND know when the comparison stops being apples-to-apples.

## Cost of running the benchmark

Approximate cost for a 50-task benchmark across 3 models:
- 150 agent invocations
- Average task is 50K input tokens, 5K output tokens
- Across mixed Haiku/Sonnet/Opus: roughly $50-150 per full benchmark run

Quarterly cost: $200-600/year. Negligible compared to the cost of routing decisions made without it.

## Companion artifacts

- [`quarterly-model-lineup-review.md`](quarterly-model-lineup-review.md) — when to run
- [`when-to-switch-primary-model.md`](when-to-switch-primary-model.md) — what to do with results
- [`benchmark-construction-anti-patterns.md`](benchmark-construction-anti-patterns.md) — common pitfalls
- `cost-discipline-runbook/model-routing-rubric.md` — adjacent (the routing this informs)
- Ch 26 §26.5, Ch 19 §19.5 — sources
