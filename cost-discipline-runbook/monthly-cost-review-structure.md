# Monthly Cost Review Structure

The monthly meeting that surfaces patterns before they become problems. Per Ch 31 §31.4 (the reference executive dashboard) and Ch 29 §29.5 (budget guardrails).

## Why monthly

Daily review is too operational; quarterly review is too retrospective. Monthly is the cadence that catches:
- Drift in model routing (a new pattern emerged)
- Drift in team budgets (the team is consistently over or under)
- Drift in cost-per-PR (something has changed in the team's work)
- Vendor cost changes (pricing shifts, tokenizer changes)

Monthly is also aligned with most companies' financial cadence.

## Who attends

Core attendees:
- Engineering leadership (VP, director)
- Platform team lead (the team that owns the cost infrastructure)
- Each team's EM (or rotating; not all every month for large orgs)
- Finance / FP&A representative (not every month, but at least quarterly)

Optional attendees:
- Senior platform engineer (for technical drill-downs)
- Specific team lead when their team is the focus

Not in scope: the meeting is operational, not strategic. The CTO doesn't routinely attend; quarterly review is when the broader strategic conversation happens.

## Cadence

Monthly. 60-90 minutes. Specific day of the month so it's predictable (e.g., the second Tuesday).

## Agenda

### Section 1 — Overall trajectory (10 minutes)

The platform team presents:

- **Total spend this month vs last 3 months** (graph)
- **Spend vs budget** (org-wide and per-team summary)
- **Per-team cost-per-merged-PR** (rolling 30-day)
- **Model mix overall** (% Haiku / Sonnet / Opus)
- **Anomalies and incidents this month** (count, severity, root causes)

What the data should show:
- Spend trajectory matches expectations
- No team is significantly over budget without conversation
- Model mix is healthy (~70-80% Sonnet, ~10-15% Haiku, ~5-10% Opus)
- No unaddressed anomalies

### Section 2 — Per-team review (30-45 minutes)

For each team (or 3-4 teams in rotation):

- **Cost vs budget**
- **Cost-per-merged-PR vs team's median**
- **Model mix**
- **Top 5 PRs by cost this month** — for outlier review
- **Pattern observations from the EM**

The EM speaks to:
- Anything explaining the cost (new project, scope shift, team change)
- Patterns observed (routing wins, routing issues, training opportunities)
- Asks of platform / leadership

### Section 3 — Cross-cutting patterns (10-15 minutes)

The platform team or VP raises:

- **Vendor changes that affect cost** (model pricing, tokenizer changes, contract terms changes)
- **Routing patterns to celebrate or address** ("Team A's Haiku usage is great; Team B might benefit")
- **Tooling improvements** (gateway changes, dashboard improvements, alerting tuning)
- **Cost incidents** (any blowups; root causes; harness improvements)

### Section 4 — Decisions and next steps (10-15 minutes)

The meeting produces:

- **Specific budget changes** (if any)
- **Specific routing or tooling changes** (if any)
- **Specific follow-up conversations** (1:1s the EM should have)
- **Items for the quarterly leadership review** (not for this meeting)

Notes captured. Decisions logged. Next meeting on the calendar.

## What good monthly review looks like

A healthy month:
- Spend within 10% of budget
- All teams within 20% of budget
- No anomaly incidents
- Model mix in the healthy range
- Cost-per-PR stable or trending down with throughput stable or up

A concerning month:
- 2+ teams over budget by >20%
- Anomaly incidents that produced significant unexpected spend
- Model mix shifting (Opus share climbing without justification)
- Cost-per-PR climbing without scope explanation

A crisis month:
- Org over budget by >20%
- Major cost incident
- Vendor pricing change without prior knowledge
- Team budgets meaningfully misaligned with reality

## Common patterns that surface

### Pattern: One team driving most growth

Often a team that's adopted AI tooling more aggressively. Investigation:
- Is the adoption producing throughput gains? (good)
- Is the routing healthy? (good if Sonnet-dominant; concerning if Opus-heavy)
- Is the cost-per-merged-PR converging or diverging from the org? (converging is fine; diverging needs investigation)

### Pattern: Spend climbing during a model migration

A new model has been released; the team is using it. Cost climbs because:
- New tokenizer (per Ch 29 §29.6) — typically 10-30% effective cost increase
- Engineers exploring the new model's capabilities — temporary
- Routing not updated — fixable

### Pattern: Persistent outlier engineer

One engineer consistently in the 95th percentile of cost. Investigation:
- Is the work warranting the spend? (some engineers do high-stakes work)
- Routing issue? (Opus on routine tasks)
- Workflow issue? (long-running sessions; context bloat)

The conversation is in 1:1, not in the monthly review. The review surfaces; the manager handles.

### Pattern: Cost climbing while throughput is flat

The leverage isn't appearing. Per Ch 29 §29.7's executive decision framework:
- What problem are we solving?
- What's the baseline metric and the goal?
- Are we tracking against the goal?
- Rollback if the metric doesn't improve in 90 days?

This pattern triggers the "is the AI investment paying off" conversation at quarterly leadership review.

### Pattern: A team's spend dropped significantly

Sometimes a positive sign (better routing); sometimes a negative one (engineers giving up on AI tooling). Investigation:
- Is throughput maintained or improved?
- Are engineers actively using the tooling?
- Is the team blocked on something the platform team should address?

## Documentation discipline

After each monthly review:

1. **Notes captured** in a shared doc; previous months remain available
2. **Decisions logged** with owner and date
3. **Action items tracked** to closure (next meeting reviews status)
4. **Quarterly trends compiled** for the leadership review

## Anti-patterns

### Cost theater

The meeting is performative. Numbers are presented; no decisions are made. The next month is the same.

Mitigation: the meeting must produce specific decisions. If a meeting doesn't, that's its own discussion item.

### Blame culture

The review surfaces individual engineers' high spend. The conversation becomes about who's "wasting" money. Engineers learn to hide usage (route around the gateway, use personal accounts, etc.).

Mitigation: the review is operational. Individual conversations happen in 1:1s. The meeting is about patterns and team-level decisions.

### Avoiding the hard conversation

The team is consistently over budget. The EM doesn't raise it because "we'll fix it." The review skips the team. Three months later it's a budget crisis.

Mitigation: the review covers all teams in rotation; persistent over-budget teams are explicitly discussed.

### Reviewing without action

The review surfaces patterns; the actions don't ship. Engineers and leadership lose trust in the review.

Mitigation: action items are tracked to closure. If a previous month's action item isn't done, it's escalated in the current meeting.

### "We don't have data"

The review is canceled because the data isn't ready. The next month, same problem.

Mitigation: data collection is the platform team's responsibility; it must be reliable. If it's not, that's the highest-priority discussion item until fixed.

## What this structure will NOT do

- Will not work without instrumentation. Per Ch 29 §29.3, telemetry is the prerequisite.
- Will not work without leadership engagement. The review only matters if leadership cares about the discipline.
- Will not catch every cost issue. Anomaly detection is the protection layer; the monthly review is for patterns.
- Will not eliminate the leadership conversation about cost vs value. The monthly review is operational; the strategic conversation is quarterly.

## Companion artifacts

- [`token-budgets-by-team.md`](token-budgets-by-team.md) — what the review tracks against
- [`anomaly-detection-workflow.md`](anomaly-detection-workflow.md) — the protection layer between reviews
- [`leadership-conversation-on-cost.md`](leadership-conversation-on-cost.md) — quarterly strategic conversation
- [`cost-blowup-incident-runbook.md`](cost-blowup-incident-runbook.md) — when something happens between reviews
- Ch 29 §29.4-§29.7, Ch 31 §31.4 — sources
