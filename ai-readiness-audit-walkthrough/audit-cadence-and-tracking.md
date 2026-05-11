# Audit Cadence and Tracking

When to run the audit, how often, what to track across runs.

## Why cadence matters

A one-time audit is a snapshot. Snapshots don't catch drift. Per `agent-autonomy-levels/autonomy-drift-monitoring.md`, drift is asymmetric and accumulates. The audit's value compounds when it's run regularly and the trajectory is tracked.

## The recommended cadence

### Per-PR (CI integration)

The audit runs on every PR via CI. Per [`how-to-run.md`](how-to-run.md), with a threshold:

- Set threshold below current score; raise as the score improves
- Catch regressions immediately
- Don't fail PRs for legitimate trade-offs (modify the audit's heuristics if needed)

This is the protection layer; catches "we accidentally broke a check" within the PR cycle.

### Weekly (scheduled CI run)

A scheduled weekly run captures the trajectory:

- Same audit, same repo, no PR triggered
- Output stored (JSON; aggregated into a dashboard)
- Drift detected: any week-over-week score drop investigated

### Quarterly (team review)

Once per quarter, the team explicitly reviews the audit:

- Overall score trajectory across the quarter
- Which checks closed; which opened
- Patterns that suggest harness investment areas for the next quarter

This is where the audit informs the roadmap.

### Cross-repo (platform team)

For platform teams running across multiple repos:
- Quarterly aggregation of scores across all repos
- Outlier identification (lowest-scoring repos)
- Cross-repo pattern detection (which checks fail universally)

---

## Tracking score over time

### What to track

Per audit run:
- Date
- Score
- Per-check status (pass/warn/fail)
- Per-category breakdown
- Specific checks that changed since last run

Aggregate:
- Score trajectory (line chart over time)
- Per-category trajectory (helps identify which areas are improving / regressing)
- Time-to-close per check (when did this check first start failing? how long until it closed?)

### Where to store

The simplest approach:
- Each weekly run produces a JSON output
- Aggregate into a single file or dashboard (could be a simple spreadsheet, or a more sophisticated dashboard)
- Quarterly review pulls from the aggregate

If using a dashboard tool: the JSON output can feed into Grafana, Looker, or similar. The platform team typically owns this.

### What to look for in trajectory

#### Steady improvement (score climbing)

Healthy sign. The team is investing in harness; the score reflects it.

What to do: continue the trajectory; track which areas are improving fastest.

#### Plateau (score stable for multiple quarters)

Could be healthy ("we're at the level we need") or concerning ("we've stopped investing").

Diagnosis:
- Is the team operating well at the current score?
- Are the remaining gaps acceptable?
- Is the team experiencing pain that closing remaining gaps would address?

If the answers suggest the plateau is healthy, no action. If they suggest the plateau is the result of stopping investment that should continue, address.

#### Regression (score dropping)

Concerning. Per `agent-autonomy-levels/autonomy-drift-monitoring.md`, drift is asymmetric — score doesn't naturally drift up. A drop is a real regression.

Investigation:
- What specific check(s) regressed?
- Was the change intentional (refactor, consolidation) or accidental (deletion, file move)?
- Is the regression on a critical-weight check or a nice-to-have?

Response: per [`prioritized-remediation-paths.md`](prioritized-remediation-paths.md), close the regressions with the same priority as new closures.

#### Spike (score jumps significantly in one run)

Could be:
- A real harness investment that closed multiple checks at once
- An audit modification (changes to the script can shift scores)
- A repo restructuring that exposed previously-hidden artifacts

Investigation: confirm the spike is real before celebrating.

---

## What to NOT track

Some metrics are tempting but produce bad incentives:

### Per-engineer score

Don't compute per-engineer audit scores. Audit is a repo-level signal; tying it to individual engineers produces gold-plating without underlying improvement.

### Score as the primary success metric

Score is one signal among many. Per `platform-team-charter/success-metrics.md`, the platform team's success metrics are adoption, impact, and quality — score correlates but isn't the same thing.

### Cross-team score competitions

Friendly "leaderboards" become adversarial fast. Cross-repo comparisons should be diagnostic (where to invest), not competitive (whose team is best).

---

## Quarterly review structure

Once per quarter, the team reviews the audit explicitly. Suggested 30-60 minute meeting:

### Agenda

1. **Score trajectory** (5 minutes) — line chart of last 4 quarters' scores
2. **Per-category trajectory** (10 minutes) — which categories improved, which regressed
3. **Specific closures this quarter** (10 minutes) — what shipped that closed checks
4. **Specific regressions this quarter** (10 minutes) — anything that opened
5. **Next quarter's targets** (15 minutes) — what to address; specific checks; specific dates
6. **Tier audit** (10 minutes) — are we operating at the right tier of investment?

### Output

- Specific checks targeted for next quarter
- Specific owners assigned
- Date for next quarterly review

### Who should attend

- Engineering manager
- Tech lead
- Platform team representative (if the team has shared platform investment)
- Senior engineers (1-2 representatives)

Don't invite leadership unless they specifically need to be there. The quarterly audit review is operational, not strategic. Strategic conversation about platform investment happens in the broader leadership review (per `platform-team-charter/`).

---

## What changes between quarters

The audit catches structural changes. Things that should change between quarters:

- New skills shipped → check 13 climbs (more skills counted)
- New subagents shipped → check 14 transitions from warn to pass
- New hooks shipped → check 15 climbs
- Documentation maturity → checks 1, 2, 4 transition from warn to pass

Things that should NOT change between quarters (stable repos):
- README, CLAUDE.md, AGENTS.md presence (these should be in place once)
- verify command (should exist permanently once added)
- CI workflow (should exist permanently)

When stable items regress, the regression is concerning regardless of overall score.

---

## Cross-repo aggregation patterns

For platform teams running across multiple repos quarterly:

### What to compute

- Median score across repos
- Distribution (interquartile range; outliers)
- Per-check pass rate across repos
- Per-team average score (if teams own multiple repos)

### What to look for

- **Consistent failures across repos:** the team has an org-wide gap. Address centrally (e.g., publish a CLAUDE.md template; ship a starter-kit improvement).
- **Outlier low-scoring repos:** specific teams need targeted help. Pair-driving sessions; harness migration support.
- **Outlier high-scoring repos:** the team has invested aggressively. Their harness components may be reusable across the org.

### What to communicate

The platform team's quarterly report includes:
- Overall org trajectory
- Outliers (anonymized if discussing in shared channels; named if in dedicated leadership review)
- Specific recommendations for the next quarter's platform investment

Per `platform-team-charter/budget-and-headcount-framing.md`, the trajectory data informs the budget conversation.

---

## What this cadence will NOT do

- Will not work without instrumentation. CI integration and storage of historical results are required.
- Will not work without engagement. Audits that nobody reads don't drive improvement.
- Will not catch all forms of harness drift. Some drift is in content quality (unmeasured) or in team practice (unmeasured).
- Will not eliminate the need for manual review. The audit is the heuristic floor; manual review of artifacts is the ceiling.

## Companion artifacts

- [`how-to-run.md`](how-to-run.md) — operational
- [`scoring-and-thresholds.md`](scoring-and-thresholds.md) — interpretation
- [`prioritized-remediation-paths.md`](prioritized-remediation-paths.md) — what to address
- `agent-autonomy-levels/autonomy-drift-monitoring.md` — adjacent (different drift dimension)
- `platform-team-charter/success-metrics.md` — adjacent metrics
EOF