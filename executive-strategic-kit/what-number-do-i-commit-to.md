# What Number Do I Commit To

The three-tier commitment framework. Per Ch 52 §52.5:

> When the board asks for a throughput commitment, anchor in three tiers (full version in Chapter 57):
>
> **With high confidence:** 10-15% throughput gain on tier-2 work over twelve months, given the harness investment is funded.
>
> **With conditions:** 25% gain on tier-2 work over twenty-four months, conditional on (a) harness team headcount, (b) certification gates respected, (c) cost gateway in place, (d) at least one full-time platform engineer on harness work.
>
> **Refuse to commit:** Doubling or quadrupling. Faster than 25% in 24 months. Anything tied to a future model release. Anything assuming a tool the team has not used yet. Anything that requires headcount cuts to fund.

This file is the operational guide for using this framework. The framework is what protects you from over-promising; using it correctly is what makes that protection durable.

## When this framework applies

Anytime someone asks for a productivity commitment from your engineering org. Specifically:

- Board meetings
- CEO 1:1s
- All-hands prep
- Board member side conversations
- Investor due diligence
- Customer references where productivity numbers come up
- Public speaking (cautiously)

The same framework, calibrated to context.

## Tier 1 — High confidence

### What you commit to

> 10-15% throughput gain on tier-2 work over twelve months, given the harness investment is funded.

The defensible commitment. Calibrated to industry data (DORA 8-15%, DX similar, Faros 12-18%). The teams that hit this range have shipped real harness investment.

### When to use

The default for board commitments. The default for CEO conversations when the CEO is asking for "what number do you commit to."

### What "given the harness investment is funded" means

Specifically:
- Platform team funded at 5-10% of engineering headcount per Ch 42 §42.4
- Skill library shipped per Ch 13
- AGENTS.md / CLAUDE.md current per Ch 6
- AI reviewer subagent shipped per Ch 14 §14.3
- Failed-one-shot triage running per `failed-one-shot-triage/`
- Cost discipline per `cost-discipline-runbook/`
- Quarterly model lineup review per `evals-and-benchmarks-runbook/`

If any of these aren't funded, the commitment doesn't hold. Make it explicit.

### How to deliver

In writing: "I commit to 12% throughput gain on tier-2 work over twelve months, conditional on the harness investment outlined in [reference]."

In conversation: "Twelve percent over twelve months. That's the defensible number. I can show you the industry data that calibrates that."

The 12% sits in the middle of the 10-15% range. Pick the middle as your target; the range gives you margin.

## Tier 2 — With conditions

### What you commit to

> 25% gain on tier-2 work over twenty-four months, conditional on:
> (a) harness team headcount,
> (b) certification gates respected,
> (c) cost gateway in place,
> (d) at least one full-time platform engineer on harness work.

The aspirational commitment. Achievable but not the default. Requires sustained investment over a longer timeline.

### When to use

When the board or CEO is pushing for more than tier 1, and the conditions can be met. The conditions matter; they're not decoration.

### What the conditions mean

**(a) Harness team headcount.** Not just "we have a platform team" but "the platform team is sized to the work." Typically 5-10% of engineering headcount, focused on harness work, not absorbed into feature delivery.

**(b) Certification gates respected.** Per `agent-autonomy-levels/certification-gates.md`. Engineers must earn higher autonomy through demonstrated capability. If certification is a rubber stamp, autonomy outpaces capability and quality decays.

**(c) Cost gateway in place.** Per `cost-discipline-runbook/`. Token spend monitored; anomalies caught; budgets enforced. Without this, costs run away and the ROI math breaks.

**(d) Full-time platform engineer on harness work.** At least one. Not a part-time assignment. Not "Sarah has 20% allocation." Full-time. The harness work compounds when someone owns it daily.

### How to deliver

> "Twenty-five percent over twenty-four months is achievable, but only if we sustain the investment. Specifically: harness team headcount stays at five percent of engineering, certification gates stay strict, cost gateway stays in place, and we have a full-time platform engineer. I can commit to that with those conditions in writing."

The "in writing" is the discipline. Tier 2 commitments require a written record of the conditions. Without that, the conditions get forgotten and the commitment becomes unconditional.

### Why 25% over 24 months specifically

- **25%**: roughly double the high-confidence number. Achievable for teams with sustained investment but not at the lower investment level.
- **24 months**: the timeline that lets compounding work. A new model release in the period; a harness investment cycle to mature.
- **Together**: the ceiling of what's defensible without entering tier-3 territory.

## Tier 3 — Refuse to commit

### What you refuse to commit to

> - Doubling or quadrupling productivity
> - Faster than 25% in 24 months
> - Anything tied to a future model release
> - Anything assuming a tool the team has not used yet
> - Anything that requires headcount cuts to fund

These are the lines you do not cross.

### Why

Each item is a different failure mode:

**Doubling or quadrupling.** No team has hit these numbers at scale. Public claims of doubling are either (a) marketing language not measuring rigorously, (b) cherry-picked time periods or teams, (c) measuring something we don't want to optimize (acceptance rate, LOC). Committing to a number no team has hit at scale is committing to fail.

**Faster than 25% in 24 months.** The compounding takes time. A team that reorganizes around a faster timeline produces friction; the friction reduces actual gains; the timeline slips. The 25% in 24 months is the ceiling.

**Anything tied to a future model release.** The future model isn't released. Its capabilities are speculation. Vendor roadmaps slip. Committing to "Claude 5 will deliver X" is committing on someone else's roadmap.

**Anything assuming a tool the team has not used yet.** Adoption takes time. Tooling fit isn't predictable from demos. The team's actual experience with the tool will reveal capabilities and limitations the demo didn't show.

**Anything that requires headcount cuts to fund.** Per [`hype-rebuttal-table.md`](hype-rebuttal-table.md) hype claim 1. The substitution + acceleration posture is incoherent. Refuse.

### How to deliver the refusal

The refusal is harder than the commitments. Most VPs avoid the conversation; the result is implicit commitments to numbers they can't hit.

The structure:

> "I am not going to commit to that number. Here's why: [specific reason from the list above]. What I can commit to is [tier 1 or tier 2]. If you want a higher number, the conversation is about [the specific investment that would justify it]. We can have that conversation."

The refusal is not "no." The refusal is "not on the current basis; here's what would change my answer."

### When the CEO insists

Sometimes the CEO will push: "I need you to commit to 50%." Three responses, in order:

#### Response 1 — restate the framework

> "I cannot commit to 50%. The defensible number on our current investment is 12%. The aspirational number with sustained investment is 25%. 50% is not in the range any team has delivered at scale. If we commit to 50%, I will fail to deliver, and you will have to find someone else to deliver — who will also fail. I am trying to save us both that conversation."

#### Response 2 — name the trade-off

> "50% can be committed to if we accept specific things: heavy outsourcing to AI on currently human-led work, acceptance of higher quality variance for 18 months, willingness to absorb the customer impact of that variance. If those trade-offs are on the table, I can commit to 50% with those acknowledgments. They are not currently on the table. I do not recommend putting them on the table."

#### Response 3 — invoke the board

> "If we commit to 50% to the board, I will need to do so in writing, with the operating posture this requires (substitution, not investment), and the corresponding quality acceptance. I do not think the board will accept that posture. If you would like to test that, I can prepare the case for it. I will not commit to 50% without that explicit posture in writing."

The third response forces the conversation to the board level. Most CEOs back down before this — they understand that committing to substitution+acceleration to the board has its own risks.

If the CEO doesn't back down, you have a different problem. You may be in the wrong job, or the CEO may need to find a different VPE. Either way, the conversation is about whether you stay, not about what number you commit to.

## Adapting the framework

### To different metrics

The framework above is for throughput. The same structure applies to other metrics:

| Metric | High confidence | With conditions | Refuse |
|---|---|---|---|
| Throughput | 10-15% / 12 months | 25% / 24 months | >25% / 24 months |
| Cost | $150-250/dev/month | Reduce 20% / 12 months on stable usage | Reduce >50% |
| Time to market on bounded features | 25-30% reduction | 40% reduction with prototype-first | >50% reduction |
| Defect escape rate | Held flat | Reduce 20% with AI reviewer subagent | Reduce >50% |
| Adoption | 90% / 6 months | 95% / 9 months | 100% (always) |

The framework is universal: there's a high-confidence number, an aspirational-with-conditions number, and a refuse-to-commit territory. Calibrate the specifics to your metric.

### To different audiences

| Audience | What they want | How to use the framework |
|---|---|---|
| Board | One commitment number per metric | Tier 1 unless they specifically push for tier 2 |
| CEO | A more conversational version of the same | Walk all three tiers; commit to tier 1 by default |
| Investors / due diligence | More detail, more confidence | Tier 1 numbers; tier 3 refusals explicit |
| Customers | Less commitment overall | Mostly tier 1; less aspirational language |
| Public speaking | Heavy caveats | Tier 1 with explicit "this is calibrated to teams with discipline" |

## What writing the commitment down does

Writing the commitment down (in the board deck, in an email, in a memo) changes the dynamics:

- **The contingencies become durable.** A verbal commitment loses contingencies in transmission. A written commitment carries them.
- **The accountability becomes specific.** The commitment is to a specific number, on a specific timeline, under specific conditions.
- **The conversation in 12 months has a reference.** When the board asks "did we hit it?", you and the board are looking at the same document.
- **Your successor (if it comes to that) inherits the commitment.** The commitment doesn't depend on you remembering it.

Verbal commitments without written follow-up are worth roughly nothing in 12 months. The written record is the discipline.

## Anti-patterns

### Committing tier 1 then drifting to tier 2 without conditions

You commit to 12%, then someone asks for "what if we pushed harder," and you drift to "we could do 18%" without naming the conditions. The conditions are forgotten; the 18% becomes the commitment.

Mitigation: tiers are bright lines. Tier 2 always has explicit conditions. If you're saying a number above tier 1, the conditions go with it.

### Committing tier 2 numbers when conditions don't hold

You commit to 25% over 24 months because the platform team is funded — but then the platform team gets reabsorbed for feature delivery six months in. Your 25% commitment doesn't hold; you don't communicate that.

Mitigation: when conditions break, the commitment changes. Communicate the change as soon as the condition breaks. Don't wait for the deadline to surface the gap.

### Committing tier 3 numbers under pressure

The CEO pushes for 50%; you commit to 35% as a "compromise." 35% is in tier-3 territory. You've effectively committed to a number you can't hit.

Mitigation: tier 3 is a bright line. The compromise should be between tier 1 and tier 2, not between tier 2 and tier 3.

### Refusing to commit at all

You refuse all numbers. The CEO concludes you're hedging. They find someone who will commit.

Mitigation: tier 1 is always available. The refusal is to overcommitment, not to commitment.

### Committing without measurement infrastructure

You commit to 12% throughput gain but the team doesn't measure throughput. The commitment is a vibe.

Mitigation: per `metrics-and-measurement-infrastructure/`, the dashboard exists. The commitment references the dashboard.

### Letting the CEO commit on your behalf

The CEO tells the board "we'll see 25% gains" without your input. You weren't consulted; you can't undo the commitment.

Mitigation: pre-brief the CEO on the framework. The CEO knows the tiers; they know the lines they shouldn't cross. If the CEO commits beyond what you can deliver, the conversation is about that breach of process — but the breach is harder to commit if the framework was pre-socialized.

## Companion artifacts

- [`realistic-roi-message.md`](realistic-roi-message.md) — the substance of tier 1
- [`hype-rebuttal-table.md`](hype-rebuttal-table.md) — what to push back against
- [`four-slide-board-deck-walkthrough.md`](four-slide-board-deck-walkthrough.md) — where the commitment lives
- [`honest-internal-message-to-engineers.md`](honest-internal-message-to-engineers.md) — the internal version of the same numbers
- `metrics-and-measurement-infrastructure/` — the dashboard the commitment references
- Ch 52 §52.5 — source
