# Detecting Burnout Symptoms

The five symptoms from Ch 44 §44.5 and how to spot them. Most managers don't realize they have a burnout situation until it's well-developed; this file is the early-warning system.

## The five symptoms (Ch 44 §44.5 verbatim)

1. The same two or three names on most reviews.
2. Review queue depth growing week-over-week.
3. Reviewers reporting fatigue or resentment in 1:1s.
4. Reviewers Slack-DMing approvals to skip the public discussion.
5. Senior engineers mentioning craft loss or culture decay.

## Symptom 1 — Same two or three names on most reviews

### What it looks like

Pull the review data: who reviewed PRs in the last 30 days? Order by count. The top 2-3 reviewers do the bulk of the work.

Specific signals:
- Top 2 reviewers do >50% of reviews
- Top 3 reviewers do >70% of reviews
- The team has 8-10 engineers but reviews concentrate on 2-3

### Why it matters

The hot reviewer pattern. A few engineers become the unofficial gatekeepers. They review faster (because they review more) and become trusted (because they review faster). The cycle reinforces.

The team becomes dependent on those 2-3 people. If any of them takes vacation, leaves, or burns out, review capacity collapses.

### How to detect

- GitHub / GitLab review data: count reviews per engineer per month
- Threshold: if top 2 do >50% or top 3 do >70%, hot reviewer pattern is present
- Trend: is the concentration growing or shrinking over time?

### Mitigations

Round-robin assignment (per [`mitigation-3-round-robin-assignment.md`](mitigation-3-round-robin-assignment.md)). Forces distribution.

## Symptom 2 — Review queue depth growing

### What it looks like

The number of open PRs awaiting review grows over time. Some PRs sit for days; some sit for a week or more.

Specific signals:
- Average time-to-first-review trending up
- Median time-to-merge trending up
- Number of PRs pending review > number of engineers on the team
- "Stuck" PRs that haven't received review in 5+ business days

### Why it matters

Review queue depth is the leading indicator of burnout. When the queue grows, reviewers feel the pressure. They start cutting corners — quick reviews, trust-based reviews, or skipping reviews entirely.

A growing queue isn't always burnout — could be:
- Increased PR volume (which is the AI tooling effect)
- Reviewer absences (vacation, sick leave)
- A specific large change being prioritized

But sustained growth (3+ weeks of climbing) is a burnout signal.

### How to detect

- Track open-PR count weekly
- Track time-to-first-review and time-to-merge
- Plot trends; flag when curves go up for 3+ weeks consecutively

### Mitigations

Multiple mitigations apply: AI reviewer subagent (per [`mitigation-1-ai-reviewer-subagent.md`](mitigation-1-ai-reviewer-subagent.md)) reduces per-PR time; round-robin distributes load; PR size limits reduce per-PR cognitive cost; throughput cap reduces total volume.

## Symptom 3 — Fatigue or resentment in 1:1s

### What it looks like

In 1:1s, senior engineers mention:
- "I'm tired of reviewing"
- "I spent my whole afternoon on PRs"
- "I never get to my own work"
- "I'm doing all the reviews on this team"

Sometimes more subtle:
- The senior engineer's own PR throughput drops (their time is consumed by review)
- They mention specific reviewers who aren't pulling weight
- They mention specific PRs that took disproportionate time

### Why it matters

This is the qualitative signal that the quantitative metrics support. By the time engineers are openly expressing fatigue, the situation is well-developed.

Some engineers express it directly; others don't (especially senior ICs who feel "this is my job"). Managers need to ask, not just listen.

### How to detect

- Ask specifically in 1:1s: "How's your review load these days?"
- Ask: "What's taking the most of your week?"
- Listen for indirect signals (mentions of working late on review; mentions of specific PRs that consumed days)

### Mitigations

The whole set. The mitigation that addresses fatigue specifically: throughput cap (per [`mitigation-6-throughput-cap.md`](mitigation-6-throughput-cap.md)) reduces volume; review office hours (per [`mitigation-4-review-office-hours.md`](mitigation-4-review-office-hours.md)) bounds the time.

## Symptom 4 — Reviewers Slack-DMing approvals

### What it looks like

Reviewers approve PRs without leaving a public comment. The PR shows "approved by X" but X's reasoning isn't documented. Discussion that should happen in PR comments happens in DM.

Specific signals:
- PRs merged with approvals but no review comments
- Discussion threads that disappear into DMs
- "Don't worry, I already talked to them about it" statements

### Why it matters

This is reviewers cutting corners to manage their load. It's understandable and rational from the reviewer's perspective; it has organizational costs:

- Knowledge isn't shared across the team
- Patterns the reviewer caught aren't visible to other reviewers
- Future engineers can't learn from the discussion
- The PR record loses substance (audit, postmortem, customer review)

### How to detect

- Spot-check approved PRs: how many have substantive review comments?
- Watch for "approved without comment" patterns
- Talk to reviewers (not in a gotcha way): "I noticed your PR was approved without comment; are you skipping the public discussion?"

### Mitigations

This symptom is mostly a behavior signal, not a process problem. The mitigations:
- Make review work visible (per [`mitigation-5-review-work-visibility.md`](mitigation-5-review-work-visibility.md)) — recognition matters
- Reduce the load (everything else) so reviewers don't feel pressure to cut corners

## Symptom 5 — Craft loss or culture decay

### What it looks like

Senior engineers mention things like:
- "We used to review more carefully"
- "Code quality has been slipping"
- "I don't recognize this codebase"
- "We don't have the bar we used to have"

Sometimes more pointed:
- "I'm thinking about going somewhere that values craft more"
- "This isn't the engineering team I joined"

### Why it matters

This is the late-stage symptom. By the time senior engineers are talking about culture decay, the team has been operating in a degraded state for months.

The risk: senior engineer attrition. Senior engineers have options; if they conclude the culture is gone, they leave. Their loss accelerates the decay (fewer senior reviewers; more burden on those who remain; more decay).

### How to detect

- Listen in 1:1s — open-ended questions
- Watch for engineers reducing their engagement (less proactive PRs; less code review; less mentoring)
- Anonymous surveys can surface the sentiment if direct conversation isn't producing it

### Mitigations

This symptom requires leadership response, not just process changes:
- Acknowledge the issue explicitly
- Communicate the mitigation plan
- Show specific actions and timelines
- Make the platform investment visible (the AI reviewer subagent shipping; the throughput cap rolling out)

If leadership doesn't respond visibly, the senior engineers' assessment is correct, and they leave.

## When two or more symptoms are present

Per the threshold above, two or more symptoms = burnout situation. The recommended response:

1. **Acknowledge in a team forum** (manager or tech lead): "We're seeing reviewer burnout symptoms. Here's what we're doing about it."
2. **Implement mitigations** (start with AI reviewer subagent and PR size limits; highest leverage)
3. **Communicate timeline** for the mitigations to land
4. **Track the symptoms over the next quarter**: are they reducing?

Don't wait until all five symptoms are present. The early-stage mitigations are the cheapest.

## How to track over time

A monthly dashboard for the manager (or platform team):

| Metric | This month | Last month | 3 months ago |
|---|---|---|---|
| **Top reviewer's share of reviews** | 32% | 28% | 24% |
| **Top 3 reviewers' share** | 65% | 60% | 55% |
| **Median time-to-first-review** | 18h | 14h | 12h |
| **Median time-to-merge** | 36h | 30h | 26h |
| **Open PR count (avg)** | 18 | 14 | 10 |
| **Engineers expressing fatigue in 1:1s (count)** | 3 | 1 | 0 |

Trends are what matter. If multiple metrics climb over 3 months, intervene.

## Anti-patterns

### Waiting until symptoms are obvious

By the time engineers are openly complaining, the situation is well-developed. Mitigation is more expensive.

Mitigation: track the leading indicators (queue depth, reviewer concentration) before the lagging indicators (fatigue, attrition).

### Treating symptoms as personality issues

"Engineer X complains a lot" is a story managers sometimes tell themselves. It's usually wrong; engineer X is the canary in the coal mine.

Mitigation: take complaints as data. Investigate the metrics.

### Assuming the AI tooling investment will fix it

Some managers assume that AI tools will reduce review burden over time. Without explicit mitigation, AI tools increase burden (more PRs, same review per PR).

Mitigation: the AI reviewer subagent is the explicit mitigation. Other mitigations are also required.

### Discounting senior engineer concerns

Senior engineers have higher quality bar; they may sound like they're complaining about issues junior engineers don't notice. Their concerns are usually leading indicators.

Mitigation: take senior concerns seriously. They see the system from a different vantage.

### Surveying without action

Anonymous surveys are conducted; results are noted; nothing changes.

Mitigation: surveys produce specific actions on specific timelines. Without follow-through, the survey produces cynicism.

## Companion artifacts

- The six mitigation files (1 through 6)
- `cost-discipline-runbook/cost-attribution-per-pr.md` — adjacent (review minutes is one of the metrics)
- `failed-one-shot-triage/` — adjacent (failed PRs add to review load)
- Ch 44 §44.5 — source
