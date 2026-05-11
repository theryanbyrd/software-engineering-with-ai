# Check-by-Check Explainer

Each of the 24 checks in `scripts/ai-readiness-audit.py`, with what passing or failing means.

## How to read this file

For each check:

- **What it tests:** the heuristic the audit script applies
- **Why it matters:** the underlying capability the check signals
- **Pass / fail meaning**
- **Common reasons for failure**
- **Specific next action**

---

## Category — Repo legibility

### Check 1: CLAUDE.md exists at repo root (weight 3, critical)

**Reference:** Ch 6, Appendix A

**What it tests:** A file named `CLAUDE.md` (or close variant) at the repo root.

**Why it matters:** CLAUDE.md is the agent's project memory — conventions, commands, architectural invariants. Without it, the agent has no team-specific context; every session starts cold.

**Pass means:** the file exists with substantive content.
**Warn means:** the file exists but is minimal (under ~500 chars).
**Fail means:** no CLAUDE.md exists.

**Common reasons for failure:**
- The team hasn't started using AI tooling extensively
- The team is using AGENTS.md only
- The team has the content scattered across other files

**Specific next action:**
- Use the template in `starter-kits/agent-friendly/CLAUDE.md` as starting point
- Cover: build commands, test commands, architectural invariants, the "never do" list
- Aim for a substantive file (1500-3000 words) but stay focused; bloat is its own problem (per Ch 29 §29.6)

### Check 2: AGENTS.md exists (weight 2, important)

**Reference:** Ch 6, Appendix B

**What it tests:** A file named `AGENTS.md` at the repo root.

**Why it matters:** AGENTS.md is cross-vendor — recognized by Claude Code, Cursor, Codex, and other agent tools.

**Specific next action:**
- If the team uses multiple AI tools, create AGENTS.md
- Often AGENTS.md can be a thinner cross-vendor companion to CLAUDE.md

### Check 3: llms.txt exists (weight 1, nice-to-have)

**Reference:** Ch 6 §6.5.3

**What it tests:** A file named `llms.txt` at the repo root.

**Why it matters:** Plain-text route map — pointers to where things are in the repo. Helps agents navigate complex repos efficiently.

**Specific next action:**
- For small repos, often unnecessary
- For monorepos or complex repos, create one with major directories and what each contains

### Check 4: README.md exists (weight 2, important)

**Reference:** Ch 6 §6.4

**What it tests:** A README.md at repo root.

**Why it matters:** Human-and-agent-readable project overview. Without it, both are flying blind.

**Specific next action:**
- Use a standard template
- Cover: what this repo is, how to set up, how to run, how to test, key concepts

### Check 5: Per-package READMEs in monorepos (weight 1, nice-to-have)

**Reference:** Ch 10, Ch 12

**What it tests:** In monorepos, each package/service has its own README or AGENTS.md.

**Why it matters:** Per-package legibility lets agents work effectively on a specific package without loading context for the whole monorepo.

**Specific next action:**
- For monorepos: per-package READMEs are real value
- For non-monorepos: this check is N/A and should pass trivially

---

## Category — Verify command

### Check 6: `verify` command defined (weight 3, critical)

**Reference:** Ch 7

**What it tests:** A single `verify` command (Makefile target, npm script, justfile recipe, etc.) that runs lint + typecheck + format + tests.

**Why it matters:** Per Ch 7, the verify command is the most important artifact in the harness. The agent runs verify before claiming completion; CI runs verify on every PR.

**Common reasons for failure:**
- The team has individual `npm run lint`, `npm run test`, etc. but no consolidated `verify`
- The team's CI has the steps separately but doesn't expose them as a local command

**Specific next action:**
- Add a `Makefile` (or justfile, or npm script) with `verify` that runs all the gates
- Document the verify command in CLAUDE.md
- Reference: Ch 7 has the canonical structure

### Check 7: Verify pipeline includes lint (weight 2, important)

**Reference:** Ch 7

**What it tests:** The verify command (or its components) includes a linter.

**Why it matters:** Linting catches a class of slop signatures (per Ch 22 §22.2 — S6 unnecessary abstractions, some S2 issues) that tests miss.

**Specific next action:**
- For Python: ruff or flake8
- For TypeScript: eslint
- For Go: golangci-lint
- Configure to be strict but not noisy

### Check 8: Verify pipeline includes typecheck/format (weight 2, important)

**Reference:** Ch 7

**What it tests:** Type checking and format checking are part of verify.

**Why it matters:** Type errors catch a category of AI-introduced bugs that tests miss; format checks catch S7 (diff bloat / pattern divergence).

**Specific next action:**
- For Python: mypy or pyright
- For TypeScript: tsc --noEmit
- For format: prettier, gofmt, ruff format, etc.

### Check 9: Verify pipeline includes tests (weight 3, critical)

**Reference:** Ch 7

**What it tests:** The verify command runs tests.

**Why it matters:** Verify without tests is not verify. The agent's "this is done" claim is gated on verify passing. If verify doesn't run tests, completed work isn't actually verified.

**Specific next action:**
- Add test execution to the verify command
- For Python: pytest
- For TypeScript/JS: jest, vitest, mocha
- For Go: `go test ./...`

---

## Category — Test discipline

### Check 10: Test files exist (weight 3, critical)

**Reference:** Ch 8

**What it tests:** Test files exist somewhere in the repo (`test_*.py`, `*.test.ts`, `*_test.go`, etc.).

**Why it matters:** Tests are how the harness keeps AI changes safe.

**Specific next action:**
- For a codebase without tests: add characterization tests (per `legacy-codebase-onboarding/`)
- For a codebase with sparse tests: prioritize by risk; add tests where AI-authored work would be most consequential

### Check 11: CI workflow exists (weight 2, important)

**Reference:** Ch 8

**What it tests:** A CI configuration file (.github/workflows/, .gitlab-ci.yml, etc.) that runs verify on every PR.

**Why it matters:** Without CI, verify is a local convention; engineers may skip it under pressure. CI is the mechanical enforcement.

**Specific next action:**
- Add a CI workflow that runs `verify` on every PR
- Standard pattern: `make verify` or equivalent in the workflow's main step

---

## Category — Harness

### Check 12: .claude/ directory exists (weight 3, critical)

**Reference:** Ch 13-15

**What it tests:** A `.claude/` directory at the repo root.

**Why it matters:** The harness lives here — skills, hooks, subagents, settings.

**Specific next action:**
- Create `.claude/` with subdirectories for skills, hooks, subagents
- Use `starter-kits/agent-friendly/.claude/` as starting point

### Check 13: At least one skill defined (weight 3, critical)

**Reference:** Ch 13, Appendix E

**What it tests:** At least one skill in `.claude/skills/` or equivalent.

**Why it matters:** Skills are reusable playbooks for repeated tasks. Per the book: start with 3-5; grow to 12.

**Common reasons for failure:**
- Team hasn't built any skills yet
- Skills are scattered (in a different location not detected)

**Specific next action:**
- Identify 3-5 most-repeated tasks in the team
- For each, create a skill: prompt + canonical pattern + invocation
- Reference: `skills/` in this repo for shape

### Check 14: Subagents defined (weight 2, important)

**Reference:** Ch 14, Appendix F

**What it tests:** Subagents exist (planner, implementer, reviewer, or similar).

**Why it matters:** The standard subagent roster is what makes L3 autonomy feasible (per `agent-autonomy-levels/autonomy-ladder.md`).

**Specific next action:**
- At minimum: a code-reviewer subagent (per Ch 22 §22.3)
- Recommended: planner / implementer / reviewer triad
- Specialized: security-reviewer, performance-reviewer, migration-reviewer

### Check 15: Hooks configured (weight 3, critical)

**Reference:** Ch 15, Appendix G

**What it tests:** Hooks configured in `.claude/settings.json` or equivalent.

**Why it matters:** Hooks are deterministic enforcement — bash firewall, protected paths. Per the autonomy ladder, hooks are the mechanical layer that prevents the forbidden categories.

**Specific next action:**
- Configure a bash firewall (per `governance/hooks/`)
- Add legacy-protected-paths if applicable
- Add fence-new-violations for slop-signature detection

---

## Category — PR discipline

### Check 16: PR template exists (weight 2, important)

**Reference:** Ch 21, Appendix D

**What it tests:** `.github/pull_request_template.md` or similar.

**Why it matters:** PR template enforces verification checklist and AI authorship disclosure.

**Specific next action:**
- Add a PR template that includes: verify status, AI authorship classification, scope confirmation

### Check 17: PR template mentions AI authorship (weight 2, important)

**Reference:** Ch 21, Ch 31 §31.6

**What it tests:** The PR template includes the four-class authorship convention (`ai:none` / `ai:assisted` / `ai:authored` / `ai:agent`).

**Why it matters:** PR tagging is the foundation of the attribution toolkit. Without it, defect rates by authorship can't be measured (per `incident-postmortem-templates/`).

**Specific next action:**
- Add a checkbox section to PR template: "AI authorship classification"
- Include each of the four classes
- Reference Ch 31 §31.6

### Check 18: CODEOWNERS file exists (weight 1, nice-to-have)

**Reference:** Ch 21

**What it tests:** A CODEOWNERS file at repo root or `.github/CODEOWNERS`.

**Why it matters:** CODEOWNERS routes reviews to the right humans and gates restricted areas (auth/billing/permissions paths).

**Specific next action:**
- For repos with sensitive paths (auth, billing, permissions): CODEOWNERS is required
- For others: nice-to-have

---

## Category — Governance

### Check 19: SECURITY.md exists (weight 2, important)

**Reference:** Ch 30

**What it tests:** A SECURITY.md at repo root.

**Why it matters:** Security policy. Should include AI tooling disclosure for customer audits (per `customer-facing-ai-disclosure/`).

**Specific next action:**
- Add SECURITY.md with: vulnerability reporting process, supported versions, security contact, AI tooling disclosure summary

### Check 20: Forbidden patterns listed in CLAUDE.md (weight 2, important)

**Reference:** Ch 6, Ch 33

**What it tests:** CLAUDE.md contains an explicit "never do" list.

**Why it matters:** The agent works much better with explicit prohibitions than with implicit norms. Per `agent-autonomy-levels/forbidden-categories.md`, the forbidden list is documented in CLAUDE.md and enforced mechanically.

**Specific next action:**
- Add a "Never do" section to CLAUDE.md
- Cover: production credentials, eval/exec, unrestricted shell, force pushes, etc.

### Check 21: Architectural invariants documented (weight 2, important)

**Reference:** Ch 9

**What it tests:** Hard architectural invariants are documented somewhere accessible.

**Why it matters:** Hard invariants the agent must respect (UI cannot import from db, all auth server-side, etc.).

**Specific next action:**
- Document architectural invariants in CLAUDE.md or in a dedicated ARCHITECTURE.md
- Cover: layering rules, data flow constraints, invariants the agent must respect

### Check 22: Data classification policy referenced (weight 2, important)

**Reference:** Ch 34

**What it tests:** Reference to a data classification matrix mapping data types to AI tool permissions.

**Why it matters:** Per `vendor-procurement-runbook/data-classification-walkthrough.md`, the matrix determines which AI tools can be used on which data classes.

**Specific next action:**
- Reference the data classification matrix in SECURITY.md or CLAUDE.md
- Either inline or link to the company-wide policy

---

## Category — Cost & observability

### Check 23: Cost telemetry / token tracking referenced (weight 1, nice-to-have)

**Reference:** Ch 26, Ch 29

**What it tests:** Reference to cost gateway, LiteLLM, Bifrost, Helicone, or token-budget mechanism.

**Why it matters:** Per `cost-discipline-runbook/`, telemetry is the foundation of cost discipline.

**Specific next action:**
- If the team has a cost gateway: reference in CLAUDE.md or README
- If not: see `cost-discipline-runbook/token-budgets-by-team.md` for setup

---

## Category — AI-aware incident response

### Check 24: AI-aware incident response runbook (weight 1, nice-to-have)

**Reference:** Ch 39

**What it tests:** A postmortem / incident-response runbook that handles AI-authored code paths.

**Why it matters:** Per `incident-postmortem-templates/`, AI-authored bugs need structured postmortem categorization.

**Specific next action:**
- Add a runbook (or reference to a shared one) covering AI-related incidents
- Use `incident-postmortem-templates/postmortem-template.md` as starting point

---

## Patterns across checks

### "We have most of repo legibility but no harness"

Common pattern for teams just starting. README, CLAUDE.md, verify command exist; .claude/, skills, subagents don't.

Diagnosis: the team is at the awareness phase; harness investment hasn't started.

Path: Per [`prioritized-remediation-paths.md`](prioritized-remediation-paths.md), invest in `.claude/` directory + first 3-5 skills + at least one hook. This unlocks the most leverage for the next quarter.

### "We have harness but no governance"

Common pattern for technical teams. Skills, subagents, hooks exist; SECURITY.md, CODEOWNERS, data classification policy don't.

Diagnosis: the team has invested in productivity but not in governance.

Path: governance gaps surface in audit / customer review / regulatory review. Close them when those events approach; they're not blocking day-to-day productivity.

### "We have governance but no harness"

Less common but happens — especially in organizations that started AI tooling adoption from a security/compliance perspective.

Diagnosis: the team has invested in policy but not in practice.

Path: the harness is what makes the policy operational. Without skills, hooks, subagents, the policy is theoretical.

### "Everything fails"

Score under 30. The team is at the very beginning.

Diagnosis: AI tooling adoption hasn't formalized.

Path: don't try to fix everything at once. Start with the critical-weight checks (1, 6, 9, 10, 12, 13, 15). The others come over the next 1-2 quarters.

### "Everything passes but score is 70-something"

The audit's heuristics give partial credit; nothing fully fails. The score is 70-something because warns and weights interact.

Diagnosis: harness exists but content quality may be low.

Path: manual review of CLAUDE.md, AGENTS.md, skills. Ensure they're substantive, not perfunctory.

## What this explainer will NOT do

- Will not handle every repo's specifics. The audit is heuristic; some checks may be N/A or differently relevant for your context.
- Will not eliminate the need to read the source. The audit's exact behavior is in the script; this explainer is the interpretation.
- Will not produce passing scores by itself. The remediation work is engineering work.

## Companion artifacts

- [`how-to-run.md`](how-to-run.md) — running the audit
- [`prioritized-remediation-paths.md`](prioritized-remediation-paths.md) — what to fix first
- [`scoring-and-thresholds.md`](scoring-and-thresholds.md) — interpreting the score
- `scripts/ai-readiness-audit.py` — the source
