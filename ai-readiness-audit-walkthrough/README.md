# AI Readiness Audit Walkthrough

The 24-check explainer for `scripts/ai-readiness-audit.py`. Direct companion to the audit script with chapter-by-chapter mapping back to [_Software Engineering with AI: A Practical Handbook for the Claude Code Era_](https://www.linkedin.com/in/ryanbyrd) by Ryan Byrd.

The audit script scores a repository against 24 criteria from the book and produces an HTML report (or JSON) with concrete next actions and chapter references. This folder is for the engineers who run the audit and want to understand:

- What each check means
- What passing or failing each check signals about the codebase's harness maturity
- The prioritized remediation paths for each common failure mode

## What's in here

| File | Purpose |
|---|---|
| [`how-to-run.md`](how-to-run.md) | Running the audit, interpreting output, integration with CI |
| [`check-by-check-explainer.md`](check-by-check-explainer.md) | Each of the 24 checks, what it tests, what passing/failing means |
| [`prioritized-remediation-paths.md`](prioritized-remediation-paths.md) | Triage flow: from audit output to specific next actions, ordered by leverage |
| [`scoring-and-thresholds.md`](scoring-and-thresholds.md) | What the scores mean, what thresholds to set in CI, how to use over time |
| [`audit-cadence-and-tracking.md`](audit-cadence-and-tracking.md) | When to run, how often, what to track across runs |

## The script's structure

The audit runs 24 checks across these categories:

| Category | Checks | What it covers |
|---|---|---|
| **Repo legibility** | 5 | CLAUDE.md, AGENTS.md, llms.txt, README, per-package READMEs |
| **Verify command** | 4 | `verify` exists; includes lint, typecheck, tests |
| **Test discipline** | 2 | Test files exist; CI workflow runs verify |
| **Harness** | 4 | `.claude/` directory, skills, subagents, hooks |
| **PR discipline** | 3 | PR template, AI authorship in template, CODEOWNERS |
| **Governance** | 4 | SECURITY.md, forbidden patterns, invariants, data classification |
| **Cost & observability** | 1 | Cost telemetry referenced |
| **AI-aware incident response** | 1 | Incident runbook exists |

Each check has a weight (1 = nice to have, 2 = important, 3 = critical) and a status (pass / warn / fail).

## How the audit produces a score

Per check: weight × status_value (1.0 / 0.5 / 0.0)

Total score = sum of (weight × status) divided by sum of (weight × 1.0) — i.e., percentage of available points earned.

## Why this folder exists alongside the script

The script tells you what's missing. This folder tells you why it matters and what to do about it.

A team that runs the audit and gets 35/100 needs:
- Understanding of why the score is 35/100 (the script gives the categorical view)
- Understanding of which gaps to close first (this folder's prioritization)
- Understanding of what closing each gap actually requires (this folder's per-check explainer)

Without the explainer, the audit is a number; with it, it's a roadmap.

## Who this is for

- **Engineering managers** running an audit on their team's repo for the first time
- **Tech leads** advocating for harness investment
- **Platform team members** running audits across multiple repos
- **VP of Engineering** running a quarterly cross-repo audit
- **Engineers new to the team** trying to understand what good looks like

## Read first

- The book chapters referenced in each check (the audit's chapter_ref column)
- `scripts/ai-readiness-audit.py` itself — read the source; it's stdlib Python and ~600 lines
- This folder's [`how-to-run.md`](how-to-run.md) for the operational side

## What this walkthrough WILL do

- Demystify the audit's output
- Connect each check back to the book chapter
- Provide specific next actions for each common failure
- Establish a prioritization for what to address first
- Build the cadence for running audits over time

## What this walkthrough will NOT do

- Will not work as substitute for the book chapters. Each check references a chapter; that's where the substantive content lives.
- Will not work without running the audit first. The walkthrough is the post-audit interpretation.
- Will not produce a passing score by itself. Closing the gaps the audit identifies is real engineering work.
- Will not protect against false positives. The audit's heuristics are imperfect; some "fail" results are reasonable trade-offs for your team.

## How this folder fits with adjacent material

| Need | Where to look |
|---|---|
| The audit script itself | `scripts/ai-readiness-audit.py` |
| The book chapters the audit references | the merged book PDF / source |
| Specific harness components the audit checks for | `starter-kits/`, `governance/`, `skills/` |
| Brownfield-specific application | `legacy-codebase-onboarding/` |
| Platform team's role in running cross-repo audits | `platform-team-charter/` |

## Companion artifacts

- `scripts/ai-readiness-audit.py` — the audit itself
- The book — the canonical source for each check's reasoning
- `starter-kits/` — the harness templates many checks look for
- `governance/` — the mechanical infrastructure many checks reference
- `legacy-codebase-onboarding/` — for teams whose audit results reflect brownfield reality
