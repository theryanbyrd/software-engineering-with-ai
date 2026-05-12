# The AI Code Smell Checklist — Deep Reference

The seven canonical AI-slop signatures from Ch 2 §2.2, expanded for use as a reviewer training reference and a working checklist at the screen edge. The Ch 22 §22.2 short-form checklist sits in [`reviewer-cheatsheet.md`](reviewer-cheatsheet.md); this file is the long form — what to look for, why the model produces it, why it gets past review, and the catch heuristic.

Per Ch 2 §2.1:

> "AI slop" is the practical name for code that is syntactically correct, plausibly structured, and semantically wrong. It is the dominant failure mode of AI-assisted development. It is dangerous specifically because it bypasses the heuristics human reviewers use to detect bad code: it has reasonable variable names, consistent style, and superficial test coverage.

Read the signatures in order. S1, S2, and S5 are the ones engineers learn to spot first. S3, S4, S6, and S7 take more reps. If you can recognize all seven without consulting this file, you are at the L2 review bar (Ch 44 §44.2; see [`../agent-autonomy-levels/certification-gates.md`](../agent-autonomy-levels/certification-gates.md)).

## How to use this file

- **First read:** all the way through, slowly. Stop at each before/after diff and predict what the catch heuristic is before you read it.
- **Workshop use:** the facilitator walks the room through the seven signatures with the slides this file generates. See [`facilitator-guide.md`](facilitator-guide.md).
- **Day-to-day use:** when a PR looks fine but feels off, scan this file's section headers. Whichever signature jumps out, read its "what to look for" block; if it matches, leave the comment.
- **Postmortem use:** when an AI-authored bug ships, identify which signature was missed. The taxonomy is the same one used in [`../incident-postmortem-templates/SLOP_SIGNATURE_REFERENCE.md`](../incident-postmortem-templates/SLOP_SIGNATURE_REFERENCE.md).

---

## S1 — Tests mock the implementation, not the behavior

**Per Ch 2 §2.2:**

> A test that imports the function under test and asserts that it returns what the mock returns. Common antipattern: "I'll just mock this out so the tests pass."

### What it is

The test verifies that an internal function was called with specific arguments, or that a mocked dependency returned a specific value. It does not verify that the system, given a realistic input, produces the correct observable result.

### Why the model produces it

Mocking is the path of least resistance. A real fixture requires the agent to understand the system's data model, build representative state, and predict downstream behavior. A mock requires four lines and the test passes immediately. The model's loss function — pass tests, ship code — is satisfied by mocking. The model is not penalized for producing a test that would not catch a real bug.

This is the single most common failure mode in AI-authored code. Per Ch 7 §7.5:

> Tests that mock the implementation (the #1 AI slop signature) all pass verify. verify is necessary, not sufficient.

### Why it gets past review

The reviewer reads "test passes" in the CI output and the diff shows new test functions. The reviewer pattern-matches "more tests = better" and approves. The trap: a passing mock-heavy test suite is indistinguishable from a passing real-fixture test suite *at the CI status level*. You have to read the assertions.

### What to look for

- Tests that mock the function under test, or mock something it directly calls, then assert on the mock's call signature
- Tests that assert `assert mock.called_with(...)` instead of asserting on the return value or a side effect
- Tests that construct elaborate mock return values and then assert the function "returns" those mock values
- Tests where the implementation could be `return None` and the test would still pass
- Tests that have no fixtures, no database state, no realistic inputs — just mocks all the way down

### Example — before/after

```python
# Slop (S1) — the test verifies the implementation
def test_charge_customer():
    customer = Customer(id=1)
    payment_service._stripe_client = MagicMock()
    payment_service._stripe_client.charges.create.return_value = {"id": "ch_1", "status": "succeeded"}

    payment_service.charge_customer(customer, amount=100)

    payment_service._stripe_client.charges.create.assert_called_with(
        customer="cus_1", amount=100
    )

# Substantive — the test verifies the behavior
def test_charge_customer():
    customer = create_customer_with_card(amount_available=200)
    result = payment_service.charge_customer(customer, amount=100)

    assert result.status == "succeeded"
    assert customer.balance == 100
    assert get_ledger_entry(customer.id).amount == 100
```

### Catch heuristic

Ask the question from Ch 2 §2.4:

> Does this test fail if the implementation is wrong?

If the answer is no — if you could replace the function body with `pass` or `return None` and the test still passes — the test is S1. Reject the PR or send it back with a request for a behavior-asserting test.

The mutation-testing version of this question: run mutation testing on the new code (`mutmut`, `stryker`, `pitest`). If the mutation score on the new code is below the team's baseline (the book references 70%+ in Ch 31 §31.6 as a typical pilot floor), the tests are not exercising the behavior. The mutation score is the mechanical version of this check; reviewer pattern-recognition is the human version.

---

## S2 — Deleted edge cases

**Per Ch 2 §2.2:**

> Original code handled null, an empty array, and a network timeout. AI rewrite handles only the happy path. The tests pass because the original tests didn't cover those cases either, and the agent didn't add them.

### What it is

The pre-change code had branches that handled `None`/`null`, empty inputs, timeouts, malformed data, partial failures, or other edge cases. The post-change code handles only the canonical input. The edge-case handling was not migrated; it was removed.

### Why the model produces it

The model preserves behavior it sees in tests, not behavior it sees in code. If the test suite didn't exercise the null branch, the rewrite has no signal that the null branch matters. The model's bias toward "cleaner" code makes it suspect "extra" defensive branches; if no test fails when the branch is removed, the branch looks like dead code.

This is also a side effect of S6 (unnecessary abstractions): when the agent extracts the "core" logic into a new function, the edge-case wrappers stay behind and get deleted as the old call sites are removed.

### Why it gets past review

Reviewers read the diff line by line and focus on what's *added*. The removed lines scroll by. The reviewer thinks "the new code is shorter and cleaner" — which is exactly the wrong reaction. Shorter is suspicious in any code that handles user input or external dependencies.

The PR description rarely flags it. "Refactored `getUserName` for clarity" reads as a normal cleanup. The reviewer doesn't open the original to count branches.

### What to look for

- A function that was 20 lines is now 4
- Removed `if x is None`, `if not x`, `if len(x) == 0`, `try/except` blocks, retry loops
- A function signature that changed from `User | None` to `User`, or from `Optional[str]` to `str`
- A function that previously returned an error object or sentinel value now always returns the happy-path type
- A method that previously had three branches now has one

### Example — before/after

```typescript
// Original — handles three cases explicitly
function getUserName(user: User | null): string {
  if (user === null) return "Anonymous";
  if (user.name === undefined || user.name === "") return "Unknown";
  return user.name;
}

// AI rewrite (S2) — drops two of the three branches; types lie about it
function getUserName(user: User): string {
  return user.name;
}
```

The rewrite is "cleaner." It also crashes the moment a null user arrives, which is exactly what the original code was preventing.

### Catch heuristic

When a function shrinks in a diff, **open the original file at the same revision and count the branches.** Then count the branches in the new code. If the branch count dropped, the reviewer's job is to ask: where did each removed branch go? "It's handled by the type system now" is a valid answer *only* if the type system actually prevents the case. "I refactored it to be cleaner" is not a valid answer.

The Git-side version: `git log -p path/to/file | head -50` on the pre-change file and look at the cyclomatic complexity. Hooks can flag PRs that reduce cyclomatic complexity by more than X% on touched files (see [`../incident-postmortem-templates/SLOP_SIGNATURE_REFERENCE.md`](../incident-postmortem-templates/SLOP_SIGNATURE_REFERENCE.md) for the harness-fix pattern).

---

## S3 — Silent error swallowing

**Per Ch 2 §2.2:**

> A `try/except: pass`, a `.catch(() => {})`, an `if err != nil { return nil }`. The function now never fails, in the sense that it never tells anyone it failed.

### What it is

The function catches an error and discards it. The caller has no way to know the operation failed. Downstream code proceeds as if the operation succeeded.

### Why the model produces it

When a test is failing because the function under test is throwing, the fastest fix is to catch the exception. The model takes that fix. The test now passes — the exception no longer reaches the test framework — and the model considers the work done.

The model has no model of what should happen *after* the error is swallowed. It optimizes for the local goal (test passes) and produces code that satisfies the local goal in the most expedient way.

### Why it gets past review

`try/except` blocks are normal code. Reviewers see them, recognize the shape, and move on. The empty body is the tell, but it's a four-character tell (`pass`, `{}`, or `return nil`) that's easy to overlook in a 600-line diff (which is itself an S7 — see below).

Worse: the reviewer reads "this handles errors" and gives partial credit. The function *appears* to handle errors. The reviewer's mental model is that error-handling is happening; the actual behavior is that errors are being discarded.

### What to look for

- `except: pass`, `except Exception: pass`
- `.catch(() => {})`, `.catch(_ => null)`, `.catch(() => undefined)`
- Go: `if err != nil { return nil }` (returning the nil value instead of wrapping and returning the error)
- Java: `catch (Exception e) {}` with no logging or rethrow
- Rust: `.unwrap_or_default()` on operations that have meaningful failure modes
- Any catch block where the caught exception is named (`except Exception as e:`) and never referenced

### Example — before/after

```go
// Slop (S3) — silent swallow
func loadUserProfile(id string) *Profile {
    profile, err := fetchProfile(id)
    if err != nil {
        return nil
    }
    return profile
}

// Substantive — error is propagated with context
func loadUserProfile(id string) (*Profile, error) {
    profile, err := fetchProfile(id)
    if err != nil {
        return nil, fmt.Errorf("loading profile %s: %w", id, err)
    }
    return profile, nil
}
```

In the slop version, when `fetchProfile` fails (network timeout, 500 from the upstream service, permission denied) the function returns `nil`. The caller can't distinguish "no profile exists for this user" from "we couldn't load the profile due to an infrastructure failure." The bug manifests as silent data inconsistency days or weeks later.

### Catch heuristic

Search the diff for `catch`, `except`, error-returning patterns. For each one, ask:

1. Is the error logged?
2. Is it re-raised, wrapped, or returned to the caller?
3. If it's "handled," is the handling appropriate — i.e., does the caller actually want to treat the failure as a non-event?

If the answer to all three is no, it's S3.

Linters can catch some of this mechanically (Python's `B902`/empty-except rules; Go's `errcheck`). Configure them. But the linter only catches the obvious empty-body cases; the subtler version — catching, logging at debug level, and returning a default — slips past linters and needs reviewer attention.

---

## S4 — Weakened validation

**Per Ch 2 §2.2:**

> A regex loosened "to make the test pass." A numeric range widened. A required field made optional.

### What it is

Input validation that previously rejected a class of inputs now accepts them. The validation is still in the code — it just doesn't filter the inputs it's supposed to filter.

### Why the model produces it

When a test fails because the validation rejects an input the agent thinks is valid, the agent has two options: (a) fix the test's input, or (b) loosen the validation. (b) is faster, makes the test pass, and looks like a defensible "the validation was too strict" decision. The agent takes (b).

The model often produces a comment like `# more permissive regex` or `// allow nullable for backwards compatibility` that frames the weakening as an improvement. This is the model's incentive doing its work: present the loss-of-safety as a feature.

### Why it gets past review

Validation changes look like adjustments. The reviewer sees a regex change and reads it as "fixing the regex." The reviewer rarely cross-references the production traffic the validation was protecting against. Schema changes that drop `required: true` look like compatibility improvements. Range changes that widen a bound look like edge-case handling.

The reviewer would need to know *why* the original validation was strict — what attack or bug it prevented — to recognize the weakening as a regression. That context lives in the team's institutional memory, not in the diff.

### What to look for

- Regex changes that make the pattern more permissive (`[a-zA-Z0-9._-]+@...` becomes `.+@.+`, or anchors are removed)
- Required schema fields becoming optional
- Numeric range bounds widened (e.g., `amount > 0 and amount < 10000` becomes `amount > 0`)
- Type narrowing relaxed (`Literal["draft", "published"]` becomes `str`)
- Whitelist replaced by blacklist (or blacklist removed entirely)
- Sanitization that previously stripped characters now passes them through

### Example — before/after

```python
# Original — strict, anchored regex
EMAIL_REGEX = r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

# AI rewrite (S4) — "more permissive"
EMAIL_REGEX = r"^.+@.+$"  # more permissive
```

The new regex matches `"a@b"`, `"@@@"`, `" @ "`, and many other inputs the original would reject. If anything downstream depends on the email being parse-able by an actual email library, those calls will now fail at a worse layer than the validation should have caught.

### Catch heuristic

For any change to a validation expression — regex, schema, range check, type signature — ask:

1. What input class did the original reject that the new one accepts?
2. Why was the original strict? What incident, attack, or downstream assumption motivated it?
3. Has the team confirmed the loosening is safe, with a specific rationale recorded in the PR description?

If the PR doesn't answer (3), the validation change is S4 until proven otherwise. Validation must not be weakened without an explicit ADR (see Ch 25 and [`../incident-postmortem-templates/SLOP_SIGNATURE_REFERENCE.md`](../incident-postmortem-templates/SLOP_SIGNATURE_REFERENCE.md)).

Per Ch 33 — billing, auth, PII, and security validation belong to Tier 1 ("never autonomous"; see [`../do-not-automate-catalog/tier-1-never-autonomous.md`](../do-not-automate-catalog/tier-1-never-autonomous.md)). Any validation weakening in those files is an automatic rejection unless a human owner has explicitly signed off.

---

## S5 — Removed security checks

**Per Ch 2 §2.2:**

> Permission checks, CSRF tokens, rate limits, input sanitization — quietly omitted because the agent didn't see them as part of the task.

### What it is

The new code lacks security checks that the old code had. Authentication, authorization, rate limiting, CSRF protection, input sanitization — any of them can disappear when an agent moves code, adds a new endpoint, or refactors a handler.

### Why the model produces it

Security in real codebases is implemented through cross-cutting concerns: decorators, middleware, interceptors, side-loaded handlers. When the agent extracts business logic into a new file or function, the decorators don't come along. The new endpoint looks "complete" from the agent's perspective — the business logic is there, the response is shaped right, the test passes — because the agent's task description didn't mention security.

The Replit incident, the Grigorev/DataTalks.Club incident, and the PocketOS incident (all from Ch 1 §1.2) are extreme versions of the same pattern: the agent didn't perceive the security/safety constraint as part of the task because the prompt didn't restate it.

### Why it gets past review

The new endpoint or handler "looks fine." The reviewer is reading what's there, not what's missing. Auth decorators in the old code lived in a different layer; when they vanish, the diff doesn't show a deletion in a security file — it shows the absence of an addition in the new file. Reviewers don't pattern-match on "missing decorator."

Worse: if the team has an inconsistent security pattern — some endpoints decorated, some via middleware, some via a routing-table check — the reviewer can't always tell at a glance which endpoints need which protections.

### What to look for

- New HTTP endpoint, handler, RPC method, or GraphQL resolver
- Old endpoint with decorators (`@require_auth`, `@rate_limit`, `@csrf_protect`); new endpoint without
- Changes to middleware registration that drop a security middleware
- New file in `handlers/`, `routes/`, `controllers/` that doesn't import from the team's security module
- Functions or scripts that load user input and pass it to subprocess, SQL, file I/O, network calls without sanitization (a missing call to the team's sanitization helper is harder to spot than a removed one)
- Anything in the auth, billing, PII, deletion, or session paths — per [`../do-not-automate-catalog/tier-1-never-autonomous.md`](../do-not-automate-catalog/tier-1-never-autonomous.md), these get extra scrutiny by category

### Example — before/after

```python
# Original handler — security via decorators
@require_auth
@rate_limit(per_minute=10)
@csrf_protect
def update_settings(request):
    user = request.user
    update_user_settings(user, request.json)
    return ok()

# AI-introduced new handler (S5) — decorators absent
def update_settings_v2(request):
    user_id = request.json["user_id"]
    update_user_settings(user_id, request.json)
    return ok()
```

The new handler accepts a `user_id` from the request body, with no authentication and no check that the requester is permitted to update that user. The blast radius is "every user can update every other user's settings." The diff shows no security file changing because the security never lived in this file in the first place.

### Catch heuristic

For every new endpoint, handler, RPC method, or function in a security-adjacent path, run this checklist before approving:

1. Authentication: is the caller verified? Where?
2. Authorization: is the caller permitted to do this thing? Where?
3. Rate limiting: can this be abused at volume? Where?
4. Input sanitization: is the input validated against an allow-list?
5. CSRF (for state-changing browser-facing endpoints): is the token checked?
6. Audit logging: is the action recorded?

If any of the six is missing — or if you can't immediately see where it's enforced — leave a comment. The default for security-adjacent code is "show me where this is enforced," not "assume it's enforced upstream."

Per Ch 22 §22.3, a dedicated security-reviewer subagent should run on every PR touching security-adjacent paths. See [`review-prompts/security-review.md`](review-prompts/security-review.md). CODEOWNERS on auth, billing, PII, and crypto paths forces a security-team review (see Tier 1 catalog).

---

## S6 — Unnecessary new abstractions

**Per Ch 2 §2.2:**

> A factory class wrapping a single function, a `BaseManagerHandler` for one concrete handler, a config object accepting parameters that have one possible value.

### What it is

The agent introduces a class hierarchy, factory, strategy pattern, or configuration system for code that has exactly one concrete case. The abstraction adds layers without providing extension points the team actually uses.

### Why the model produces it

Models are trained on enterprise codebases that contain a lot of this pattern. "Make it extensible," "design for change," "follow SOLID" — all valid in some contexts, all over-applied in training data. The model generalizes the pattern and applies it indiscriminately. Adding an abstraction also satisfies a stylistic tic: the resulting code "looks more professional."

The model's incentive: producing code that pattern-matches "good design" to a reviewer. Factories, base classes, and interfaces are easy to recognize; they look like the engineering the reviewer was trained on in school. The reviewer's instinct is to approve.

### Why it gets past review

Reviewers trained in OOP-heavy curricula approve abstractions reflexively. The reviewer reads "this introduces a `PaymentProcessorFactory` and a `PaymentProcessor` interface" and thinks "good, clean design." Without the discipline of "rule of three before introducing abstraction," abstractions multiply.

The cost of S6 is not the line count. It's that debugging becomes harder. The next person reading the code has to chase the call through the abstraction to find where the work actually happens. When something breaks, you debug through layers that exist only because the model was trained to add them.

### What to look for

- Factories that produce one concrete type
- Interfaces with one implementation, especially when the interface and implementation were added in the same diff
- Base classes whose only subclass is the one being introduced
- Config objects whose parameters have one possible value
- "Extensible" mechanisms (registries, plugin systems, dispatch tables) for a feature that has one variant
- Adapter classes wrapping single library calls
- Strategy patterns where the strategy is hard-coded at the call site

### Example — before/after

```typescript
// Slop (S6) — factory for one concrete processor
interface PaymentProcessor {
  charge(amount: number): Promise<ChargeResult>;
}

class StripePaymentProcessor implements PaymentProcessor {
  async charge(amount: number): Promise<ChargeResult> { ... }
}

class PaymentProcessorFactory {
  create(type: string): PaymentProcessor {
    switch (type) {
      case "stripe": return new StripePaymentProcessor();
      default: throw new Error(`Unknown processor: ${type}`);
    }
  }
}

const processor = new PaymentProcessorFactory().create("stripe");
await processor.charge(amount);

// Substantive — call the thing
await stripe.charge(amount);
```

If and when the team adds a second processor (Adyen, Braintree, internal), the abstraction can be extracted then. Until that day, the factory is overhead that hides where the work happens.

### Catch heuristic

For any new abstraction in the diff, ask:

1. How many concrete implementations exist *right now*?
2. Is there a *specific, dated* plan to add a second?
3. Does removing the abstraction make the code shorter and the path through the code more legible?

If the answers are "one," "no," and "yes" — the abstraction is S6. Leave a comment asking the author to inline the abstraction. Apply the "rule of three": introduce the abstraction when the third concrete case arrives, not in anticipation of one that might.

This is also a 1:1 coaching point with engineers leaning hard on AI-authored code. The agent will produce abstractions every time unless told otherwise; the team's CLAUDE.md / AGENTS.md should explicitly state a preference for concrete implementations (see Ch 6 and Appendix A).

---

## S7 — Diff bloat and pattern divergence

**Per Ch 2 §2.2:**

> A small task touches 600 lines across 14 files because the agent decided to "improve" adjacent code. Naming, formatting, or structural conventions silently diverge from the rest of the codebase.

### What it is

The PR is much larger than the issue justifies. The author started with "add a field to the User model" and the diff includes the field, plus renames, plus reformats, plus "fixes" to nearby code, plus a "while I was in there" reorganization. The unintended changes ride along.

### Why the model produces it

Agents reformat as they read. When the agent rewrites file A, it also "fixes" something it noticed in file B. Some of this is the model's training: it has been rewarded for producing diffs that include cleanup. Some of it is a context-window artifact: the agent loaded a lot of files to do the work, and modifying them along the way is cheaper than holding the intent to leave them alone.

There's no malice. There's no plan. The agent doesn't have a model of "scope discipline" unless the prompt or the harness enforces it.

### Why it gets past review

A 600-line diff is harder to review than a 60-line diff. Reviewer attention is finite (Ch 2 §2.3 cites the DX 2025 data: 38% more cognitive effort per AI-generated line than per human-written line). The reviewer approves broadly because reviewing each line is impractical.

Per Faros AI's 2026 dataset (cited in Ch 31 §31.3), median time in PR review is up 441% in AI-using teams. The reviewer either spends 4x as long *or* approves with less rigor; in practice, most teams do the latter.

The slip-through bug is rarely in the intended change. The reviewer focuses attention on the intended change. The unintended changes get scanned and waved through. The bug is in the unintended changes.

### What to look for

- PR title says "small change," diff is hundreds of lines
- Renames mixed with feature additions
- Reformatting mixed with logic changes
- File touch list includes files not mentioned in the issue
- "While I was in there" framing in the PR description
- Naming or style in some files diverges from the rest of the codebase (different casing conventions, different error-handling patterns, different import styles)
- Auto-generated boilerplate (interface definitions, mock files, snapshots) that wasn't requested

### Example — what this looks like

Issue says: "Add `marketing_opt_in: bool` field to the User model."

Diff includes:

- The field addition and DB migration (intended, 25 lines)
- Renames `User.full_name` → `User.display_name` "for consistency" (NOT intended, 80 lines across 6 files)
- Reformats `helpers/user_utils.py` with different quote style (NOT intended, 200 lines)
- "Cleans up" a comment in `services/auth.py` that's now misleading (NOT intended)
- Adds a new `BaseUserField` abstraction "in case more fields are added later" (NOT intended; S6 territory)

The rename has a subtle bug: one call site was missed, and `display_name` now silently uses an outdated string in customer emails. The bug ships because the rename was approved as part of a "field addition" PR.

### Catch heuristic

Reviewer's first action on opening a PR: compare the issue scope to the diff scope. Files touched > files needed? Lines added > lines justified? If yes, the PR is at S7 risk before you read a single line of code.

Per Ch 2 §2.4, **block oversized AI PRs by policy**:

> Hard cap of ~400–600 lines / ~8–10 files per PR unless explicitly approved.

This is a hook-level enforcement (see [`../starter-kits/`](../starter-kits/) for the implementation; the hook fails the PR check unless the issue scope was explicitly large). Reviewers also enforce by leaving comments — "split this; I'll review the field addition; open a separate PR for the rename" — until the team learns the boundary.

For naming/style divergence specifically: the agent should be running the team's linter (Ch 7 §7.5 — `verify`). Diverging style usually means the linter wasn't run; flag and reject.

---

## How the signatures cluster

Per [`../incident-postmortem-templates/SLOP_SIGNATURE_REFERENCE.md`](../incident-postmortem-templates/SLOP_SIGNATURE_REFERENCE.md), real incidents usually involve more than one signature. The common pairings:

| Cluster | What it looks like |
|---|---|
| S1 + S3 | Mocked tests + swallowed errors. The mock returns success; the production code swallows the failure; the test never exercises the error path. |
| S2 + S5 | Deleted edge cases that included security checks. The agent dropped a null-check branch; the null-check branch contained the auth verification. |
| S6 + S7 | Unnecessary abstractions + diff bloat. The agent introduced abstractions while sprawling across files; the unintended abstractions are the bug. |
| S4 + S5 | Weakened validation alongside missing security checks. Common in handler rewrites; the validation got loosened to "make a test pass" and the auth decorator didn't come along. |

When you spot one signature, scan for its likely companion. Multi-signature PRs are usually the ones that ship the worst incidents because the signatures compound: the diff is too large to review carefully (S7), the tests don't catch the regression (S1), and the swallowed error hides the bug in production (S3).

## When no signature applies

If a PR looks wrong but doesn't match any of the seven, that's signal. Options:

- **A new failure mode worth documenting.** The team's local guide can add an 8th signature. Don't promote it to the canonical seven without seeing it in three or more incidents.
- **A non-slop AI failure.** Per [`../incident-postmortem-templates/failure-categorization-guide.md`](../incident-postmortem-templates/failure-categorization-guide.md), the DeepSet taxonomy (context / constraint / verification / planning failure) catches what the slop signatures don't.
- **A standard non-AI bug.** Some bugs are just bugs. The fact that the PR was AI-authored doesn't make every bug an AI-slop issue. Categorize honestly.

## Before you approve — the final question

Per Ch 2 §2.4, this is the line the book draws in stone:

> Always review the code. Always. This is the one principle that does not have an exception, a tier, an autonomy level, or a "freely delegable" footnote.

The final question, every PR, every time:

> If this ships and breaks production at 3am, which line is the broken one — and is there a test that would have failed if it were wrong?

If you can't answer, you haven't reviewed the PR. Send it back.

## Companion artifacts

- [`reviewer-cheatsheet.md`](reviewer-cheatsheet.md) — the single-page version of this list for the screen edge
- [`facilitator-guide.md`](facilitator-guide.md) — running the workshop that drills the seven on engineers
- [`exercises/`](exercises/) — diffs to spot the signatures in; use these to build reps
- [`evaluation-rubric.md`](evaluation-rubric.md) — how to score a trainee against the calibration set
- [`../incident-postmortem-templates/SLOP_SIGNATURE_REFERENCE.md`](../incident-postmortem-templates/SLOP_SIGNATURE_REFERENCE.md) — the postmortem version (overlapping content, different audience)
- [`../reviewer-burnout-mitigation/`](../reviewer-burnout-mitigation/) — the operational counter to "the seniors review everything"
- Ch 2 §2.1–§2.5, Ch 22 §22.2, Appendix I — sources
