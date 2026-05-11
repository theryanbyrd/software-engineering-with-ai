# Evals and Benchmarks Runbook

The operational discipline for running model evaluations against the team's actual workloads. Direct implementation of Chapter 26 + Chapter 27 of [_Software Engineering with AI: A Practical Handbook for the Claude Code Era_](https://www.linkedin.com/in/ryanbyrd) by Ryan Byrd, with the quarterly model lineup review from Ch 44 §44.4 item 8.

The book's framing:

> The model leaderboard for coding (LMArena, SWE-bench Verified, Aider Polyglot, LiveCodeBench, every internal benchmark) reorders on a roughly weekly cadence in 2026. The vendor that was clearly best last quarter is rarely clearly best this quarter.
>
> — Ch 26 §26.5

> Switch when a new model is markedly better on your internal benchmark — not the public one. "Markedly" means at least 5 points on aggregate score and a clear pattern across multiple task types in your evaluation set. A 1-2 point bump is noise; a 5+ point bump is signal.
>
> — Ch 26 §26.5

This folder operationalizes the discipline: build the team's internal benchmark, run it against candidate models, decide when to switch, update the routing policy.

## What's in here

| File | Purpose |
|---|---|
| [`README.md`](README.md) | Overview, why internal evals matter more than public benchmarks |
| [`internal-benchmark-construction.md`](internal-benchmark-construction.md) | How to build the team's eval set from real work |
| [`quarterly-model-lineup-review.md`](quarterly-model-lineup-review.md) | The recurring review structure per Ch 44 §44.4 item 8 |
| [`when-to-switch-primary-model.md`](when-to-switch-primary-model.md) | The 5-point rule and the broader decision framework |
| [`routing-policy-update-process.md`](routing-policy-update-process.md) | How to update the team's routing rubric after eval results |
| [`benchmark-construction-anti-patterns.md`](benchmark-construction-anti-patterns.md) | Common failure modes when teams build internal evals |

## Why internal evals matter

Per Ch 26 §26.5, public benchmarks reorder weekly. They're useful as background but not as decision input. Specifically:

- **Public benchmarks measure general capability.** Your team uses models for specific tasks with specific constraints; general capability doesn't predict task-specific quality.
- **Public benchmarks are gameable.** Vendors optimize for what's published. Your internal benchmark is what isn't.
- **Public benchmarks miss your team's edge cases.** Your codebase has invariants, conventions, and patterns that public benchmarks can't test for.
- **Public benchmarks are stale by the time they're published.** A new model release shifts the rankings within days.

The teams that route well in 2026 are the teams with internal benchmarks. The teams that chase public benchmarks produce expensive switches that don't move productivity metrics.

## Who this is for

- **Platform team members** running the quarterly evals
- **Tech leads** advising on model routing decisions
- **Engineering managers** allocating eval time
- **VPs of Engineering / CTO** making model selection decisions
- **Engineers** who want to understand why the team uses the model it uses

## Read first

- Ch 26 — the source chapter on model selection
- Ch 27 — economics (model selection has cost implications)
- `cost-discipline-runbook/model-routing-rubric.md` — adjacent (the routing this informs)
- `cost-discipline-runbook/monthly-cost-review-structure.md` — adjacent (model mix surfaces in monthly review)

## What this runbook WILL do

- Establish the team's internal benchmark for model evaluation
- Provide the cadence and structure for quarterly model lineup review
- Set the criteria for when a model switch is warranted
- Connect eval results to routing policy updates
- Distinguish signal from noise in benchmark data

## What this runbook will NOT do

- Will not eliminate model selection judgment. Evals inform; engineers decide.
- Will not work without time investment. Building and maintaining an internal benchmark is real engineering work.
- Will not protect against vendor-side changes that emerge between reviews. Major model behavior shifts may warrant mid-cycle review.
- Will not produce a "best model" answer. Different work types warrant different models; the routing rubric reflects this.

## How this folder fits with adjacent material

| Need | Where to look |
|---|---|
| Day-to-day routing decisions | `cost-discipline-runbook/model-routing-rubric.md` |
| Cost implications of routing | `cost-discipline-runbook/token-budgets-by-team.md` |
| Vendor side of model selection | `vendor-procurement-runbook/` |
| Capability vs work category mapping | `agent-autonomy-levels/task-taxonomy-rubric.md` |
| Why we don't sign long-term contracts | Ch 26 §26.5; `vendor-procurement-runbook/renewal-discipline.md` |

## The core principle

Per Ch 26 §26.5:

> Standardize on one model family for stability. Do not chase every benchmark win. Switching is expensive in retraining, retesting, and harness adaptation.
>
> But switch when a new model is markedly better on your internal benchmark.

The discipline is calibrated patience. Don't switch on noise; do switch on signal. The internal benchmark is what tells you which is which.

## Companion artifacts

- `cost-discipline-runbook/` — adjacent
- `vendor-procurement-runbook/` — adjacent
- `agent-autonomy-levels/` — adjacent (autonomy depends on model capability)
- Ch 26, Ch 27, Ch 44 §44.4 item 8 — sources
