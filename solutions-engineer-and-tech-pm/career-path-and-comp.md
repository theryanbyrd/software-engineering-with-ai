# Career Path and Compensation

How SE and TPM tracks integrate with the engineering ladder. The operational implementation of Ch 42 §42.5's principle:

> The implication: these roles are becoming part of the engineering competency ladder, not adjacent to it. Hire and compensate accordingly.

## The principle

**SE and TPM levels map directly to engineering levels.** Same comp bands, same calibration, same expectations of trajectory. An SE3 is at the same comp as an L3 engineer; an SE4 at L4; an SE5 at L5. Same for TPM.

This is meaningfully different from how most companies have historically structured these tracks, where SE and TPM had their own bands (often lower than equivalent engineering levels). The historical structure is a hiring liability in 2026.

## The level map

| Level | Engineering | Solutions Engineer | Technical PM |
|---|---|---|---|
| L3 | Engineer (~18 months in) | SE3 | TPM3 |
| L4 | Senior Engineer | SE4 (Senior SE) | TPM4 (Senior TPM) |
| L5 | Staff Engineer | SE5 (Staff SE) | TPM5 (Staff TPM) |
| L6 | Senior Staff | SE6 (Principal SE) | TPM6 (Principal TPM) |
| L7+ | Distinguished / Fellow | (rare) | (rare) |

L3 is realistic for SE and TPM but not common. Most SE and TPM hires are at L4+. This is consistent with the historical pattern that SE/TPM are mid-career roles rather than entry points.

## Compensation parity

Specific numbers are company-specific. The principle: an SE4 and an L4 engineer at the same company are paid equivalently — base, equity, bonus.

Expected first-time discovery for most companies: your existing SE and TPM bands are 10-25% below your engineering bands at equivalent levels. The correction is to bring them up. This is uncomfortable for finance; it's necessary for retention.

## Career mobility

The principle: **mobility is the default, both directions.** An SE who wants to move to product engineering can; an engineer who wants to move to SE can. Same for TPM.

### SE → engineering

The most common transition. SEs with 2-3 years of customer-facing engineering work often want to move to product engineering — fewer customer meetings, more sustained engineering depth.

The mechanics:
- The SE talks to the manager of the engineering team they want to join
- Existing technical bar applies; the SE goes through a (usually shortened) interview process
- If hired, the SE moves at the same level (SE4 → L4)
- Comp is unchanged
- 30-60 day transition period for handoff of customer relationships

What works: SEs moving to teams adjacent to their customer work. Their domain knowledge transfers.
What doesn't: SEs trying to leap to a wholly unfamiliar domain. The engineering bar is met but the contextual knowledge has to rebuild.

### Engineering → SE

Less common but valuable. Senior engineers (L5+) sometimes want to move to SE — more variety, more customer interaction, often less on-call.

The mechanics:
- The engineer talks to the SE manager
- A short evaluation: can they handle the customer dimension? Conversation with a customer (with appropriate framing), conversation with a salesperson
- Move at same level (L5 → SE5)
- Comp unchanged
- 60-90 day ramp on customer-facing skills if needed

This is a great move for senior engineers approaching burnout. The variety reset can extend a career meaningfully.

### TPM → engineering management

Common. Senior TPMs (TPM4+) sometimes want to move to engineering management — combining their cross-functional skill with people leadership.

The mechanics:
- TPM works with their current manager and the EM track manager
- Some companies require an EM-track interview; others treat it as an internal transition
- Move from TPM4 to EM-equivalent level
- Comp adjusted to EM band (sometimes higher, sometimes equivalent)
- 90-day ramp typically with an experienced EM mentor

What works: TPMs with strong cross-functional discipline who already operate at the manager-of-manager interface.
What doesn't: TPMs who want to escape the discovery dimension. EM has its own discovery (one-on-ones, team problems) and is not relief from people work.

### TPM → product leadership

The other common path. Senior TPMs move to Director / VP of Product roles.

The mechanics:
- Standard product-leadership interviewing
- The technical depth from the TPM role becomes the differentiator vs. non-technical PM candidates
- Move into the product leadership track at appropriate level

### Engineering → TPM

Rare but real. Engineers who want to do more strategy and discovery work, less individual-contributor coding.

The mechanics:
- Conversation with the TPM manager
- Often needs to demonstrate the strategy/discovery muscle, which engineering doesn't always exercise
- Move at same level
- 90-day ramp

The harder transition. Most engineers who say they want this end up unhappy when the actual TPM job involves significant amounts of writing specs, running meetings, and mediating between functions. Some thrive. Calibrate carefully.

### IC career through Principal

The principle: SE and TPM tracks both go through L6 / Principal level. The ceiling is not L4.

For SE: SE6 / Principal SE roles exist for the SEs who want to remain customer-facing, IC, and senior. They tend to be deeply technical, deeply customer-relationship-skilled, and the resource the company sends to the hardest accounts.

For TPM: TPM6 / Principal TPM roles exist for the TPMs who want to remain IC and senior. They tend to own the most strategic product surfaces, with significant cross-functional influence without people management.

These levels are rare. Most companies have 1-3 Principal SEs and 1-3 Principal TPMs. They are deeply impactful and well-compensated.

## Performance review structure

The principle: use the engineering perf review structure. SE and TPM are not on a separate review system.

The artifacts in `people/perf-reviews/` apply. Adaptations:

### For SE

The "harness contribution" criterion in `people/perf-reviews/harness-contribution.md` is replaced or augmented with **customer-engagement contribution**: did the SE's work in customer environments produce reusable assets, integration patterns, or feedback that improved our product?

The "code review" dimension is reframed as **customer-environment code review**: did the SE catch issues in customer integrations the customer's team would have missed?

### For TPM

The "harness contribution" criterion is replaced or augmented with **spec contribution**: did the TPM's specs ship features that worked, or did the specs require significant rework during implementation?

The "code review" dimension is replaced with **PR / spec review**: did the TPM's reviews of engineering work surface meaningful issues, or were they rubber-stamps?

## Hiring loop calibration

Use the dedicated rubrics:

- [`se-interview-rubric.md`](se-interview-rubric.md) for SE
- [`tpm-interview-rubric.md`](tpm-interview-rubric.md) for TPM

Both rubrics calibrate to the same bar as the engineering interview rubrics in `people/interview-rubrics/` for the same level. An SE4 hire has the same fundamental technical bar as an L4 engineer hire; the differences are in the customer/spec/strategy dimensions tested in the SE/TPM-specific rounds.

## What this means for your existing team

If you're updating from a historical SE/TPM track to this structure, expect:

### The good

- Retention improves. SEs and TPMs who were on a slower-paid track stop leaving for engineering roles at competitors.
- Hiring quality improves. The candidates you attract have stronger engineering backgrounds because the comp is competitive.
- Internal mobility unlocks. Engineers who'd been stuck see SE and TPM as real options.

### The friction

- **Comp adjustments.** Some SEs and TPMs will need raises to match equivalent engineering levels. The CFO will not love this.
- **Calibration disagreements.** Some existing SEs may not be at the level they thought they were when measured against the engineering ladder. Have honest conversations.
- **Title changes.** "SE" titles may need clarification (Senior SE vs. SE4 — what's the difference?). Consider unified titles.
- **Cross-functional confusion.** Customers and partners who know your SEs by name may be confused by title changes.

The friction is real. The alternative — keeping the historical structure — produces compounding talent loss. Most companies that have made this transition report the friction was worth it within 12-18 months.

## What to do this quarter if you're updating

Three concrete actions:

1. **Audit current SE and TPM comp against engineering bands at equivalent levels.** Identify the gaps.
2. **Pick the most affected role and update first.** Don't try to update both simultaneously; pick the one with worse retention or hiring difficulty.
3. **Communicate to the team transparently.** "We're updating the comp structure to match engineering. Here's why. Here's what changes for you specifically."

The transparent communication is the most important. Surprise comp restructuring is corrosive even when it's a raise.

## What this will NOT do

- Will not work in companies where engineering is itself underpaid relative to market. Fix that upstream first.
- Will not work without leadership commitment. The CFO and VPE need to be aligned that this is the structural change.
- Will not eliminate friction with sales / GTM teams that have their own SE comp structure. Some negotiation needed there.

## Companion artifacts

- [`solutions-engineer-jd.md`](solutions-engineer-jd.md)
- [`technical-product-manager-jd.md`](technical-product-manager-jd.md)
- [`se-interview-rubric.md`](se-interview-rubric.md)
- [`tpm-interview-rubric.md`](tpm-interview-rubric.md)
- [`when-this-stops-being-a-separate-role.md`](when-this-stops-being-a-separate-role.md)
- `people/career-ladder/` — the engineering ladder this maps to
- `people/perf-reviews/` — review structure
- Ch 42 §42.5 — the source
