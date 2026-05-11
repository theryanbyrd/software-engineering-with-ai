# Leadership Conversation on Cost

The honest cost-vs-value conversation with finance and executive leadership. Per Ch 29 §29.2:

> The incoherent position — "we will pay for tokens and freeze hiring and not reduce headcount and expect 2x throughput" — is the one most CEOs are pitching after listening to vendor keynotes. Push back, in writing, with numbers.

This file is the structured conversation. Use it when leadership is making cost demands that don't survive scrutiny, or when the AI tooling investment is being questioned.

## When to have this conversation

- **Quarterly budget review.** Standard cadence; AI tooling cost is a line item.
- **When cost growth is questioned.** "Why are we spending so much on AI tools?"
- **When leadership demands productivity gains.** "We're paying for these tools; why aren't we delivering more?"
- **When leadership asks for cost reduction.** "Can we cut AI tooling spend by 30%?"
- **Before vendor renewal.** The conversation calibrates expectations for the next year.

## The setup

The conversation works only if:

1. **You have data.** Per Ch 29 §29.3, OpenTelemetry-instrumented spend, attributed per team and per developer.
2. **You have throughput data.** Cost-per-merged-PR, throughput trends, defect-rate data per Ch 31 §31.1.
3. **You have a position.** "Our AI tooling investment is producing X" or "We're not seeing the throughput gain we expected; here's why."

Without these, the conversation is theatrical. Don't have the meeting until the data is real.

## The opening

> "I want to walk you through where we are on AI tooling cost. The data first, then the strategic question.
>
> Our current monthly spend is $[N]. That's [up / flat / down] from last quarter. We have it instrumented per team, per developer, per merged PR.
>
> The throughput side: our cost per merged PR is $[X], with throughput at [Y PRs/quarter]. Year-over-year, throughput is [up / flat / down] [Z]%.
>
> The strategic question I want to discuss: are we investing the right amount, in the right places, for the right outcomes? The answer to that informs what we do next."

## The two coherent positions

Per Ch 29 §29.2, there are two coherent strategic positions on AI tooling spend:

### Position 1 — Investment posture

> "Add tokens on top of current headcount. Expect throughput up, quality flat or modestly up (with harness investment), revenue up. Do not promise headcount reductions to the board; they will not materialize on the timeline boards want."

The argument:

> "Investment posture means: we keep the team size, we add AI tooling cost, we expect throughput to go up. The data supporting it: [your specific data on throughput improvement, quality improvement, capacity unlocks].
>
> What this requires from leadership: tolerance for OPEX growth in the AI tooling line, with offsetting throughput gains showing up over 6-12 months, not in the next quarter.
>
> What this prevents: headcount reduction promises that don't materialize. The board hears 'AI replaces engineers'; the reality is 'AI makes engineers faster, but not in 90 days.'"

### Position 2 — Substitution posture

> "Hold engineering budget flat. Some headcount reduction funds the token spend. Throughput holds with smaller team, quality requires aggressive harness investment, attrition risk is real."

The argument:

> "Substitution posture means: we reduce headcount, we add AI tooling cost, total engineering budget is flat. The data supporting whether this works: [your specific data].
>
> What this requires: a serious investment in the harness — the team has to be smaller AND more productive; without the harness, the smaller team produces worse outcomes.
>
> What this risks: attrition (the engineers we'd want to keep are the ones who can leave fastest), the discomfort of layoffs, the harness investment that doesn't pay off if the smaller team is too small."

### The incoherent position

> "The pattern I want to flag: the incoherent position is 'pay for tokens AND freeze hiring AND keep team the same size AND expect 2× throughput.' Per the empirical data on AI engineering productivity, that combination doesn't deliver. The honest read: pick one of the two coherent positions; don't pretend both."

## Common leadership pushbacks

### "Vendors are showing 10× productivity gains. Why aren't we seeing that?"

> "Vendor demos run on ideal conditions: clean codebases, controlled tasks, presenter-driven flow. The empirical data on production teams shows different numbers. Specifically: most teams see 10-30% throughput gains with appropriate harness investment, declining if the harness isn't in place.
>
> If we're below the 10-30% range, it's a harness issue, not a tooling issue. The fix: more harness investment (per `platform-team-charter/`), not different tooling.
>
> If we're at the 10-30% range, we're getting industry-typical returns. 10× is a vendor claim, not an industry observation."

### "Can we cut AI tooling spend by 30%?"

> "We can, with explicit tradeoffs. Specifically:
>
> - Cut model usage to Sonnet-only (no Opus): saves ~25-35% but degrades quality on architecture/security work
> - Reduce per-developer caps: saves variable amount; reduces engineer satisfaction with tooling
> - Eliminate background agents: saves ~10-20%; loses code-review subagent value
>
> The combinations that achieve 30% reduction: [your specific options based on your spend mix]. Each has a real trade-off; I want us to choose them deliberately, not pretend the cut is free.
>
> Question for you: what's driving the 30% target? If it's a temporary cash constraint, we can pause certain work. If it's a sustained budget shift, we should plan more carefully."

### "Why are some engineers spending so much more than others?"

> "Three reasons, in order of typical frequency:
>
> 1. The engineer is doing more AI-leveraged work (legitimate; they're using the tools more)
> 2. The engineer is routing inefficiently (Opus where Sonnet would suffice; correctable through coaching)
> 3. The engineer has agent loops or context bloat (a workflow problem; correctable)
>
> The data per developer is in the dashboard. The pattern matters more than absolute numbers — engineers in the 90th percentile consistently are usually category 1 or 2; engineers spiking once are usually category 3.
>
> Don't surface this in punitive ways. The engineers in the 90th percentile may be the most productive on the team; their cost is the cost of their productivity."

### "Headcount is flat next year; we need productivity gains"

> "Headcount flat plus growing scope means productivity gains have to come from somewhere. AI tooling is one source.
>
> What I can commit to: with the current AI tooling investment plus harness investment, we can plan for [N]% productivity gain over the year. With increased AI tooling investment plus dedicated platform headcount, we can plan for [more]% over 12-18 months.
>
> What I can't commit to: 2× throughput in 12 months on flat headcount with no incremental investment. The empirical data doesn't support that promise.
>
> What I'd recommend: pick a realistic target and the supporting investment. If the company needs 2× engineering output, that's a multi-year program with substantial harness investment, not a flip-the-switch decision."

### "I want a quarterly throughput report tied to AI tooling spend"

> "Yes, this is reasonable. Per Ch 31 §31.4 (the executive dashboard framework), the appropriate metrics:
>
> - Cost per merged PR by team (rolling 30-day, year-over-year)
> - Lead time for changes (DORA metric)
> - Defect rate by AI authorship classification
> - Token spend per developer (median; 90th percentile separately)
>
> These are reportable monthly; quarterly summary is appropriate for leadership review. I'll commit to delivering them.
>
> What I'd push back on: simplistic metrics like 'lines of AI code' or 'percentage of code AI-written' — these are vanity metrics; they don't reflect business value. The cost-per-PR and defect-rate framing is what makes the investment defensible."

### "When does this AI tooling spend pay off?"

> "Different timeframes for different parts:
>
> - **Tactical wins (first 90 days):** specific high-friction tasks (code review, test generation, documentation) get faster. Measurable.
> - **Productivity gains (3-12 months):** with appropriate harness investment, throughput trends measurably up. Visible in DORA metrics.
> - **Strategic capability (12-24 months):** the team handles work that wouldn't have been feasible without AI tooling. Hard to measure quantitatively; visible in roadmap.
>
> What I won't promise: Year 1 ROI calculations that match what vendors claim. The empirical data doesn't support those claims.
>
> What I will commit to: quarterly reviews showing whether we're on the trajectory. If we're not, we adjust the investment level."

## When the conversation goes badly

Some leaders won't engage substantively. They'll demand the incoherent position; they'll dismiss the data; they'll insist on vendor-marketing-shaped outcomes.

When this happens:

- **Document the disagreement.** "I noted my position; the decision went a different way."
- **Predict the outcome.** "If we cut budget 30% without changing scope expectations, here's what I expect to happen by Q3."
- **Hold the line on safety.** Cost reduction can't compromise the autonomy ladder, the slop-detector, or the security-reviewer subagent. Those are floor-level investments.
- **Plan the pivot.** When the predicted outcome materializes, the position is "as I said in [memo]" — not "I told you so" but a calibrated reset.

## What this conversation will NOT do

- Will not eliminate the political pressure on AI tooling spend. Some leaders will continue to demand incoherent outcomes.
- Will not work without data. The conversation depends on actual instrumentation and metrics.
- Will not change minds in a single meeting. The discipline is repeated honest engagement over quarters.
- Will not work in cultures that punish honest pushback. If raising substantive concerns produces career risk, the conversation can't happen — that's a different problem.

## Companion artifacts

- [`token-budgets-by-team.md`](token-budgets-by-team.md) — operational budgets
- [`monthly-cost-review-structure.md`](monthly-cost-review-structure.md) — operational cadence
- `platform-team-charter/budget-and-headcount-framing.md` — adjacent
- `skip-level-defense/` — adjacent
- Ch 29 §29.2, Ch 29 §29.7 — sources
