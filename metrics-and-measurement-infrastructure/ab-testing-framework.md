# A/B Testing Framework — Measuring AI Adoption Impact

Direct expansion of Ch 31 §31.6 "A/B testing AI adoption (the credible version)." The methodology that lets a CTO say "yes, AI is working" with evidence — not vibes.

Per the book:

> Most "AI productivity" claims cannot be defended because they were never measured against a control. This section is the credible toolkit: an A/B framework, a PR authorship convention, and the leading indicators for quality decay.
>
> — Ch 31 §31.6

This file is the operational expansion of the A/B portion. The PR authorship convention lives in [`README.md`](README.md) and [`code-maturity-rubric.md`](code-maturity-rubric.md); the leading indicators live in [`quality-decay-signals.md`](quality-decay-signals.md).

## The book's design (Ch 31 §31.6)

The framework, verbatim:

> Two teams of similar size and seniority. One adopts the AI tooling stack on Day 0; the other holds off for 90 days. Both report metrics weekly.

That's the core. Three details follow.

### Criteria for picking the pair

Per Ch 31 §31.6:

> - Similar team size (within 1 engineer).
> - Similar seniority distribution.
> - Similar product surface (consumer vs. internal vs. infrastructure).
> - Similar baseline metrics for the prior 90 days.

The "similar baseline metrics" criterion is load-bearing. If the two teams have wildly different velocity or lead time pre-rollout, you're not testing AI's impact — you're testing the gap between two teams plus AI.

### What to measure

Per Ch 31 §31.6:

> - Lead time on tier-2 tickets.
> - PR review time per merged PR.
> - Change failure rate.
> - Self-reported developer satisfaction (one survey question, weekly: "How would you rate your week, 1-5?").

That's the full list from the book. Note the absence of:

- Lines of code (per Ch 31 §31.2 — discredited)
- Token usage (adoption metric, not productivity)
- Commit count (gameable)
- Suggestion acceptance rate (per Ch 31 §31.2 — discredited)

### Duration

Per Ch 31 §31.6:

> Duration: 90 days minimum. Anything shorter is noise.

Three months. Not three sprints. Not six weeks. The book is explicit on this and on why:

> The honest read at Day 90: typically the AI-adopting team shows a 5-15% improvement on lead time and a smaller improvement on PR review time, with no measurable change on change failure rate.

If you measure at day 30, you get setup-cost noise (the AI team is learning). If you measure at day 60, you're seeing partial adoption. Day 90 is the earliest defensible read.

## The expected outcome (calibration)

Per Ch 31 §31.6, the typical honest read at day 90:

| Metric | Typical change vs control |
|---|---|
| Lead time on T2 tickets | 5–15% improvement |
| PR review time per merged PR | Smaller improvement (or no change) |
| Change failure rate | No measurable change |
| Developer satisfaction | Variable; depends on the team |

If your A/B result looks dramatically better than this (e.g., 40% lead time improvement) at day 90, **something is wrong with the measurement.** Common causes:

1. The control team is gaming the metrics (deliberately or not) because they know they're the control
2. The teams aren't actually comparable on the baseline
3. One team had a confounding event (incident, reorg, vacation cluster)
4. The metric definition shifted between teams (different "T2" definition, different "merged" definition)

If your result looks substantially worse than this (control beats AI on lead time), either:

1. The AI rollout was poorly executed (no harness, no training, no CLAUDE.md)
2. The team is in the J-curve dip (first 30 days of any AI rollout costs more than it saves)
3. The work this team does isn't well-suited to AI assistance (research-heavy, novel-problem-heavy)

## Honest reporting

Per Ch 31 §31.6 directly:

> This is enough to be defensible to your board and CFO. It is not a randomized controlled trial. Do not oversell.

The "do not oversell" is the discipline. The A/B framework is not an RCT — engineers self-select into teams, teams choose their own work, the control team doesn't stay perfectly frozen. What it produces is **a defensible comparison**, not a causal proof.

The defensible claim:

> "Our AI-adopting team improved lead time by X% compared to our control team across 90 days, with no measurable change in change failure rate. Both teams had similar baselines. This is consistent with industry benchmarks at roughly the median; it is not a controlled trial."

The over-claim to avoid:

> "AI made our team 35% more productive."

The first is provable from the data. The second isn't.

## Two-team vs two-cohort design

The book describes a two-*team* design. There's a variant — two-*cohort* — that's useful for larger orgs.

### Two-team design (the book's framework)

| Setup | Two existing teams; one adopts on day 0; the other holds for 90 days |
|---|---|
| **Pros** | Easier to set up; teams have stable identity and product surface |
| **Cons** | Self-selection (which team volunteered? probably the one excited about AI); team composition isn't randomized |
| **Best for** | Mid-sized orgs (20–100 engineers) doing initial adoption decision |

### Two-cohort design (the variant)

| Setup | Split a single large team into two cohorts; cohort A gets AI; cohort B doesn't |
|---|---|
| **Pros** | Same team identity, same product, same culture, same management; closer to controlled |
| **Cons** | Politically harder (engineers in cohort B feel like a control group); harder to maintain isolation (cohort B will see cohort A using AI) |
| **Best for** | Larger orgs (>100 engineers) and orgs that need a more rigorous comparison |

Most teams should use the two-team design first. The two-cohort design is appropriate when the two-team result is contested or when the stakes warrant the higher rigor.

## Handling the confounds

The four common confounds and the mitigations:

### Confound 1: seniority differences

**The problem:** AI helps senior engineers more (or less) than junior engineers, so an AI team that happens to be more senior will appear to win on AI when really they're winning on seniority.

**Mitigation:**
- Match seniority distribution within ±1 engineer per level (junior / mid / senior / staff)
- Pre-rollout, capture per-level metrics from each team; if one team is materially better at the senior level pre-AI, that's a baseline confound
- Report results both aggregate AND by seniority level; if the AI win is concentrated in one seniority band, name it

### Confound 2: project-type differences

**The problem:** AI helps consumer features more than infrastructure, or vice versa. If the AI team happens to be on consumer work that quarter and the control team is on infra, the result is project-type, not AI.

**Mitigation:**
- Match product surface (consumer / internal / infrastructure) at the team level
- Match work mix (% bugs / % features / % refactors) for the comparison period
- If the work mix shifts mid-experiment, document it and account for it in the read

### Confound 3: the Hawthorne effect on the AI team

**The problem:** The AI team knows they're being measured, knows leadership is watching, knows their performance reflects on the AI rollout. They work harder.

**Mitigation:**
- Don't publicize the experiment internally. Run the measurement without telling engineers they're being compared.
- Keep the framing operational: "we're measuring lead time across teams as part of our usual metrics review." Both teams hear the same message.

### Confound 4: control-team contamination

**The problem:** Per Ch 31 §31.6:

> The control team usually does not stay frozen — they adopt informally as they see the other team's results — so the comparison degrades after 60 days.

**Mitigation:**
- Set an explicit policy with the control team's manager: no AI tool adoption during the 90-day window
- Monitor token-usage data on the control team; if usage spikes, the team isn't actually a control
- Accept that the comparison degrades; the honest read is "Day 30, Day 60, Day 90" trends, not just the endpoint

## Sample size guidance

The book doesn't prescribe specific sample sizes. The pragmatic guidance:

- **Two teams of 5–10 engineers each is the minimum.** Below 5, individual variation swamps the signal.
- **The unit of analysis is the team-week.** Across 90 days, you have ~13 team-weeks per team for the statistical comparison.
- **For lead time:** 25+ merged PRs per team across the period. Below that, the median is noisy.
- **For change failure rate:** at most teams, you'll see <5 changes-that-fail across 90 days. The metric is signal-poor by design; don't try to detect statistical significance on it.
- **For developer satisfaction:** weekly survey with 80%+ completion. Below that, response bias dominates.

For statistical comparison: use Mann-Whitney U test or bootstrap confidence intervals on the team-week metrics. Don't try to compute p-values on individual PRs; the unit of analysis is the team-week.

## The weekly cadence

The operational cadence during the 90-day window:

| Cadence | Activity |
|---|---|
| Weekly | Per-team metric snapshot (lead time, PR review time, change failure rate, satisfaction) |
| Weekly | One-question satisfaction survey ("How would you rate your week, 1-5?") |
| Bi-weekly | Sponsor (VP eng or equivalent) reviews data, flags anomalies, does not intervene |
| At day 30 | Interim read — confirm both teams' baselines look right; correct any data collection issues |
| At day 60 | Interim read — note any drift in the control team |
| At day 90 | Final read — write up the result; decide rollout |
| At day 90 + 30 | Follow-up read — does the win persist past the experiment? |

The day-90-plus-30 follow-up is the often-missed step. If the AI team's win evaporates after the experiment ends (because the Hawthorne effect drove it), that's worth knowing.

## When the A/B is over

Per Ch 31 §31.6:

> This is enough to be defensible to your board and CFO. It is not a randomized controlled trial. Do not oversell.

At day 90, the decision tree:

| Result | Action |
|---|---|
| AI team improved on lead time (5–15%) AND change failure rate held | Roll out broadly with confidence; document the win |
| AI team improved on lead time AND change failure rate worsened | Slop pattern — pause rollout; audit harness; re-test on next round |
| AI team flat on lead time AND change failure rate held | Inconclusive; either tooling is wrong for the work, or harness investment was insufficient — investigate before broad rollout |
| AI team worsened on lead time | Rollout was poorly executed (likely harness gaps); fix and re-test on next round |
| Developer satisfaction dropped on the AI team | Investigate independently of the throughput numbers; satisfaction often leads attrition |

## Sample report structure

The report you write at day 90 should fit on one page and look approximately like:

```markdown
# A/B Test Read — AI Tooling Adoption, Q[N] 2026

## Setup
- Test team: [Team A], 8 engineers, [seniority mix]
- Control team: [Team B], 8 engineers, [seniority mix]
- Pre-rollout baseline period: 90 days
- Test period: 90 days, [start] to [end]
- Test team adopted: Claude Code (Sonnet 4.6 default), pre-shipped CLAUDE.md, slop-detector hook

## Results

| Metric | Pre-AI (both teams) | Test team end | Control team end | Test vs Control |
|---|---|---|---|---|
| Median lead time (T2 tickets) | 4.2 days | 3.7 days (-12%) | 4.1 days (-2%) | -10pp |
| Median PR review time | 8.5h | 9.2h (+8%) | 8.6h (+1%) | +7pp |
| Change failure rate | 6% | 7% | 6% | +1pp (within noise) |
| Developer satisfaction | 3.6/5 | 3.8/5 | 3.5/5 | +0.3 |

## Confounds noted
- Control team adopted Cursor for autocomplete starting day 47 (informal); this likely understates the AI team's win
- Test team had one fewer P0 incident during the period; not statistically significant at this N

## Read
The AI-adopting team improved median lead time by 12% vs a 2% improvement
on the control team across 90 days. Change failure rate was statistically
indistinguishable. PR review time rose slightly on both teams; rose more on
the AI team, consistent with industry data.

This is consistent with the book's published expected range (5–15% lead
time improvement, no measurable change in change failure rate). This is not
a controlled trial; engineers self-selected to teams and the control team
partially contaminated.

## Decision
Recommended: broad rollout to all teams. Maintain the leading-indicator
dashboard (quality-decay-signals.md) during the broader rollout; pull the
lever per the established rule if signals deteriorate.

## Next steps
- Day 90 + 30 follow-up read
- Rollout plan for remaining teams
- Quarterly re-validation of the LLM code-maturity grader
```

This is the artifact your CFO and board want. Keep it factual; don't oversell; cite the book's expected ranges as calibration.

## Anti-patterns to avoid

### Comparing teams with very different baselines

The trap: Team A's pre-AI lead time was 2 days; Team B's was 8 days. After AI, Team A is at 1.8 days and Team B is at 7 days. The AI team "improved more." But maybe Team A's lower baseline was already at the team's floor and they couldn't improve much.

Mitigation: include the % change, not the absolute change. And note when the baseline gap is large (>30%) — at that point the comparison is shaky.

### Measuring too early

The trap: a "30-day A/B" produces no signal because both teams are still in setup cost. Leadership concludes "AI doesn't work." Per Ch 31 §31.6: 90 days minimum.

### Cherry-picking the winning metric

The trap: the AI team improved on lead time by 12%; on PR review time it got worse; on satisfaction it dropped. The report headlines the lead time win and buries the rest. Six months later when satisfaction-driven attrition surfaces, the credibility of the metric system collapses.

Mitigation: report all four metrics in the table. Headline the most important one (lead time, per the book), but make the others visible.

### Treating the result as causal

The trap: "Our A/B proved AI made us 12% faster." It didn't prove anything — it produced a defensible comparison. The book is direct: "It is not a randomized controlled trial."

Mitigation: language matters. "Consistent with" is defensible; "proved" is not. "The AI-adopting team improved" is defensible; "AI made us improve" is not.

### Skipping the day-30 interim check

The trap: the data collection has a bug; you don't notice until day 90; the experiment is unusable. The day-30 check catches data-quality issues while there's still time to fix them.

### Comparing test team to control team's *post-AI* numbers when control adopts informally

The trap: control team starts using AI informally at day 50. By day 90, both teams are AI-using; the gap closes. Looks like AI doesn't matter. The mitigation: monitor adoption on the control team; report a "pre-contamination" comparison (day 1 to day 50) separately from the full window.

## What this framework will NOT do

- Will not produce randomized causal proof. It produces defensible comparison.
- Will not work without a stable 90-day baseline period. See [`baseline-measurement-template.md`](baseline-measurement-template.md).
- Will not work without disciplined metric definitions. Re-using the same metric definitions across the test and control teams is non-negotiable.
- Will not work in a culture where the test team feels surveilled. Hawthorne contamination dominates.

## Companion artifacts

- [`baseline-measurement-template.md`](baseline-measurement-template.md) — the pre-test baseline capture
- [`README.md`](README.md) — the directory index
- [`quality-decay-signals.md`](quality-decay-signals.md) — the leading indicators that run alongside the A/B
- [`code-maturity-rubric.md`](code-maturity-rubric.md) — the keystone quality metric for the test
- `../benchmarks/` — the regression-test methodology that pairs with this for "is the model getting worse" detection
- Ch 31 §31.2, §31.6 — sources
