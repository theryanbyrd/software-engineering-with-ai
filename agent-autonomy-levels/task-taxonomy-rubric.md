# Task Taxonomy Rubric — Which Work Runs at Which Autonomy Level

The decision rubric for matching tasks to autonomy levels. Direct implementation of Ch 32 §32.3.

The book's three categories:

- **AI-friendly:** L2-L4 candidate
- **AI-cautious:** L1-L2 only
- **AI-dangerous:** L0-L1, human leads

This file extends those categories with calibration questions and worked examples.

## Use this rubric when

- A new type of work surfaces and you're not sure what level it can run at
- An engineer proposes raising the level for a category
- An incident postmortem (per `incident-postmortem-templates/`) suggests downgrading a category
- Quarterly autonomy ladder review

## The three categories

### AI-friendly (L2-L4 candidate)

These task types have the lowest blast radius and are well-suited to AI tooling at the team's earned autonomy level.

Per Ch 32 §32.3:

- New isolated features behind a feature flag with full test coverage required
- Test additions for existing behavior
- Documentation generation and updates
- Type annotation additions
- Lint and format fixes
- Refactors with golden-master tests in place
- Boilerplate scaffolding from a contract
- Bug fixes with reproduction tests

**What "AI-friendly" requires:**
- Tests can characterize whether the change is correct
- The change's blast radius is bounded
- The change is reversible (revert PR within minutes)
- The change does not touch any AI-dangerous category

**What "AI-friendly" does NOT mean:**
- "AI gets it right consistently" — even friendly tasks have failure modes
- "No human review" — review discipline still applies
- "Anywhere in the codebase" — friendly task type AND non-dangerous code path both required

### AI-cautious (L1-L2 only)

Tasks where the agent can contribute but human leadership is required.

Per Ch 32 §32.3:

- Cross-cutting refactors
- Performance work
- New endpoints adding to a public API
- Logging, observability, or telemetry additions
- Dependency upgrades

**Why these are cautious:**
- Cross-cutting refactors: the agent can produce locally-correct changes that don't compose globally
- Performance work: requires understanding actual bottlenecks; agents often optimize the wrong thing
- New API endpoints: API shape is a contract; mistakes are expensive
- Observability: incorrect telemetry is worse than missing telemetry (gives false confidence)
- Dependency upgrades: subtle behavior changes; agents miss them

**Common pattern:** the engineer drives the design; the agent implements within the design. The engineer's review is substantive, not perfunctory.

### AI-dangerous (L0-L1, human leads)

Tasks where AI tooling is most likely to cause harm.

Per Ch 32 §32.3:

- Authentication, authorization, session management
- Billing, payments, refunds, settlement
- Permissions and RBAC
- Database schema migrations
- Cryptography
- Compliance-critical code paths
- Anything in the Do-Not-Automate catalog (Ch 33)

**Why these are dangerous:**
- The failure mode is severe (data loss, security breach, financial harm)
- The failure mode often surfaces weeks later, not at PR time
- The verification cost (proving correctness) is high
- The agent's confidence is poorly calibrated against reality in these domains

**Mode of operation:** the human writes the code; the agent assists with reading, suggesting, and reviewing. Even at L0, the agent can be useful — exploring related code, asking questions, surfacing patterns. At L1, the agent can propose specific edits that the human reviews carefully. Above L1, these categories don't go.

---

## Calibration questions

For a task you're trying to categorize:

### 1. What's the blast radius?

- **Bounded to one feature behind a flag:** AI-friendly candidate
- **Cross-cutting; affects many users:** AI-cautious
- **Affects all users; no rollback:** AI-dangerous

### 2. How verifiable is the change?

- **Tests can prove correctness:** AI-friendly candidate
- **Tests cover most cases; some manual verification:** AI-cautious
- **Verification requires deep domain expertise OR can't be tested without production:** AI-dangerous

### 3. How reversible is the change?

- **Revert PR within minutes:** AI-friendly candidate
- **Reversal requires migration / coordination:** AI-cautious
- **Effectively irreversible (data lost; auth surface compromised; financial commitment made):** AI-dangerous

### 4. What's the regulatory or compliance scope?

- **None or low:** AI-friendly candidate
- **SOC 2 / standard compliance:** AI-cautious
- **HIPAA / financial / PCI / regulated:** AI-dangerous

### 5. What's the cost of being wrong for 30 days?

- **Inconvenience or fixable mid-quarter:** AI-friendly candidate
- **Customer impact requiring incident response:** AI-cautious
- **Financial loss, regulatory exposure, customer churn:** AI-dangerous

If any answer points to "AI-dangerous," the task is AI-dangerous. The most dangerous dimension wins.

---

## Worked examples

### Example A — Adding a new API endpoint to query user preferences

- Blast radius: bounded but customer-facing
- Verifiable: contract tests + integration tests cover most cases
- Reversible: yes, but coordinate with frontend team
- Compliance scope: low (preferences aren't sensitive data class)
- Cost of being wrong: minor inconvenience for some users for some hours

**Verdict:** AI-cautious. New API endpoint surface; engineer drives the contract design; agent implements. Run at L1 or L2.

### Example B — Adding a new password-reset flow

- Blast radius: all users
- Verifiable: hard; subtle authentication semantics
- Reversible: hard; rollback after deployment is messy
- Compliance scope: high (auth)
- Cost of being wrong: severe (account takeover potential)

**Verdict:** AI-dangerous. L0-L1 only; human leads. Even at L1, every change reviewed line-by-line. Per Ch 32, "any code change to authentication, authorization, billing, payment, or permission code without a human review gate" is forbidden.

### Example C — Generating type annotations for an untyped Python module

- Blast radius: type-checking only; no runtime change
- Verifiable: type checker catches inconsistencies
- Reversible: trivially (revert PR)
- Compliance scope: none
- Cost of being wrong: failed type-check; fix in minutes

**Verdict:** AI-friendly. Run at L2 with PR review, or L3 in a multi-module sweep, or L4 if the team has earned auto-merge for type-only changes.

### Example D — Refactoring a 5-year-old payment-processing module

- Blast radius: financial transactions
- Verifiable: characterization tests possible but coverage is incomplete
- Reversible: hard if state has shifted
- Compliance scope: high (PCI, financial)
- Cost of being wrong: monetary loss, customer trust loss

**Verdict:** AI-dangerous regardless of the "refactor" framing. Refactoring payment code is still touching payment code. L0-L1; human leads. The refactor needs characterization tests first (per Ch 11), then strangler-fig new code alongside, NOT in-place refactor of the legacy module.

### Example E — Adding a new database index for performance

- Blast radius: query performance, possibly contention
- Verifiable: load testing can characterize
- Reversible: yes, drop the index
- Compliance scope: low
- Cost of being wrong: degraded performance until index dropped

**Verdict:** AI-cautious. The agent can propose; the engineer reviews; deployment goes through standard schema-change discipline (which is itself L0-L1 — schema migrations are AI-dangerous per Ch 32).

### Example F — Updating a README to fix typos

- Blast radius: documentation only
- Verifiable: trivial
- Reversible: trivial
- Compliance scope: none
- Cost of being wrong: minor doc inconsistency

**Verdict:** AI-friendly. L4 candidate if the team has earned it. Most teams should run docs at L3 or L4 — this is exactly the kind of work where auto-merge pays off.

### Example G — Bumping a major dependency version

- Blast radius: depends on the dependency; can be wide
- Verifiable: regression tests partially; subtle behavior changes often missed
- Reversible: usually, but coordinated rollback
- Compliance scope: depends on the dependency
- Cost of being wrong: moderate (broken builds; subtle bugs in production)

**Verdict:** AI-cautious for minor deps; trending dangerous for foundational deps (the framework, the database driver, the auth library). Run at L1-L2 with substantial human review of the changelog and integration testing.

---

## When the rubric is unclear

For ambiguous tasks, default to the more conservative category. Specifically:

- **Between AI-friendly and AI-cautious:** assume AI-cautious until proven friendly with track record
- **Between AI-cautious and AI-dangerous:** assume AI-dangerous until the team has explicit experience showing AI-cautious is sufficient
- **In doubt:** AI-cautious

The asymmetry is intentional. A task incorrectly run at AI-friendly when it should be AI-cautious produces incidents; a task incorrectly run at AI-cautious when it could be AI-friendly produces friction. Friction is recoverable; incidents are sometimes not.

## Edge cases

### "This task is technically friendly but I want to learn from it"

A senior engineer reviewing AI-friendly work at L1 (rather than L2) is a reasonable training discipline for newer engineers. Don't downgrade the task category; downgrade the autonomy level for learning purposes.

### "This task spans multiple categories"

Common pattern: a task that includes a friendly portion (test additions) and a dangerous portion (auth code). The whole task runs at the most dangerous portion's level. Don't split execution across levels — the engineer's discipline applies to the whole change.

### "The task is friendly but the codebase is brownfield"

Per [`legacy-codebase-autonomy-rule.md`](legacy-codebase-autonomy-rule.md), the legacy ceiling overrides the task's friendliness. AI-friendly tasks in legacy code at MVH Level 0-1 still run at L1 maximum.

## Companion artifacts

- [`autonomy-ladder.md`](autonomy-ladder.md) — the levels themselves
- [`forbidden-categories.md`](forbidden-categories.md) — what's never allowed
- [`legacy-codebase-autonomy-rule.md`](legacy-codebase-autonomy-rule.md) — the brownfield override
- Ch 32 §32.3 — source
