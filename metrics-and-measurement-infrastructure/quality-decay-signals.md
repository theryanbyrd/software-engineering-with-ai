# Quality Decay Signals — The Six Leading Indicators

Direct expansion of Ch 31 §31.6. Six monthly-tracked signals that catch AI-driven quality decay early — before customer-reported defects and before the postmortem.

Per the book:

> Six leading indicators that quality is decaying under AI adoption. Track all six monthly. Two consecutive months of decay on three or more is a "pull the lever" signal — pause new-team rollout, audit the harness, run a senior-engineer-led code-review-quality review.
>
> — Ch 31 §31.6

These are leading indicators by design. By the time customer-reported defects spike, you are already three months late. The first five of these signals will turn red one to three months before the sixth one (customer defects) does.

## The six signals at a glance

| # | Signal | Direction that means decay | What it tells you |
|---|---|---|---|
| 1 | Mutation score | Trending **down** | Tests still pass but kill fewer mutants — tests are testing implementation, not behavior |
| 2 | PR size (avg LOC) | Trending **up** | Agents generating more than they should |
| 3 | Review-time-per-line | Trending **down** | Rubber-stamping; reviewers can't keep up |
| 4 | Revert rate | Trending **up** | PRs reverted within 30 days — the most direct signal |
| 5 | Customer-reported defects | Trending **up** | End users finding bugs that escaped your harness |
| 6 | Senior-engineer 1:1 culture concerns | Reports rising | Soft signal but reliable; treat seriously |

The pull-the-lever rule: **three or more signals showing decay across two consecutive months.** Not one bad month. Not two signals over five months. Three signals, two months — that is the threshold the book is precise about.

---

## Signal 1 — Mutation score trending down

### Definition

Mutation score is the percentage of code mutations (deliberate small bugs injected into the codebase) that the test suite catches. A mutation score of 80% means 80% of the injected mutations cause at least one test to fail.

Per Ch 31:

> Tests still pass but kill fewer mutants. Tells you tests are testing implementation, not behavior.

This is the keystone quality signal. AI-generated tests have a well-documented failure mode: they assert that the implementation does what the implementation does. They mirror the code's structure rather than testing its observable behavior. A mutation suite catches this because a mutation that changes the implementation but preserves the contract should be killed by a behavior-test and survived by an implementation-test.

### How to measure

The tooling:

| Language | Tool |
|---|---|
| Python | [`mutmut`](https://github.com/boxed/mutmut), [`cosmic-ray`](https://github.com/sixty-north/cosmic-ray) |
| JavaScript / TypeScript | [`Stryker`](https://stryker-mutator.io/) |
| Java | [`PIT`](https://pitest.org/) |
| Go | [`go-mutesting`](https://github.com/zimmski/go-mutesting) |
| Rust | [`cargo-mutants`](https://mutants.rs/) |

The discipline:

```bash
# Weekly mutation run, scoped to changed modules in the last week
git diff --name-only HEAD@{1.week.ago} HEAD \
  | grep -E '\.(py|ts|go)$' \
  | xargs mutmut run --paths-to-mutate

# Score
mutmut results | awk '/killed/ {killed=$2} /total/ {total=$2} END {print killed/total}'
```

Store the score per module per week. Roll up to a team-level moving average.

### PromQL

If you push mutation scores to Prometheus via a custom collector:

```promql
# Team-level 4-week moving average
avg_over_time(
  mutation_score_ratio{team="$team"}[4w]
)

# Decay detection: current 4w avg < previous 4w avg by >2 percentage points
(
  avg_over_time(mutation_score_ratio{team="$team"}[4w])
  -
  avg_over_time(mutation_score_ratio{team="$team"}[4w] offset 4w)
) < -0.02
```

### Threshold

- **Healthy:** mutation score stable or rising; >70% on changed modules
- **Watch:** mutation score dropping 1–2 percentage points month over month
- **Decay:** mutation score dropping >2 percentage points month over month, for two consecutive months

### Corrective action

Three plays, in order:

1. **Senior-engineer review of recent AI-authored test code.** Look for the four anti-patterns: tests that assert implementation details, tests that mock the unit under test, tests that re-encode the production code in fixtures, tests that test framework behavior rather than business logic.
2. **Add a mutation-score gate to CI** for changed modules. Set it 5 points below the team's current score so the gate catches regressions, not the baseline.
3. **Update CLAUDE.md / AGENTS.md** with explicit guidance on behavior-vs-implementation testing, with examples drawn from the failing audit.

See also `../evals-and-benchmarks-runbook/` for mutation testing as the keystone evaluation, per Ch 22.

### Anti-patterns to avoid

- **Running mutation tests against the whole codebase nightly.** Mutation runs are O(test_count × mutation_count). Scope to changed code. A full-repo nightly mutation run on a 200K LOC codebase can take 12+ hours and nobody will look at the result.
- **Mutation gate set at the team's current score.** This makes the gate flap on noise. Set it 5 points below the team's median.
- **Treating mutation score as a per-engineer metric.** It's a team-level signal. Individual mutation scores will be too noisy and too punitive.

---

## Signal 2 — PR size trending up

### Definition

Average lines of code per merged PR (additions, ignoring deletions and renames). Tracked at the team-week level.

Per Ch 31:

> Average lines per PR creeping up means agents are generating more than they should.

Reference number from the book (Ch 31 §31.3):

> Faros AI's data shows AI-using teams produce PRs that are 51–154% larger on average.

That is the entire industry's data. Your team's job is to keep PR size in the lower half of that range — preferably flat against your pre-AI baseline (see [`baseline-measurement-template.md`](baseline-measurement-template.md)).

### How to measure

GitHub API:

```bash
gh api graphql -f query='
  query($org: String!, $repo: String!, $since: DateTime!) {
    repository(owner: $org, name: $repo) {
      pullRequests(states: MERGED, first: 100, orderBy: {field: UPDATED_AT, direction: DESC}) {
        nodes {
          number
          additions
          deletions
          mergedAt
          author { login }
          labels(first: 10) { nodes { name } }
        }
      }
    }
  }' -F org=$ORG -F repo=$REPO -F since=$(date -v -30d -u +%Y-%m-%dT%H:%M:%SZ)
```

SQL (if you ETL PRs to a warehouse):

```sql
SELECT
  date_trunc('week', merged_at) AS week,
  team,
  PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY additions) AS median_pr_size,
  PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY additions) AS p90_pr_size,
  COUNT(*) AS pr_count
FROM pull_requests
WHERE merged_at >= NOW() - INTERVAL '12 weeks'
GROUP BY 1, 2
ORDER BY 1, 2;
```

### Threshold

- **Healthy:** median PR size stable; 90th percentile <600 lines
- **Watch:** median PR size rising 10–25% month over month
- **Decay:** median PR size up >25% for two consecutive months, or 90th percentile creeping above 1,000 lines

The 90th percentile matters as much as the median. A team can have a healthy median and a long tail of 2,000-line PRs that nobody is actually reading. The long tail is where the slop lives.

### Corrective action

- **Add a soft size warning** to the PR template ("PRs over 500 lines: expected reviewer time is >2 hours; consider splitting").
- **Add a hard size limit** for AI-tagged PRs (per Ch 31 §31.6 authorship tagging). `ai:authored` and `ai:agent` PRs over N lines require an explicit "split skipped because…" comment from the author.
- **Audit recent oversized PRs** for the prefix of slop they're enabling — usually one of: speculative additions, file-by-file CRUD scaffolds the agent generated rather than reading, or "while I was in there" drive-by changes.

### Anti-patterns to avoid

- **Counting deletions in PR size.** Deletions are good. A 2,000-line PR that's 1,800 deletions and 200 additions is a celebration, not a slop signal.
- **Hard-capping PR size with no exceptions.** Some legitimate work — generated migrations, mass renames — is necessarily large. The escape hatch is a human attestation, not a rejected PR.
- **Counting AI-generated lockfile / generated-file changes.** Filter `package-lock.json`, `Cargo.lock`, `*.pb.go`, `*.sql.go`, etc. out of LOC counts before computing the metric.

---

## Signal 3 — Review-time-per-line trending down

### Definition

Median (PR review elapsed time) / (PR additions), per merged PR, rolled up at the team-week level.

Per Ch 31:

> Reviews getting faster per line of diff means rubber-stamping.

Reference number from the book (Ch 31 §31.3):

> Faros AI's 2026 dataset showed median time in PR review up 441%.

PR review time has gone up across the industry as AI-authored PR volume rose. **Your team-level signal is review-time-per-line going down even as overall review time goes up.** Reviewers spending more total time on PRs but less time per line of code = they are processing more code at the same depth, or they are processing the same code at less depth. The metric does not distinguish; the slop-detector heuristics and the postmortem corpus do.

### How to measure

GitHub API + a small computation:

```python
# Pseudocode
for pr in merged_prs_last_4_weeks():
    review_seconds = pr.merged_at - pr.first_review_requested_at
    lines = pr.additions
    if lines > 0:
        yield {
            "pr": pr.number,
            "team": pr.team,
            "seconds_per_line": review_seconds / lines,
            "merged_at": pr.merged_at,
        }
```

SQL:

```sql
SELECT
  date_trunc('week', merged_at) AS week,
  team,
  PERCENTILE_CONT(0.50) WITHIN GROUP (
    ORDER BY EXTRACT(EPOCH FROM (merged_at - first_review_requested_at)) / NULLIF(additions, 0)
  ) AS median_seconds_per_line
FROM pull_requests
WHERE merged_at >= NOW() - INTERVAL '12 weeks'
  AND additions > 0
GROUP BY 1, 2
ORDER BY 1, 2;
```

### Threshold

- **Healthy:** seconds-per-line stable or rising; >2 seconds per line on substantive PRs (excluding `ai:none` typo fixes)
- **Watch:** seconds-per-line dropping 10–25% month over month
- **Decay:** seconds-per-line dropping >25% for two consecutive months, especially on `ai:authored` PRs

The 2-second-per-line floor is a calibration anchor, not a hard rule. A reviewer reading code at 2 seconds per line is reading; at 0.5 seconds per line they are skimming. Pair this signal with the `ai:authored` vs `ai:none` review-time comparison from Ch 31 §31.6:

> Track review time by tag — a PR labeled `ai:authored` should NOT be reviewed faster than `ai:none`. If your `ai:authored` PRs have 3x the defect rate of `ai:none`, your harness is broken or your reviewers are rubber-stamping.

### Corrective action

- **Reviewer training session** with the seven slop signatures from Ch 22 §22.2. Reviewers who don't know what to look for in AI code will rubber-stamp.
- **Slow-review hooks** — if a PR is approved in under N seconds per line, surface a soft warning ("This review was 30 seconds for a 500-line diff; was that intentional?").
- **Reviewer rotation.** A senior reviewer with their name on every PR will skim. Distribute reviews; require two approvals on `ai:authored` PRs over 200 lines.
- **Reviewer load audit.** If reviewers are reviewing >5 PRs/day, something has to give. Likely candidates: cap auto-merge to L4 categories (per `../agent-autonomy-levels/autonomy-ladder.md`), or invest in AI reviewer subagents to triage.

### Anti-patterns to avoid

- **Counting bot-author PRs (Renovate, Dependabot) in the metric.** They're approved-in-seconds by design. Filter them.
- **Counting empty review time when PR is opened and merged by same person.** The review-time metric needs at least one non-author reviewer to be meaningful.
- **Punishing fast reviewers.** Some PRs deserve a 30-second review. The signal is the trend, not the individual review.

---

## Signal 4 — Revert rate trending up

### Definition

Percentage of merged PRs that are reverted within 30 days. Per Ch 31, this is "the most direct signal" — the others are leading; this one is closer to lagging but more reliable.

### How to measure

A "revert" is any PR whose title or commit message starts with `Revert ` (GitHub's default) or that targets the same files as a prior PR with a same-week timestamp and a "revert" / "rollback" label.

Detection:

```sql
WITH reverts AS (
  SELECT
    pr.number AS revert_pr_number,
    pr.merged_at AS revert_merged_at,
    REGEXP_EXTRACT(pr.title, 'Revert "?(#?\d+)') AS original_pr_ref,
    pr.team
  FROM pull_requests pr
  WHERE pr.title LIKE 'Revert %'
     OR EXISTS (
       SELECT 1 FROM pr_labels l
       WHERE l.pr_number = pr.number AND l.label IN ('revert', 'rollback')
     )
)
SELECT
  date_trunc('week', revert_merged_at) AS week,
  team,
  COUNT(*) AS revert_count,
  COUNT(*) / NULLIF((
    SELECT COUNT(*) FROM pull_requests
    WHERE date_trunc('week', merged_at) = date_trunc('week', revert_merged_at)
      AND team = reverts.team
  ), 0) AS revert_rate
FROM reverts
WHERE revert_merged_at >= NOW() - INTERVAL '12 weeks'
GROUP BY 1, 2
ORDER BY 1, 2;
```

PromQL (if you push revert events to a counter):

```promql
# Revert rate over the last 30 days, by team
sum by (team) (
  rate(pr_reverts_total{team=~".+"}[30d])
)
/
sum by (team) (
  rate(pr_merges_total{team=~".+"}[30d])
)
```

### Threshold

- **Healthy:** <2% of merged PRs reverted within 30 days
- **Watch:** 2–5% revert rate
- **Decay:** >5% revert rate, or revert rate doubling month over month

### Cross-tag the reverts

Per Ch 31 §31.6's authorship tagging convention, every revert should carry forward the original PR's authorship tag. The diagnostic is:

```sql
SELECT
  authorship_tag,    -- ai:none | ai:assisted | ai:authored | ai:agent
  COUNT(*) AS reverts,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct_of_reverts
FROM reverts
WHERE revert_merged_at >= NOW() - INTERVAL '90 days'
GROUP BY 1
ORDER BY 2 DESC;
```

If `ai:authored` reverts are >3x their share of merged PRs, that is the harness signal Ch 31 §31.6 describes:

> If your ai:authored PRs have 3x the defect rate of ai:none, your harness is broken or your reviewers are rubber-stamping. Either way, you have data.

### Corrective action

- **Per-revert postmortem** using the AI-authored template in `../incident-postmortem-templates/`. Specifically the slop-signature section and harness-deficiency checklist.
- **Quarantine the failing harness pattern.** If three reverts in a month traced to the same skill / CLAUDE.md section / autonomy level, that pattern is paused until the harness gap is closed.
- **Lower the autonomy ceiling** for the work category that produced the revert, per `../agent-autonomy-levels/raising-and-lowering-autonomy.md`.

### Anti-patterns to avoid

- **Counting reverts that were planned rollouts** (feature flag flips that look like reverts). Filter by commit-message pattern, not by file diff alone.
- **Reverting reverts (the "let's try again" pattern) without postmortem.** Each revert is data; ship the postmortem before re-attempting.

---

## Signal 5 — Customer-reported defects up

### Definition

The count of customer-reported bugs that:
1. Are confirmed as real bugs (not user error or expected behavior),
2. Reproduce on a recent build,
3. Map to a specific deploy that landed in the last 90 days.

This is the least leading of the leading indicators. By the time customers are reporting, the other signals should have flashed already. **If signal 5 fires before signals 1–4, your dashboard is broken.**

### How to measure

The data source: your support ticketing system (Zendesk, Linear, GitHub Issues, internal tooling). The discipline:

1. Bug-classified tickets are tagged by component
2. Each confirmed bug references the offending deploy (the commit range that introduced it)
3. The deploy-to-component map exists in your release tooling

SQL pseudocode:

```sql
SELECT
  date_trunc('week', confirmed_at) AS week,
  affected_team,
  COUNT(*) AS confirmed_customer_defects
FROM support_tickets
WHERE category = 'bug'
  AND status IN ('confirmed', 'resolved')
  AND confirmed_at >= NOW() - INTERVAL '12 weeks'
GROUP BY 1, 2
ORDER BY 1, 2;
```

### Threshold

- **Healthy:** week-over-week count stable; rate per 10K monthly active users below team baseline
- **Watch:** 20% increase month over month
- **Decay:** sustained increase across two consecutive months, OR a sudden spike correlated with a recent deploy

### Pair with the AI-authorship attribution

Per Ch 31 §31.6, every customer-reported defect that becomes a postmortem should carry the AI-authorship tag of the introducing PR. The diagnostic over time:

| Authorship tag | Defects per 100 merged PRs |
|---|---|
| `ai:none` | (baseline) |
| `ai:assisted` | (should be ≤ baseline) |
| `ai:authored` | (should be ≤ baseline) |
| `ai:agent` | (should be ≤ baseline) |

If any of the AI-tagged categories is significantly above the `ai:none` baseline, the harness is failing for that category.

### Corrective action

The full incident response loop applies — see `../incident-postmortem-templates/`. Specific to the decay-signal dashboard:

- **Each confirmed customer defect feeds the agent-ready-issue pipeline** (see [`agent-ready-issue-pipeline.md`](agent-ready-issue-pipeline.md)). The triage agent files the reproduction case automatically.
- **The defect-introducing commit is reviewed for slop signatures** — even if the defect is being fixed, the audit is the durable artifact.
- **The harness gap is identified** per `../incident-postmortem-templates/harness-deficiency-checklist.md`.

### Anti-patterns to avoid

- **Counting all support tickets as "defects."** Filter to confirmed bugs. Confusion tickets, feature requests, and user errors will swamp the signal.
- **Treating the metric as a per-engineer signal.** It's a team-level harness signal; never used in performance review.

---

## Signal 6 — Senior-engineer 1:1 culture concerns

### Definition

Per Ch 31:

> Soft signal but reliable; treat seriously.

The mechanism: in 1:1s with senior engineers (Staff+, IC5+, or whatever your level naming uses), the engineering manager asks once per month some variant of:

> "Are you seeing any patterns in the team's AI-assisted code or workflow that concern you? Not specific incidents — patterns. Things you'd want to see at the team level."

The signal is the count of senior engineers in a given month who flag a concern in this conversation, normalized by the count of senior engineers in those 1:1s.

### How to measure

This is the only signal in the six that does not live on a dashboard. It lives in 1:1 notes (whoever you use — manager notes, Lattice, 15Five, Reflektive, a Google Doc). The discipline:

- The question is asked monthly
- Responses are logged in a single field (concern: Y/N, with notes)
- An anonymized count is maintained at the engineering-leadership layer

### Threshold

- **Healthy:** <10% of senior engineers flag a concern in a given month
- **Watch:** 10–25%
- **Decay:** >25% for two consecutive months — or any month where a specific concern is raised independently by 3+ senior engineers

The independent-concurrent-flag pattern is the strongest version of this signal. When three senior engineers — who do not work on the same team and have not coordinated — raise the same concern in the same month, it is almost always real and almost always actionable.

### Corrective action

- **Senior-engineer roundtable.** A 90-minute facilitated session where the senior engineers who raised concerns walk through what they're seeing. The output: a prioritized list of harness gaps and culture concerns.
- **Action items with owners and dates.** No "we'll talk to people about this." Specific items: update CLAUDE.md, lower autonomy on category X, ship skill Y, audit Z module's test coverage.
- **Re-survey at month 6.** Concerns that persist after one round are the deeper-rooted issues.

### Anti-patterns to avoid

- **Asking the question once and never again.** This signal works because of the repetition; senior engineers learn that their input is sought and weighted.
- **Reporting individual responses.** Always anonymized; always rolled up. The signal evaporates the moment senior engineers think their concerns will be attributed.
- **Treating "no concerns this month" as the goal.** Some months will have concerns; the goal is to see the concerns when they're real, not to suppress them.

---

## The "pull the lever" rule (Ch 31)

The book is explicit:

> Two consecutive months of decay on three or more is a "pull the lever" signal — pause new-team rollout, audit the harness, run a senior-engineer-led code-review-quality review.

The rule in code:

```python
def should_pull_the_lever(decay_history: dict[str, list[bool]]) -> bool:
    """
    decay_history: {signal_name: [is_decaying_month_n_minus_1, is_decaying_month_n]}
    Returns True if 3+ signals are decaying for 2 consecutive months.
    """
    signals_decaying_both_months = sum(
        1 for history in decay_history.values()
        if len(history) >= 2 and all(history[-2:])
    )
    return signals_decaying_both_months >= 3
```

What "pull the lever" means in practice:

1. **Pause new-team rollout.** No new teams adopt the AI tooling until the audit completes. Teams currently using it continue but at a held autonomy level — no L2→L3 or L3→L4 raises during the audit period.
2. **Audit the harness.** A senior-engineer-led review of:
   - CLAUDE.md / AGENTS.md across the affected repos
   - Slop-detector hook coverage
   - Mutation test gates
   - Reviewer load
   - Postmortem corpus from the last 90 days
3. **Senior-engineer-led review-quality review.** Sample 30 recent PRs across the team. Have a senior engineer re-review them against the seven slop signatures (Ch 22 §22.2). Tally the catches that the original review missed. The catch rate is the team's actual review quality.
4. **A specific harness improvement ships before the lever is released.** Not "we talked about it." Not "we'll be more careful." A specific skill, hook, CLAUDE.md section, or autonomy-level change ships with a date.

The lever stays pulled until the audit's action items ship AND the next month's signals show improvement.

## Putting it together: the decay-signal dashboard

See [`six-metric-dashboard/dashboard-overview.md`](six-metric-dashboard/dashboard-overview.md) for the layout. The decay-signal tile is its own panel and updates monthly, not weekly — these are slow signals by design.

A reference layout:

```
┌──────────────────────────────────────────────────────────────────┐
│ Quality Decay Signals                  Last updated: 2026-MM-DD  │
├──────────────────────────────────────────────────────────────────┤
│ Mutation score              74.2%  ▲ +0.4   [HEALTHY]            │
│ Median PR size              247 LOC ▼ -12   [HEALTHY]            │
│ Review seconds/line         2.8s   ▲ +0.2   [HEALTHY]            │
│ Revert rate (30d)           1.8%   ▼ -0.2   [HEALTHY]            │
│ Customer-reported defects   12     ▼ -3     [HEALTHY]            │
│ Senior 1:1 concerns         1 of 8 ▼ -1     [HEALTHY]            │
├──────────────────────────────────────────────────────────────────┤
│ Pull-the-lever status: GREEN (0 signals decaying for 2 months)   │
└──────────────────────────────────────────────────────────────────┘
```

When the lever indicator goes yellow or red, it links to a runbook page that lists the specific signals decaying, the timeline, and the current audit owner.

## What this dashboard will NOT do

- Will not catch every quality issue. It catches AI-driven decay specifically; other kinds of quality issues require their own instrumentation.
- Will not work without the AI-authorship tagging convention (Ch 31 §31.6). The signals tell you decay is happening; the tagging tells you which kind of authorship is driving it.
- Will not work as a performance management tool. Per Ch 31 §31.1: never show individual scores; team-level only.
- Will not produce useful data in the first month. The signals require 60–90 days of baseline before "trending" means anything. Capture the baseline now per [`baseline-measurement-template.md`](baseline-measurement-template.md).

## Companion artifacts

- [`code-maturity-rubric.md`](code-maturity-rubric.md) — the LLM-graded maturity signal that pairs with these decay signals
- [`six-metric-dashboard/`](six-metric-dashboard/) — the broader six-metric dashboard these signals overlay onto
- [`agent-ready-issue-pipeline.md`](agent-ready-issue-pipeline.md) — what happens when signal 5 fires
- [`baseline-measurement-template.md`](baseline-measurement-template.md) — the pre-rollout baseline you need to detect "trending"
- `../incident-postmortem-templates/` — where confirmed defects feed
- `../agent-autonomy-levels/raising-and-lowering-autonomy.md` — the autonomy-ceiling adjustment that follows the lever
- Ch 31 §31.3, Ch 31 §31.6 — sources
