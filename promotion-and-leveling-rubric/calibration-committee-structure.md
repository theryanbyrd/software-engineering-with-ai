# Calibration Committee Structure

How calibration committees should be structured to handle leveling decisions consistently across the org. Specifically calibrated to handle the AI-tooling fluency dimension that some legacy committees aren't equipped for.

## Why calibration committees exist

Without committees, leveling decisions vary by manager. Some managers under-promote (engineers leave); some over-promote (the bar erodes; everyone becomes "senior"). The committee is the consistency mechanism.

The committee:
- Reviews promotion packets
- Compares engineers across teams against shared criteria
- Surfaces disagreements between managers
- Documents decisions for institutional memory
- Catches inconsistencies (e.g., one manager rating "L4 in code review" much more loosely than another)

## Committee composition

### For L3 → L4 promotions

- 4-6 members
- Mix of engineering managers and senior IC engineers (L5+)
- At least one member from outside the candidate's direct team
- Chair: an engineering director or senior manager who runs the meeting

### For L4 → L5 promotions

- 4-6 members
- Mix of L5/L6 ICs and engineering directors
- At least 2 members from outside the candidate's direct team
- Chair: senior engineering leadership (VP or comparable)

### For L5 → L6 promotions

- 6-8 members
- Mix of L6+ ICs and engineering leadership
- Cross-org representation (at least one member from each major engineering org)
- Chair: VP of Engineering or CTO

### For L6 → L7 promotions (rare)

- Convened ad-hoc, often outside the regular cycle
- 6-10 members including external advisors or board members
- Chair: CTO or comparable

## Rotation cadence

- Members serve on committees for 4-6 cycles (a year)
- Replacement is staggered — 1/4 to 1/3 of the committee turns over each cycle
- The chair stays for at least 2 cycles to maintain consistency

Rotation prevents committee members from developing fixed views and ensures fresh perspectives. Staggered rotation prevents the institutional memory from disappearing all at once.

## Pre-committee work

The manager prepares a packet (see [`promotion-packet-template.md`](promotion-packet-template.md)) with:

- Engineer's self-assessment
- Manager's case for promotion
- Specific examples mapped to rubric criteria
- Peer feedback (3-5 peers, anonymized in the packet)
- Sample artifacts (PRs, design docs, harness contributions)

The packet is distributed to committee members 5-7 business days before the meeting. Committee members are expected to read packets in advance.

## Committee meeting structure

### Format

- Per case: 20-30 minutes
- Total committee meeting: 2-3 hours (5-7 cases per session)
- Cases are batched by level (all L3→L4 cases in one session; L4→L5 in another)

### Per-case structure

1. **Manager presents** (5 minutes) — the case for promotion, with specific examples
2. **Committee questions** (5-10 minutes) — clarifying questions about scope, evidence, calibration
3. **Discussion** (5-10 minutes) — committee discusses without the manager (manager steps out, or the meeting protocol allows the manager to be present but not speak during discussion)
4. **Decision** (2-3 minutes) — vote, or chair-led consensus
5. **Notes captured** — the chair (or designated note-taker) records the decision and reasoning

### Decision rules

The committee uses one of these protocols (pick one and stick to it):

**Option A — Consensus required.** All committee members must agree. Disagreement triggers more discussion or a deferral.

**Option B — Supermajority.** 75%+ approval required for promotion.

**Option C — Veto rights for chair.** Committee discusses; chair makes the call but considers committee input.

Most companies use Option B for L3-L4 and Option A for L5+.

### When the committee disagrees

Patterns:

- **Manager strongly advocates; committee skeptical.** Defer to next cycle. The manager invests in closing the named gaps; engineer's case strengthens.
- **Committee split evenly.** Defer or reduce to "promotion deferred with specific path forward."
- **Manager doesn't push; committee asks "should we promote anyway?"** Rare but real. Usually means the manager is being too conservative or has missed evidence. Promote with note that manager should engage more in next cycle.

The discipline: don't force decisions when the committee is split. Deferral is better than a forced decision that erodes credibility.

## AI-tooling fluency calibration

The dimension that's new in 2026 and easy to handle inconsistently. Specific calibration discipline:

### Anchor cases

The committee maintains anchor cases — specific examples of L4 fluency, L5 fluency, etc. — that members can reference. New members are calibrated against the anchors.

Example anchor for L4 fluency:

> Engineer X (anonymized in committee discussions but widely known to longtime members): shipped `skills/migration-discipline/` over Q2 2025; the skill is used by 4 stream-aligned teams; engineer iterated based on adoption feedback; engineer's PR reviews catch slop signatures consistently. This is the L4 anchor for AI-tooling fluency.

When a new case comes up, committee members compare to the anchor: "is this engineer's fluency comparable to Engineer X's?" If yes, they meet the L4 bar. If significantly weaker, they don't.

### Common pitfalls

**"They use AI a lot."** Heavy usage isn't fluency. Calibrate against impact and contribution, not volume.

**"They built a custom tool."** Custom tools matter only if other engineers use them. A tool that nobody else uses might be a learning artifact, not a contribution.

**"They're skeptical of AI tooling."** Calibrated skepticism (Ch 42 §42.1's "skepticism without cynicism") is good. Refusal to engage is a fluency gap.

**"They're a senior IC; they can't be at L4 fluency."** Yes they can. Senior ICs who haven't engaged with AI tooling have a fluency gap. The level depends on other dimensions; fluency is its own dimension.

### When fluency is the limiting factor

Sometimes an engineer is strong on every dimension except AI-tooling fluency. The honest call:

- L3 → L4 with weak AI tooling fluency: usually deferred. The L4 bar requires fluency; promotion without it sets the wrong precedent.
- L4 → L5 with weak AI tooling fluency: same. The bar requires it.
- L5+ with weak fluency: the engineer has a genuine gap that's blocking advancement. The conversation is about whether they'll close it; if not, they cap.

The committee's job is to apply the rubric, not to make exceptions. Exceptions erode the rubric.

## Anti-patterns to watch for

### Favoritism

A committee member advocates strongly for engineers from their team or organization. Mitigation: explicit recusal protocols, cross-org representation, calibration against anchor cases.

### Level inflation

Pressure to promote more engineers each cycle to retain talent or signal growth. Mitigation: the rubric is enforced regardless; committee chair holds the line.

### Level deflation under cost pressure

Pressure to under-promote to control comp costs. Mitigation: comp implications discussed separately from leveling decisions. Leveling reflects work done; comp is a separate conversation.

### Halo effect

A strong reputation across dimensions makes the committee miss specific gaps. Mitigation: explicit dimension-by-dimension review per the rubric.

### Recency bias

Recent work weighed disproportionately. Mitigation: the packet covers 2+ quarters; committee members read full packet.

### Comparison to specific peers

"They're like Engineer X who got promoted last cycle." Comparison can be useful as anchor but not as substitute for rubric. Mitigation: anchor cases are explicit; comparisons reference the rubric.

## What the committee's output looks like

After each meeting, the chair produces:

- **Per-case decision** — promoted / deferred / declined, with brief reasoning
- **Per-case notes** — what specifically was discussed; what gaps were named for deferred cases
- **Calibration notes** — anything the committee learned about the rubric or the bar that should inform future cycles

The decisions are communicated to the engineer's manager within 1-2 business days; the manager communicates to the engineer.

## Annual rubric review

Once per year, the committee chairs (across cycles) convene for a rubric review:

- Are the criteria still right?
- Have new dimensions emerged that need explicit treatment?
- Are anchor cases still good or do they need updating?
- Are there patterns in which managers are over- or under-calibrated?

The output of the review is updates to the rubric for the next year.

## What this structure will NOT do

- Will not eliminate disagreements. Calibration is genuinely hard.
- Will not work in cultures where leadership routinely overrides the committee. Then the committee is decorative.
- Will not work without skilled committee chairs. Bad chairs produce bad decisions.
- Will not handle every edge case. New situations will arise; the committee adapts.

## Companion artifacts

- [`level-rubric.md`](level-rubric.md) — what the committee applies
- [`ai-tooling-fluency-by-level.md`](ai-tooling-fluency-by-level.md) — the new dimension to calibrate consistently
- [`promotion-conversation-script.md`](promotion-conversation-script.md) — what happens after the committee
- [`promotion-packet-template.md`](promotion-packet-template.md) — what the committee reviews
- `people/perf-reviews/` — adjacent (perf reviews, separate from leveling)
