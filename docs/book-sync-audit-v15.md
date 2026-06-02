# Book ↔ Repo Sync Audit — *Software Engineering with AI* (revised v15)

Full chapter-by-chapter audit of the companion repository against the book manuscript
**revised v15** (May 2026). It records what was checked, what was already in sync, what
gaps were found, and what this sync changed. Re-run this audit on each book revision.

**Method:** every Part, Chapter (1–61, including the v15 sub-chapters 6.6 / 33.5 / 43.6 /
47.5 / 50.5), and Appendix (A–L) was mapped to its companion-repo artifact via the
README's "Book → folder map," then the path was verified to exist on disk and its content
sanity-checked against the book. Terminology was checked for drift (model names, the
Intake rename, the canonical repo URL).

## Summary

- **Already in sync:** the bulk of the repo. 12 starter skills (App E) ✓, the Intake
  rename ✓ (no stray "Tixie"), the canonical URL ✓, model names consistent with the book
  (Sonnet 4.6 / Opus 4.7 / Haiku 4.5; "Sonnet 5"/"Haiku 4.6" appear only as legitimate
  forward-looking examples), and most chapters mapped to real artifacts.
- **Gaps fixed in this sync:** the book promised several companion-repo paths that did not
  exist, and several README-referenced scripts were missing. All created. The v15
  sub-chapters now have artifacts and map rows.
- **Intentionally book-only:** a set of pure-prose chapters have no artifact and are not
  expected to (listed below).

## Changes made in this sync (to book v15)

| Change | Book reference | Detail |
|--------|----------------|--------|
| `subagents/` created (renamed from `agents/`) | Appendix F, Ch 14 | Book cites `/subagents/`; repo used `/agents/`. Renamed for literal match; all references updated (README, CONTRIBUTING, and stale `governance/subagents/` pointers). |
| `scorecard/ai-readiness.xlsx` + `scorecard/README.md` | Appendix H | Book cites a fillable xlsx scorecard; repo only had the Python audit script. Added the spreadsheet (same 23 criteria, categories, weights, chapter refs) as the manual counterpart. |
| `checklists/code-smells.md` | Appendix I | Was absent. Authored from the seven slop signatures (Ch 2 §2.2) + reviewer countermeasures. |
| `checklists/test-review.md` | Appendix K | Was absent. Authored from Ch 7 / Ch 8 / Ch 21 test-review discipline. |
| `prompts/` library (7 pattern files + README) | Appendix J | Was absent. Authored durable prompt patterns (agent-ready issue, information-requirements, plan→implement→review, independent verification, slop review, task decomposition). |
| `benchmarks/local-llms-current-state/README.md` | Ch 28 §28.3 | Book explicitly moves perishable local-LLM specifics to this path; directory did not exist. Added with the durable principle + a dated-snapshot structure. |
| `do-not-automate-catalog/net-negative-domains.md` | Ch 33.5 (v15) | Added the six net-negative domains + the "this list will shrink" trajectory. |
| `docs/ai-in-non-coding-engineering-work.md` | Ch 47.5 (v15) | Added the seven non-coding workflows + caveats. |
| `docs/ic-perspective-running-agents.md` | Ch 43.6 (v15) | Added the durable, actionable points of the IC chapter. |
| `docs/what-i-might-be-wrong-about.md` | Ch 50.5 (v15) | Added the five steelman counter-cases + the falsifiable thesis-flip conditions. |
| `scripts/token-cost-estimator.py`, `pr-ai-tagger.py`, `llms-txt-generator.py`, `skill-linter.py` | Ch 26/29, Ch 21/31, Ch 6 §6.5.3, CONTRIBUTING | All four were named in the README/CONTRIBUTING but missing from `scripts/`. Implemented as working utilities. |
| README "Book → folder map" extended | Appendices I/J/K; Ch 28; Ch 33.5/43.6/47.5/50.5 | New rows added; App F → `/subagents/`, App H → xlsx + script. |
| CONTRIBUTING + README "forthcoming" notes corrected | — | `subagents/_TEMPLATE.md` exists; "(forthcoming)" removed. |

## Chapter-by-chapter inventory

Status legend: **synced** (artifact exists & matches), **fixed** (gap closed in this sync),
**book-only** (pure prose, no artifact expected), **partial** (covered indirectly / future).

| Ch | Topic | Artifact | Status |
|----|-------|----------|--------|
| **Part I — Foundations** | | | |
| 1 | AI-native engineering reality | — | book-only |
| 2 | AI slop & review crisis | `code-review-craft-workshop/`, `scripts/slop-detector.py`, `checklists/code-smells.md` | synced |
| 3 | Two-loop workflow | — | book-only |
| 4 | AI-native product lifecycle | — | book-only |
| 5 | Role evolution by function | `people/`, `solutions-engineer-and-tech-pm/` | partial |
| **Part II — Repo as Agent Habitat** | | | |
| 6 | Repo legibility | `templates/CLAUDE.md`, `templates/AGENTS.md` | synced |
| 6.6 | Testing the harness | `benchmarks/`, `evals-and-benchmarks-runbook/` | synced |
| 7 | Verify command | `starter-kits/*/scripts/verify.sh` | synced |
| 8 | Verification pyramid | `benchmarks/`, `checklists/test-review.md` | partial |
| 9 | Architecture invariants | `hooks/` | partial |
| 10 | Agent locality | `starter-kits/*` per-pkg READMEs | partial |
| 11 | AI in legacy codebases | `legacy-codebase-onboarding/`, `starter-kits/legacy-bridge/`, `docs/legacy-migration/` | synced |
| 12 | Monorepo & microservice patterns | `starter-kits/typescript-monorepo/` | partial |
| **Part III — The Claude Code Harness** | | | |
| 13 | Skills as playbooks | `skills/` (12) | synced |
| 14 | Subagents as a small team | `subagents/` | synced (fixed path) |
| 15 | Hooks as deterministic enforcement | `hooks/` | synced |
| 16 | Plugins for company standards | `docs/plugin-marketplace.md` | partial |
| 17 | MCP tools & permissions | — | book-only |
| 18 | Skills & plugins practical guide | `docs/plugin-marketplace.md` | synced |
| **Part IV — Day-to-Day Workflow** | | | |
| 19 | Agent-ready issues | `templates/agent-ready-issue.md`, `prompts/agent-ready-issue.md` | synced |
| 20 | Plan → Implement → Review | `prompts/plan-implement-review.md`, `subagents/planner.md` | synced |
| 21 | PR standards for AI code | `templates/pr-template.md` | synced |
| 22 | Code review in the AI era | `scripts/slop-detector.py`, `code-review-craft-workshop/`, `checklists/code-smells.md` | synced |
| 23 | Release mgmt & progressive delivery | — | book-only |
| 24 | Observability as feedback | `skills/observability-change/` | partial |
| 25 | AI-assisted ADRs | — | book-only |
| **Part V — Economics, Models, Tooling** | | | |
| 26 | Model selection & cost discipline | `cost-discipline-runbook/`, `scripts/token-cost-estimator.py` | synced (script added) |
| 27 | AI engineering economics (CFO) | `executive-strategic-kit/roi-calculator.md` | partial |
| 28 | Cost optimization w/ local LLMs | `benchmarks/local-llms-current-state/` | synced (added) |
| 29 | Token cost warning (exec) | `cost-discipline-runbook/`, `docs/measurement-dashboards/` | partial |
| 30 | Approved tooling matrix | `executive-strategic-kit/approved-tooling-matrix-template.md` | synced |
| 31 | Software metrics for the AI era | `metrics-and-measurement-infrastructure/`, `failed-one-shot-triage/` | synced |
| **Part VI — Governance and Safety** | | | |
| 32 | Autonomy levels & taxonomy | `agent-autonomy-levels/` | synced |
| 33 | Do-Not-Automate catalog | `do-not-automate-catalog/` | synced |
| 33.5 | Domains AI is net-negative | `do-not-automate-catalog/net-negative-domains.md` | synced (added) |
| 34 | Data classification & IP | `executive-strategic-kit/data-classification-matrix.md` | synced |
| 35 | Sandbox reference architecture | — | book-only |
| 36 | Security controls & prompt injection | `prompt-injection-test-suite/` | synced |
| 37 | Prompt injection testing | `prompt-injection-test-suite/` | synced |
| 38 | Vendor risk & procurement | `vendor-procurement-runbook/` | synced |
| 39 | Incident response for AI bugs | `incident-postmortem-templates/` | synced |
| 40 | Provenance, audit, outcomes | `scripts/pr-ai-tagger.py` | partial (tagger added) |
| **Part VII — The Organization** | | | |
| 41 | AI-native SDLC & agile | — | book-only |
| 42 | Team structure, roles, hiring | `people/`, `platform-team-charter/` | synced |
| 43 | Human skill development | `junior-trajectory/` | synced |
| 43.6 | The IC perspective | `docs/ic-perspective-running-agents.md` | synced (added) |
| 44 | Onboarding, certification, rollout | `ai-tooling-onboarding-curriculum/` | synced |
| 45 | Enterprise change management | — | book-only |
| 46 | Managing hyped expectations | `executive-strategic-kit/hype-rebuttal-table.md` | partial |
| 47 | Worked end-to-end examples | `examples/` (stub; v2026.q4) | partial |
| 47.5 | AI in non-coding engineering work | `docs/ai-in-non-coding-engineering-work.md` | synced (added) |
| 48 | Management & executive guidance | `executive-strategic-kit/` | partial |
| 49 | AI coding reading list | `reading-list/` | synced |
| 50 | The closing principle | — | book-only |
| 50.5 | What I might be wrong about | `docs/what-i-might-be-wrong-about.md` | synced (added) |
| **Part VIII — The Mid-Size Playbook** | | | |
| 51 | 90-day VP plan | `executive-strategic-kit/90-day-plan.md`, `docs/90-day-vp-playbook/` | synced |
| 52 | CEO & board kit | `executive-strategic-kit/board-deck-template.md`, `.../ceo-emails/` | synced |
| 53 | Migration from existing tooling | `migration-playbooks/` | synced |
| 54 | Mid-size economics | `executive-strategic-kit/roi-calculator.md` | synced |
| 55 | Platform-capacity-constrained playbook | `platform-team-charter/` | partial |
| 56 | Customer-facing AI story | `customer-facing-ai-disclosure/`, `executive-strategic-kit/security-questionnaire-answers.md` | synced |
| 57 | What to commit / refuse | `executive-strategic-kit/what-number-do-i-commit-to.md` | synced |
| 58 | Recovery playbooks | `incident-postmortem-templates/`, `failed-one-shot-triage/` | partial |
| 59 | Working with peer executives | — | book-only |
| 60 | Comp, leveling & retention | `promotion-and-leveling-rubric/`, `people/` | synced |
| 61 | The skip-level defense | `skip-level-defense/` | synced |
| **Appendices** | | | |
| A | CLAUDE.md template | `templates/CLAUDE.md` | synced |
| B | AGENTS.md template | `templates/AGENTS.md` | synced |
| C | Agent-ready issue template | `templates/agent-ready-issue.md` | synced |
| D | PR template | `templates/pr-template.md` | synced |
| E | 12 starter skills | `skills/` | synced |
| F | Subagent library | `subagents/` | synced (fixed path) |
| G | Hook library | `hooks/` | synced |
| H | Readiness scorecard | `scorecard/ai-readiness.xlsx` + `scripts/ai-readiness-audit.py` | synced (xlsx added) |
| I | AI code smell checklist | `checklists/code-smells.md` | synced (added) |
| J | Prompt pattern library | `prompts/` | synced (added) |
| K | AI test review checklist | `checklists/test-review.md` | synced (added) |
| L | Field notes (code-forge pilot) | `war-stories/` | synced |

## Intentionally book-only (no artifact expected)

Ch 1, 3, 4, 17, 23, 25, 35, 41, 45, 50, 59 are pure-prose chapters with no companion
artifact. They are listed here so a future auditor doesn't mistake their absence for a gap.

## Partial / future (tracked, not blocking)

These are covered indirectly today and are candidates for dedicated artifacts in a future
release: Ch 5, 8, 9, 10, 12, 16, 24, 27, 29, 40, 46, 47 (`examples/` stub → v2026.q4),
48, 55, 58. None are book-promised explicit paths, so they are not sync-blocking — unlike
the appendix paths fixed above.
