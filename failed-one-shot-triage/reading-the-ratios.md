# Reading the Ratios

What the ratios mean over time and what to do about them. Per Ch 31 §31.5:

> The ratios over time are the team's harness-maturity signal. A team that is improving will see Train and Opportunity counts fall over months as PMs sharpen and harnesses fill in gaps. Question counts fall stepwise when new models drop. Score counts rise. A team that is stagnating sees the same Train/Opportunity mix month after month — usually because nobody is closing the loop on the failures.

This file is the operational guide to interpreting the trend data.

## The healthy trajectory

A team that's working well shows, over 3-6 months:

- **Score share rises**: from ~50-70% in early adoption to ~80-90% in mature operation
- **Train share falls**: PMs are getting sharper; the assistant is helping
- **Opportunity share falls**: harness gaps are being closed
- **Question share holds steady or falls stepwise** with model releases

The shape:

```
Month 1:  Score 50% | Train 25% | Opportunity 20% | Question  5%
Month 3:  Score 65% | Train 18% | Opportunity 13% | Question  4%
Month 6:  Score 78% | Train 10% | Opportunity  8% | Question  4%
Month 12: Score 85% | Train  6% | Opportunity  5% | Question  4%
```

This is what working harness investment looks like over time. The Train and Opportunity declines are the team's improvement signal.

## The stagnating trajectory

A team that's not improving shows the same ratios month after month:

```
Month 1:  Score 50% | Train 25% | Opportunity 20% | Question  5%
Month 3:  Score 50% | Train 25% | Opportunity 20% | Question  5%
Month 6:  Score 50% | Train 25% | Opportunity 20% | Question  5%
```

Per Ch 31 §31.5: "usually because nobody is closing the loop on the failures."

If the ratios aren't moving, ask:
- Is the triage actually running?
- Are Opportunity tickets being shipped?
- Is Train coaching actually happening?
- Is the team's harness investment time being protected?

Stagnation is a leadership signal. The discipline isn't producing improvement.

## Diagnostic patterns

Per Ch 31 §31.5, the bucket distribution diagnoses the team's specific issue.

### Mostly Train (>50% of failures)

The issue is Direction (Ch 5). Specs are vague, contradictory, or incomplete.

What to do:
- PM coaching becomes the highest-leverage activity
- Implement the ticket-writing assistant pattern (per Ch 19 §19.5)
- Review the team's spec template; is it sufficient?
- Check whether engineers are writing specs ad-hoc rather than using the template

### Mostly Opportunity (>50% of failures)

The issue is Architecture/Legibility (Part II). The harness is missing context the agent needs.

What to do:
- Allocate explicit time for harness investment (skills, AGENTS.md, fixtures)
- Per `platform-team-charter/`, the platform team's roadmap should reflect this
- Survey engineers: what harness improvements would have prevented their last 5 failures?
- Quarterly harness audit (per `ai-readiness-audit-walkthrough/`)

### Mostly Question (>50% of failures)

The issue is model selection or scope mismatch (Ch 26). The team is asking the model to do work it can't do, or using the wrong model for the work.

What to do:
- Quarterly model lineup review (per `evals-and-benchmarks-runbook/quarterly-model-lineup-review.md`) — possibly out of cycle
- Routing rubric audit (per `cost-discipline-runbook/model-routing-rubric.md`) — are the right work types going to the right models?
- Capability boundary review — are some work types being attempted that should be human-only per `do-not-automate-catalog/`?

### Mostly Score (>80% of work)

The system is working for that work type. Per Ch 31 §31.5:

> Mostly Score: invest the saved time in raising the autonomy ceiling for that work type (Chapter 32, 44).

What to do:
- Per `agent-autonomy-levels/raising-and-lowering-autonomy.md`, the conversation about raising autonomy is on the table
- The Score data is the evidence that supports the raise
- Specific work types with high Score rates may be candidates for L4 (auto-merge) per `agent-autonomy-levels/autonomy-ladder.md`

## Sub-pattern reading

The aggregate ratios are useful; sub-patterns are more useful.

### Train concentrated in one PM

The team's overall Train rate is 25%. Drilling in: 80% of Train failures came from one PM.

Diagnosis: that PM needs coaching specifically; the rest of the team is fine.

Action: 1:1 coaching with that PM (private). General PM training stays on track.

### Opportunity concentrated in one module

The team's overall Opportunity rate is 20%. Drilling in: 70% of Opportunity failures came from work in the billing module.

Diagnosis: the billing module's harness is specifically thin.

Action: dedicated billing-legibility sprint. Improve AGENTS.md, add fixtures, document conventions.

### Question concentrated in one work type

The team's overall Question rate is 8%. Drilling in: 90% of Question failures came from cross-system reasoning tasks.

Diagnosis: the model is consistently struggling with that specific capability.

Action: route cross-system reasoning to humans for now. Re-test on next model release. Consider Opus for that work type until the gap closes.

### Question that doesn't reduce after model upgrade

A new model dropped. Question rate didn't fall. Per Ch 31 §31.5, "Question counts fall stepwise when new models drop."

Diagnosis: the new model isn't substantially better for this team's work — or the team's Question failures are deeper than model capability (architectural complexity, undocumented constraints).

Action:
- Verify with the internal benchmark (per `evals-and-benchmarks-runbook/`)
- If benchmark agrees: the new model isn't better; routing decisions stay
- If benchmark disagrees: the work-classification might be wrong; what's labeled Question may actually be Opportunity in disguise

## Reading at different time scales

### Weekly

Looking at week-over-week is mostly noise. Don't over-react. A bad week doesn't mean the trajectory is bad.

What to look at weekly:
- Specific failures and their resolutions
- Patterns within the week (multiple failures on the same module)

### Monthly

Monthly aggregation starts to reveal trends.

What to look at monthly:
- Ratios are moving in the expected direction
- Patterns surfacing across multiple weeks
- Specific harness investments showing up in the data

### Quarterly

Quarterly is where the real signal lives.

What to look at quarterly:
- Score share trajectory (is it climbing?)
- Train and Opportunity trajectory (are they falling?)
- Question stepwise reductions (did the new model help?)
- Cost-per-PR (cross-reference with `cost-discipline-runbook/cost-attribution-per-pr.md`)
- Defect rate (cross-reference with the broader metrics)

## When the data conflicts

Sometimes the ratios suggest one thing; the team's experience suggests another. E.g., Score share is high but engineers feel like they're spending more time on review than building.

Reconcile:
- The Score data captures successful merges; doesn't capture review time
- High Score rate with rising review fatigue is a `reviewer-burnout-mitigation/` issue, not a triage issue
- The triage data is one signal among many; the team's qualitative experience matters too

## Anti-patterns

### Reading the ratios without acting

The team tracks ratios; nobody changes anything based on them. The data is informational.

Mitigation: per [`closing-the-loop.md`](closing-the-loop.md), each bucket has a resolution path. The data drives action.

### Reading the ratios punitively

The data is used to argue for cuts ("the AI is failing 40% of the time; it's not working"). Stops the discipline.

Mitigation: the data is diagnostic. Failure rate isn't the metric; trend over time is.

### Reading the ratios in isolation

The ratios are interpreted without context (cost data, defect rate, throughput).

Mitigation: cross-reference with other metrics. Per Ch 31, the seven metrics work together.

### Reading the ratios at the wrong cadence

Looking weekly for trend signal: too noisy. Looking quarterly for tactical signal: too slow.

Mitigation: weekly for tactical, monthly for short-term trend, quarterly for strategic.

### Comparing ratios across teams

Team A has 80% Score; Team B has 60% Score. Conclusion: Team B is worse. Often wrong.

Mitigation: teams have different work distributions. A team doing more T3 work has lower Score by design. Compare same-work-type ratios, not aggregate.

## Companion artifacts

- [`the-four-buckets.md`](the-four-buckets.md) — the taxonomy
- [`triage-process.md`](triage-process.md) — how the data is generated
- [`tracking-spreadsheet-template.md`](tracking-spreadsheet-template.md) — the data structure
- [`closing-the-loop.md`](closing-the-loop.md) — what's done about each bucket
- `cost-discipline-runbook/cost-attribution-per-pr.md` — adjacent metric
- `evals-and-benchmarks-runbook/` — adjacent (Question failures inform model selection)
- Ch 31 §31.5 — source
