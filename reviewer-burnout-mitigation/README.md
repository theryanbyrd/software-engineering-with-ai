# Reviewer Burnout Mitigation

Operational discipline for what Ch 44 §44.5 calls "the silent threat" — the senior-engineer review burden in AI rollouts. Direct implementation of Chapter 44 §44.5 of [_Software Engineering with AI: A Practical Handbook for the Claude Code Era_](https://www.linkedin.com/in/ryanbyrd) by Ryan Byrd.

The book's framing:

> The single most consistent complaint from senior engineers in mid-size AI rollouts in 2026: review burden has gone up, not down. The volume of PRs increased. The cognitive load per PR did not decrease in proportion. The "hot reviewer" problem (one or two engineers reviewing most PRs because they're trusted) intensified.
>
> — Ch 44 §44.5

This folder operationalizes the six mitigations from §44.5.

## What's in here

| File | Purpose |
|---|---|
| [`README.md`](README.md) | Overview, the symptoms, the six mitigations |
| [`detecting-burnout-symptoms.md`](detecting-burnout-symptoms.md) | The five symptoms from §44.5 and how to spot them |
| [`mitigation-1-ai-reviewer-subagent.md`](mitigation-1-ai-reviewer-subagent.md) | The first-pass filter that saves 30-40% of human review time |
| [`mitigation-2-pr-size-limits.md`](mitigation-2-pr-size-limits.md) | Hard limits on diff size; auto-flag for split |
| [`mitigation-3-round-robin-assignment.md`](mitigation-3-round-robin-assignment.md) | Auto-assignment to break the hot reviewer pattern |
| [`mitigation-4-review-office-hours.md`](mitigation-4-review-office-hours.md) | Synchronous review windows with juniors |
| [`mitigation-5-review-work-visibility.md`](mitigation-5-review-work-visibility.md) | Making review effort visible in performance reviews |
| [`mitigation-6-throughput-cap.md`](mitigation-6-throughput-cap.md) | Capping PRs per author per week |

## The five symptoms (from Ch 44 §44.5 verbatim)

> Symptoms:
> - The same two or three names on most reviews.
> - Review queue depth growing week-over-week.
> - Reviewers reporting fatigue or resentment in 1:1s.
> - Reviewers Slack-DMing approvals to skip the public discussion.
> - Senior engineers mentioning craft loss or culture decay.

If two or more of these are present, the team has a reviewer burnout situation. The mitigations are the operational response.

## The six mitigations (Ch 44 §44.5 verbatim, in order of leverage)

1. **The AI reviewer subagent on every PR.** Not as a replacement for human review — as a first-pass filter. The subagent flags slop signatures, missing tests, and scope creep. The human reviewer reads the subagent output, then reads the diff. Net: 30-40% time saved per PR for the human, with no quality loss observed in most teams (Chapter 14 §14.3).

2. **Hard PR-size limits.** Diffs over 400 lines are auto-flagged for split. Most agent-generated diffs do not need to be 800 lines; they are because the engineer didn't decompose. Enforce decomposition.

3. **Round-robin reviewer assignment.** Stop letting the team self-assign to "the trusted reviewer." Auto-assign with deliberate rotation. Yes, this means some reviews are slower; the alternative is one engineer becoming a single point of failure.

4. **A "review office hours" pattern.** The senior reviewer holds two hours per week explicitly for synchronous review with a junior author, walking through the diff together. This is faster than async review for complex PRs and trains the junior. It also bounds the senior's review hours.

5. **Make review work visible in performance reviews.** If review judgment is a leveling criterion (Chapter 60) but reviews are not tracked or recognized, you are punishing the engineers doing the work. Track review counts, depth, and outcomes. Recognize publicly.

6. **Cap PR throughput per author per week.** Counterintuitive but effective: an engineer who ships 30 PRs/week is generating 30 review-loads. If the team's review capacity is 100 PRs/week, the math doesn't work. Some teams have moved to "you can have 4 PRs in flight at any time" as a forcing function.

## Why this matters

Per Ch 44 §44.5 closing:

> The reviewer burnout problem is the hidden cost of throughput-focused AI rollouts. Address it deliberately or it eats the program from underneath.

The pattern: AI tooling enables higher throughput per author. Total team output goes up. Review capacity doesn't scale at the same rate (each PR still requires substantive human review). Senior engineers become bottlenecks. They burn out, leave, or stop reviewing carefully — at which point quality drops and the AI tooling investment becomes net-negative.

Without explicit mitigation:
- Senior engineers do 70-80% of reviews
- Review queues grow
- Quality erodes (faster reviews, less thoughtful)
- Senior engineer attrition risk rises
- Cultural decay sets in

With explicit mitigation:
- Review burden distributes
- AI subagents catch the easy issues; humans focus on the hard ones
- Throughput caps force decomposition
- Review work is recognized and rewarded
- The system stays sustainable

## Who this is for

- **Engineering managers** running review capacity for their teams
- **Tech leads** experiencing the burden personally
- **Senior engineers** doing too many reviews
- **VP of Engineering / CTO** allocating headcount and prioritizing the platform investment
- **Platform team** building the AI reviewer subagent and PR-size enforcement

## Read first

- Ch 44 §44.5 — the source section
- Ch 22 — review patterns generally; the seven slop signatures
- Ch 14 §14.3 — the AI reviewer subagent
- `failed-one-shot-triage/` — adjacent (some review burden comes from review of failures)
- `cost-discipline-runbook/cost-attribution-per-pr.md` — adjacent (per-PR cost; review minutes adjacent metric)

## What this folder WILL do

- Make the burnout problem visible
- Provide the six concrete mitigations from the book
- Establish the discipline of measuring review burden
- Give engineers and managers shared language ("we're hitting the burnout pattern")

## What this folder will NOT do

- Will not eliminate review work. Review is real engineering; the goal is sustainable, not absent.
- Will not work without leadership backing. The throughput cap and round-robin assignment require leadership commitment.
- Will not work in cultures that privilege "shipping fast" over sustainability. Cultural alignment is upstream.
- Will not eliminate hot reviewer dynamics. Some engineers will always be in higher demand; the goal is to bound the burden, not eliminate the gradient.

## How this folder fits with adjacent material

| Need | Where to look |
|---|---|
| Building the AI reviewer subagent | `subagents/` |
| Slop signature detection (subagent input) | Ch 22 §22.2; `governance/hooks/slop-detector.py` |
| Per-PR cost tracking (review minutes adjacent) | `cost-discipline-runbook/cost-attribution-per-pr.md` |
| Review patterns | Ch 22 |
| Performance review integration | `promotion-and-leveling-rubric/` |
| Triage data (some review pain comes from failures) | `failed-one-shot-triage/` |

## Implementation order

The six mitigations have different costs and different leverage. Suggested implementation order for a team experiencing burnout:

1. **AI reviewer subagent** (highest leverage, weeks 1-4) — reduces every reviewer's per-PR time
2. **PR size limits** (weeks 2-4) — forces better decomposition; mechanical enforcement is straightforward
3. **Round-robin assignment** (weeks 4-6) — distributes the burden more evenly
4. **Throughput cap** (weeks 4-8) — controversial but addresses the volume side
5. **Review office hours** (weeks 4-6) — bounded structured time with juniors
6. **Performance review integration** (next review cycle) — recognition; cultural

Mitigations 1, 2, 3, 5 are platform/process work. Mitigations 4, 6 are leadership work.

## The core principle

Per Ch 44 §44.5:

> Address it deliberately or it eats the program from underneath.

Burnout doesn't fix itself. AI tooling makes the dynamic worse, not better. Without the mitigations, the team's most valuable engineers leave or stop being effective.

The mitigations have real costs (slower reviews; more friction). They're worth it.

## Companion artifacts

- `subagents/` — adjacent (AI reviewer)
- Ch 22 §22.2 — slop signatures (subagent input)
- `failed-one-shot-triage/` — adjacent
- `promotion-and-leveling-rubric/` — adjacent
- Ch 44 §44.5 — source
