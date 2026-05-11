# Mitigation 4 — Review Office Hours

The synchronous review pattern. Per Ch 44 §44.5:

> A "review office hours" pattern. The senior reviewer holds two hours per week explicitly for synchronous review with a junior author, walking through the diff together. This is faster than async review for complex PRs and trains the junior. It also bounds the senior's review hours.

## What office hours are

A weekly two-hour block on the senior reviewer's calendar, dedicated to synchronous review with junior authors. The author brings their PR; the senior walks through it with them in real time.

This is not:
- General "ask me anything" office hours
- Pair programming on new code
- Code review training in the abstract

This is:
- Synchronous review of specific PRs the junior has open
- The senior reading the diff with the author present
- Real-time questions and discussion

## Why this works

### Faster than async for complex PRs

For a complex PR, async review involves multiple round trips:
- Reviewer leaves comments
- Author addresses them
- Reviewer re-reads
- More comments
- Etc.

Each round trip has latency (hours to days). A complex PR might take 5-10 round trips over a week.

Synchronous review compresses this. Author and reviewer go through the diff together; questions are asked and answered in real time. A 90-minute sync session can replace a week of async back-and-forth.

### Trains the junior

The senior's reasoning is visible. The author sees:
- What the senior looks at first (often: tests; or the boundary changes)
- What questions the senior asks
- What the senior considers acceptable vs concerning
- How the senior thinks about trade-offs

This is mentorship through review, made explicit. Async review hides the reasoning; synchronous review surfaces it.

### Bounds the senior's hours

The two-hour block is the budget. Outside the block, the senior reviews on their normal cadence (which, after the office hours rolls out, often becomes much smaller — the complex PRs that consumed the most time are now handled in the block).

The senior knows: "Tuesday 2-4pm is my review time. Other reviews fit my normal flow."

## Scheduling

### When to schedule

A specific recurring time. Common patterns:
- Tuesday or Wednesday afternoon (mid-week; engineers have made progress; not Friday rush)
- 2-4pm or 3-5pm (post-lunch; before end-of-day)
- 90-120 minutes (long enough for 1-2 substantive PRs; short enough to maintain focus)

Avoid Mondays (engineers haven't progressed yet) and Fridays (people leaving early).

### Booking the slot

The author books a 30-60 minute slot within the office hours block. They:
- Open the PR before the slot
- Add a brief description: "I want to walk through the migration logic in this PR"
- Confirm with the senior that the slot works

The senior may have multiple authors in the block (3 × 30 minutes); or one author for the full two hours on a complex PR.

### Cadence

Weekly is the recommended cadence. If the senior's load is too high for weekly, every-other-week is acceptable. Less than that and the discipline degrades.

### Opt-in or required

For junior authors, opt-in is the default. The senior advertises the office hours; juniors book when they want.

For specific PR types (large migrations, security-sensitive changes), the office hours review may be required. CODEOWNERS or PR templates can specify.

## What happens in the session

A typical 60-minute session:

### Minutes 0-5 — Context

Author summarizes the PR:
- What it does
- Why this approach
- What they're worried about

The senior reads the spec / ticket if they haven't already.

### Minutes 5-40 — Walk through the diff

Author drives; senior asks questions:
- "Why this pattern?"
- "What happens if input is null?"
- "How does this interact with X?"

The senior reads the code with the author present. Questions are answered in real time. The author updates code in real time if needed (small fixes; not full rewrites).

### Minutes 40-55 — Substantive discussion

The senior raises larger concerns:
- "I think this approach has a scalability issue"
- "The contract here doesn't match how the rest of the system handles this"
- "Have you considered Y?"

Discussion. The author may agree (and plan changes); may push back (and explain reasoning); may disagree productively.

### Minutes 55-60 — Wrap

Specific action items:
- "Before merge: add tests for X, address Y"
- "After merge: open follow-up ticket for Z"
- "Approved as is"

The senior leaves a comment summarizing the office hours review on the PR.

## What good office hours look like

Healthy:
- The block is consistently used (>80% of weeks)
- Junior authors come prepared (PR is open; they have questions)
- Senior comes prepared (has read the spec at minimum)
- Sessions produce substantive review (not just rubber-stamping)
- Async review queue stays manageable (the office hours absorbs the heaviest reviews)

Concerning:
- Block is rarely used; senior cancels for other priorities
- Junior authors come unprepared; sessions feel like the senior reading code cold
- Sessions feel like meetings ("status updates"); not real review
- Async queue still grows (office hours isn't displacing the queue)

## Common implementation issues

### Senior cancels frequently

Other priorities consume the block. Office hours degrade.

Mitigation: leadership commitment. The block is on the senior's calendar with the same protection as customer commitments.

### Junior authors don't book

Office hours exist; nobody uses. Maybe the juniors don't know; maybe they're intimidated; maybe they prefer async.

Mitigation: tech lead actively books juniors for their first session. After 2-3 sessions, they're comfortable booking themselves.

### Sessions become unstructured

The 60-minute slot turns into a general engineering conversation. The PR review doesn't happen.

Mitigation: agenda is the diff. Senior keeps the focus on the code; broader topics get separate slots.

### Office hours used as escape hatch

Authors avoid normal async review by routing everything to office hours. The senior's block is overbooked.

Mitigation: office hours are for specific cases (complex PRs, junior authors, specific learning opportunities). Not a substitute for async review.

### Senior's review style isn't mentorship-friendly

Senior reviews aggressively; junior feels attacked. Office hours becomes a stressful experience; juniors stop booking.

Mitigation: the senior's review style is part of the leadership discipline. If the senior can't do mentorship-friendly review, this mitigation isn't right for that senior.

## Anti-patterns

### Office hours without bounded time

The senior holds office hours but extends to whatever the queue requires. Defeats the bound on senior's hours.

Mitigation: the two-hour block is the budget. If the queue exceeds, the queue waits or routes to others.

### Office hours for everyone

The senior holds office hours for the whole team. Becomes a synchronous review queue without bound.

Mitigation: focus on specific cases (junior authors; complex PRs; specific learning opportunities). The default review path stays async.

### Office hours without commitment

The block is on the calendar; engineers know it's optional for the senior. The senior cancels regularly.

Mitigation: same protection as any other commitment. Cancellations are exceptions, not norms.

### Office hours that displace senior's own work

The two hours is real; the senior's other commitments don't shrink to compensate. Senior burns out from the office hours specifically.

Mitigation: the two hours is in the senior's allocation, not in addition to it. If senior was doing 10 hours of review/week, the two hours is 2 of those 10 — the rest is async.

### Office hours that trains the senior, not the junior

The session becomes about the senior's questions and the junior's defensive answers. No teaching happens.

Mitigation: the senior frames as teaching ("here's what I look at first"; "here's why I'd write it differently"). The senior's questions are pedagogical, not evaluative.

## Bounding the senior's hours

This is the under-discussed value of office hours. Per Ch 44 §44.5: "It also bounds the senior's review hours."

The mechanism:
- Without office hours: complex PRs from juniors absorb 5-10 hours of senior time across async back-and-forth
- With office hours: those PRs absorb the 2-hour block (sometimes split across multiple PRs)
- Senior's total review time drops; juniors get more direct mentorship

The senior trades async fragments (5-10 hours/week of context-switching) for a focused block (2 hours of focused work). Total time decreases; quality increases.

## Companion artifacts

- [`mitigation-1-ai-reviewer-subagent.md`](mitigation-1-ai-reviewer-subagent.md) — adjacent (subagent reduces async time)
- [`mitigation-3-round-robin-assignment.md`](mitigation-3-round-robin-assignment.md) — adjacent
- `junior-trajectory/pair-driving-guide.md` — adjacent (general pair patterns)
- `promotion-and-leveling-rubric/` — adjacent (review work visibility)
- Ch 44 §44.5 mitigation 4 — source
