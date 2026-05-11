# Mitigation 6 — PR Throughput Cap

The volume control. Per Ch 44 §44.5:

> Cap PR throughput per author per week. Counterintuitive but effective: an engineer who ships 30 PRs/week is generating 30 review-loads. If the team's review capacity is 100 PRs/week, the math doesn't work. Some teams have moved to "you can have 4 PRs in flight at any time" as a forcing function.

The most controversial of the six mitigations. Implement when other mitigations aren't sufficient.

## Why caps matter

Without a cap:
- AI tooling enables high-throughput engineers (an engineer can ship 20-30 PRs/week)
- High-throughput engineers generate 20-30 review-loads each
- A team of 5 engineers, with 2 high-throughput engineers, can generate 60-80 PRs/week
- Review capacity (with all other mitigations) is maybe 100-120 PRs/week
- The math breaks
- Review queue grows; reviewer fatigue rises

The cap reverses the asymmetry. Each engineer's volume is bounded; total team volume is bounded; review capacity matches.

## The 4-in-flight pattern

Per Ch 44 §44.5: "you can have 4 PRs in flight at any time."

"In flight" means: open PR that isn't merged or closed. The cap forces:
- Engineers can't open a 5th PR until they merge/close one of the 4
- Forces engineers to drive PRs to completion (rather than starting many)
- Distributes work over time (engineers ship 4 today, then can't ship more until reviews complete)

### Why 4 specifically

- 4 is small enough to feel like a constraint
- 4 is large enough to allow real work (an engineer can have a feature, a bug fix, a refactor, and a test improvement all in flight)
- Specific number is arbitrary; teams adjust (3 is tighter; 5 is looser)

Calibrate based on team review capacity.

## Other patterns

### PRs-per-week cap

Engineer can open up to N PRs per week (e.g., 8). After 8, they wait for next week.

Variation: PRs-per-author-per-day cap (e.g., 3). Smooths the spikes.

### Combined caps

In-flight + per-week. Belt and suspenders.

### Per-team cap rather than per-engineer

The team as a whole can have N open PRs. Engineers self-coordinate within the team.

This works for small teams; harder at scale.

## What counts as "in flight"

Definition matters:

- **Open PR that's not merged or closed**: typical definition
- **Open PR that's awaiting review** (not yet reviewed): tighter definition
- **Open PR that's awaiting author action** (post-review-comments): looser definition

The book's framing is the broadest: any open PR. Adjust based on what the team's actual bottleneck is.

## Why counterintuitive

Engineers are trained to "ship more = better." The cap explicitly says: ship less.

Pushback patterns:
- "But I'm being more productive — why limit me?"
- "This will slow the team down"
- "What about urgent fixes?"

The response:
- The cap addresses team capacity, not individual capacity
- The team's bottleneck is review, not authoring
- An engineer who ships more PRs than the team can review isn't more productive — they're consuming review capacity disproportionately
- Urgent fixes have a bypass mechanism

This is a culture conversation. The math has to be visible.

## Implementation

### Mechanical (via GitHub label)

Bot or workflow that:
- Tracks open PRs per author
- Adds a label `over-cap` when an author exceeds 4 open PRs
- Optionally: blocks new PRs from that author until count drops

Rough mechanical implementation; works for most teams.

### Soft (via team norm)

Manager / tech lead announces the norm. Engineers track informally. Manager checks during 1:1s.

Lighter touch; relies on culture rather than tooling.

### Hybrid

Soft norm for most engineers; mechanical enforcement only after pattern of exceeding.

## Bypass

Some legitimate reasons to exceed:

- **Urgent fixes**: hot-fix to production; can't wait
- **Atomic decomposition**: a feature genuinely requires 6 PRs and they all need to be in flight together
- **PR awaiting external review**: PR is open but blocked on customer or external party

Bypass mechanism:
- Engineer adds label or message: `cap-bypass-justified` with reason
- Visible to team; spot-checkable

If bypass rate exceeds 10%, the cap isn't real. Tighten or address why bypasses are common.

## Side effect: forces focus

The cap has a side effect engineers often appreciate after adapting:

- Forces the engineer to focus on completing PRs rather than starting more
- Reduces context-switching (an engineer with 12 open PRs is switching constantly)
- Makes the engineer drive their PRs to merge

After 2-3 weeks, engineers often report:
- "I'm actually getting more work merged"
- "I'm focused on fewer things at a time"
- "The PRs I do open get more attention"

The throughput per merged PR may go up even as raw open-PR rate goes down.

## What good caps look like

Healthy:
- Engineers' merged-PR rate stays roughly steady (the cap doesn't hurt productivity)
- Open-PR count stays manageable
- Review queue depth stops growing
- Engineers report the cap as a positive forcing function (after initial resistance)

Concerning:
- Engineers route around the cap (bypass label routinely)
- Engineers' merged-PR rate drops substantially
- Engineer satisfaction drops
- Engineers feel the cap as punishment

## Common implementation issues

### Cap too tight

The cap is 2; legitimate work needs 3-4 in flight. Engineers feel choked.

Mitigation: 4 is the recommended starting point. Adjust based on team's actual review capacity.

### Cap with too many bypasses

Engineers add `cap-bypass-justified` to most PRs. The cap is decorative.

Mitigation: spot-check bypasses. Are they real? If most are gaming, tighten.

### Cap as performance metric

"Engineer X exceeded the cap 3 times last quarter; concerning." Backwards.

Mitigation: the cap is operational, not evaluative. Engineers exceeding occasionally is fine; it's the structural pattern that matters.

### Cap circumvented via WIP work locally

Engineers do work locally without opening PRs. The "in flight" count is artificially low; the work pile grows offline.

Mitigation: the cap addresses team review capacity. Local WIP is the engineer's choice but doesn't generate review load until pushed.

### Cap that doesn't account for PR types

Migration PRs and trivial PRs counted equally. A migration PR consumes more review capacity than a typo fix.

Mitigation: the simple cap counts all PRs equally. More complex schemes (weighted by PR type) add complexity for marginal benefit.

## Communicating the cap

Implementing this is a culture change. Communication:

- Manager / VPE announces explicitly
- Specific date for the change
- Specific cap (4 in flight)
- Bypass mechanism documented
- Acknowledge the controversy ("this is counterintuitive; here's why")
- Specific check-in date (60-90 days) to assess

If communicated poorly, the cap feels punitive. Engineers route around or push back hard.

## When to use this mitigation

Throughput cap is the heaviest of the six. Use when:

- Other mitigations have been implemented
- Review queue depth is still growing
- Engineers' open-PR counts are visibly extreme (some engineers have 10+ open PRs)
- Team review capacity is provably exceeded

If the team is functioning, the cap may not be necessary. Don't impose it preemptively.

## Anti-patterns

### Cap as the first mitigation

Implementing the cap before AI subagent, size limits, rotation. The team feels singled-out for high throughput; the easier mitigations weren't tried first.

Mitigation: cap is mitigation 6. Implement 1-5 first.

### Cap without context

The cap is announced; engineers don't understand why. They route around.

Mitigation: the math is shared. "Our team's review capacity is X PRs/week; we're generating Y PRs/week; here's why we're capping."

### Cap with no exceptions

A truly atomic decomposition (6 PRs that need to ship together) can't proceed. The cap blocks legitimate work.

Mitigation: explicit bypass for atomic decomposition. Justified bypasses are normal.

### Cap that drives engineers to game

Engineers learn to keep work local until ready, then ship 6 PRs at once. The cap is gamed.

Mitigation: the gaming pattern is itself a signal. Address upstream (why are engineers gaming?).

### Cap with no reduction in queue

The cap is implemented; review queue depth doesn't drop. Other mitigations are missing.

Mitigation: cap addresses volume; other mitigations address per-PR cost. All six together.

## Companion artifacts

- [`mitigation-1-ai-reviewer-subagent.md`](mitigation-1-ai-reviewer-subagent.md) — adjacent
- [`mitigation-2-pr-size-limits.md`](mitigation-2-pr-size-limits.md) — adjacent (size + throughput together)
- [`mitigation-3-round-robin-assignment.md`](mitigation-3-round-robin-assignment.md) — adjacent
- [`detecting-burnout-symptoms.md`](detecting-burnout-symptoms.md) — when this becomes necessary
- Ch 44 §44.5 mitigation 6 — source
