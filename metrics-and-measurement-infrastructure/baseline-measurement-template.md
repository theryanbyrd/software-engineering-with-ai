# Baseline Measurement Template — Pre-Rollout Capture

The discipline that makes everything else in this directory work. Without a pre-AI baseline, you have no defensible comparison — no A/B read, no "is the rollout helping" answer, no defensible response to the board's question at month 4.

Per the framing in Ch 31 §31.6:

> The CEO who is asking for proof at month 4 will get a defensible answer if you set this up at month 1; they will not get a defensible answer if you set it up the week they ask.

This file is the operational template for "setting this up at month 1." Specifically: the metrics you capture, the methodology, the timing (4 weeks pre-rollout), the survey instrument, and where the data lives.

## Why this matters

The most common mistake in AI rollout measurement is starting the measurement on rollout day. Once AI is in the team's hands:

- You can't measure what work was like *without* AI — engineers can't reliably self-report
- Your post-AI metric numbers have no comparison
- You can't distinguish "lead time improved by 15%" from "lead time was always 15% better in Q2 than Q1" — there's no controlled comparison

The fix is mechanical: capture metrics for 4 weeks (minimum) before AI tooling lands. Then compare.

## When to do this

Per Ch 31 §31.6's A/B framework, similar baselines for the prior 90 days are a *criterion* for picking the comparison pair. The 4-week minimum here is a floor; the more baseline data you have, the more defensible the comparison.

| Timeline | What you have |
|---|---|
| 0 weeks of baseline | Vibes |
| 2 weeks of baseline | Plot exists; trend is meaningless |
| 4 weeks of baseline | Minimum defensible; trend can be discussed cautiously |
| 8 weeks of baseline | Solid; trend is reliable |
| 13 weeks (one quarter) | Strong; this is what Ch 31 §31.6 calls for in the A/B framework |
| 26 weeks (two quarters) | Excellent; can detect seasonal effects |

**Start the baseline 4 weeks before the rollout if you're in a rush.** Start 13 weeks before if you have the runway. Start *now* even if rollout is months out.

## What to capture

The baseline must capture every metric the post-rollout dashboard will surface. Specifically:

### From [`six-metric-dashboard/`](six-metric-dashboard/)

| # | Metric | Baseline method |
|---|---|---|
| 1 | AI Token Usage per Developer | Not applicable pre-AI; baseline is zero |
| 2 | Code Maturity Score (1–10) | Run the LLM grader on the prior 90 days of PRs; establish the pre-AI mean per team |
| 3 | Features Delivered / Bugs Introduced | Pull the last 90 days from the story tracker; compute monthly |
| 4 | Time from Story to Production | Pull the last 90 days of stories; compute median lead time per team |
| 5 | Story Points Delivered | Pull velocity for the last 6 sprints per team |
| 6 | Predictability — 1 − (σ/µ) | Compute from #5 + commitments for the last 6 sprints |

### From [`quality-decay-signals.md`](quality-decay-signals.md)

| Signal | Baseline method |
|---|---|
| Mutation score | Run mutation tests on a representative module; establish per-module baseline |
| PR size (median, p90) | Pull last 90 days of merged PRs; compute |
| Review-time-per-line | Pull last 90 days; compute |
| Revert rate | Pull last 90 days; count reverts; compute % |
| Customer-reported defects | Pull last 90 days from support tracker |
| Senior 1:1 culture concerns | Survey now (see template below); establish baseline response rate |

### From [`ab-testing-framework.md`](ab-testing-framework.md)

| Field | Method |
|---|---|
| Lead time on T2 tickets specifically | Pull last 90 days; compute median per team |
| PR review time per merged PR | Already captured above |
| Change failure rate | Pull last 90 days; compute per team |
| Developer satisfaction baseline | Run the weekly survey for 4 weeks pre-rollout |

## The baseline survey instrument

A specific instrument to run pre-rollout. The structure:

### Survey 1: Engineer survey (weekly during baseline)

**Audience:** every engineer on the team
**Cadence:** weekly, for 4+ weeks
**Length:** 2 minutes
**Anonymity:** optional (engineer-by-engineer toggle); manager sees aggregates only

```markdown
# Weekly Engineering Pulse (Baseline)

## How would you rate your week, 1–5?
1 = bad, 5 = great
[ ] 1  [ ] 2  [ ] 3  [ ] 4  [ ] 5

## What was the biggest blocker this week?
[free text, 1-2 sentences]

## What % of your time was spent on:
- Implementation:  ___ %
- Code review (yours or others'):  ___ %
- Meetings:  ___ %
- Investigation / debugging:  ___ %
- Documentation:  ___ %
- Other:  ___ %

## Have you used AI coding tools in the past week?
[ ] No, I don't use any AI coding tools
[ ] Yes, for autocomplete (Copilot, Codeium, similar)
[ ] Yes, for chat/Q&A (ChatGPT, Claude.ai)
[ ] Yes, for agentic work (Claude Code, Cursor agent, Cline)

## (Optional) Any other observations?
[free text]
```

The "Have you used AI coding tools" question is critical for the baseline. Most teams have *some* informal AI usage pre-rollout (engineers using personal Claude or ChatGPT accounts). The baseline isn't "zero AI"; it's "the team's current informal AI usage." Capture it.

### Survey 2: Senior engineer culture survey (one-time pre-rollout, then monthly)

**Audience:** Staff+ engineers
**Cadence:** one-time at baseline; monthly thereafter (per [`quality-decay-signals.md`](quality-decay-signals.md) signal 6)
**Length:** 10 minutes
**Anonymity:** mandatory

```markdown
# Senior Engineer Culture Baseline

## Current quality observations

### On a scale of 1–5, how would you rate:
- The team's code quality currently:  ___
- The team's test discipline currently:  ___
- The team's review thoroughness currently:  ___
- The team's spec quality currently:  ___

## What patterns of concern are you seeing now?

(If none, write "none.")

[free text, up to 200 words]

## What patterns would you specifically want to track if AI tooling rolls out?

[free text, up to 200 words]

## What would change your confidence in the team's quality?

[free text, up to 200 words]
```

This establishes the senior-engineer concern baseline. If 2 of 5 senior engineers raise a concern about test discipline at baseline, that's the baseline — not "0 concerns." Post-rollout, you're tracking *change from baseline*, not "any concerns at all."

### Survey 3: Manager observation log (one-time at baseline)

**Audience:** engineering managers
**Cadence:** one-time at baseline; quarterly thereafter
**Anonymity:** by team (manager sees their team; VP sees rolled up)

```markdown
# Engineering Manager Baseline Observations

For each team you manage, capture:

## Current state assessment

- Team size: ___ engineers
- Seniority mix: ___ staff / ___ senior / ___ mid / ___ junior
- Product surface: [consumer / internal / infrastructure / mixed]
- Primary stack: [language(s); framework(s)]

## Process baseline

- Typical sprint length: ___ weeks
- Typical commitment per sprint: ___ points
- Typical delivery per sprint (last 6 sprints): ___ points
- Predictability score (1 − σ/µ): ___

## Pain points

What are your team's top 3 process pain points today, in your judgment?

1. ___
2. ___
3. ___

## Expected AI impact

Where do you expect AI tooling to help most, and where to help least?

[free text]
```

The "expected AI impact" question creates a pre-registered prediction. At day 90, you compare actual impact to predicted impact. This is a useful discipline — managers who predict accurately get more leeway in subsequent decisions; managers whose predictions miss systematically have a calibration issue to address.

## Where the baseline data lives

The data needs a permanent home. Options in rough order of preference:

| Storage | Pros | Cons |
|---|---|---|
| The metrics warehouse (BigQuery, Snowflake, Redshift) | Survives team / tool / vendor changes; queryable | Setup overhead |
| Git-versioned files in this repo (`baseline/`) | Version-controlled; accessible to engineers | Doesn't scale to live metrics |
| A dedicated Grafana dashboard with persistent data store | Visualization; queryable | Requires the data store |
| A spreadsheet (Google Sheets, Excel) | Easy; everyone can read it | Data quality degrades; gets lost |

The baseline should be in *at least two* of the above. The warehouse holds the data; the dashboard renders it; the repo holds the survey responses and the documentation of the methodology.

A reference directory structure:

```
metrics-and-measurement-infrastructure/
├── baseline/
│   ├── README.md                ← this file's instructions, repeated here for self-containment
│   ├── methodology.md           ← the team's actual methodology (start from this template)
│   ├── data/
│   │   ├── pr-data-baseline.csv      ← 90-day PR pull
│   │   ├── story-data-baseline.csv   ← 90-day story pull
│   │   ├── revert-data-baseline.csv  ← 90-day revert pull
│   │   └── survey-responses/         ← anonymized survey data
│   ├── reports/
│   │   ├── baseline-summary.md       ← the rolled-up numbers
│   │   └── senior-engineer-survey.md ← the qualitative baseline
│   └── code-maturity-gold-set/
│       ├── README.md                 ← the 50-PR validation set
│       └── (graded sample data)
```

## Who runs it

The roles:

| Role | Responsibility |
|---|---|
| **VP of Engineering** | Sponsor; commits the team to the baseline period; sets expectations with the business |
| **Engineering Manager** | Runs the surveys; ensures team participation; captures qualitative observations |
| **Platform Engineer** | Builds the data extraction; sets up the dashboards; owns the pipeline |
| **Tech Lead / Senior Engineer** | Runs the LLM grader gold-set validation; reviews the baseline numbers for plausibility |
| **PM (data-curious)** | Pulls the story-tracker data; defines "T2" consistently with how the post-rollout metric will count |
| **HR / People Ops** | Reviews the survey for compliance with employee-data policies; ensures anonymity holds |

The "HR reviews for compliance" step is sometimes skipped in startups. Don't skip it. Survey data — especially the weekly pulse — must be handled per your jurisdiction's employee-data rules.

## A timeline for the baseline period

The recommended 8-week baseline plan:

| Week | Activity |
|---|---|
| -8 to -7 | Set up data extraction; verify metric definitions; build the dashboard |
| -7 | Run LLM grader on 50-PR gold set; complete the validation procedure |
| -6 | Launch weekly engineer pulse survey; first week of data |
| -6 | Run senior engineer culture survey one-time |
| -5 to -1 | Continue weekly pulse; quarterly metric pulls; nothing else changes |
| Day 0 | AI tooling lands |
| Day 7 | Continue all measurement; first post-rollout snapshot |
| Day 30 | Interim read |
| Day 60 | Interim read |
| Day 90 | Full A/B read (per [`ab-testing-framework.md`](ab-testing-framework.md)) |

## What to capture in the baseline report

The artifact you produce at the end of the baseline period:

```markdown
# Baseline Report — Engineering Metrics, Pre-AI Rollout

## Period
From [date] to [date], inclusive

## Teams included
- Team A: [name], [N] engineers, [stack], [product surface]
- Team B: [name], [N] engineers, [stack], [product surface]

## Quantitative baseline

| Metric | Team A | Team B |
|---|---|---|
| Median lead time (T2) | X days | Y days |
| Median PR size | X LOC | Y LOC |
| Median PR review time | X hours | Y hours |
| Median seconds-per-line on review | X sec | Y sec |
| Revert rate (30-day) | X % | Y % |
| Mutation score (representative module) | X % | Y % |
| Velocity (6-sprint avg) | X points | Y points |
| Predictability (1 − σ/µ) | 0.XX | 0.XX |
| Code maturity score (90-day mean) | X.X | Y.Y |
| Features / bugs ratio (90 days) | X.X | Y.Y |

## Qualitative baseline

### Engineer pulse (4 weeks)
- Average weekly rating: X.X/5
- Top reported blocker: [aggregated text]
- Time allocation: [implementation/review/meetings/...]
- Informal AI usage: X% of engineers report some form

### Senior engineer concerns
[Aggregated themes from survey 2]

### Manager observations
[Per-team summaries from survey 3]

## Predictions (pre-registered)

[The managers' predicted impacts, captured before rollout]

## Plan
- Rollout date: [date]
- A/B test design: [link to ab-testing-framework.md]
- Day 30 / 60 / 90 read schedule: [dates]
- Decision criteria: [criteria for broader rollout decision]
```

This artifact is what makes the post-rollout claim defensible. The version-controlled, dated, signed-off baseline report — produced before AI lands — is the evidence that the comparison is real.

## Anti-patterns to avoid

### "We'll start measuring after rollout starts"

The mistake that makes all subsequent measurement meaningless. The baseline has to happen *before* the rollout. If the rollout has already started, the closest defensible thing is to delay the AI for one team (a control) and use that team for a retroactive A/B per the framework.

### Measuring only the easy things

The trap: lead time and velocity are easy to pull; mutation score and code maturity require setup. The team measures only the easy ones at baseline. Post-rollout, the missing metrics start fresh — and you have no baseline for the things that matter most.

Mitigation: do the LLM grader validation and the mutation test setup *before* rollout starts. Yes, it's slow. Yes, it's the work that pays off.

### Skipping the senior-engineer culture survey

The trap: this signal feels soft and qualitative; engineering leaders skip it. Six months in, when signal #6 ("senior engineers reporting concerns") fires, there's no baseline to compare against. Was this concern level present before AI? Unknown.

Mitigation: run it. The 10-minute survey gives you the comparison point that no other instrument provides.

### Pulling baseline data from the wrong period

The trap: pulling the 90 days that happened to include holidays, an incident, or a reorg. The baseline is distorted; everything that follows compares against a distorted reference.

Mitigation: when pulling baseline data, check for: holiday weeks (reduced capacity); known incidents (P0/P1 in the period); reorgs or team-composition changes; product launches (different work mix). Note them in the baseline report; consider extending the window to dilute them.

### Letting the baseline "drift" through the rollout

The trap: the baseline is set on day 0, then never re-examined. Six months later, the comparison point is stale — the codebase has evolved, the team has changed, the product surface has shifted. The "baseline" is from a different reality.

Mitigation: re-baseline annually. The Q1 baseline drives the year's comparisons; the next Q1 sets the new baseline. Trends across multiple baselines reveal multi-year patterns.

### Not anonymizing the survey data

The trap: engineers don't trust the survey; response rate is 30%; the data is biased toward the most engaged engineers. The baseline is wrong from the start.

Mitigation: anonymize from the start; have HR review; communicate the anonymity to engineers in writing.

## What this baseline will NOT do

- Will not work if started after rollout. The whole point is "before."
- Will not work without management commitment to the 4-week minimum (and ideally 8 weeks). Compressed baselines produce noise, not data.
- Will not survive a culture where engineers think they're being measured punitively. The survey is a feedback loop; if it's read as surveillance, response rates collapse.
- Will not replace ongoing measurement. The baseline is the starting line; the dashboard is the race.
- Will not produce useful data without metric-definition discipline. "Lead time" must mean the same thing in baseline and post-rollout.

## Companion artifacts

- [`README.md`](README.md) — the directory index
- [`six-metric-dashboard/`](six-metric-dashboard/) — what gets measured ongoing
- [`quality-decay-signals.md`](quality-decay-signals.md) — the leading indicators that need their own baseline
- [`code-maturity-rubric.md`](code-maturity-rubric.md) — the validation procedure that pairs with this baseline
- [`ab-testing-framework.md`](ab-testing-framework.md) — what the baseline feeds
- `../benchmarks/` — adjacent regression-test discipline
- Ch 31 §31.6 — source
