# Success Metrics

How the platform team's value is measured and reported. Per Ch 42 §42.4, platform is a real product team — and product teams measure themselves on what they ship and what gets used.

This document defines:
- What we measure (and what we don't)
- How we report
- The cadence of reviews

## Three categories of metrics

The platform team's success has three dimensions:

1. **Adoption** — Are stream-aligned teams using what we ship?
2. **Impact** — Does what we ship measurably change engineering outcomes?
3. **Quality** — Does what we ship work reliably?

A team strong on all three is a healthy platform team. A team strong on only one or two has a specific gap to address.

## Adoption metrics

### What we measure

- **Active users per harness component.** For each skill, hook, subagent, MCP server: how many distinct engineers used it in the last 30 days.
- **Active teams per harness component.** Same data aggregated to team level.
- **Coverage of canonical patterns.** What fraction of recurring engineering tasks have a corresponding skill / hook / subagent? Stretch goal: 80%+ coverage of canonical patterns.
- **Office hours attendance.** Number of distinct engineers attending office hours over the quarter. (A measure of engagement, not just consumption.)
- **Pair-driving sessions completed.** Number of pair-driving sessions between platform engineers and stream-aligned engineers per quarter.

### What we DON'T measure

- **Total invocations.** A skill that runs 10,000 times in low-value contexts is not better than a skill that runs 100 times in high-value contexts. Volume is not adoption.
- **GitHub stars or similar vanity metrics.** The team's customers are stream-aligned engineers in this company; not external developers.

### Calibration

- 50%+ of stream-aligned engineers using the platform's tools weekly: healthy adoption
- 25-50%: building adoption; investigate what's gating
- <25%: adoption gap; either the tools don't fit or the discovery / onboarding is broken

## Impact metrics

### What we measure

- **Defect rate by AI authorship classification.** Per Ch 31 §31.6's PR tagging convention. The platform team's tools should keep AI-authored defect rates within statistical noise of human-authored.
- **Lead time for changes** (per DORA). The platform team's tools should reduce lead time, not increase it. Track quarterly.
- **Time spent in PR review.** Per Ch 31 §31.3, time-in-review is one of the slop-detector indicators. Track quarterly to ensure platform investments aren't increasing review burden.
- **Token spend per developer (median).** From Ch 31 §31.1's six metrics. Platform team's cost dashboards and routing should keep this in a healthy band.
- **Migration completion times.** When the platform team executes a migration playbook (per `migration-playbooks/`), how long did it take from kickoff to steady state? Track each migration.
- **Incident reduction** for incidents that the harness's slop-detector / subagents could catch.

### What we DON'T measure

- **Engineering hours saved.** Easy to claim, hard to defend. Some "hours saved" calculations are 5-10x off.
- **Self-reported developer satisfaction with the platform.** Possible to measure, but vulnerable to recency bias and political pressure. Use sparingly; not as primary.
- **Number of incidents prevented.** Counterfactual. Hard to defend.

### Calibration

The impact metrics should trend positively over the team's first 12 months. If they're flat or negative after 6 months, something's wrong with the harness; investigate.

## Quality metrics

### What we measure

- **Harness component error rates.** When a hook misfires (false positive or false negative), it's tracked. When a subagent produces wrong output, it's tracked.
- **Harness component reliability.** Uptime of MCP servers, dashboards, etc.
- **Time-to-fix for harness bugs.** When a stream-aligned team reports a harness bug, how long until it's fixed?
- **Documentation completeness.** Per harness component: does it have a README? Does the README pass a quick quality bar (purpose, usage, gotchas)?
- **Customer-reported issues.** Number of issues filed by stream-aligned teams against the platform; weighted by severity.

### What we DON'T measure

- **Lines of code per component.** Quantity is not quality.
- **Number of components shipped.** Volume is not quality.

### Calibration

- Harness components have <2% error rate (false positives plus false negatives) — healthy
- 2-5% — investigate; tune heuristics
- >5% — the component is a net negative; the noise produces dismissal habits

## How we report

### Quarterly metrics dashboard

The platform team produces a quarterly dashboard with the metrics above. Format:

- **Section 1 — Adoption.** Per-harness-component adoption metrics with trend
- **Section 2 — Impact.** Per-impact-metric trend, with attribution where possible
- **Section 3 — Quality.** Per-component reliability and customer-reported issues

The dashboard is shared with engineering leadership monthly and presented at quarterly business reviews.

### Adoption deep-dive (annual)

Once per year, the platform team produces a detailed adoption study:

- Which harness components are most-used? Why?
- Which are least-used? Why? Are they being deprecated, or do they need investment?
- Which teams are most engaged? Which least? What does the gap teach us?
- What's the trajectory of adoption — growing, stable, declining?

The study informs the next year's roadmap.

### Customer interviews (quarterly, rotating)

The platform team interviews 3-5 engineers from rotating stream-aligned teams each quarter. The interviews are structured:

- What's working in the harness for you?
- What's not?
- What would you ask the platform team to ship next?
- Where are you working around the harness instead of with it?

Findings inform roadmap. Specific quotes and patterns are documented (anonymized) and shared.

## What good looks like

Healthy quarter:

- Adoption metrics trending up across most components
- Impact metrics stable or improving (defect rates flat, lead time stable or down)
- Quality metrics meeting targets (error rates <2%, no severe bugs in customer-reported issues)
- Customer interviews surface a manageable backlog of improvements, not a cascade of complaints
- Roadmap delivered roughly as planned

Concerning quarter:

- Adoption flat or declining for major components
- Defect rates trending up on AI-authored work
- Lead time trending up
- Multiple severe bugs reported by customers
- Customer interviews surface widespread frustration
- Roadmap significantly underdelivered

The concerning pattern, if persistent across quarters, demands action: either harness-component-level fixes, or strategic re-evaluation of what the team is shipping.

## What this metrics framework will NOT do

- Will not work without instrumentation. Adoption, impact, quality — all require data; the data requires investment in instrumentation.
- Will not eliminate political pressure. Some leadership will press for vanity metrics (lines of code, engineer hours saved); the discipline is to not give in.
- Will not capture everything. Some platform team value is genuinely unmeasurable in the short term. The framework is a useful approximation, not a complete picture.

## Companion artifacts

- [`charter.md`](charter.md) — what the team is measuring against
- [`budget-and-headcount-framing.md`](budget-and-headcount-framing.md) — the metrics for the budget conversation
- [`case-studies.md`](case-studies.md) — qualitative examples to complement the quantitative
- Ch 31 §31.1, §31.3, §31.6 — adjacent metrics framing
- Ch 42 §42.4 — source
