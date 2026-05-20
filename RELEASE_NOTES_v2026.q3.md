# Release Notes — v2026.q3 (May 2026)

The first tagged release of the companion repository for *Software Engineering with AI*. This release exists to close the gap the v2026.q3 README and CHANGELOG were already claiming: the substantive work was in `main`, but there was no tag and no release artifact, so a careful visitor saw "0 releases" on the Releases page and bounced.

## What's in this tag

This tag corresponds to a substantial structural and content pass on the repo. The headline changes:

### Structure

- **Single source of truth per concept.** Deduplicated `governance/prompt-injection-test-suite/` into `prompt-injection-test-suite/` (keeping the more complete top-level runner and pulling in the governance fixtures, scripts, and `_TEMPLATE.md`). Deduplicated `exec-kit/` into `executive-strategic-kit/` (keeping the executive-strategic-kit naming, pulling in the 90-day plan, security questionnaire answers, vendor negotiation scripts, and CEO email templates from exec-kit, and moving the binary renders into `executive-strategic-kit/rendered/`).
- **Stubs filled for aspirational directories.** `docs/`, `templates/`, `hooks/`, `agents/`, `examples/`, and `tools/` now exist as referenced from the README. Templates and starter agents/hooks are populated from the typescript-monorepo starter kit; `docs/` subdirectories carry README pointers to the closest existing content with explicit "forthcoming in v2026.q4" framing for content still under development.
- **Top-level README rewritten.** Added a "What's inside" section with three sentences per top-level directory, so a cold visitor can find what they need without reading the CHANGELOG.

### Content

- **Intake (formerly "Tixie") pattern.** Renamed everywhere in the repo and the book. The pattern name was distracting; "Intake" is descriptive of what it does.
- **URL inconsistency fixed.** All `github.com/ryanbyrd/ai-engineering-handbook` references replaced with `github.com/theryanbyrd/software-engineering-with-ai` (the actual repo location). Affected: README, audit script HTML footer, starter-kit CI workflows, exec-kit README.
- **Binary deliverables replaced with markdown sources.** ROI calculator, board deck template, all-hands deck template, approved tooling matrix, and data classification matrix are now agent-readable markdown. The rendered `.xlsx`/`.pptx` files remain in `executive-strategic-kit/rendered/` for executives who prefer those formats, but the markdown is the source of truth (Ch 6 §6.0 — code/text is the source of truth).

### Audit script (`scripts/ai-readiness-audit.py`)

- **Sharpened `check_invariants_documented`.** Now requires at least one positively-phrased invariant heading (e.g., a Markdown `## Architecture invariants` section) rather than counting keyword matches in any context. The old check would false-positive on a repo that documents what NOT to do — exactly the auditor-hallucination problem Appendix L warns about.
- **`check_cost_telemetry_referenced` bumped from weight 1 → 2.** Ch 29 treats cost telemetry as near-mandatory for any production agentic workflow; "nice-to-have" understated the stakes.
- **New: `check_claude_settings_permissions`.** Verifies that `.claude/settings.json` exists and has an explicit `permissions` block. The single most likely place an autonomy-drift incident starts.
- **New: `check_branch_protection` (opt-in).** Requires `--github-token` to query the GitHub API. Without the token, the check is skipped with a `warn` explaining the limitation.

### CI

- **`.github/workflows/audit.yml`** — runs the AI-readiness audit against each starter kit on every PR and push to main. Uploads HTML + JSON artifacts. Comments a per-kit summary on the PR. Includes a `audit-self` job that runs the audit against this repo's own root.
- **`.github/workflows/reading-list-stale.yml`** — weekly cron (Monday 14:00 UTC) running `reading-list/scripts/generate.py --check-stale`. Opens a `reading-list-stale` labeled issue if anything is within 60 days of `dated_through`; appends to the existing issue rather than spamming new ones.

### Documentation

- **`CONTRIBUTING.md`** updated with explicit links to the five `_TEMPLATE` files reviewers should start from (skills, agents, hooks, war stories, prompt-injection test cases).

## Audit score for the starter kits (as of this tag)

Run `python3 scripts/ai-readiness-audit.py starter-kits/typescript-monorepo --json` to reproduce.

| Starter kit | Score | Percent |
|---|---|---|
| `starter-kits/typescript-monorepo/` | 48 / 55 | 87% |
| `starter-kits/python-service/` | _to verify in CI_ | _to verify in CI_ |
| `starter-kits/legacy-bridge/` | _to verify in CI_ | _intentionally lower; brownfield MVH_ |

The audit-self job for the repo root will also publish a score on every push to main — that's the "do we eat our own dog food" check.

## What this release deliberately does NOT include

- **No new starter kits.** The Next.js starter kit promised in the README is forthcoming in v2026.q4.
- **No new community stack kits.** Java, Go, Rust, .NET, Ruby remain at "community fork" status; no first-class CI for them yet.
- **No `examples/` content.** The directory now exists with a stub README, but the end-to-end walkthrough examples are forthcoming in v2026.q4.
- **No PDF / EPUB of the book.** The book is published separately; this repo is the companion repository for the operational artifacts.

## Upgrade notes (if you forked an earlier `main`)

- If you forked before this tag and you have a `governance/prompt-injection-test-suite/` directory, you can delete it; the unified version lives at `prompt-injection-test-suite/`. The `cases/` files map to `test-cases/`; fixtures and scripts are in their original-named subdirectories.
- If you forked before this tag and you have an `exec-kit/` directory, similarly: it has been merged into `executive-strategic-kit/`. The binary deliverables are at `executive-strategic-kit/rendered/`.
- If you imported the audit script: `--json` now accepts an optional path argument (`--json audit.json`) and emits a `failed_checks` field for CI summary use. The behavior with no path argument is unchanged. The `check_branch_protection` check is appended to results; without a `--github-token` it returns `warn`.

## Errata for the printed book

None in this release. Errata for the printed book will be tracked in `CHANGELOG.md` under each release header as they accumulate.

— Ryan Byrd, May 2026
