# Tier 3 — AI-Led with Light Human Gate

The Tier 3 catalog. Per Ch 33 §33.3:

> Tier 3 (AI-led with light human gate)

Work where AI can lead and the human review is light — catch obvious issues, ensure scope discipline, sign off. The bulk of routine engineering work falls here.

## The Tier 3 list (verbatim from Ch 33)

1. **Documentation.**
2. **Internal-only scripts.**
3. **Test additions.**
4. **Type fixes.**
5. **Style and lint fixes.**
6. **Dependency security patches with no API change.**

## Why each item is here

### Documentation

**Why it's Tier 3:** documentation is reversible (revert PR), the failure mode is low (incorrect docs are correctable), and AI tooling is good at it.

**Common Tier 3 work:** generating release notes, updating API documentation, writing internal engineering documentation, summarizing complex modules.

**The "light human gate":** the reviewer scans for accuracy, scope (didn't introduce documentation about systems the agent doesn't know), and tone consistency.

**Common failure mode:** AI-generated docs hallucinate features that don't exist or describe behavior incorrectly. Light review catches the obvious cases.

**At L4 autonomy:** documentation can auto-merge if the team has earned it (per `agent-autonomy-levels/autonomy-ladder.md`). Common pattern: docs PRs are L4-eligible; an AI reviewer subagent runs; if it passes and CI passes, auto-merge.

### Internal-only scripts

**Why it's Tier 3:** internal scripts have low blast radius (they affect engineers, not customers), they're typically reversible, and the failure mode is local.

**Common Tier 3 work:** dev-environment setup scripts, log analysis scripts, internal admin tools, code-generation scripts.

**The "light human gate":** the reviewer checks scope (does this introduce a new pattern that should be canonicalized?) and basic correctness.

**Common failure mode:** internal scripts that work for the author but not for other engineers (different OS, different setup). Light review catches the obvious portability issues.

**At L4 autonomy:** typically not. Internal scripts vary enough in shape that auto-merge produces noise.

### Test additions

**Why it's Tier 3:** adding tests has low risk (tests don't ship to customers; they protect existing behavior). AI tooling is good at test generation when the team has clear patterns.

**Common Tier 3 work:** characterization tests for legacy code (per `legacy-codebase-onboarding/`), edge-case tests for existing functionality, regression tests for closed bugs.

**The "light human gate":** the reviewer checks that tests actually test (not slop signature S1 — tests mocking implementation rather than asserting behavior). Test quality matters even at Tier 3.

**Common failure mode:** AI-generated tests that pass against current code but don't catch deliberate breakage. The reviewer should verify tests are substantive.

**At L4 autonomy:** common candidate. Many teams run test additions at L4 once they've verified the AI reviewer subagent catches mock-heavy tests.

### Type fixes

**Why it's Tier 3:** type annotations don't change runtime behavior; type checker validates correctness; reversal is trivial.

**Common Tier 3 work:** adding type annotations to untyped Python modules, tightening TypeScript `any` to specific types, fixing type errors that the type checker reports.

**The "light human gate":** the reviewer scans for over-specification (types that are tighter than the actual contract) and consistency with the team's typing conventions.

**Common failure mode:** AI types that are technically correct but break downstream consumers (e.g., narrowing a parameter from `string | number` to `string` when callers pass numbers).

**At L4 autonomy:** common candidate. Many teams run type fixes at L4 once the type checker is the authoritative gate.

### Style and lint fixes

**Why it's Tier 3:** style fixes are deterministic and reversible. Linters catch style violations; AI applies the fixes.

**Common Tier 3 work:** running formatters, fixing lint warnings, applying consistent import ordering.

**The "light human gate":** the reviewer verifies the fix is mechanical (didn't introduce semantic changes alongside the style fix).

**Common failure mode:** AI "fixes" that include semantic changes ("I improved the variable name while I was at it"). Light review catches the scope creep.

**At L4 autonomy:** common candidate, often integrated into pre-commit hooks rather than separate PRs.

### Dependency security patches with no API change

**Why it's Tier 3:** security patches are necessary, time-sensitive, and typically don't change application behavior.

**Common Tier 3 work:** bumping `package.json` dependencies in response to CVEs, applying renovate/dependabot suggestions.

**The "light human gate":** the reviewer verifies the patch genuinely has no API change (read the changelog) and that tests still pass.

**Common failure mode:** "patches with no API change" that actually have subtle behavior changes. The reviewer's job is to confirm the changelog matches reality.

**At L4 autonomy:** sometimes. Patches from highly-trusted maintainers (e.g., security-only updates from Node, Python core teams) are common L4 candidates.

## What "light human gate" means in practice

For each Tier 3 category:

- **Maximum autonomy level:** L4 (auto-merge with AI reviewer + CI gating) for tier-restricted whitelist categories
- **Required reviewers:** at least an AI reviewer subagent; human review can be lighter (a quick read, not a deep audit)
- **Required tests:** standard tests pass; specific category-relevant checks (e.g., type checker for type fixes; lint check for style fixes)
- **Required documentation:** typically minimal; the change itself is self-documenting

What this means for engineers:

- You can run AI tooling at the highest autonomy level the team has earned
- The human gate is real but light — a 1-2 minute review for most Tier 3 PRs
- Auto-merge is appropriate for many Tier 3 PRs once the team has earned L4 for the specific category

## When Tier 3 work isn't Tier 3

Some work patterns that look like Tier 3 but aren't:

### "Documentation about Tier 1 systems"

Generating documentation about the auth system is still Tier 3 work — it's documentation, not auth code. The reviewer should be careful about correctness (don't document what the auth system doesn't actually do) but the failure mode is low.

The exception: documentation that's customer-facing (public API docs, security docs, compliance docs). Those become Tier 2 because the failure mode includes customer trust and compliance exposure.

### "Internal scripts that touch production"

A script that "just queries production for diagnostic purposes" isn't Tier 3 — production access elevates it. Internal scripts that touch production data are Tier 2 at minimum.

### "Tests for Tier 1 code"

Tests for auth code, billing code, etc. are still Tier 3 work — they're tests, not the auth/billing code itself. The reviewer should be substantive (the tests need to actually catch failures) but the failure mode is "the tests don't catch what they should," which is recoverable.

### "Type fixes that change runtime behavior"

If your "type fix" changes runtime behavior (some languages allow this), it's not Tier 3. It's a refactor with type changes; review accordingly.

### "Lint fixes that touch security-sensitive paths"

A lint fix in auth code is still touching auth code. The lint fix should still go through the auth-aware review process even though the change is "just style."

## Where Tier 3 enables L4 auto-merge

Per `agent-autonomy-levels/autonomy-ladder.md`, L4 (auto-merge after CI) is appropriate for tier-restricted whitelist categories. Tier 3 is the source of those categories. Specifically:

- **Documentation** — common L4 candidate
- **Type fixes** — common L4 candidate
- **Style/lint fixes** — common L4 candidate, often via pre-commit
- **Test additions** — common L4 candidate

NOT typical L4 candidates:
- Internal scripts (varies too much)
- Dependency patches (the "no API change" claim needs human verification)

The team's L4 whitelist should be specific (which Tier 3 categories) not broad (all Tier 3).

## Common pushback

### "Why isn't [specific work] in Tier 3?"

The most common pushback is wanting work to be Tier 3 for speed. The discipline: the failure mode determines the tier, not the desire to ship faster.

### "We're treating Tier 3 too lightly; bugs are shipping"

If Tier 3 work is producing bugs in production, the issue might be:
- The tier is wrong for some specific work pattern (raise to Tier 2)
- The "light gate" isn't light enough (improve the AI reviewer subagent)
- The team's discipline is drifting (per `agent-autonomy-levels/autonomy-drift-monitoring.md`)

### "Tier 3 is most of our work; should we just trust the AI more?"

Trusting the AI is the discipline; the gate is what makes the trust durable. Without the light gate, Tier 3 work drifts in quality. The gate is the protection against drift.

## Companion artifacts

- [`tier-1-never-autonomous.md`](tier-1-never-autonomous.md) — adjacent
- [`tier-2-mandatory-human-gate.md`](tier-2-mandatory-human-gate.md) — adjacent
- [`my-use-case-decision-flow.md`](my-use-case-decision-flow.md) — when in doubt
- `agent-autonomy-levels/autonomy-ladder.md` — adjacent (L4 autonomy details)
- `agent-autonomy-levels/task-taxonomy-rubric.md` — adjacent (AI-friendly tasks)
- Ch 33 §33.3 — source
