# The Realistic ROI Message

The number you commit to. Per Ch 46 §46.2:

> When the board asks for a number, give them this one:
>
> - **Adoption:** ~90% of engineers, daily or weekly use, within 6 months of approved rollout.
> - **Throughput:** 8-20% PR-throughput improvement, contingent on harness investment.
> - **Quality:** held flat or improved, contingent on review discipline.
> - **Time-to-market on bounded features:** 25-40% reduction, contingent on prototype-first discovery.
> - **Cost:** $150-250/active developer/month token spend, plus harness team capacity (~5-10% of engineering headcount).

> If you promise more than this without evidence in your own dashboard, you are setting yourself up to be the leader who fails to deliver on the AI thesis. If you promise less than this, you are inviting the CEO to find a leader who will promise more.

## Why these specific numbers

### Adoption: ~90% within 6 months

Realistic. Anything higher is forced (and produces resistance). Anything lower suggests the rollout is failing.

The 6-month frame is calibrated to:
- Time for initial pilot (weeks 1-4)
- Time to expand to all engineering (weeks 4-12)
- Time for laggards to come on board (weeks 12-24)

If you commit to 90% in 90 days, you are forcing it. If you commit to 90% in 12 months, you are telegraphing slow execution.

### Throughput: 8-20% with harness contingency

Calibrated to industry data:
- DORA 2025: 8-15% throughput gain on prepared teams
- DX 2025: similar range with high variance
- Faros 2026: 12-18% on teams with mature harness
- METR: -19% on poorly harnessed senior engineers (the floor of the range)

The "8-20%" range with "contingent on harness investment" is the defensible commitment. The lower bound (8%) is what you get from minimal harness; the upper bound (20%) requires sustained platform investment.

If you commit to "30% throughput gain," you are committing to numbers no team has hit at scale.

If you commit to "modest improvement," you are giving the CEO no reason to keep funding.

### Quality: held flat or improved with review contingency

The honest truth. Per Ch 22 (review crisis), AI tooling can erode quality if reviews aren't disciplined. The commitment is "we will hold quality flat or improve it" — which requires the review investment to be funded.

If you commit to "quality unchanged" without the review contingency, you are committing on a basis you don't control.

### Time-to-market on bounded features: 25-40% reduction

The most aggressive number in the set. Calibrated to:
- Bounded features (T2 work per Ch 19) — not architectural work
- Prototype-first discovery (per Ch 38) — not waterfall execution

The "25-40%" is achievable when:
- Specs are sharp (per the Intake pattern)
- Harness is mature
- Prototype iterations are short
- Reviews are paced with throughput

If you commit to this without the contingencies, you are setting up for a number you can't hit.

### Cost: $150-250/developer/month + 5-10% headcount

Per Ch 27 §27.1 and §27.2. The book's worked example: a 50-engineer team at average usage spends ~$13,000/month on tokens. Plus the platform team (5-10% of engineering headcount) building the harness.

Per Anthropic's own published guidance (cited in Ch 27): "average cost is around $13 per developer per active day and $150-250 per developer per month."

If you commit to lower than $150/month, you are committing to a usage level that doesn't match real productivity. If you commit to higher than $250/month without the harness investment, you are committing to runaway cost.

## How to deliver the message

### To the board

In writing, in the four-slide deck (per [`four-slide-board-deck-walkthrough.md`](four-slide-board-deck-walkthrough.md)).

Slide 2 (Investment) covers the cost commitment. Slide 3 (Metrics) shows the throughput, quality, and adoption commitments with trend lines.

The realistic ROI message is the substance behind the deck. The deck is the surface; this is the substance.

### To the CEO

Verbally first, then in writing. Per Ch 52 §52.2 ("Defending the investment"), the email template references these numbers:

> Token spend tracked to $X this quarter against the budget of $Y. Per-developer median is $Z/week, well below the per-seat ceiling we set.
>
> Median lead time on tier-2 tickets dropped from N days to M days.

Substitute your actual numbers. The commitment framework above is what makes the actual numbers defensible.

### To engineering managers

In all-hands or in the engineering leadership channel. Per Ch 46 §46.3 (the honest internal message), the framing for engineers is different from the framing for the board. See [`honest-internal-message-to-engineers.md`](honest-internal-message-to-engineers.md).

## What the contingencies mean specifically

The commitment is not "8-20% throughput, full stop." It's "8-20% throughput contingent on harness investment." The contingency matters.

What "harness investment" means specifically:
- Platform team funded with 5-10% of engineering headcount per Ch 42 §42.4
- Skill library maintained per Ch 13
- AGENTS.md and CLAUDE.md kept current per Ch 6
- AI reviewer subagent shipped per Ch 14 §14.3 / `reviewer-burnout-mitigation/mitigation-1-ai-reviewer-subagent.md`
- Failed-one-shot triage running per `failed-one-shot-triage/`
- Cost discipline running per `cost-discipline-runbook/`

If any of these aren't funded, the commitment doesn't hold. State that explicitly.

What "review discipline" means specifically:
- Reviews continue to take meaningful time (per Ch 22)
- AI reviewer subagent is a floor, not ceiling
- PR size limits enforced per `reviewer-burnout-mitigation/mitigation-2-pr-size-limits.md`
- Review work is recognized per `reviewer-burnout-mitigation/mitigation-5-review-work-visibility.md`

If reviews degrade to rubber-stamping, quality drops. State that explicitly.

What "prototype-first discovery" means specifically:
- Time-to-market gains require iterative discovery, not waterfall delivery
- Most features have a prototype phase before the production phase
- The 25-40% gain is on the production phase only

If the team is asked to ship features without a discovery phase, the commitment doesn't hold.

## What if the CEO wants more

Common reaction: "8-20% is fine, but our competitors are claiming 50%."

The response (per [`hype-rebuttal-table.md`](hype-rebuttal-table.md) hype claim 1):

> The 50% number is in marketing, not in production. The teams that announce 50% productivity gains either (a) measured something we can verify is wrong (LOC, suggestion acceptance, token usage) or (b) cherry-picked a quarter or a small team. The aggregate, defensible number is the one I gave you.
>
> If we want to commit to 30%, I need to see harness funding 2x what we have, the platform team headcount doubled, and a 12-month timeline minimum. We can have that conversation. We cannot commit to 30% on the current investment.

This is the spine. The CEO can ask for more; you can give it conditional on more investment. What you cannot do is commit to higher numbers on the current investment.

## What if the CEO wants less

Less common, but happens. "Just commit to 5%; let's not over-promise."

The response:

> 5% is below the floor of what teams with disciplined harness deliver. If we commit to 5%, the CEO is going to be disappointed when the actual number is higher, and the board will conclude we sandbagged. The 8-20% range is the honest range; let's commit there.

Underselling has its own cost. The CEO who commits to 5% and delivers 12% looks like they didn't know what they were doing.

## What if the CEO wants a single number

The board often wants one number, not a range. The response:

> I commit to 12% throughput gain on tier-2 work over twelve months, with quality flat or improved, with the harness investment we have today. If you want me to commit to a higher number, I need a corresponding commitment on harness investment.

The 12% sits in the middle of the 8-20% range. It's defensible. It's not sandbagged.

If the CEO wants to negotiate the number up, route through the [`what-number-do-i-commit-to.md`](what-number-do-i-commit-to.md) framework — three tiers (high confidence / with conditions / refuse to commit).

## What if the dashboard says we're below the commitment

Three months in, the dashboard shows 5% gain, not 12%.

Three things to do:

1. **Investigate** — is the commitment wrong, or is the harness investment lagging? Use `failed-one-shot-triage/` to see if it's Train, Opportunity, or Question.
2. **Communicate honestly** — don't hide the gap. Per Ch 52 §52.2, the email template walks the actual numbers and the trajectory.
3. **Adjust** — either accelerate harness investment to close the gap, or revise the commitment with explicit acknowledgment.

The worst answer is to spin the numbers. The CEO will figure it out, and your credibility for future commitments collapses.

## Anti-patterns

### Committing without contingencies

"I commit to 15% throughput gain" — full stop. The contingencies are dropped because they're "obvious." They aren't obvious; they get dropped from memory; the commitment becomes unconditional.

Mitigation: write the contingencies into the commitment every time. The contingencies are part of the commitment.

### Committing the team without consulting the team

You commit to 18%; the engineering managers find out from the all-hands. They feel the number is unrealistic; they push back internally; the commitment erodes.

Mitigation: pre-socialize. Engineering managers should see the commitment before it goes to the board.

### Committing to numbers you don't measure

You commit to "quality held flat" but the team isn't tracking quality metrics. The commitment is a vibe.

Mitigation: per `metrics-and-measurement-infrastructure/`, the dashboard measures all four (adoption, throughput, quality, cost). The commitment references the dashboard.

### Committing to point-in-time

"30% gain by Q3." Point-in-time commitments break when reality has variance. A bad quarter blows the commitment.

Mitigation: trajectory commitments. "12% gain over 12 months" is a trajectory; one bad quarter doesn't blow it.

### Committing to a number the CEO heard somewhere

The CEO heard "75% productivity gain" on a podcast and asks if you can match. You commit to 50% as a "compromise." Six months later, you've delivered 12% and you're being asked why.

Mitigation: don't compromise on the floor of defensibility. The 8-20% range is the defensible range. Going higher is committing to numbers no team delivers at scale.

## Companion artifacts

- [`hype-rebuttal-table.md`](hype-rebuttal-table.md) — the rebuttals
- [`what-number-do-i-commit-to.md`](what-number-do-i-commit-to.md) — the three-tier framework
- [`four-slide-board-deck-walkthrough.md`](four-slide-board-deck-walkthrough.md) — the deck
- [`worked-examples-as-case-studies.md`](worked-examples-as-case-studies.md) — making it concrete
- `metrics-and-measurement-infrastructure/` — the dashboard the commitment references
- `executive-strategic-kit/roi-calculator.xlsx` — the operational tool for filling in numbers
- Ch 46 §46.2 — source
