# Scoring and Thresholds

What the scores mean, what thresholds to set in CI, how to use the score over time.

## How the score is computed

Per check: `weight × status_value` where `status_value` is `1.0` for pass, `0.5` for warn, `0.0` for fail.

Total score = sum of (weight × status_value) divided by sum of weights, expressed as a percentage.

Maximum possible score = 100. Minimum possible = 0.

Weights:
- 1 = nice to have (5 checks)
- 2 = important (12 checks)
- 3 = critical (7 checks)

A repo missing all the critical checks but passing nice-to-haves can still score below 30. A repo passing all critical checks but missing nice-to-haves typically scores 80+.

## What the scores mean

These are calibration anchors. Adjust to your context.

### 0-30 — Pre-AI-tooling

The repo has not formalized for AI tooling. Tier 1 (foundation) checks are mostly failing.

What to do: the team is at the very beginning. Run the 30/60/90 plan from `legacy-codebase-onboarding/` if applicable, or the agent-friendly starter kit setup if greenfield. Don't worry about score; focus on Tier 1 closure.

### 30-50 — Early adoption

The repo has some legibility (CLAUDE.md, README) but the harness is mostly missing. Tier 1 partially closed; Tier 2 mostly open.

What to do: close remaining Tier 1, then Tier 2. Score should climb to 60+ within 4-8 weeks of focused work.

### 50-70 — Maturing

Tier 1 mostly closed; Tier 2 partially closed; Tier 3 emerging. The team is past the beginner phase.

What to do: work through Tier 3 (skills, subagents, PR template). The leverage from Tier 3 is what enables the team to operate at L2-L3 autonomy.

### 70-85 — Mature

Tiers 1, 2, 3 mostly closed; Tier 4 in progress. The team is operating well; remaining gaps are typically governance or polish.

What to do: address Tier 4 driven by specific events (customer audit coming, regulatory shift, scaling pressure). Don't try to push score for its own sake.

### 85+ — Excellent

All tiers mostly closed; remaining gaps are typically Tier 5 polish or specific intentional trade-offs.

What to do: maintenance and iteration. Per [`audit-cadence-and-tracking.md`](audit-cadence-and-tracking.md), keep the score above 80 over time; investigate any drop.

### 95+ — Aspirational

Rare. Typically requires monorepo/multi-repo discipline plus active maintenance. Don't optimize for 95+ at the expense of actual engineering work.

---

## CI thresholds

Setting the audit as a CI gate. The threshold should be:

- **Above your current score by 5-10 points** — push the team forward without producing constant noise
- **Below 90 in most cases** — high thresholds produce false positives and dismissal habits
- **Adjusted upward as the score improves** — every quarter or when a major harness investment ships

### Suggested thresholds by team maturity

| Team maturity | Threshold |
|---|---|
| Early adoption (current score 30-50) | 50 |
| Maturing (current score 50-70) | 65 |
| Mature (current score 70-85) | 80 |
| Excellent (current score 85+) | 85 |

Don't use thresholds higher than what your team can reliably maintain. A threshold that fails CI on 20% of PRs is too strict; engineers learn to override.

### When the audit fails CI

If the audit fails because a specific check started failing (e.g., a new file removed CLAUDE.md content), the right response:

1. **Investigate the change.** What was removed and why?
2. **Restore if accidental.** Most failures are unintentional regressions.
3. **Decide if intentional.** Sometimes a change is intentional but produces a check failure (e.g., consolidating CLAUDE.md content into AGENTS.md). Decide whether to:
   - Adapt the change (keep CLAUDE.md as a thin pointer to AGENTS.md)
   - Modify the audit (script change to recognize the pattern)
   - Accept the lower score (rare)

### When the audit passes CI but score drops

The repo is still above the threshold but lower than last week. Investigation:

- Look at which check regressed
- Determine if the regression is real (a file was deleted) or false (audit's heuristic missed a pattern)
- Address before it accumulates

---

## What the score doesn't measure

The score is a heuristic. It captures presence/absence of artifacts; it doesn't capture:

- **Quality of artifacts.** A 1-line CLAUDE.md and a 3000-word substantive one both pass.
- **Use of artifacts.** Skills that exist but are never invoked don't reduce the score.
- **Team discipline.** PR template that exists but is rubber-stamped doesn't reduce the score.
- **Actual safety.** A repo with high score but bad harness content can still ship slop.

For these dimensions, the audit is necessary but not sufficient. Pair with:
- Manual review of CLAUDE.md / AGENTS.md / skills (per [`check-by-check-explainer.md`](check-by-check-explainer.md))
- Adoption metrics (per `platform-team-charter/success-metrics.md`)
- Drift monitoring (per `agent-autonomy-levels/autonomy-drift-monitoring.md`)

---

## Cross-repo score comparisons

When platform teams aggregate scores across multiple repos, patterns emerge:

### "Median score 60, distribution wide"

Diagnosis: the org has uneven adoption. Some teams have invested; others haven't.

Path: identify the outliers (top and bottom). Have the top teams help the bottom teams (pair-driving sessions, shared harness components). Don't impose top-down — make the leverage visible.

### "Median score 75, narrow distribution"

Diagnosis: the org has consistent investment. Some teams may be at 70, others at 80, but no severe outliers.

Path: focus on the next quarter's investment area for the org. The score is healthy; specific gaps may still warrant attention.

### "One repo at 90, others at 40"

Diagnosis: one team has invested heavily; others haven't followed. Possibly one team's lead is championing AI tooling without org-wide alignment.

Path: leadership conversation. Either the high-scoring team's investment is the model the org should adopt (and deserves resources to spread), or it's an outlier and should be brought back into the team norm.

---

## Anti-patterns

### "We're at 90; we're done"

Score is one signal among many. A 90 with bad CLAUDE.md content is a worse harness than an 80 with substantive content. Don't optimize for the number.

### Setting CI thresholds aggressively

A threshold of 95 produces constant CI failures. Engineers learn to override. The threshold becomes ignored.

Mitigation: thresholds calibrated to current state + small increment. Raise as you improve.

### Scoring as performance metric

Using the score as input to performance reviews or team comparisons. Engineers will gold-plate; the score will rise without underlying improvement.

Mitigation: score is operational data; not performance data. Use for self-direction and prioritization, not for evaluation.

### Ignoring score drops

Score drops 70 → 65 over a quarter. Investigation is skipped because "we're still passing." The drop continues.

Mitigation: per [`audit-cadence-and-tracking.md`](audit-cadence-and-tracking.md), track score over time; investigate drops promptly.

---

## What this scoring will NOT do

- Will not give you a definitive answer about whether the repo is "AI-ready"
- Will not capture content quality
- Will not protect against gold-plating to inflate the score
- Will not transfer cleanly to all repo types (very small repos, vendor-managed code, generated code)

## Companion artifacts

- [`check-by-check-explainer.md`](check-by-check-explainer.md) — what each check means
- [`prioritized-remediation-paths.md`](prioritized-remediation-paths.md) — what to fix first
- [`audit-cadence-and-tracking.md`](audit-cadence-and-tracking.md) — over-time discipline
- `scripts/ai-readiness-audit.py` — the source
