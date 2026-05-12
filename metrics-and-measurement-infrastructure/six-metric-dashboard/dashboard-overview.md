# Dashboard Overview — The CEO-Defensible Read

How the six metrics fit together. The framing here is the answer to the question every CTO will be asked at month 4: **"Is AI working?"**

Per Ch 31 §31.6:

> The CEO who is asking for proof at month 4 will get a defensible answer if you set this up at month 1; they will not get a defensible answer if you set it up the week they ask.

This file is the structure of that answer.

## The story the six metrics tell

The six metrics fit into three pairs. Each pair is one piece of the story.

### Pair 1: adoption + cost — "Are people using it, and what does it cost?"

- **Metric 1: Token usage per developer** answers "are people actually using AI?"
- The Ch 31 §31.4 "Cost" tile (median spend per developer per week) answers "what does that usage cost?"

This pair is the cheapest to instrument and the least informative. Adoption and cost data is necessary — you can't claim ROI without it — but adoption can be high while the work is slop, and cost can be low while engineers are silently working around the tooling. Treat this pair as the table stakes, not the answer.

The diagnostic this pair surfaces:

| Pattern | Diagnosis |
|---|---|
| Adoption flat, cost flat | The rollout has plateaued — investigate why some engineers haven't adopted |
| Adoption rising, cost rising linearly | Normal early-rollout |
| Adoption rising, cost rising super-linearly | Routing problem (Opus on routine work, per Ch 26 §26.2) |
| Adoption falling, cost flat | Engineers are silently leaving the platform — survey them |
| Adoption high, cost dropping | Caching is working; routing is working; the team is mature |

### Pair 2: speed + quantity — "Is more work getting done?"

- **Metric 4: Time from user story to production** answers "is work getting through faster?"
- **Metric 5: Story points delivered** answers "is more work getting done?"

This pair is what the CFO wants to see. Both should be improving for AI to be paying off — but neither, alone, proves the rollout worked. Lead time can drop because engineers are skipping reviews. Velocity can rise because the team is generating more, lower-quality work.

The diagnostic this pair surfaces:

| Pattern | Diagnosis |
|---|---|
| Both rising | Plausible win; check pair 3 to confirm |
| Speed rising, velocity flat | The team is reorganizing work, not producing more |
| Speed flat, velocity rising | The team is doing more, slower per unit — check PR size signal |
| Both flat | AI rollout has not yet shown impact; check pair 3 and the leading indicators |
| Both rising AND pair 3 worsening | This is the "slop rollout" pattern — generating more, lower quality. Pull the lever. |

### Pair 3: quality + maturity — "Is the work any good?"

- **Metric 2: Code maturity score** is the LLM-graded leading quality signal
- **Metric 3: Features delivered to bugs introduced ratio** is the lagging quality signal

Per Ch 31 §31.7:

> LLM-graded code maturity is the highest-leverage metric and the highest-investment.

This pair is the answer to "is the work any good?" — and it's the pair that distinguishes a real AI win from a slop rollout. The book is explicit (Ch 31 §31.1):

> AI rollouts that produce real productivity gains show velocity rising while the ratio in metric (3) stays flat or improves; AI rollouts that produce slop show velocity rising while metric (3) deteriorates.

The diagnostic this pair surfaces:

| Pattern | Diagnosis |
|---|---|
| Both stable or rising | Genuine quality story; defensible |
| Maturity rising, ratio falling | Suspicious — the LLM grader may be biased, OR engineers are gaming the rubric; re-validate grader |
| Maturity falling, ratio stable | The lagging signal hasn't caught up yet; intervention now prevents the lag |
| Both falling | Quality decay; pull the lever (per [`../quality-decay-signals.md`](../quality-decay-signals.md)) |

## The seventh dimension: predictability

Metric 6 is the orthogonal axis. Per Ch 31 §31.1:

> The single most underrated metric in software engineering. A team that consistently delivers 35 ± 3 points is dramatically more valuable than a team that delivers 50 ± 25 points.

Predictability matters because AI rollouts often cause the variance to go up before the mean does — the team learns new patterns and some sprints overshoot while others under-shoot. A healthy rollout shows variance contracting after the first 90 days; an unhealthy rollout shows it expanding.

The pattern to look for:

- **Pre-AI baseline:** measure the variance. Most teams sit around 0.6–0.75 on 1 − (σ/µ).
- **First 90 days:** variance often expands (0.5–0.6). This is normal.
- **Day 90–180:** variance should contract back to baseline or below as the team stabilizes new patterns.
- **Day 180+:** healthy teams reach 0.85–0.9. Teams that stay below 0.7 after six months have a process problem (often: spec quality issues feeding the agent).

## The CEO-defensible read in one paragraph

The structure of the answer:

> Pair 1 shows adoption: [N]% of engineers are active weekly, with median spend stable at $[X]/dev/week. Pair 2 shows speed and volume: lead time has [improved/held] by [X]%; velocity has [risen/held] by [Y]%. Pair 3 — the part that distinguishes a real win from slop — shows quality: code maturity score is [stable/rising] at [N.M], and the features-to-bugs ratio is [stable/rising/falling]. Predictability is [N.M] and [trending in the right direction / holding]. The "pull the lever" signal from the decay dashboard is [green/yellow/red] with [N] of 6 signals decaying. We are [confidently / cautiously] reporting that AI investment is paying off; the artifacts that support this claim are the 90-day baseline, the AI-authorship attribution data, and the validated code-maturity grader. We will repeat this assessment quarterly.

Variations of this paragraph land at the board level, the CFO level, and the all-hands level with minor adjustments. The structure is the same. The point is to make the answer **answerable** — not to make it always good.

## What "all green" means and why you should be suspicious

Per Ch 31 §31.4:

> If all are green, you are either an exceptional organization or your dashboard is lying to you — investigate the second possibility first.

The honest read of "all green":

1. **You are gaming a metric.** Look for the easy-to-game ones: token usage, velocity, lead time (especially if "story enters in-progress" is being delayed to game the start time).
2. **Your grader is broken.** Re-run the validation procedure from [`../code-maturity-rubric.md`](../code-maturity-rubric.md). If the gold-set MAE has drifted >1.5, the grader is not measuring what you think it is.
3. **Your AI-authorship tagging is broken.** If everyone is tagging `ai:none` (or nobody is tagging), the per-tag breakdowns mean nothing.
4. **Sample size is too small.** "All green" on a team of 4 engineers across 6 weeks is noise.
5. **You are an exceptional organization.** (Maybe.)

Five teams will report "all green" at month 3. Four of them will have one of the first four issues. The fifth is genuine.

## What "five green, three red" means

Per Ch 31 §31.4: this is the "normal operating range." Most healthy teams sit here.

The three red tiles in a normal-operating team tend to be (in rough order of commonness):

1. **Predictability red** — story-point variance is high. Common for teams still learning to size with AI involved.
2. **Cost red** — spend is rising faster than the team would like. Routing fix usually closes this.
3. **Lead time red** — review time is the bottleneck, not implementation time. This is the modern bottleneck for AI-assisted teams.

These three being red is a normal mid-rollout state. The "pull the lever" rule from `../quality-decay-signals.md` is specifically about the *quality* signals — not these process signals.

## What "three or more decay signals red for two months" means

Per Ch 31 §31.6:

> Two consecutive months of decay on three or more is a "pull the lever" signal — pause new-team rollout, audit the harness, run a senior-engineer-led code-review-quality review.

This is in [`../quality-decay-signals.md`](../quality-decay-signals.md) in detail. The dashboard surfaces it as a status indicator that turns red when the rule fires:

```
┌──────────────────────────────────────────────────────────────┐
│ Pull-the-lever status: RED                                   │
│ 4 of 6 decay signals trending wrong for 2+ months            │
│   - Mutation score: 76% → 72% → 69% (3-month decay)          │
│   - PR size: 234 → 287 → 312 LOC                             │
│   - Review seconds/line: 3.1 → 2.4 → 1.9                     │
│   - Revert rate: 1.8% → 3.2% → 4.7%                          │
│ Audit owner: <name>                                          │
│ Audit start date: 2026-MM-DD                                 │
│ Held autonomy ceiling: L2 (no new-team rollout)              │
└──────────────────────────────────────────────────────────────┘
```

The dashboard tile links to the runbook page where the audit's status, owner, and action items are tracked.

## The dashboard hierarchy

Three levels of dashboard, each with the same six metrics but different aggregation:

### Level 1: per-team dashboard

- The six metrics for one team
- The team's pull-the-lever status
- Drill-down into specific PRs / engineers (for coaching, not ranking)
- Updated daily (most signals) / weekly (mutation, surveys)

### Level 2: org rollup dashboard

- Each team's tiles in a small-multiples grid
- Comparison across teams (range and median, never per-engineer)
- Roll-up "pull the lever" indicator (any team yellow → org yellow)
- Updated weekly

### Level 3: executive dashboard

- The eight-tile layout from Ch 31 §31.4
- One number per tile, with sparkline
- Adoption / cost / speed / quantity / quality / maturity / predictability / slop alerts
- Updated monthly; reviewed in the monthly engineering review

## What this dashboard will NOT do

- Will not tell you whether to roll out AI to a new team. That's a judgment call informed by the dashboard.
- Will not catch every kind of regression. The leading indicators in [`../quality-decay-signals.md`](../quality-decay-signals.md) are the early-warning layer.
- Will not work without a baseline. See [`../baseline-measurement-template.md`](../baseline-measurement-template.md).
- Will not survive the "all green" trap if the grader isn't validated.

## Companion artifacts

- [`README.md`](README.md) — the six-metric index
- [`metric-01-token-usage.md`](metric-01-token-usage.md) through [`metric-06-predictability.md`](metric-06-predictability.md) — individual metric specs
- [`../quality-decay-signals.md`](../quality-decay-signals.md) — the leading indicators that pair with the lagging dashboard
- [`../code-maturity-rubric.md`](../code-maturity-rubric.md) — the rubric for metric #2
- Ch 31 §31.1, §31.4, §31.6, §31.7 — sources
