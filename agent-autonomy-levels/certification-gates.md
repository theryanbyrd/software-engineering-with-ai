# Certification Gates — Per Ch 44

Certifications gate autonomy access. Per Ch 44 §44.2:

> Certify access to autonomy levels. Don't let it drift. This is the single most important governance discipline in AI-native engineering.
>
> Certifications expire. Review yearly. The drift is real, and it is asymmetric: people drift up, never down, unless you actively re-certify.

This file is the operational discipline for tying autonomy access to certifications.

## The three certifications

### L1 certification — read-only-then-suggest

What it gates: ability to operate at L1 (agent suggests, human approves each edit).

What's required to earn it:
- Read CLAUDE.md, AGENTS.md for the team's primary repos
- Read the published autonomy ladder ([`autonomy-ladder.md`](autonomy-ladder.md))
- Complete one pair-driving session at L0 with a senior engineer (per `junior-trajectory/pair-driving-guide.md`)
- Demonstrate one productive L1 session (5 PRs in the new mode) with senior review

Time to earn: typically 1-2 weeks for a new engineer; less for engineers transitioning from another team.

### L2 certification — bounded autonomous task

What it gates: ability to operate at L2 (agent runs defined task end-to-end on a feature branch).

What's required to earn it:
- L1 certification held for at least 30 days
- 30+ AI-assisted PRs reviewed at L1 without a slop incident (per Ch 32 §32.4)
- Demonstrated ability to write agent-ready specs from scratch (per Ch 19)
- Demonstrated ability to recognize the seven slop signatures (per Ch 22 §22.2) in code review
- Senior engineer signs off

Time to earn: typically 6-12 weeks for an engineer who entered at L1.

### L3 certification — multi-task autonomy under supervision

What it gates: ability to operate at L3 (agent runs queue of tasks with periodic checkpoints).

What's required to earn it:
- L2 certification held for at least 90 days
- 30+ PRs at L2 without slop incident
- Demonstrated multi-agent queue management (one productive L3 session under senior observation)
- One quarter of production incidents reviewed (the engineer has read postmortems and can name patterns)
- Two senior engineers sign off (the manager and one peer-or-better senior)

Time to earn: typically 6-9 months for an engineer who started at L2.

### L4 certification

L4 is not certified per engineer; it's certified per task category at the team level. See [`autonomy-ladder.md`](autonomy-ladder.md). Individual engineers don't earn L4; the team's harness earns L4 for specific task categories (docs / tests / types only).

## How certifications work in practice

### Certification record

Each engineer has a certification record:

| Engineer | L1 cert | L2 cert | L3 cert | Last reviewed |
|---|---|---|---|---|
| @rbyrd | 2025-08-15 | 2025-11-22 | 2026-04-10 | 2026-04-10 |
| @ssmith | 2025-09-01 | 2026-01-12 | (not held) | 2026-01-12 |
| @bnewhire | 2026-04-22 | (not held) | (not held) | 2026-04-22 |

The record is visible to the team; it's not personal data, it's operational state.

### What certification access looks like mechanically

The team's tooling reads the certification record:
- Engineers without L1 certification have agent access at L0 only (read-only); the agent's permission modes won't let them go higher
- Engineers with L1 cert can configure the agent for L1 operation
- Engineers with L2 cert can run bounded autonomous tasks
- Engineers with L3 cert can run multi-task queues with the team's whitelist

The tooling enforces this; engineers can't self-promote to a higher level without certification.

### How an engineer earns the next certification

The path is structured:

1. **Engineer requests** — usually in a 1:1 with their manager. "I think I'm ready for L2; here's why."
2. **Manager reviews against criteria** — has the engineer met the bar? Specific evidence?
3. **Senior signs off** — for L2, one senior; for L3, two seniors
4. **Certification recorded** — added to the team's certification record
5. **Tooling updated** — permissions adjusted

The bar is the bar; manager doesn't push for early certification; engineer doesn't push for certification without evidence.

### Annual recertification

Per Ch 44, certifications expire. Annual review:

- Each engineer's certifications reviewed against current criteria
- Engineers who've operated at the certified level cleanly: re-certified
- Engineers who've been operating at lower levels for the year (no L2 work despite L2 cert): consider whether the cert is still active
- Engineers who've had incidents at their certified level: cert reviewed; possibly reset

### Re-certification after an incident

If an engineer is involved in an incident traced to AI authorship at their certified level, the cert may be temporarily reset:

- L2 cert holder ships an incident at L2; cert reset to L1; re-earned via the standard L1 → L2 process (which usually takes 30-60 days)
- L3 cert holder ships an incident at L3; cert reset to L2; re-earned via L2 → L3 process (90 days)

This isn't punitive. The incident shows the certification's discipline didn't translate; resetting forces re-development of the muscle.

## Why certifications matter

### Without them, drift wins

Per Ch 32 opening, drift is asymmetric: people drift up, never down. Without the recertification discipline, the team operates at the level individual engineers have drifted to, not the level the team has earned.

### They make the political conversation possible

Per Ch 44:

> The certification gates serve two purposes: they are honest signals of competence, and they are the political artifact you point to when the CEO asks "are your engineers ready for L4 autonomy?" Without them, the answer is hand-wavy. With them, the answer is a list of names and dates.

### They make raising autonomy possible

Per [`raising-and-lowering-autonomy.md`](raising-and-lowering-autonomy.md), raising the team's autonomy level requires the team's harness, discipline, and history. Certifications are the discipline component made explicit.

## Common failure modes

### Certification inflation

Managers grant certifications to retain engineers ("they'll quit if I don't certify them"). The cert becomes meaningless.

Mitigation: senior sign-off ensures the certifying manager isn't unilaterally deciding; the second senior can hold the line.

### Certification by tenure

Engineers earn certification by being on the team for X months, regardless of demonstrated discipline.

Mitigation: certification criteria are explicit and require demonstrated work, not tenure.

### Certifications that don't gate anything

Certifications are recorded but the tooling doesn't enforce them. Engineers operate at any level regardless of cert.

Mitigation: certifications must be tied to mechanical permission enforcement. Otherwise they're decorative.

### Annual review skipped

The annual recertification doesn't happen. Engineers retain L3 cert from 18 months ago; their actual operation has shifted; the cert is stale.

Mitigation: annual review is on the calendar; tied to a specific person's responsibility (typically the engineering manager).

### Cert resets seen as punitive

After an incident, the cert reset is communicated as punishment rather than discipline. Engineers feel demoted; morale suffers.

Mitigation: per the lowering-autonomy script, frame as harness response, not engineer response. The engineer's specific knowledge isn't the issue; the discipline lapsed; we re-build.

## What certifications won't do

- Will not work without leadership backing for the discipline. Engineers will push back; without backing, the bar erodes.
- Will not eliminate disagreements about whether an engineer is ready. Senior sign-off helps but doesn't eliminate.
- Will not protect against rapid model changes that shift behavior. Major model changes may invalidate the criteria; mid-cycle review is appropriate.
- Will not work as a one-time exercise. Drift requires continuous discipline.

## Companion artifacts

- [`autonomy-ladder.md`](autonomy-ladder.md) — what's being certified against
- [`raising-and-lowering-autonomy.md`](raising-and-lowering-autonomy.md) — adjacent discipline
- [`autonomy-drift-monitoring.md`](autonomy-drift-monitoring.md) — what re-certification responds to
- `promotion-and-leveling-rubric/` — distinct (engineer leveling, not autonomy)
- Ch 44 — source
