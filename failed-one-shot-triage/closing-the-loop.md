# Closing the Loop

What happens after triage. Per Ch 31 §31.5, the team that improves is the team that closes the loop on failures. Each bucket has a different resolution path.

## Why this matters

Per Ch 31 §31.5:

> A team that is stagnating sees the same Train/Opportunity mix month after month — usually because nobody is closing the loop on the failures.

Triage without resolution is theatrical. The data exists; the team feels productive about classifying it; nothing actually improves. Closing the loop is the difference between data and discipline.

## Score → no resolution; trend tracking

Score outcomes don't need resolution. They're logged for trend data. Per [`reading-the-ratios.md`](reading-the-ratios.md), Score share is one of the team's leading indicators.

What Score outcomes inform:
- Routing decisions (this work type works on Sonnet)
- Autonomy decisions (consider raising the ceiling)
- Spec patterns (this spec template worked; reuse)

What Score outcomes don't generate:
- Tickets
- Coaching
- Action items beyond the trend tracking

## Question → flag for next model review; route to humans now

### Immediate

When a failure is classified Question:
- The specific work goes to humans (or to a more capable model for the next attempt)
- The failure is logged in the Question log (per [`tracking-spreadsheet-template.md`](tracking-spreadsheet-template.md))
- Per `agent-autonomy-levels/forbidden-categories.md`, if the work is also high-stakes, that may already require human-led approach

### At quarterly model review

Per `evals-and-benchmarks-runbook/quarterly-model-lineup-review.md`:
- The Question log feeds the review
- Each Question entry is tested against new candidate models
- If a new model handles the work: routing updates; the Question becomes Score
- If no new model handles it: the Question persists; capability gap remains

### When the model upgrades

Per Ch 31 §31.5: "Question counts fall stepwise when new models drop."

The cycle:
1. Model X has capability gap Y
2. Team logs Question failures involving Y
3. Model X+1 is released
4. Team re-tests Question failures
5. Some pass on X+1 → routing updates; capability has expanded
6. Some still fail → capability gap persists

## Opportunity → legibility ticket; harness improvement

### Immediate

When a failure is classified Opportunity:
- Open a "legibility ticket" per Ch 19 §19.5
- The ticket describes what's missing and where it should live
- Assign owner (typically the team that owns the relevant module)

### What goes in a legibility ticket

Per Ch 19 §19.5, a legibility ticket is a specific harness improvement:
- Add a README to a specific directory
- Add an AGENTS.md section to a specific service
- Create a fixture for a specific test pattern
- Document an architectural decision in an ADR
- Build a skill for a repeated pattern

### Sizing

Most legibility tickets are small (1-2 hours of work). Some are larger (a full AGENTS.md for a complex service might be 1-2 days). The discipline is to make them specific and actionable.

### Owner

Typically:
- Module-specific tickets: the team that owns the module
- Cross-cutting tickets: the platform team
- Skill or subagent tickets: the platform team or skill author

### Tracking

Open Opportunity tickets are tracked in [`tracking-spreadsheet-template.md`](tracking-spreadsheet-template.md) Tab 4 (Open Opportunities). Reviewed weekly at the retro.

### When the ticket ships

The harness is improved. Per Ch 31 §31.5: "the next attempt at this kind of work succeeds." The team's Opportunity rate falls; Score rate rises.

### Common Opportunity tickets

Patterns that recur across many teams:

- **AGENTS.md in monorepo packages** — most common; the canonical "this package has its own conventions"
- **Fixtures for testing** — agent can't write tests without realistic fixtures
- **Skill for repeated patterns** — once a pattern recurs 3+ times, it's a skill candidate
- **ADR for surprising designs** — agent assumes the obvious design; the actual design has a reason
- **README in undocumented directories** — orientation that humans figured out by asking; agent can't ask

## Train → coaching loop; spec quality

### Immediate

When a failure is classified Train:
- Note the spec author (often a PM, sometimes an engineer)
- Manager schedules a 1:1 to discuss

The conversation isn't punitive. The framing: "this spec didn't give the agent enough; let's talk about what would have."

### What good Train coaching looks like

- 15-20 minutes
- Specific to the failed spec
- Walks through what was unclear
- Discusses what would have made it work
- Generalizes to spec patterns

The PM (or engineer) leaves with:
- Understanding of the specific gap
- Patterns to apply to future specs
- Examples of better specs (often from the team's archive)

### What bad Train coaching looks like

- Public callouts
- Performance review feedback
- "Your specs are bad" framing without specifics
- General lectures about spec quality

This kills the discipline. Engineers stop logging honestly; PMs stop iterating on spec quality.

### When Train concentrates

Per [`reading-the-ratios.md`](reading-the-ratios.md), if Train failures concentrate in one author:

- The 1:1 coaching becomes a series, not a one-off
- The team's ticket-writing assistant pattern (per Ch 19 §19.5) is implemented if it isn't already
- The PM uses the ticket-writing assistant routinely

If Train concentrates across many authors, the team-level intervention is:
- Ticket-writing assistant rollout
- Spec template review and iteration
- Examples library (good specs and bad specs side-by-side)

### What Train coaching produces over time

Per Ch 31 §31.5, the team's Train rate falls as:
- Specific authors improve through coaching
- Team-level patterns improve through better templates
- The ticket-writing assistant catches gaps before they reach the agent

A team that does Train coaching consistently sees the rate drop from 25-30% to 5-10% over 3-6 months.

## Cross-cutting: when resolutions don't ship

The triage system can produce action items that don't materialize:

- Opportunity tickets are opened but not assigned
- Opportunity tickets are assigned but not prioritized
- Train coaching is scheduled but doesn't happen
- Question entries pile up but the model review doesn't reference them

When this happens:
- The triage data still informs (the trend stays signal)
- But the resolution loop is broken
- Per `reading-the-ratios.md`, this is what stagnation looks like

Mitigations:
- Weekly review of open Opportunity tickets at the retro
- 1:1 coaching is on the manager's calendar, not just intended
- The quarterly model review explicitly walks the Question log
- Leadership commitment to harness investment time

## When to escalate beyond resolution

Some failures should escalate:

### Production incident

If an AI-authored failure produced a production incident, the failure goes through `incident-postmortem-templates/` rather than (or in addition to) the triage. The postmortem captures the harness deficiency separately.

### Repeated capability gap

If the same Question failure recurs across multiple model releases (the model isn't getting better at this work), it may indicate:
- The work shouldn't be automated (per `do-not-automate-catalog/`)
- The team needs to re-architect to avoid the work pattern
- The team should escalate to vendor (Anthropic, OpenAI, etc.) as a use case

### Harness gap that stays open

If an Opportunity ticket has been open for 60+ days, the gap isn't being closed. Investigation:
- Is the owner responsible for it actually able to close it?
- Is the priority right?
- Is the gap larger than initially scoped?

The triage flag the persistence; resolution is the broader engineering process.

### Train pattern that doesn't improve

If a PM has been receiving Train coaching for 3+ months and the pattern persists:
- The coaching isn't landing
- The role fit may be wrong
- Different intervention is needed (different coach; different role; etc.)

This is a manager conversation, not a triage outcome.

## Anti-patterns

### Resolution without follow-up

Tickets are opened; nobody checks if they shipped. Coaching is scheduled; nobody checks if patterns improve.

Mitigation: weekly review at the retro of open Opportunities and recent coaching outcomes.

### Resolution without ownership

Ticket is opened with "the team" as owner. Nobody specifically responsible. Doesn't ship.

Mitigation: every ticket has a named owner. If the team can't agree, the manager assigns.

### Train coaching public

Coaching happens in retro or in a public channel. PMs feel embarrassed; stop logging or stop participating.

Mitigation: 1:1, private, supportive tone.

### Question without testing

Question failures are logged but not re-tested when models update. The log just grows.

Mitigation: quarterly model review walks the Question log explicitly.

### Resolution that's too slow

Opportunity tickets take 6 months to ship. The same gaps cause repeated failures in the meantime.

Mitigation: tickets are sized small; large gaps are decomposed. Quick wins are prioritized.

## What good closing-the-loop looks like

Healthy:
- Each week's failures produce specific resolutions
- Resolutions ship within a reasonable timeline (most within 2-4 weeks)
- The team's ratios reflect the resolutions over time
- Engineers feel that their reported failures led to improvements

Concerning:
- Failures are logged but resolutions don't ship
- The same Opportunity tickets accumulate week after week
- Train coaching is scheduled but doesn't change patterns
- Engineers stop logging because nothing changes

## Companion artifacts

- [`the-four-buckets.md`](the-four-buckets.md) — the taxonomy
- [`triage-process.md`](triage-process.md) — generates the action items
- [`weekly-retro-structure.md`](weekly-retro-structure.md) — where action items are reviewed
- [`reading-the-ratios.md`](reading-the-ratios.md) — interprets the trend
- `evals-and-benchmarks-runbook/quarterly-model-lineup-review.md` — adjacent (Question reviews)
- `incident-postmortem-templates/` — adjacent (escalation path)
- Ch 19 §19.5, Ch 31 §31.5 — sources
