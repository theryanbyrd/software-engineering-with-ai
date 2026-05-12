# Triage Taxonomy — Score / Question / Opportunity / Train

The seventh metric. Per Ch 31 §31.7:

> The seventh metric — Score/Question/Opportunity/Train triage — lives in retro, not on a dashboard, but it tells you which category of investment to prioritize next.

This file is the measurement-infrastructure view of the taxonomy. The full taxonomy lives in `../failed-one-shot-triage/the-four-buckets.md` — this file focuses on **how the categorization gets logged, what the ratios mean as a metric, and how the categorization improves the harness over time.**

## The four buckets (Ch 19 §19.5)

Per Ch 19 §19.5, verbatim:

> 1. Score — the agent succeeded. Note the tier, the model, the time, the cost. This is your evidence of where the system works.
> 2. Question — the failure is a genuine "jagged edge" of current AI capability. The model can't yet do this kind of work reliably regardless of how good the spec is. Flag it; revisit at the next model release; in the meantime, route this work to humans.
> 3. Opportunity — the failure was caused by a missing piece of the codebase (an undocumented module, a missing fixture, a contract the agent couldn't find). This becomes a legibility ticket: improve the AGENTS.md, add a README, add a fixture, add an ADR. The harness improves; the next attempt at this kind of work succeeds.
> 4. Train — the failure was caused by a slop spec, full stop. The PM didn't articulate what they actually wanted. This becomes a coaching loop: the assistant flags the gap, the PM upgrades the spec, the team's general spec quality rises over time.

Per Ch 31 §31.5:

> The ratios over time are the team's harness-maturity signal. A team that is improving will see Train and Opportunity counts fall over months as PMs sharpen and harnesses fill in gaps. Question counts fall stepwise when new models drop. Score counts rise. A team that is stagnating sees the same Train/Opportunity mix month after month — usually because nobody is closing the loop on the failures.

## Why this is the *seventh* metric, not the first

The six dashboard metrics tell you *what* is happening. This metric tells you *why*. Per Ch 31 §31.5:

> The diagnostic value is worth more than the precise count.

Specifically, the four-bucket distribution is the diagnostic lens for the other six:

- A team with declining maturity score and a Train-heavy triage distribution has a **spec quality** problem
- A team with rising PR size and an Opportunity-heavy distribution has a **harness coverage** problem
- A team with low Score count and a Question-heavy distribution has a **model selection** problem
- A team with rising velocity and a Score-heavy distribution has a **autonomy ceiling** opportunity

The seventh metric tells you which lever to pull when the dashboard turns yellow.

## How to log each bucket

Per Ch 31 §31.5:

> Capture this in the standup or weekly review. Do not bother building elaborate tooling for it; a shared spreadsheet works. The discipline is in the triage itself, not the surface area of the tracking.

The book is direct: don't over-engineer this. A spreadsheet works. The minimum fields per row:

| Field | Description |
|---|---|
| Date | When the agent run happened |
| Issue / PR ID | What the agent was working on |
| Tier (T1 / T2 / T3) | Per Ch 19 §19.5 |
| Model | Sonnet / Opus / Haiku |
| Outcome | Score / Question / Opportunity / Train |
| Time spent | From spec finalized to outcome resolved |
| Cost (tokens / dollars) | Per `../cost-discipline-runbook/cost-attribution-per-pr.md` |
| Notes | One line: what made it work / what was missing / what the spec missed |

For ongoing categorization, see `../failed-one-shot-triage/tracking-spreadsheet-template.md`.

## The bucket → action map

Per Ch 31 §31.5:

> If a team is logging mostly Train failures, the issue is Direction (Chapter 5). If mostly Opportunity, the issue is Architecture/Legibility (Part II). If mostly Question, the issue is model selection or scope mismatch (Chapter 26). Mostly Score: invest the saved time in raising the autonomy ceiling for that work type (Chapter 32, 44).

The operational expansion:

### Score → invest in raising autonomy ceiling

The bucket that confirms the system is working. The action:

- Document what made the work succeed (the spec pattern, the harness, the model choice)
- Use it as a template for similar future work
- Consider raising the autonomy ceiling for this work category, per `../agent-autonomy-levels/raising-and-lowering-autonomy.md`
- Specifically: 30+ consecutive Scores at L2 on a work category is grounds for L3 consideration

### Question → route to humans; revisit at next model release

The bucket that names the model's current limitations. The action:

- Document the specific capability gap (not "the model failed" — the specific failure mode)
- Update the routing table: this work goes to humans for now
- Add a re-test entry for the next model release
- If three or more Questions cluster on a specific work type, that's a routing-table change, not a one-off

### Opportunity → ship harness improvement (legibility ticket)

The bucket that names a specific, addressable harness gap. The action:

- Open a "legibility ticket" per Ch 19 §19.5 (a ticket for the harness, not the product)
- Specific examples:
  - Missing fixture → add the fixture
  - Missing AGENTS.md section → add the section
  - Missing skill → write the skill (per Ch 41)
  - Missing CODEOWNERS → update CODEOWNERS
  - Missing ADR → write the ADR (per Ch 25)
  - Stale documentation → update or remove it
- Verify the fix: re-attempt similar work; the agent succeeds

### Train → coach the spec author

The bucket that names a spec-quality gap. The action:

- In 1:1 (NOT publicly): walk the spec author through what was missing
- Update the team's spec template / examples to address the pattern
- Consider the "Tixie" ticket-writing assistant pattern from Ch 19 §19.5

## Reading the ratios over time

Per Ch 31 §31.5, the patterns over time:

### Healthy team trajectory

| Month | Score | Question | Opportunity | Train |
|---|---|---|---|---|
| Month 1 | 25% | 15% | 35% | 25% |
| Month 3 | 35% | 15% | 25% | 25% |
| Month 6 | 50% | 10% | 20% | 20% |
| Month 12 | 65% | 10% | 15% | 10% |

Score rising. Train and Opportunity falling. Question stepwise (drops at model releases).

### Stagnating team trajectory

| Month | Score | Question | Opportunity | Train |
|---|---|---|---|---|
| Month 1 | 25% | 15% | 35% | 25% |
| Month 3 | 27% | 15% | 33% | 25% |
| Month 6 | 28% | 15% | 32% | 25% |
| Month 12 | 30% | 15% | 30% | 25% |

The mix barely shifts. Per Ch 31 §31.5: "usually because nobody is closing the loop on the failures." The Opportunity tickets aren't getting filed; the Train coaching isn't happening; the harness isn't improving.

The intervention: a dedicated harness sprint. Every Opportunity from the last 60 days gets a ticket; every Train pattern becomes a spec-template improvement. Re-run the triage 6 weeks later; expect the ratios to shift.

### Slop-pattern trajectory

| Month | Score | Question | Opportunity | Train |
|---|---|---|---|---|
| Month 1 | 25% | 15% | 35% | 25% |
| Month 3 | 40% | 15% | 25% | 20% |
| Month 6 | 60% | 10% | 15% | 15% |
| Month 12 | 75% | 5% | 10% | 10% |

Looks like the healthy trajectory. But check it against the six dashboard metrics: if quality decay signals are firing while triage shows mostly Score, **the Score classification is wrong.** The team is marking failures as Score because the PRs merged, but the merged PRs are introducing defects. The Score discipline collapsed; the triage is no longer measuring what it should.

The fix is in `../failed-one-shot-triage/the-four-buckets.md`:

> Score with substantial rework: the agent produced a PR but the engineer rewrote half of it before merge. That's closer to a Train or Opportunity outcome — the harness/spec didn't actually deliver.
>
> Score that introduced incidents later: the PR merged but produced a production issue 2 weeks later. ... reclassify as Train, Opportunity, or Question depending on root cause.

## How the categorization improves the harness

The feedback loop:

```
Agent run → outcome → categorization → action
  ↓                                       │
  ↓                                       ▼
  ├──── Score ─────→ template + autonomy ceiling raise
  ├──── Question ──→ routing-table update + model re-test on release
  ├──── Opportunity → legibility ticket → harness update
  └──── Train ─────→ spec-template improvement → PM coaching
                                              │
                                              ▼
                                      Next agent run is better-positioned
```

The compounding: each iteration tightens the system. The harness fills in. The spec template improves. The model selection sharpens. After 6–12 months, the team's failure distribution has shifted dramatically toward Score.

This compounding only happens if the loop closes. Per Ch 31 §31.5:

> The diagnostic value is worth more than the precise count.

Categorizing without acting is performative. The action is the point.

## How to run the weekly triage

Per Ch 31 §31.5:

> Capture this in the standup or weekly review.

Operational structure (15-minute weekly meeting):

```
1. (2 min) Pull list of all agent runs from the past week
2. (10 min) For each:
   - Quick group call: Score, Question, Opportunity, or Train?
   - One-line note on what made it that bucket
   - Owner if action is required
3. (3 min) Roll-up: counts per bucket; flag any concerning patterns
```

For details on the meeting structure, see `../failed-one-shot-triage/weekly-retro-structure.md`.

## What goes on the "dashboard" (and what doesn't)

Per Ch 31 §31.5 / §31.7: this metric lives in retro, not on a dashboard. Specifically:

### On the dashboard

- **Monthly distribution** (bar chart): % Score / Question / Opportunity / Train
- **Trend over the last 6 months**: are the percentages shifting in the healthy direction?
- **Score-per-tier-per-model rate**: which combinations work?

### NOT on the dashboard

- Individual triage decisions (these are noisy)
- Per-engineer Score rates (this would turn into a surveillance tool)
- "Failure count" alone without categorization (counting failures without diagnosing them is what the book is specifically pushing back against)

The chart, when it exists, is for the engineering leadership review — not the executive view. It's a leading indicator of harness investment quality.

## Cross-tier breakdown

The triage ratios should be reported per-tier (T1 / T2 / T3) per Ch 19 §19.5. A typical mature team:

| Tier | Score | Question | Opportunity | Train |
|---|---|---|---|---|
| T1 (Simple) | 90% | 0% | 5% | 5% |
| T2 (Inspection) | 65% | 5% | 15% | 15% |
| T3 (Architecting) | 30% | 25% | 25% | 20% |

T1 should be almost all Score. T3 will always have substantial Question (the architectural work is the agent's jagged edge). T2 is where the harness investment compounds — and where most of the value lives.

A team where T1 is only 60% Score has either a spec-template problem (Train), a harness gap (Opportunity), or a process problem where T1 work is being misclassified upward.

A team where T3 is 60% Score either has unusually strong harness AND unusually strong specs (real possibility), or is misclassifying T3 work as Score when it actually required substantial human direction (more likely; see "slop pattern" above).

## Anti-patterns to avoid

### Logging only failures

The trap: the team only logs Question, Opportunity, and Train. Score gets no entry because "it worked, what's to record?" The ratios are misleading from the start. Score is logged with the same discipline as failures; the Score data is what tells you what works.

### Categorizing without acting

The trap: weekly triage runs; categories are noted; nothing changes. The harness doesn't fill in; the spec template doesn't improve. After 6 months, the ratios look identical to month 1. Per Ch 31 §31.5: "usually because nobody is closing the loop."

### Categorizing without consensus

The trap: one engineer thinks the failure was Train; another thinks Opportunity. They both log differently. The data isn't consistent. The mitigation: triage is a group decision, not an individual one. When in doubt, default to Train or Opportunity (per `../failed-one-shot-triage/the-four-buckets.md`).

### Over-engineering the tracking

The trap: building elaborate tooling, custom dashboards, automated classifiers. The team spends more time on the tracking than on the triage. Per Ch 31 §31.5: "Do not bother building elaborate tooling for it; a shared spreadsheet works."

### Using the categorization for performance evaluation

The trap: a manager notices Engineer X's PRs are the source of many Train failures, attributes that to Engineer X's spec quality, raises it in performance review. Within a quarter, Engineer X stops volunteering specs; engineers in general start avoiding the triage. The data collapses.

Mitigation: the metric is at the team level. Individual coaching happens in 1:1, never in performance evaluation, never in calibration discussions.

### Conflating "agent didn't finish" with "agent failed"

The trap: the engineer stops the agent at 30% completion because they got impatient. They log the result as a Question (capability gap). Actually it's that the agent was on track and the engineer didn't wait. The categorization is wrong; the resulting routing decision is wrong.

Mitigation: in the triage, the question to ask is "did the agent attempt the full task end to end?" If the answer is no, the result doesn't categorize cleanly. It's either Opportunity (the engineer needed more harness to feel confident waiting), Train (the spec was unclear so the engineer cut their losses), or operational (separate from the triage).

## What this taxonomy will NOT do

- Will not work without weekly cadence. Monthly is too infrequent; the failures aren't fresh enough to triage.
- Will not work without closing the loop. Categorizing without acting is performance theater.
- Will not work as a surveillance tool. Per [`code-maturity-rubric.md`](code-maturity-rubric.md) — team-level only.
- Will not work without precise definitions of the four buckets. The `../failed-one-shot-triage/the-four-buckets.md` definitions are the canonical reference.

## Companion artifacts

- [`README.md`](README.md) — the directory index
- [`agent-ready-issue-pipeline.md`](agent-ready-issue-pipeline.md) — the pipeline that auto-creates issues; failed runs from this feed the triage
- [`six-metric-dashboard/`](six-metric-dashboard/) — the six metrics this seventh metric diagnoses
- `../failed-one-shot-triage/` — the full taxonomy reference (the four buckets, the process, the weekly retro)
- `../agent-autonomy-levels/raising-and-lowering-autonomy.md` — what to do with Score-heavy work types
- `../cost-discipline-runbook/cost-attribution-per-pr.md` — the cost data captured per triage row
- Ch 19 §19.5, Ch 31 §31.5, §31.7 — sources
