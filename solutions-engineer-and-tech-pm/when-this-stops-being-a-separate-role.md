# When This Stops Being a Separate Role

The 2027 question. SE and TPM roles are converging with engineering; they are not yet merged. This document describes the signals that say it's time to converge — and the counter-signals that say keep them separate. It's the strategic frame the rest of the convergence material assumes.

## The book's framing

> The implication: these roles are becoming part of the engineering competency ladder, not adjacent to it. Hire and compensate accordingly.
>
> — Ch 42 §42.5

The book is direct that the roles are *part of* the engineering ladder. It is not direct about whether they remain *separate* roles within the ladder. That's the operational question.

## The current state (mid-2026)

For most mid-size companies in 2026:

- **SE remains a separate role.** The customer-relationship dimension is real and persistent. SEs have a customer rolodex, customer-context memory, and customer-side trust that takes years to build and doesn't transfer cleanly to product engineering.
- **TPM remains a separate role.** The product-strategy and customer-discovery dimensions are real and persistent. TPMs run discovery, build theses, defend them — work that engineering does not typically do well in addition to engineering.
- **Both roles are absorbing engineering competencies.** The bar for both is rising; the JDs are converging with senior engineering JDs. Comp is converging too.

The honest forecast: **both roles continue as separate functions through 2027 in most companies, but the lines blur further.** A meaningful minority of mid-size companies will experiment with merging one or both roles; most will not.

This is not a hot take. The convergence is in motion; the merge is not.

## The signals that say "time to converge"

### For SE → engineering

Signals it might be time to fold SE into engineering at your company:

1. **Your SEs are doing >70% engineering and <30% customer-relationship work.** The customer-facing dimension has shrunk to deal-cycle support. Most of the work is integration coding.
2. **Customer Success or Sales has absorbed the relationship dimension.** SE doesn't own customer relationships anymore; CS does. SE has become a specialty integrations engineer.
3. **Your product has matured to the point that POCs are routine and predictable.** Less novel customer work; more "configure the standard integration." The complexity has moved out of SE work.
4. **You're losing SE candidates because they want eng-track careers and your SE track caps out at L4-equivalent.** The career ceiling is making SE recruiting harder than engineering recruiting.
5. **Your engineering team is itself doing customer-facing work as part of the senior IC track.** The L5-L6 engineers regularly run customer integrations. The "SE" function is duplicating their work.

If 3+ of these are true, run the merge analysis.

### For TPM → engineering

Signals it might be time to fold TPM into engineering at your company:

1. **Your TPMs are spending >60% of time writing executable specs and <40% on strategy/discovery.** The strategy/discovery dimension has shrunk; the work has become "spec engineer."
2. **Discovery has been absorbed by senior product designers, customer success, or engineering managers.** The discovery dimension lives elsewhere; TPM is left with execution.
3. **Your TPMs are routinely shipping T2 work themselves with engineering review.** Light engineering has become medium engineering. The boundary has shifted.
4. **You're losing TPM candidates because the comp gap with engineering is widening.** Comp at the equivalent level for engineering is meaningfully higher; TPMs are leaving for engineering roles.
5. **Your product strategy work has moved up to a single Head of Product or VP Product.** Individual TPM contributors aren't owning strategy; they're executing on someone else's. The strategy dimension lives at one level only.

If 3+ of these are true, run the merge analysis.

## The signals that say "keep them separate"

### For SE

Signals SE remains a distinct function:

1. **Your customers' technical buyers expect SE engagement.** Customer-side procurement requires a "your SE" relationship for trust and continuity.
2. **Your product is novel enough that POCs are creative engineering work that needs customer context.** The integration shape varies meaningfully by customer.
3. **Your sales motion is enterprise-heavy with long sales cycles.** SE is integral to deal-making; folding into engineering loses this capability.
4. **Your SEs have customer relationships that span multiple deals.** A 5-year SE who's done 12 customer engagements has institutional value engineering can't replicate.
5. **Your engineering team does NOT regularly do customer-facing work.** Folding SE into engineering would force engineering into work the team isn't structured for.

If 3+ of these are true, hold separate.

### For TPM

Signals TPM remains a distinct function:

1. **Your TPMs own real product strategy.** They build theses, defend them, change roadmaps. Strategy is not concentrated at the Head of Product level.
2. **Your discovery is hard.** Customer needs are not obvious; the work of figuring out what to build is itself a craft and not absorbed elsewhere.
3. **Your engineering team doesn't run customer interviews.** TPM is the bridge; folding into engineering loses the customer-discovery channel.
4. **Your roadmap requires sustained cross-functional negotiation.** The PM craft of holding the org together around priorities is real and not absorbed elsewhere.
5. **Product designers are not embedded enough to absorb the discovery dimension.** Some companies have very strong product design teams; in those, TPM might be redundant. In most, design and TPM are complementary.

If 3+ of these are true, hold separate.

## How to actually decide

The convergence/separation question is not a feeling. Run the analysis:

### Step 1 — Time-tracking audit

For two weeks, ask the SEs (or TPMs) to log their time in 30-minute buckets. Categorize:

For SE:
- A: Pre-sales technical work (discovery, demo, POC)
- B: Customer-environment coding
- C: Spec workshops and documentation
- D: Customer relationship maintenance (regular check-ins, business-side work)
- E: Internal coordination (handoffs, roadmap input)
- F: Other (administrative, meetings)

For TPM:
- A: Discovery (customer interviews, market research)
- B: Strategy (theses, prioritization, roadmap)
- C: Spec writing and refinement
- D: Cross-functional coordination (engineering, design, leadership)
- E: Light engineering (your TPM shipping T1/T2 work)
- F: Other

The honest distribution surfaces what the role actually is. The job description is what you wrote; this is what's happening.

### Step 2 — Career data audit

- How many SEs have left in the past 24 months? Where did they go?
- How many SEs in the past 24 months were promoted to the equivalent of L5+? (And do you have an L5+ SE level?)
- Same questions for TPM.

If the answer is "they're leaving for engineering roles at higher comp," your separate-track is leaking talent.

### Step 3 — Comp benchmark

- What's an L4 SE comp at your company? What's an L4 engineer? Are they the same?
- Same for TPM.

If the gaps are >15-20% at equivalent levels, the separate track is undercompensating, and the natural correction is to merge.

### Step 4 — Customer / partner conversation

If you're considering merging, talk to 5-10 customers (or sales partners, account executives — the people on the receiving end of SE work). Ask:

- "Who do you call at our company when you have a technical question about our product?"
- "What's the value of having a dedicated SE relationship vs. a rotating engineering presence?"
- "Would you be comfortable if we rotated engineers through your account instead?"

If customers are indifferent, you can probably merge. If customers value the SE relationship specifically, hold separate.

### Step 5 — Make the decision

Combine the signals:

- Time-tracking shows >70% engineering work AND career data shows talent loss AND comp gap is significant AND customers are indifferent → strong signal to merge
- Time-tracking shows balanced work OR career data is healthy OR customers value the relationship → strong signal to hold separate
- Mixed signals → hold separate this year; revisit annually

## What "merge" actually looks like (if you go that direction)

Folding SE or TPM into engineering is not a JD update. It's a real organizational change.

For SE → engineering:
- The SE function becomes a customer-facing-engineer specialty within the engineering ladder
- The SE-specific career levels are mapped onto engineering levels (SE3 → L3, SE4 → L4, etc.)
- SEs with strong customer relationships rotate between customer-facing and product-facing work
- The "Solutions Engineer" title may go away or may be retained as a specialty
- Customer relationship continuity is preserved through Customer Success or via account-aligned engineering rotations
- Comp moves to engineering bands (likely up for most SEs)

For TPM → engineering:
- The TPM function becomes a "product engineer" specialty within engineering or a "technical PM" specialty within product
- The discovery dimension either moves to engineering managers, product designers, or to a dedicated discovery team
- TPMs with strong strategy skills move to senior product roles or engineering management
- TPMs with strong execution skills move to senior IC engineering tracks
- Comp moves to engineering bands

This is significant change. Don't take it lightly. The cost of an aborted merge is real — the people you lose, the customers you confuse, the engineering culture that absorbs an unfamiliar function.

## What to do if signals say "keep separate"

The harder discipline. The convergence is real even if the merge isn't.

- Update JDs annually to keep up with the rising bar (the templates in this folder are calibrated for mid-2026; calibrate to your team)
- Update interview rubrics annually
- Calibrate comp annually against engineering bands at equivalent levels
- Provide career mobility — SEs who want to move to engineering can; TPMs too
- Resist the temptation to use SE or TPM titles as a "soft entry" to engineering for non-technical hires. The bar is higher now.

## The 2027 prediction

Honest take, knowing it will be wrong in some specifics:

- **Most mid-size companies (60-70%) will keep SE and TPM as separate roles through 2027 and beyond.** The customer and discovery dimensions will hold the line.
- **A meaningful minority (20-30%) will merge one of the two — usually TPM into engineering.** TPM has a faster convergence curve because the strategy dimension can be absorbed by Head of Product or by senior engineering managers in companies that aren't deeply discovery-led.
- **A small fraction (5-10%) will merge both** — typically smaller, more technical companies where the engineering team is already doing customer-facing work. These mergers will succeed at higher rates than the larger-company experiments.

If you're in the minority that merges, expect 12-18 months of friction. The function that's absorbed loses identity; the absorbing function takes on unfamiliar work; some people leave. The companies that pull it off do so because they had the signals lined up before merging — not because they had a strong leader who made it happen by force of will.

## What to do this quarter

Regardless of which side of the merge question you're on, three concrete actions:

1. **Run the time-tracking audit** for your SEs and TPMs. Even if you're not considering a merge, the data is useful for calibration.
2. **Run the career data audit.** Where are people going? What's the comp gap?
3. **Update one JD.** Pick whichever (SE or TPM) is more out of date and update it using the templates here. JD updates are the lightest-weight calibration discipline.

In two quarters, run the audits again. Compare.

## What this document will NOT do

- Will not give you a one-size-fits-all answer. The convergence vs. merge question is genuinely company-specific.
- Will not protect you from political pressure to merge faster than the data supports. (Or to merge slower than the data supports.) Templates can give you the analysis; the org has to make the decision.
- Will not work in isolation from broader role-level conversations. If your engineering ladder is unhealthy, fixing the SE / TPM track first won't solve the underlying issues.

## Companion artifacts

- [`solutions-engineer-jd.md`](solutions-engineer-jd.md) — the SE JD
- [`technical-product-manager-jd.md`](technical-product-manager-jd.md) — the TPM JD
- [`career-path-and-comp.md`](career-path-and-comp.md) — how the roles map to engineering levels
- `people/career-ladder/` — the engineering ladder this is converging with
- Ch 42 §42.5 — the source
