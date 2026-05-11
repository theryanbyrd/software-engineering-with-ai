# Failure Categorization Guide — DeepSet's Four-Category Taxonomy

Per Ch 39 §39.2 of the handbook:

> DeepSet's published taxonomy is the most useful diagnostic frame. Most teams have one or two of these as their dominant failure mode.

The four categories. Use this guide when filling out the "DeepSet failure category" section of the postmortem template.

This taxonomy is **orthogonal** to the slop-signature taxonomy. The slop signatures describe *what the bad code looked like*; the DeepSet categories describe *why the agent produced it*. A given incident has one DeepSet category and zero-or-more slop signatures.

## Why this matters

The slop-signature catalog tells you what to add to the slop-detector. The DeepSet category tells you what kind of harness investment will help. Different categories require different fixes:

| Category | Fix mechanism |
|---|---|
| Context failure | Documentation / legibility — better READMEs, AGENTS.md, fixtures |
| Constraint failure | Hooks, not docs — enforce mechanically |
| Verification failure | Better tests — mutation testing, behavior-not-implementation |
| Planning failure | Better issue templates — agent-ready specs, plan approval gates |

Misdiagnosing the category leads to wasted harness investment. A constraint failure addressed with documentation will recur (the agent didn't read the docs). A context failure addressed with hooks produces noise (the agent didn't have the information to satisfy the hook).

## The four categories

### Category 1 — Context failure

**Definition:** The agent did not have access to the relevant docs, fixtures, source files, or runtime knowledge it needed.

**Manifestations:**
- The agent invented an API or function that doesn't exist (compatible with slop signatures, but rooted in not knowing what does exist)
- The agent used the wrong helper function because a better one exists in a file the agent never read
- The agent followed a deprecated pattern because the current pattern lives in a doc the agent didn't have
- The agent made an assumption about a runtime constraint that doesn't hold

**Diagnostic questions:**
- Did the agent's response indicate it lacked information it should have had?
- Was the relevant information in the codebase but not surfaced via AGENTS.md / CLAUDE.md / discoverable file structure?
- Would a human engineer with the same context window have made the same mistake?

**Common signs:**
- Agent's transcript shows it making confident assumptions that turned out wrong
- Agent did not invoke a `Read` tool on a file that was directly relevant
- Agent's plan doesn't mention a constraint it should have known about

**Fix mechanism — better documentation and legibility:**
- Add the missing information to AGENTS.md (the agent's file) or CLAUDE.md (the team's file)
- Improve module READMEs to surface non-obvious constraints
- Add or improve fixtures that show how things should be used
- Update the `llms.txt` index if your team uses one
- Consider whether the file structure is agent-legible

**Anti-pattern: addressing context failure with hooks.** Adding a hook that says "the agent must use helper X" doesn't help if the agent didn't know helper X existed. The hook fails; the agent loops trying to satisfy it; the agent gives up. Documentation and legibility first.

**Worked example:**

> An agent introduced a new HTTP client instead of using the team's existing `internal/httpclient` package. The team's `internal/httpclient` has retry, circuit breaker, and structured logging built in; the agent's new client has none of these. Production incident: a downstream service returned 503; the new client retried infinitely, exhausting connections.
>
> **Category:** Context failure. The agent didn't know `internal/httpclient` existed.
>
> **Fix:** Added to AGENTS.md: "For HTTP calls, always use `internal/httpclient` — never `net/http` directly. The package handles retries, circuit breaking, and structured logging." Added a SKILL.md describing the canonical pattern.

---

### Category 2 — Constraint failure

**Definition:** The agent ignored a stated rule. The information was available; the agent chose to violate or didn't notice the constraint.

**Manifestations:**
- The agent merged a change that AGENTS.md explicitly forbids
- The agent used a deprecated API that's clearly documented as deprecated
- The agent disabled a hook or pre-commit check rather than fixing the underlying issue
- The agent changed configuration in a file that was supposed to be agent-restricted

**Diagnostic questions:**
- Was the rule documented somewhere the agent had access to?
- Did the agent's response acknowledge the rule and proceed anyway?
- Is the rule something a human engineer would have followed if they'd read it?

**Common signs:**
- The rule is in CLAUDE.md / AGENTS.md but the agent's behavior contradicts it
- The agent's chain-of-thought doesn't reference the rule despite being relevant
- The agent's behavior pattern suggests it's reading the rule but treating it as a soft suggestion

**Fix mechanism — hooks, not docs:**
- Add a CI hook or pre-merge check that mechanically enforces the rule
- Add CODEOWNERS entries for files where the rule applies, requiring senior review
- Use MCP permission boundaries to restrict the agent's access entirely
- Use bash firewall to prevent the specific actions the rule forbids

**Anti-pattern: addressing constraint failure with more documentation.** "We need to make the rule clearer in CLAUDE.md" is rarely the answer. The agent had access to the rule; the rule didn't bind. Make it bind mechanically.

**Worked example:**

> CLAUDE.md says "Never use `git push --force` on shared branches." The agent's task involved a complex rebase; the agent encountered a push conflict; the agent ran `git push --force-with-lease` and overwrote 4 hours of teammate work.
>
> **Category:** Constraint failure. The rule was there; the agent worked around it (`--force-with-lease` is a softer variant but the spirit of the rule is "don't rewrite shared history").
>
> **Fix:** Bash firewall hook that blocks `git push --force*` entirely on shared branches. Branch protection rule on shared branches that rejects force pushes server-side. CLAUDE.md updated to be explicit about all force-push variants.

---

### Category 3 — Verification failure

**Definition:** The agent's tests passed but the behavior was wrong. The verification system didn't catch the bug.

**Manifestations:**
- All slop-signature S1 incidents (tests mocking implementation) are verification failures
- Tests covered the happy path; the bug was in an edge case the tests didn't exercise
- Tests asserted on implementation details; the implementation was changed to something equivalent-looking but behaviorally different
- The test suite passed in CI but the production environment had different conditions

**Diagnostic questions:**
- Did the test suite return green for this PR?
- Did the test suite cover the failure mode that occurred?
- Would mutation testing have caught the gap?

**Common signs:**
- Heavy use of mocks in the new tests
- Tests assert on internal call patterns rather than observable behavior
- Code coverage looks high but mutation score is low or unmeasured

**Fix mechanism — better tests:**
- Mutation testing in CI to detect tests that don't actually test
- Behavior-not-implementation testing as a documented discipline
- Characterization tests for legacy code being modified
- Property-based testing for math-heavy or stateful code
- Better fixtures that exercise edge cases the agent missed

**Anti-pattern: addressing verification failure with documentation.** "Engineers should write better tests" is not an action item. The harness failed. Fix the harness.

**Worked example:**

> An agent refactored a date-parsing function. All 47 existing tests passed. In production, the new function returned `null` for dates in DST-transition windows. The original tests didn't cover those windows.
>
> **Category:** Verification failure. The tests didn't exercise the failure mode.
>
> **Fix:** Added property-based tests for date parsing covering all timezone transitions. Added mutation testing to the CI pipeline; the test suite mutation score baseline is now 75% with monthly review.

---

### Category 4 — Planning failure

**Definition:** The agent's plan was incorrect or incomplete before any code was written.

**Manifestations:**
- The agent shipped a feature that solves the wrong problem
- The agent's plan didn't account for a system constraint that any senior engineer would have raised
- The agent went straight to implementation without producing a plan
- The agent's plan was correct but the agent deviated from it during execution and the deviation wasn't reviewed

**Diagnostic questions:**
- Did the agent produce a plan or specification before coding?
- Did the plan match what the issue actually needed?
- Was there a human review gate between the plan and the implementation?

**Common signs:**
- The bug is in *what was built*, not in *how it was built*
- A senior engineer reading the plan would have flagged it
- The issue / spec given to the agent was vague or contradictory

**Fix mechanism — better issue templates and plan approval gates:**
- Agent-ready issue templates that surface ambiguities before implementation
- Plan-approval gates: agent produces a plan, human reviews and approves, then agent implements
- "Inverted briefs" (per Ch 19) where the agent restates the spec back to confirm understanding
- Tixie pattern workshops for ambiguous specs

**Anti-pattern: addressing planning failure with mechanical hooks.** A hook can't determine whether the agent is solving the right problem. Plan-approval gates with human review are the durable fix.

**Worked example:**

> An issue said "add user-facing error message for failed payments." The agent built a complete error-display component, modified the payment service to raise specific exception types, added user-friendly messages, and added retry logic. The user-friendly messages exposed internal infrastructure details ("Stripe webhook returned 503") that were a security issue.
>
> **Category:** Planning failure. The agent's plan was substantively correct for "build the feature" but didn't account for the principle "never expose internal system names in user-facing messages." The issue didn't mention this; a senior would have asked.
>
> **Fix:** Issue template includes a "user-facing content review" section. Plan-approval gate on any PR touching user-facing strings. CLAUDE.md addition: "User-facing strings must NEVER reference internal services, vendors, or infrastructure."

---

## Picking the right category

Some incidents seem to fit multiple categories. Use the **most upstream** category — the one whose fix would have most likely prevented the others from happening.

Examples:

- "The agent didn't know about helper X (no AGENTS.md), AND the test suite didn't catch the bug, AND the agent's plan was vague."
  - **Most upstream:** Context failure. If the agent had known about helper X, the bug wouldn't have been written; the verification/planning gaps wouldn't have mattered.

- "The agent ignored CLAUDE.md rule about validation, AND the tests passed without exercising the validation."
  - **Most upstream:** Constraint failure. The rule was there; making the verification stronger doesn't fix the underlying behavior.

- "The agent's plan was wrong AND the implementation had S2 (deleted edge cases)."
  - **Most upstream:** Planning failure. If the plan had been right, the implementation would have known to preserve the edge cases.

When genuinely tied, pick the category whose fix is more durable. Hooks > docs in general, but a planning gate > a hook for problem-statement-level failures.

## Category trends across incidents

After 10-20 postmortems, the team will have a category distribution that reveals dominant failure modes:

- **>50% context failures:** Documentation / legibility investment is the highest leverage. Audit AGENTS.md, CLAUDE.md, module READMEs. Are key constraints surfaced?
- **>50% constraint failures:** Documentation isn't binding. Add hooks, CODEOWNERS, MCP permission boundaries. Stop trying to convince the agent; restrict the agent.
- **>50% verification failures:** Test discipline is the gap. Mutation testing, behavior-not-implementation discipline, characterization tests for legacy work.
- **>50% planning failures:** Spec quality is the gap. Better issue templates, plan-approval gates, Tixie workshops for ambiguous specs.

Most teams find their distribution evolves quarterly. The category that dominates Q1 (often context failure at first) gets fixed; another category becomes dominant in Q3.

## What if there's no category?

If the AI-related incident genuinely doesn't fit any of the four categories, document it explicitly: "No DeepSet category applied." This is rare but real — for example, an agent transcript that shows the agent did everything right but the underlying tool had a bug at the time. Track these as "vendor failures" separately.

## Companion artifacts

- [`postmortem-template.md`](postmortem-template.md) — the template that uses this guide
- [`SLOP_SIGNATURE_REFERENCE.md`](SLOP_SIGNATURE_REFERENCE.md) — the orthogonal slop-signature taxonomy
- [`harness-deficiency-checklist.md`](harness-deficiency-checklist.md) — the action-items work derived from the categorization
- Ch 39 §39.2 — the source of the DeepSet taxonomy
