# How to Run the Audit

Operational guidance for running `scripts/ai-readiness-audit.py`, interpreting output, and integrating with CI.

## Quick start

```bash
# Basic audit, prints HTML report to stdout
python3 scripts/ai-readiness-audit.py /path/to/repo

# Save HTML report to file
python3 scripts/ai-readiness-audit.py /path/to/repo -o report.html

# JSON output (for tooling integration)
python3 scripts/ai-readiness-audit.py /path/to/repo --json

# Exit non-zero if score below threshold (for CI)
python3 scripts/ai-readiness-audit.py /path/to/repo --threshold 60
```

## Requirements

- Python 3.9+
- Standard library only (no pip install needed)
- Read access to the repo

## What the script reads

The script reads the repo's filesystem. Specifically:

- Top-level files (CLAUDE.md, AGENTS.md, README.md, etc.)
- Common directories (`.claude/`, `.github/`, `tests/`, etc.)
- File contents for keyword matching (e.g., looking for `lint` or `pytest` in package.json scripts)

The script does NOT:
- Run the verify command
- Execute tests
- Check git history
- Connect to external services
- Modify any files

It's a static read-only audit; it's safe to run on any repo without side effects.

## Interpreting output

### HTML report

The HTML report has:

1. **Header section** — overall score, breakdown by category, repo metadata
2. **Failed checks** at the top — these are the gaps to address first
3. **Warnings** — partial credit; checks where some criteria are met but not all
4. **Passed checks** — the harness components in place

Each check shows:
- Check name
- Category
- Chapter reference (back to the book)
- Description (what it tests for)
- Status (pass / warn / fail)
- Details (what the audit found)
- Fix (specific next action)

### JSON output

For integration with dashboards or other tooling. Schema:

```json
{
  "version": "2026.q3",
  "repo": "/path/to/repo",
  "timestamp": "2026-MM-DDTHH:MM:SSZ",
  "score": 73.5,
  "max_score": 100,
  "checks": [
    {
      "name": "...",
      "category": "...",
      "chapter_ref": "...",
      "description": "...",
      "weight": 3,
      "status": "pass",
      "details": "...",
      "fix": ""
    }
  ]
}
```

## When to run the audit

### Initial baseline

When a team is starting AI tooling adoption (or formalizing it), run the audit to establish a baseline. The first audit is for self-awareness; expect a low score.

### After harness investments

After shipping harness components (a new skill, a new hook, a new subagent), re-run to verify the audit reflects the change. The audit's weight on specific checks should align with what was shipped.

### Quarterly

Run quarterly to track progress over time. Per [`audit-cadence-and-tracking.md`](audit-cadence-and-tracking.md).

### Pre-audit (before customer audits, security reviews)

When a customer audit or security review is upcoming, the AI readiness audit can surface gaps that the customer or auditor may ask about.

### Cross-repo audit

Platform team or VPE running an audit across all repos in the org to identify outliers and patterns.

## CI integration

For ongoing visibility, integrate the audit into CI:

```yaml
# .github/workflows/ai-readiness.yml
name: AI Readiness Audit
on:
  pull_request:
  schedule:
    - cron: '0 0 * * 1'  # Weekly Monday

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python3 scripts/ai-readiness-audit.py . --threshold 60
```

The threshold:
- 60 is a starting bar for a maturing team
- 75 for a team that's invested seriously
- 85+ for a team running at high autonomy and high reliability

Don't set the threshold too high too soon. A failing check on a PR creates noise; engineers learn to ignore. Set the threshold at the team's current score + 5-10 points; raise it as the score improves.

## Cross-repo aggregation

For platform teams running across multiple repos:

```bash
# Audit all repos and aggregate
for repo in /path/to/repos/*; do
    python3 scripts/ai-readiness-audit.py "$repo" --json > "audits/$(basename "$repo").json"
done

# Aggregate (your script — common pattern):
# - Per-team score average
# - Per-check pass rate across repos
# - Outliers (repos significantly below median)
```

The aggregation surfaces:
- Which checks are universally failing (org-wide gap)
- Which checks are passing universally (table stakes; don't focus there)
- Which repos are outliers (need targeted help)

## What the audit doesn't capture

The audit is heuristic. It's looking for the presence of specific files and patterns. It doesn't catch:

- **Whether the files have good content.** A 2-line CLAUDE.md gets the same pass as a comprehensive one.
- **Whether the harness is actually used.** A skills directory with stale skills doesn't reduce the audit score.
- **Whether the team's discipline matches the artifacts.** The audit can't measure review discipline; it only checks that PR templates exist.
- **Whether the team operates at the autonomy level the harness supports.** The audit doesn't check for drift.

For these, see:
- [`check-by-check-explainer.md`](check-by-check-explainer.md) — what each check actually measures
- `agent-autonomy-levels/autonomy-drift-monitoring.md` — drift detection separately

## Common failure modes when running the audit

### "Audit says we have a CLAUDE.md but the file is one line"

Audit's heuristic: file exists, file has content. If the content is minimal, the check passes mechanically but the harness value is low.

Mitigation: pair the audit with manual review. The audit is the floor; manual review of CLAUDE.md / AGENTS.md / skills is the ceiling.

### "We have a verify command but the audit didn't find it"

Audit looks for common patterns (Makefile targets, package.json scripts, justfile, taskfile, scripts/verify.sh). If your verify is in an uncommon location, the audit might miss it.

Mitigation: add a standard entry point. Even a `scripts/verify.sh` that calls into your actual verify is enough for the audit to find.

### "We have skills in `.claude/skills/` but the count is reported low"

Audit counts files in the skills directory. If your skills are subdirectories (`.claude/skills/skill-name/SKILL.md`), the audit's counting may differ.

Mitigation: read the source; understand what the audit actually counts. Some checks may need adaptation for your specific layout.

## What this guide will NOT do

- Will not handle every repo layout. The audit is heuristic; some adjustment may be needed.
- Will not produce a meaningful score for very small repos (a 5-file repo doesn't need most of these artifacts).
- Will not automate the actual harness work. Running the audit doesn't ship the changes; engineering does.

## Companion artifacts

- [`check-by-check-explainer.md`](check-by-check-explainer.md) — what each check means
- [`prioritized-remediation-paths.md`](prioritized-remediation-paths.md) — what to fix first
- [`scoring-and-thresholds.md`](scoring-and-thresholds.md) — interpreting the score
- [`audit-cadence-and-tracking.md`](audit-cadence-and-tracking.md) — running over time
- `scripts/ai-readiness-audit.py` — the script
