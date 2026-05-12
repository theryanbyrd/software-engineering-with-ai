# Metrics and Measurement Infrastructure

The dashboards, signal definitions, and telemetry pipelines that turn AI-assisted engineering from a vibe into something a CEO can ask about and you can defend. Direct companion to **Chapter 24 — Observability as an Agent Feedback Loop** and **Chapter 31 — Software Metrics for the AI Era** of [_Software Engineering with AI: A Practical Handbook for the Claude Code Era_](https://github.com/theryanbyrd/software-engineering-with-ai) by Ryan Byrd.

The book's framing:

> The point of this toolkit is not to slow down. It is to ship fast with evidence rather than fast with hope. The CEO who is asking for proof at month 4 will get a defensible answer if you set this up at month 1; they will not get a defensible answer if you set it up the week they ask.
>
> — Ch 31

This folder turns that toolkit into running infrastructure: the six-metric dashboard you can drop into Grafana on day one, the quality-decay signal queries that tell you when AI adoption is degrading codebase health, the observability hooks that auto-file agent-ready issues from production signals, and the A/B framework for measuring adoption impact honestly.

## What's in here

| File | Purpose |
|---|---|
| [`six-metric-dashboard/`](six-metric-dashboard/) | Grafana JSON exports and PromQL/SQL queries for the six canonical metrics from Ch 31.1 |
| [`quality-decay-signals.md`](quality-decay-signals.md) | The six leading indicators of quality decay (Ch 31), with detection queries and thresholds |
| [`code-maturity-rubric.md`](code-maturity-rubric.md) | The 1–10 LLM-graded code maturity rubric from Ch 31.1, plus the validation procedure (grade against human-scored samples before trusting) |
| [`agent-ready-issue-pipeline.md`](agent-ready-issue-pipeline.md) | The Ch 24 observability-to-issue automation: production signal → triage → auto-filed agent-ready ticket |
| [`ab-testing-framework.md`](ab-testing-framework.md) | The A/B framework for measuring AI adoption impact without confounding throughput with quality |
| [`baseline-measurement-template.md`](baseline-measurement-template.md) | The pre-rollout survey: capture baseline metrics before AI lands, or you have nothing to compare against |
| [`triage-taxonomy.md`](triage-taxonomy.md) | Score / Question / Opportunity / Train — the seventh metric, used to triage failed one-shots |

## The book's core stance

Per Ch 31.7:

> Six metrics on the dashboard, no more. Resist dashboard sprawl. LLM-graded code maturity is the highest-leverage metric and the highest-investment. Lines of code is the discredited metric for AI productivity.

Three things follow:

1. **Adoption metrics are not productivity metrics.** Token usage tells you who is *using* AI. It does not tell you whether that usage is helping. Track separately.
2. **The leading indicators are leading.** Quality decay shows up in mutation score and revert rate before it shows up in incidents. By the time customer-reported defects spike, you are already three months late.
3. **Never show individual developers their own daily score.** Per Ch 31.1 — team-level trends only. Individual scores are for coaching, never for ranking. Surveillance kills the feedback loop you're trying to build.

## The six metrics (Ch 31.1)

| # | Metric | What it tells you |
|---|---|---|
| 1 | AI Token Usage per Developer | Adoption rate and cost-control input — *never* a perf-eval metric |
| 2 | Code Maturity Score (1–10, LLM-graded) | The highest-leverage signal — and the highest-investment to set up |
| 3 | Features Delivered to Bugs Introduced Ratio | DORA "change failure rate" inverted |
| 4 | Time from User Story to Production | DORA "lead time" with the in-progress-column anchor |
| 5 | Story Points Delivered | Team velocity — track the trend, not the absolute |
| 6 | Predictability: 1 − (σ/µ) | The single most underrated metric in software engineering |
| 7 | Score / Question / Opportunity / Train | Lives in [`triage-taxonomy.md`](triage-taxonomy.md), tied to [`../failed-one-shot-triage`](../failed-one-shot-triage) |

## The six quality decay signals (Ch 31)

1. **Mutation score trending down.** Tests still pass but kill fewer mutants — tests are testing implementation, not behavior.
2. **PR size trending up.** Agents generating more than they should.
3. **Review-time-per-line trending down.** Rubber-stamping.
4. **Revert rate trending up.** PRs reverted within 30 days — the most direct signal.
5. **Customer-reported defects up.** End users finding bugs that escaped your harness.
6. **Senior engineer 1:1s reporting culture concerns.** Soft signal, reliable, treat seriously.

Per Ch 31: two consecutive months of decay on three or more is a "pull the lever" signal — pause new-team rollout, audit the harness, run a senior-engineer-led review-quality review.

## Who this is for

- **VPs of Engineering** who need to answer "is the AI investment working?" with evidence rather than vibes
- **CTOs** preparing the board-level ROI conversation (see also [`../exec-kit`](../exec-kit))
- **Platform engineers** building the measurement layer once, so individual teams don't reinvent it
- **Engineering managers** running a team-level rollout who need the right dashboard before week 1

## Related sections in this repo

- [`../benchmarks`](../benchmarks) — A/B testing methodology and the DX/DORA/METR baseline numbers
- [`../evals-and-benchmarks-runbook`](../evals-and-benchmarks-runbook) — mutation testing as the keystone evaluation
- [`../failed-one-shot-triage`](../failed-one-shot-triage) — Score/Question/Opportunity/Train, the 7th metric
- [`../incident-postmortem-templates`](../incident-postmortem-templates) — the AI-specific postmortem template that feeds the agent-ready-issue pipeline

> Early access. The six-metric dashboard JSON exports and the quality-decay queries are the priority files. Code-maturity rubric and validation procedure follow.
