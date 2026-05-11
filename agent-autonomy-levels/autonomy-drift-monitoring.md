# Autonomy Drift Monitoring

How to detect upward drift before it produces incidents. Per Ch 32 opening:

> Anthropic's own Feb 2026 paper on agent autonomy showed individual auto-approve rates climbing from ~20% in the first 50 sessions to >40% by 750 sessions. Trust co-constructs upward whether you intend it to or not.

Drift is real, asymmetric (always upward), and inevitable without explicit countervailing discipline. This file is the detection and response mechanism.

## What drift looks like

Drift is not a single moment; it's a slow shift across many small decisions. Common patterns:

### 1. Permission-mode loosening

Engineers configure their agent permission modes more loosely over time. The "ask before each edit" mode becomes "ask only for changes affecting auth/billing/permissions." The "single file" mode becomes "the whole module." Each step seems reasonable; the cumulative shift produces L3 operation under the L2 ladder.

### 2. Auto-approve climb

Engineers approve PRs faster. Five-minute reviews become two-minute reviews; the diff scrolls past without close reading. The slop-detector signal becomes background noise. Per the Anthropic data, this happens to nearly everyone who works with agents long enough — without countervailing discipline.

### 3. Whitelist expansion

The L3 task whitelist starts narrow ("type annotations only"). Six weeks later it includes "and small refactors of typed code." Six months later it includes "and dependency updates." Each expansion looks reasonable; the cumulative whitelist no longer fits L3's discipline.

### 4. CODEOWNERS erosion

CODEOWNERS files start strict (auth paths require security team review). Over time, exceptions accumulate ("this file isn't really auth," "the security team is bottlenecked, let's add EM as approver"). The CODEOWNERS protection thins out.

### 5. Bypass normalization

A specific task that should run at L1 is run at L2 because "it's blocked otherwise." The exception is logged, then the next exception isn't. By the third exception, no one logs the bypass.

### 6. Subagent staleness

The team's subagents (security-reviewer, performance-reviewer) were tuned in Q1. By Q3, the heuristics haven't been updated. The subagents pass things they should have caught; engineers stop reading their output carefully.

## How to detect drift

Drift is hard to detect because each step is small. The detection mechanisms:

### Mechanism 1 — Per-engineer auto-approve rate telemetry

If your tooling supports it, instrument:
- Auto-approve rate per engineer per week
- Diff size and review time per PR per engineer
- Time-in-review trends

What to look for:
- Auto-approve rate climbing >5% per quarter for an engineer is a flag
- Median review time dropping below 3 minutes for substantive changes is a flag
- Time-in-review compressed at the team level is a flag (per Ch 31 §31.3 — one of the slop-detector signals)

### Mechanism 2 — Quarterly audit of actual operation against published ladder

Once a quarter, the platform team or tech lead audits:
- For each work category in the published ladder, are engineers actually operating at the documented level?
- Sample 10 random PRs across the team; assess whether the operation matched the documented level
- Spot-check permission configurations across engineers' setups

What to look for:
- Documented L2; actual operation L2.5 or L3 — drift detected
- Documented L1; actual operation L2 — drift detected
- Inconsistency across engineers (some at L1, some at L3 for the same category) — discipline gap

### Mechanism 3 — CODEOWNERS audit

Once a quarter, audit CODEOWNERS:
- Are auth/billing/permissions paths still requiring senior + security review?
- Have exceptions accumulated?
- Are there paths that should be CODEOWNERS-protected but aren't?

What to look for:
- Net loosening of CODEOWNERS over the quarter — drift
- Specific categories getting weaker reviewer requirements — drift

### Mechanism 4 — Subagent freshness audit

Once a quarter, audit subagents:
- When was the security-reviewer subagent's heuristics last updated?
- Is the slop-detector script catching the patterns from recent postmortems?
- Are subagent false-positive rates trending up (engineers learning to ignore)?

What to look for:
- Subagents not updated within 6 months — staleness
- False-positive rates >5% for any subagent — engineers will dismiss
- Postmortem heuristics that should be in subagents but aren't — gap

### Mechanism 5 — Whitelist scope audit

Once a quarter, audit any L3+ whitelist:
- What's in the whitelist today vs. what was in it at quarter start?
- Were any expansions explicit, or did they accumulate informally?
- Do all current whitelist items still meet the L3 criteria?

What to look for:
- Net expansion without explicit decisions — scope creep
- Items that have outgrown L3 criteria but remain whitelisted — drift

### Mechanism 6 — Incident root-cause coding

Per `incident-postmortem-templates/`, postmortems include the question of whether autonomy was a factor. Across postmortems, look for patterns:
- Multiple incidents at L3+ in the same category
- Incidents on tasks that shouldn't have been at the level they ran at
- Near-misses that suggest the level is too high

What to look for:
- 2+ incidents per quarter where autonomy is a factor — investigate the affected category
- Repeated near-misses at the boundary of a level — consider lowering

## How to respond to drift

### Specific drift detected → specific intervention

Per [`raising-and-lowering-autonomy.md`](raising-and-lowering-autonomy.md), the lowering-autonomy script applies. Specifically:

- **Permission-mode drift:** reset permissions; communicate the reset; run the lowering script if the affected category is misaligned
- **Auto-approve climb:** convene the team; review the data; reset expectations on review depth; if drift is severe, lower autonomy on the affected category
- **Whitelist expansion:** review the whitelist; remove items that no longer meet criteria; communicate the reset
- **CODEOWNERS erosion:** restore the CODEOWNERS protections; investigate why the erosion happened (often: bottleneck in the original reviewer pool)
- **Subagent staleness:** allocate time for subagent maintenance; if staleness is structural, increase platform team capacity
- **Bypass normalization:** reset the rules; communicate that bypasses require explicit logging; track in the next quarter

### Pattern-level drift → systematic intervention

If multiple drift mechanisms are firing, the issue is systemic. The interventions:

- Re-establish the published ladder (revisit `autonomy-ladder.md`)
- Refresh certifications (per `certification-gates.md`)
- Communicate to the team explicitly: "we've drifted; here's the reset"
- Schedule monthly (rather than quarterly) drift audits until the pattern stabilizes

### Cultural drift → leadership intervention

If the team's culture has shifted to "we don't care about the autonomy discipline," interventions are at the leadership level:

- VP/CTO communication on why the discipline matters
- Visible enforcement (e.g., a specific incident traced to drift, used as the case study)
- Adjustment of incentives (per Ch 44, certifications and promotion tied to discipline)

If cultural drift is severe and leadership doesn't intervene, the drift produces a major incident that forces the conversation. Better to have the conversation before the incident.

## What good monitoring cadence looks like

| Monitoring | Cadence | Owner |
|---|---|---|
| Per-engineer auto-approve telemetry | Continuous; reviewed monthly | Tech lead |
| Quarterly ladder audit | Quarterly | Platform team or VP |
| CODEOWNERS audit | Quarterly | Platform team |
| Subagent freshness audit | Quarterly | Platform team |
| Whitelist scope audit | Quarterly | Platform team |
| Incident pattern analysis | Per incident + quarterly aggregate | Engineering leadership |

## Anti-patterns

### "We don't have telemetry; we can't measure drift"

The absence of telemetry is itself a signal of risk. If the tooling doesn't expose per-engineer or per-team data, that's a platform investment to make. Until it's available, use the qualitative audits.

### "Our team is small; drift isn't a concern"

Small teams drift faster than large teams in some ways — fewer eyes on the discipline. Drift is a function of session count, not team size; per Anthropic's data, drift accumulates with experience.

### "We monitored once and didn't find drift; we're good"

Monitoring is a discipline, not an event. The next quarter's drift won't show up in last quarter's audit.

### "Drift is normal; let's just lower the bar"

The drift isn't the bar moving; it's behavior moving away from the bar. Lowering the bar to match drift is decorative — you've changed the document, not the discipline.

## What this monitoring will NOT do

- Will not work without instrumentation or audit time. Both require investment.
- Will not catch cultural drift directly. Quantitative metrics catch behavior; culture is qualitative.
- Will not fix drift; only detect it. The fix is the lowering-autonomy discipline.
- Will not eliminate the underlying drift force. Trust co-construction is intrinsic to the model-user-harness system; monitoring is the countervailing force, not a replacement for it.

## Companion artifacts

- [`autonomy-ladder.md`](autonomy-ladder.md) — what we're auditing against
- [`raising-and-lowering-autonomy.md`](raising-and-lowering-autonomy.md) — the response discipline
- `incident-postmortem-templates/` — incidents that surface drift
- `platform-team-charter/success-metrics.md` — adjacent metrics
- Ch 32 opening, Ch 31 §31.3 (slop-detector) — sources
