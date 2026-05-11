# Mitigation 3 — Round-Robin Reviewer Assignment

Breaking the hot reviewer pattern. Per Ch 44 §44.5:

> Round-robin reviewer assignment. Stop letting the team self-assign to "the trusted reviewer." Auto-assign with deliberate rotation. Yes, this means some reviews are slower; the alternative is one engineer becoming a single point of failure.

## The problem

Teams self-organize around the most trusted reviewer. Engineers tag the same person; that person becomes faster (because they review more); the cycle reinforces.

After a few months:
- 2-3 engineers do 60-70% of reviews
- Other engineers do <5% each
- Knowledge concentrates
- The team's review capacity is bottlenecked on those 2-3

When one of them takes vacation, leaves, or burns out, the team's review capacity collapses. Per `detecting-burnout-symptoms.md`, this is symptom 1.

## The fix

Auto-assign reviewers with deliberate rotation. The team doesn't choose; the system chooses.

## How to implement

### GitHub native

GitHub has built-in round-robin assignment via team settings:
- Create a review team for the engineering team
- Configure the team's review request settings to "round robin"
- Engineers' PRs get assigned automatically

### CODEOWNERS-based

For path-specific routing:
- CODEOWNERS specifies the team for each path
- Round-robin within the team
- Specific reviewers can be required for specific paths (e.g., security team for auth code)

### Custom

For complex requirements:
- A bot or workflow that monitors PR opens
- Assigns based on:
  - Team membership
  - Recent review load (don't assign the engineer who just reviewed 3 PRs)
  - Path expertise (some auto-routing based on file paths)
- Posts assignment as PR review request

## What "rotation" means specifically

A simple rotation: engineers in the team are listed; each PR cycles through the list.

A weighted rotation: engineers' availability is factored in:
- On-call engineer reviews fewer (focused on incident response)
- Engineers on PTO are skipped
- New engineers are paired with mentors during onboarding

A capability-aware rotation: some engineers are auto-excluded from specific paths (e.g., the engineer who only joined 2 weeks ago doesn't get auth-code reviews).

Most teams start with simple rotation; iterate based on what doesn't work.

## When to bypass

Some bypasses are legitimate:

- **Specific expertise required**: a database migration genuinely needs the DBA's review
- **Author requests specific reviewer**: the author has worked closely with someone on this; they have the context
- **CODEOWNERS specifies**: path-specific reviewers per CODEOWNERS

These bypasses are fine. The discipline is preventing the default-to-trusted-reviewer pattern when nothing specific requires it.

## What rotation costs

Per Ch 44 §44.5:

> Yes, this means some reviews are slower; the alternative is one engineer becoming a single point of failure.

Specific costs:
- Some PRs go to engineers who are slower at review
- Some PRs go to engineers without specific path expertise
- Average time-to-first-review may increase initially
- Quality may dip slightly during the transition

These costs are real. The benefits (capacity distribution, knowledge spread, no SPOF) exceed them.

## What rotation enables

Beyond avoiding burnout:

### Knowledge distribution

When everyone reviews everything, everyone learns the codebase. Junior engineers see senior patterns; senior engineers see what juniors are working on.

### Mentorship through review

Senior engineers' review comments become teaching moments for junior engineers (when juniors review senior PRs). The reverse also: juniors asking questions surfaces context juniors need.

### Reduced concentration risk

If 70% of review knowledge concentrates in 2-3 people and one of them leaves, the team has a real capability gap. Distributed review reduces this risk.

### Cultural alignment

When every engineer reviews work across the team, the team's review standards stay consistent. No "this engineer's reviews are stricter than that one's" pattern.

## Common implementation issues

### Rotation produces low-quality reviews

Engineers who haven't been doing reviews suddenly do many. Quality dips.

Mitigation: pair rotation with the AI reviewer subagent (per [`mitigation-1-ai-reviewer-subagent.md`](mitigation-1-ai-reviewer-subagent.md)). The subagent catches obvious issues; the human focuses on substantive ones.

### Rotation skips junior engineers

The system rotates among "senior enough" engineers; junior engineers are exempted. The hot reviewer pattern persists in a smaller group.

Mitigation: include junior engineers in rotation, with appropriate scope (Tier-3 work; not security-sensitive paths). The mentorship through review is part of the value.

### Rotation creates queue depth

Engineers who are slow reviewers now have more PRs in their queue. Time-to-first-review climbs.

Mitigation: complementary mitigations. Throughput cap (per `mitigation-6-throughput-cap.md`); PR size limits; AI subagent. Don't rely on rotation alone.

### Rotation is gameable

Engineers self-assign to PRs they prefer to review (easier ones). The auto-assignment becomes performative.

Mitigation: enforce mechanically. The auto-assignment is the requirement; opt-out requires justification.

### Specific expertise gets bypassed too often

Many PRs claim "this needs specific expertise" to avoid rotation. The rotation rarely happens.

Mitigation: spot-check expertise claims. Are they real? If most PRs claim expertise needed, the bar is too low.

## Communicating the change

Implementing round-robin is a culture change. Communicate explicitly:

- Manager/tech lead announces: "We're moving to round-robin reviewer assignment to address review distribution."
- Specific date for the change
- Acknowledgment of trade-offs ("reviews may be slightly slower; in exchange we get sustainable review capacity")
- Expected outcomes
- Specific check-in date (typically 60-90 days) to assess

If the change isn't communicated, engineers feel it as imposed and route around.

## Tracking the change

Metrics to watch:

- **Reviewer concentration**: top 3 reviewers' share of total reviews
- **Time-to-first-review**: median and 90th percentile
- **Time-to-merge**: median and 90th percentile
- **Review depth signal** (qualitative): are reviews still substantive?

Healthy progression after rotation rolls out:

- Concentration drops (top 3 share goes from 65% to 40-50%)
- Time-to-first-review climbs initially, then stabilizes
- Time-to-merge holds steady or improves over 60-90 days
- Review depth maintained (subagent helps; team adjusts)

## Anti-patterns

### Rotation without complementary mitigations

Just rotation, no AI subagent, no size limits, no throughput cap. The burden distributes but stays high.

Mitigation: rotation is one of six. The full set works together.

### Rotation as punishment

Engineers who complain about review burden are assigned more reviews "to share the load." Backwards.

Mitigation: rotation is fair distribution, not retribution.

### Rotation visible only in dashboards

The rotation happens; the team's lived experience is unchanged. No visibility into who's reviewing what.

Mitigation: review distribution metrics shared with the team. Engineers see the change in real numbers.

### Rotation that creates gridlock

Engineers waiting on each other for reviews. Nobody's PR moves.

Mitigation: cross-rotation if a team is too small. Or a "review one PR for every PR you have in flight" norm.

## Companion artifacts

- [`mitigation-1-ai-reviewer-subagent.md`](mitigation-1-ai-reviewer-subagent.md) — adjacent
- [`mitigation-2-pr-size-limits.md`](mitigation-2-pr-size-limits.md) — adjacent
- [`mitigation-6-throughput-cap.md`](mitigation-6-throughput-cap.md) — adjacent
- [`detecting-burnout-symptoms.md`](detecting-burnout-symptoms.md) — symptoms this addresses
- Ch 44 §44.5 mitigation 3 — source
