# Case Studies — "Platform Team Built This; Here's What Shipped"

Calibration examples for what the platform team produces. Not actual case studies (those are company-specific) — illustrative ones that show the shape of platform team work.

Use these to:
- Calibrate new platform engineers on what good work looks like
- Show stakeholders the kind of impact platform work produces
- Anchor budget conversations in concrete examples

## Case study 1 — The shipping skill that replaced ad-hoc patterns

### The situation

Engineers across 8 stream-aligned teams were each writing their own variant of "deploy this service to production." Patterns differed in subtle ways: some teams ran migrations manually, some skipped tests in emergencies, some had broken canary processes. Production deployments were producing inconsistent results; postmortems pointed to "engineer didn't follow the right pattern" repeatedly.

### What the platform team did

Built a `skills/deploy-service/` skill. Six weeks of focused work:

- Week 1-2: interviewed 8 stream-aligned team leads; documented the variations
- Week 3: identified the canonical pattern; got buy-in from team leads
- Week 4: built the skill; documented; tested with two willing teams
- Week 5: refined based on feedback; broader rollout
- Week 6: iterated on the rough edges

### What shipped

A skill that engineers (and agents) invoke before any production deploy. The skill checks pre-conditions, runs migrations in the right order, executes canary, monitors metrics, completes deployment, posts to the deploy log.

### What changed

After 90 days of adoption (6 of 8 teams using regularly):

- Deploy-related incidents down 40%
- Time from PR merge to production deploy median: 38 min → 22 min
- Engineer-reported deploy frustration down significantly (qualitative; from interviews)

### What it cost

- 6 weeks of one platform engineer
- ~3 hours per stream-aligned team for the discovery interviews
- 1 week of ongoing maintenance per quarter

### Why it worked

- Clear pain point with measurable impact
- Buy-in from stream-aligned team leads before the work started (not after)
- Started with two willing teams, not a forced rollout to all 8
- Iterated on rough edges quickly

---

## Case study 2 — The migration playbook that compressed timeline

### The situation

The company decided to migrate from Cursor + Copilot to Claude Code as the primary IDE-side AI tool. Initial estimate: 4 months for full migration across 12 stream-aligned teams.

### What the platform team did

Built `migration-playbooks/cursor-to-claude-code.md` (now in this repo) before starting the migration. Two weeks of upfront work to produce the playbook; saved months in execution.

### What shipped

- Migration playbook with phase-by-phase guidance
- Pre-migration checklist (the 21-item gate)
- Team conversation scripts for the inevitable pushback
- Specific metrics for "this team has migrated successfully"

### What changed

Migration completed in 8 weeks instead of 16:

- Phase 0 (preconditions): 2 weeks instead of 4
- Phase 1 (pilot): 2 weeks instead of 4
- Phase 2 (broader rollout): 3 weeks instead of 6
- Phase 3 (consolidation): 1 week instead of 2

The compression was real, not vendor-marketing. Specifically: each team had clear next-step guidance; the conversation scripts handled the pushback that would have produced negotiation cycles; the checklist prevented half-prepared rollouts.

### What it cost

- 2 weeks of one staff platform engineer for the playbook
- Ongoing platform engineer time during execution (~10 hours / week / for 8 weeks)

### Why it worked

- Playbook before action, not after
- Specific guidance for each phase, not generic principles
- Scripts for the pushback meant team leads weren't improvising
- Metrics for "migrated successfully" prevented premature claims of completion

---

## Case study 3 — The slop-detector that caught real bugs

### The situation

The team was seeing AI-authored bugs ship to production occasionally. The seven slop signatures from Ch 22 §22.2 were known but not enforced; the team relied on review discipline alone.

### What the platform team did

Built `scripts/slop-detector.py` — a heuristic checker for the seven signatures. Integration with CI to flag PRs.

### What shipped

- `slop-detector.py` running on every PR
- Per-signature heuristics, tuned to <5% false positive rate
- Dashboard showing detector hits per team per month
- Integration with the postmortem template (per `incident-postmortem-templates/`) for closing the loop

### What changed

In the first quarter of operation:

- 47 PRs flagged with potential slop signatures
- 31 of the 47 had genuine issues (66% true-positive rate)
- 14 of those 31 would have shipped to production without the detector
- Estimated severity-weighted incident reduction: ~15-20% of would-be AI-related incidents prevented

### What it cost

- 4 weeks of one platform engineer for the initial implementation
- ~1 week / quarter for heuristic tuning based on incident postmortems

### Why it worked

- Direct mapping to a published taxonomy (Ch 22 §22.2 seven signatures)
- Tuned to acceptable false positive rate before broad rollout
- Integration with postmortems closed the feedback loop — heuristics improved as bugs surfaced
- Dashboard surfaced patterns at team level, supporting team-by-team conversations

---

## Case study 4 — The cost dashboard that surfaced waste

### The situation

AI tooling spend was growing 20% month-over-month with no clear visibility into where the spend was going. CFO was asking; engineering leadership couldn't answer specifically.

### What the platform team did

Built a cost dashboard combining vendor APIs, internal tracking, and team attribution. Three weeks of focused work.

### What shipped

- Per-team token spend, with breakdown by model tier (Opus / Sonnet / Haiku)
- Per-engineer median spend (anonymized in cross-team views, identified within teams)
- Anomaly detection for individual engineers or teams with unusual spikes
- Monthly cost report sent to engineering leadership

### What changed

In the first 90 days:

- Identified two engineers consistently using Opus for tasks that Sonnet would have handled (cost savings: ~$3K / month after coaching)
- Surfaced one team using AI tooling on workloads that should have been on a cheaper API tier (savings: ~$8K / month)
- Surfaced a vendor billing discrepancy worth $4K (vendor credited)
- Total Q1 savings: ~$45K, against a dashboard cost of about 3 person-weeks

### What it cost

- 3 weeks of one platform engineer for initial implementation
- ~2 days / month for ongoing maintenance and report generation

### Why it worked

- Direct ROI math (savings >> cost) made the budget conversation easy
- Per-engineer visibility enabled coaching (without becoming surveillance — the threshold was anomalies, not routine)
- Monthly cadence kept it visible without becoming noise
- Started with the highest-leverage signal (cost) before expanding to other dimensions

---

## Case study 5 — The bash firewall that prevented a SEV-1

### The situation

An engineer running an autonomous agent task encountered a complex git situation. The agent attempted `git push --force` on a shared branch. The action was caught by a hook that the platform team had built two weeks prior.

### What the platform team did

Built a bash firewall hook (`governance/hooks/no-force-push.sh`) that blocks `git push --force*` variants in agent contexts. Two days of focused work.

### What shipped

- Bash firewall hook integrated with the agent's bash tool
- Server-side branch protection on `main` and `release/*` branches
- CLAUDE.md addition explaining the rule
- An ADR documenting the decision

### What changed

The hook fired on the day described above, blocking what would have been a SEV-1 (force-push overwrites teammate work, hours of recovery, no customer impact but real engineering disruption). The agent surfaced the block; the engineer reviewed; the situation was resolved without the force push.

A few weeks later, the same hook fired in a different team's context, preventing a similar incident.

### What it cost

- 2 days of one platform engineer for implementation
- Ongoing maintenance: nearly zero

### Why it worked

- Specific to a known anti-pattern (force-push on shared branches)
- Mechanical enforcement, not "documentation that engineers will ignore under pressure"
- Defense in depth (client-side hook + server-side branch protection)
- Documented reasoning in an ADR so future engineers (or agents) understand why

---

## What good case studies have in common

Across the five examples above:

1. **Specific pain point identified.** Not "we should have a dashboard"; "engineers don't know where their AI spend is going, and the CFO is asking."
2. **Bounded scope.** Two days to four weeks of platform engineer time. Not "build the framework that will solve everything for the next two years."
3. **Buy-in before building.** Stream-aligned teams or leadership had asked for the thing or had a problem; the platform team didn't push it without that.
4. **Started small.** Pilot with one or two teams; broader rollout after iteration.
5. **Measurable outcome.** Specific numbers (incidents prevented, cost saved, time compressed). Not "engineers feel better."
6. **Documented after.** Each case study is the post-hoc record. The discipline is to actually write these.

## What bad case studies look like

The patterns to avoid:

- **The framework that nobody asked for.** Platform team builds an elaborate abstraction; stream-aligned teams don't use it because their need was different from what the framework solved.
- **The dashboard that nobody reads.** Built once, never iterated, dies in 6 months.
- **The migration playbook that wasn't followed.** Written, but the migration happened ad hoc; no enforcement of the playbook structure.
- **The hook that's too noisy.** False positive rate too high; engineers learn to bypass.
- **The skill that's too generic.** Tries to handle all cases of a pattern; ends up being too vague to be useful for any specific case.

These are also worth documenting (in retrospectives, not as case studies). The platform team learns as much from what didn't work as from what did.

## How to write a case study

The structure used above:

1. **The situation** — what was the pain point or trigger
2. **What the platform team did** — scope, time, approach
3. **What shipped** — concrete artifacts
4. **What changed** — measurable outcomes (or qualitative if measurement isn't feasible)
5. **What it cost** — be honest about platform engineer time
6. **Why it worked** — the durable lesson

Aim for 300-500 words per case study. The discipline is to write them within 30 days of the work shipping; otherwise they don't get written.

## What case studies will NOT do

- Will not substitute for real metrics (per [`success-metrics.md`](success-metrics.md))
- Will not be persuasive without honest data
- Will not work if they're vanity case studies (avoiding mention of what didn't work)

## Companion artifacts

- [`success-metrics.md`](success-metrics.md) — quantitative side
- [`charter.md`](charter.md) — the source of the principles these examples illustrate
- `migration-playbooks/` — the actual migration playbooks referenced in case study 2
- `scripts/slop-detector.py` — the actual detector referenced in case study 3
- Ch 42 §42.4 — source
