# Prioritized Remediation Paths

The triage flow from audit output to specific next actions, ordered by leverage. Use this when the audit has identified gaps and the team needs to pick what to address first.

The principle: not all gaps are equal. A team with 10 gaps shouldn't address them in arbitrary order; it should address them in leverage order — the gap that, once closed, makes the next gaps easier to close, that protects against the highest-cost incidents, that enables the most engineering work.

## The leverage hierarchy

The 24 checks fall into rough leverage tiers. Address in this order regardless of audit score:

### Tier 1 — Foundation (close before anything else)

These are the prerequisites for the rest of the harness to work. Without them, other investments are decorative.

1. **Check 1: CLAUDE.md exists** — without this, the agent has no team-specific context
2. **Check 6: verify command defined** — without this, "done" has no objective meaning
3. **Check 9: verify includes tests** — without this, verify is theatrical
4. **Check 10: test files exist** — without tests, the verification can't catch anything
5. **Check 11: CI workflow exists** — without CI, verify is a local convention engineers will skip under pressure

If any Tier 1 check is failing, address it before moving down. Time to close: typically 1-2 weeks of focused work for a team starting from zero.

### Tier 2 — Mechanical safety (close before scaling AI tooling adoption)

These are the layers that prevent catastrophic incidents. Required before raising autonomy beyond L1.

6. **Check 12: .claude/ directory exists** — the harness lives here
7. **Check 15: hooks configured** — the bash firewall, protected paths, mechanical enforcement
8. **Check 20: forbidden patterns listed in CLAUDE.md** — the agent's "never do" list (per `agent-autonomy-levels/forbidden-categories.md`)
9. **Check 17: PR template mentions AI authorship** — the foundation of attribution (per Ch 31 §31.6)

Time to close: typically 2-4 weeks once Tier 1 is in place.

### Tier 3 — Productivity multipliers (close as the team scales)

These are the leverage components that make AI tooling productive at scale.

10. **Check 13: at least one skill defined** — start with 3-5; grow to 12
11. **Check 14: subagents defined** — at minimum, code-reviewer; ideally planner/implementer/reviewer
12. **Check 7: verify includes lint** — catches a class of slop
13. **Check 8: verify includes typecheck/format** — catches another class
14. **Check 16: PR template exists** — the verification checklist
15. **Check 21: architectural invariants documented** — the agent's design constraints

Time to close: typically 4-12 weeks; often partial completion is fine while iterating.

### Tier 4 — Operational maturity (close as the team matures)

These distinguish a serious AI-tooling team from a beginning one.

16. **Check 2: AGENTS.md exists** — multi-vendor cross-compatibility
17. **Check 4: README.md exists** — should already be true; check anyway
18. **Check 18: CODEOWNERS file exists** — required for sensitive paths
19. **Check 19: SECURITY.md exists** — for customer audits
20. **Check 22: data classification policy referenced** — for compliance
21. **Check 24: AI-aware incident response runbook** — for AI-related incidents

Time to close: spread across 1-2 quarters as the team matures.

### Tier 5 — Polish (close opportunistically)

These are nice-to-haves; address when convenient.

22. **Check 3: llms.txt exists** — useful for complex monorepos
23. **Check 5: per-package READMEs** — useful for monorepos
24. **Check 23: cost telemetry referenced** — important if the team has scale; less critical otherwise

---

## Decision flow

Given an audit with a specific score and specific failing checks, the decision flow:

### Step 1 — Identify Tier 1 gaps

Look at checks 1, 6, 9, 10, 11. Are any failing or warning?

If yes, **stop here and close those first**. Don't move on. Tier 1 is foundation; without it, work in higher tiers can't compound.

### Step 2 — Identify Tier 2 gaps

Look at checks 12, 15, 17, 20. Are any failing?

If yes, close before scaling AI tooling adoption beyond a small group. Specifically:
- Check 12 (.claude/ directory) — without this, you have no place for harness components
- Check 15 (hooks) — without this, the autonomy ladder can't enforce mechanically
- Check 20 (forbidden patterns) — without this, the agent doesn't know the boundaries

### Step 3 — Pick 3-5 Tier 3 items for the next quarter

Among checks 7, 8, 13, 14, 16, 21:
- Pick 3-5 that have highest leverage for your team's specific context
- Schedule for the next quarter
- Don't try to do all six at once

### Step 4 — Schedule Tier 4 for the next 6 months

Among checks 2, 4, 18, 19, 22, 24:
- Map to the team's specific drivers (customer audit coming? regulatory? scaling?)
- Schedule based on driver

### Step 5 — Tier 5 items as opportunistic

Don't schedule. Address when convenient or when a specific situation requires.

---

## Common patterns and their remediation

### Pattern: "Score 25-40, mostly Tier 1 failures"

Diagnosis: very early in AI tooling adoption.

Remediation order:
1. CLAUDE.md (1-2 days for first version; iterate over weeks)
2. verify command (1-2 days)
3. CI workflow if missing (1-2 days)
4. tests if completely absent (1-4 weeks of catch-up)

Outcome: score climbs to 50-60 in 2-4 weeks of focused work.

### Pattern: "Score 50-65, harness gaps"

Diagnosis: legibility is in place but the harness isn't.

Remediation order:
1. .claude/ directory + at least one skill (1 week)
2. Hooks (1-2 weeks)
3. Subagents (2-4 weeks)
4. PR template with AI authorship (1 day)

Outcome: score climbs to 70-80 in 4-8 weeks.

### Pattern: "Score 70-80, governance gaps"

Diagnosis: harness is in place; governance hasn't been formalized.

Remediation order:
1. SECURITY.md (1 day to draft; iterate)
2. CODEOWNERS for sensitive paths (1 day)
3. Data classification reference in CLAUDE.md or SECURITY.md (1 day)
4. AI-aware incident runbook (1-2 weeks; reference `incident-postmortem-templates/`)

Outcome: score climbs to 85+. The remaining 15 points are typically polish (Tier 5) and warns that may be acceptable for your team.

### Pattern: "Score 80+, everything fails specific way"

Diagnosis: the audit's heuristic doesn't match the team's setup. Some checks are passing in spirit but failing the audit's specific pattern.

Remediation: review the specific checks. Decide whether to:
- Adapt the team's setup to match the audit's pattern (often fine)
- Accept the audit miss as a known limitation
- Modify the audit script for your team's context (acceptable; document the modification)

---

## What NOT to do

### Don't try to close all gaps simultaneously

Closing 24 gaps in parallel produces 24 half-finished investments. Pick the leverage-ordered subset; ship them; iterate.

### Don't address Tier 5 before Tier 1

A repo with cost telemetry but no CLAUDE.md or verify command is in a worse state than a repo with CLAUDE.md and verify but no cost telemetry. Tier order matters.

### Don't gold-plate Tier 1

CLAUDE.md doesn't need to be perfect on day one. A 1500-word substantive version that the team will iterate on is better than a 5000-word polished version that took 3 weeks.

### Don't skip the audit

Some teams resist the audit because "we know what we're doing." Run it anyway. The audit has surprised every team I've seen.

### Don't take Tier 2 lightly

The Tier 2 items prevent catastrophic incidents. A team with great Tier 1 and Tier 3 but failing Tier 2 has the worst-of-both-worlds: confident AI usage without mechanical safety. Per the autonomy ladder, you can't operate above L1 without these.

### Don't ignore warns

Warns are partial credit. They surface checks where the artifact exists but is minimal. Often the warn → pass transition is just an investment in content quality, not a structural change. Worth addressing.

---

## What this prioritization will NOT do

- Will not produce a passing score by itself. The remediation work is engineering work.
- Will not work for every team's context. Your team may have different leverage; adjust.
- Will not protect against political pressure to skip Tier 1 in favor of visible Tier 3 wins. The discipline is to do the unsexy work first.
- Will not eliminate the audit's heuristic limitations. Some checks may be misleading for your repo.

## Companion artifacts

- [`check-by-check-explainer.md`](check-by-check-explainer.md) — what each check means
- [`scoring-and-thresholds.md`](scoring-and-thresholds.md) — what the scores indicate
- [`audit-cadence-and-tracking.md`](audit-cadence-and-tracking.md) — running over time
- `legacy-codebase-onboarding/` — for brownfield context
- `platform-team-charter/` — for platform team running cross-repo audits
