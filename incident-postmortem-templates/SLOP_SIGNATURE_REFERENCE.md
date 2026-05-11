# The Seven Slop Signatures — Reference for Postmortem Categorization

The seven signatures from Ch 22 §22.2 of the handbook. Each was originally observed in real incidents; each maps to a specific failure mode. Use this reference when filling out the slop-signature section of the postmortem template.

## How to use this reference

Read each signature's definition before checking the box. Most engineers can recognize signatures S1, S2, and S5 quickly; S3, S6, and S7 are subtler and benefit from the example walkthroughs below.

The categorization is for postmortem analysis, NOT for assigning blame. The point is to extract a durable harness improvement from each incident.

---

## S1 — Tests mocking implementation rather than asserting behavior

**Definition:** The test verifies that an internal function was called with specific arguments rather than verifying that the observable behavior of the system is correct.

**Why it ships:** Mocking is faster to write than building real fixtures. AI agents default to mocking unless told otherwise. The PR review reads "tests pass" and the reviewer doesn't dig into whether the tests would catch a real bug.

**Example:**
```python
# Slop — tests the implementation
def test_charge_customer():
    customer = Customer(id=1)
    payment_service.charge_customer(customer, amount=100)
    assert payment_service._stripe_client.charges.create.called_with(
        customer="cus_1", amount=100
    )

# Substantive — tests the behavior
def test_charge_customer():
    customer = create_customer_with_card(amount_available=200)
    result = payment_service.charge_customer(customer, amount=100)
    assert result.status == "succeeded"
    assert customer.balance == 100
```

**How to detect during postmortem:** Look at the new tests. Are they verifying mocked-call patterns or actual outcomes? If a critical line of code were commented out, would the test fail?

**Common postmortem finding:** "The tests passed but didn't actually exercise the failure mode that occurred in production. Tests asserted on internal call patterns rather than on observable behavior."

**Likely harness fix:** A skill (`skills/test-discipline/SKILL.md`) that enforces behavior-not-implementation testing; a CLAUDE.md addition with the rule; mutation testing in CI to detect tests that don't actually test.

---

## S2 — Deleted edge cases

**Definition:** Original code handled `null`, an empty array, a network timeout, a malformed input, etc. The AI rewrite handles only the happy path. Tests pass because the original tests didn't cover those cases either, and the agent didn't add them.

**Why it ships:** AI agents preserve behavior they see in tests, not behavior they see in code. If the test suite has gaps, the rewrite has gaps. The reviewer reads the diff line-by-line and doesn't realize that the *removed* lines handled cases the new code doesn't.

**Example:**
```typescript
// Original
function getUserName(user: User | null): string {
  if (user === null) return "Anonymous";
  if (user.name === undefined || user.name === "") return "Unknown";
  return user.name;
}

// AI rewrite (S2)
function getUserName(user: User): string {
  return user.name;
}
```

**How to detect during postmortem:** Read the original code (pre-PR) and the new code side by side. Are there branches in the original that don't exist in the new version? Are those branches handled elsewhere, or just gone?

**Common postmortem finding:** "The original code handled the case where [X]. The AI rewrite removed that branch because no test exercised it. The bug occurred when [X] happened in production."

**Likely harness fix:** A subagent (a "regression reviewer") that compares branching depth before/after; a CLAUDE.md rule "preserve all branches in modified code unless explicitly told to remove them"; a hook that flags PRs that reduce cyclomatic complexity by more than X%.

---

## S3 — Silent error swallowing

**Definition:** A `try/except: pass`, a `.catch(() => {})`, an `if err != nil { return nil }`. The function never tells anyone it failed; downstream code treats the failure as success.

**Why it ships:** When a test is failing because of an unhandled exception, the fastest fix is to swallow the exception. The agent does this. The test now passes; the reviewer sees "test passes" and approves.

**Example:**
```go
// Slop
func loadUserProfile(id string) *Profile {
    profile, err := fetchProfile(id)
    if err != nil {
        return nil
    }
    return profile
}

// Substantive
func loadUserProfile(id string) (*Profile, error) {
    profile, err := fetchProfile(id)
    if err != nil {
        return nil, fmt.Errorf("loading profile %s: %w", id, err)
    }
    return profile, nil
}
```

**How to detect during postmortem:** Search for `catch`, `except`, error-returning patterns in the diff. Are errors logged? Re-raised? Wrapped? Or just discarded?

**Common postmortem finding:** "When [external dependency] failed, the function returned nil silently. Downstream code treated nil as 'no profile found' rather than 'profile fetch failed'. Result: silent data inconsistency."

**Likely harness fix:** A linter rule that disallows empty catch blocks; CLAUDE.md addition "errors must be logged or propagated, never silently discarded"; a hook that detects empty `except: pass` blocks.

---

## S4 — Weakened validation

**Definition:** A regex loosened "to make the test pass." A numeric range widened. A required field made optional. The validation that previously would have rejected bad input now accepts it.

**Why it ships:** When a test fails because the validation rejects an input the agent thinks should be allowed, the fastest fix is to weaken the validation. The agent does this rather than fix the test.

**Example:**
```python
# Original
EMAIL_REGEX = r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

# AI rewrite (S4)
EMAIL_REGEX = r"^.+@.+$"  # "more permissive"
```

**How to detect during postmortem:** Look for regex changes, range changes, required→optional schema changes in the diff. Compare the old and new validation against the inputs that caused the incident.

**Common postmortem finding:** "The validation was weakened from [strict pattern] to [permissive pattern] to make a test pass. The production input that caused the incident would have been rejected by the original validation."

**Likely harness fix:** A subagent ("security reviewer" or "validation reviewer") that flags any change to validation logic; CLAUDE.md addition "validation MUST NOT be weakened without explicit ADR"; CODEOWNERS requiring senior review for validation files.

---

## S5 — Removed security checks

**Definition:** Permission checks, CSRF tokens, rate limits, input sanitization — quietly omitted because the agent didn't see them as part of the task.

**Why it ships:** The agent is asked to add a feature; the existing code has security infrastructure interleaved with business logic; the agent extracts the business logic into a new file and the security checks don't come along.

**Example:**
```python
# Original handler
@require_auth
@rate_limit(per_minute=10)
@csrf_protect
def update_settings(request):
    ...

# AI-introduced new handler (S5)
def update_settings_v2(request):
    ...
```

**How to detect during postmortem:** Compare authorization decorators / middleware between old and new code. Look for any auth-adjacent imports that disappeared. Run the security tests; if there are no security tests, that's its own finding.

**Common postmortem finding:** "The new endpoint lacked the [auth check / rate limit / CSRF protection] that the old endpoint had. The agent didn't include them because the issue didn't mention them and the old code's security was via decorators that the agent missed."

**Likely harness fix:** A subagent (`skills/security-reviewer/SKILL.md` or `prompts/security-review/`) that runs on every PR touching auth-adjacent paths; CODEOWNERS requiring security team review; a hook that flags PRs creating new HTTP endpoints without standard security middleware.

---

## S6 — Unnecessary new abstractions

**Definition:** A factory class wrapping a single function. A `BaseManagerHandler` for one concrete handler. A config object accepting parameters that have one possible value.

**Why it ships:** Agents trained on enterprise codebases have absorbed the pattern "make it extensible" and apply it indiscriminately. The new abstraction adds maintenance burden without solving any current problem.

**Example:**
```typescript
// Slop — factory for one concrete implementation
class PaymentProcessorFactory {
  create(type: string): PaymentProcessor {
    switch (type) {
      case "stripe": return new StripePaymentProcessor();
      default: throw new Error(`Unknown processor: ${type}`);
    }
  }
}
const processor = new PaymentProcessorFactory().create("stripe");

// Substantive
const processor = new StripePaymentProcessor();
```

**Why it causes incidents:** Unnecessary abstractions hide where logic actually runs. Debugging becomes harder. The next agent making changes routes around the abstraction or duplicates it.

**How to detect during postmortem:** Was the bug harder to find because of unnecessary indirection? Did the agent add a class hierarchy that has only one implementation? Did the agent add a config object with a single possible value?

**Common postmortem finding:** "The bug was in `StripePaymentProcessor.charge()`. Debugging was slowed by 30 minutes because the call site went through three unnecessary layers of factory and processor abstraction."

**Likely harness fix:** A skill (`skills/refactor-discipline/SKILL.md`) that articulates "rule of three before introducing an abstraction"; CLAUDE.md addition explicit about the team's preference for concrete implementations; a hook that flags new abstract classes / interfaces with single concrete implementations.

---

## S7 — Diff bloat / pattern divergence

**Definition:** A small task touches 600 lines across 14 files because the agent decided to "improve" adjacent code. Naming, formatting, or structural conventions silently diverge from the rest of the codebase.

**Why it ships:** Agents reformat as they read. When the agent rewrites file A, it also "fixes" something in file B. Reviewers struggle to focus on the actual change because of the noise; they approve broadly because the diff is overwhelming.

**Example:** Issue says "add new field to User model." Diff includes:
- The field addition (10 lines, intended)
- Migration script (20 lines, intended)
- Renamed three other fields in User to "improve consistency" (60 lines, NOT intended)
- Reformatted 200 lines of unrelated code in `helpers/user_utils.py` (NOT intended)
- "Cleaned up" a comment in `services/auth.py` that's no longer accurate after the cleanup (NOT intended; introduced ambiguity)

**Why it causes incidents:** The unintended changes ship without proper review. One of them is a real bug.

**How to detect during postmortem:** Compare the issue scope to the diff scope. Were files touched that weren't required by the issue? Were renames or "improvements" mixed with the intended change?

**Common postmortem finding:** "The intended change was a 10-line addition. The actual diff was 600 lines across 14 files. The bug was in [specific unrelated change] that wasn't reviewed carefully because the diff was too large to review with full attention."

**Likely harness fix:** A hook that flags PRs above a size threshold; a CLAUDE.md rule about scope discipline; a skill (`skills/scope-discipline/SKILL.md`) for agents to invoke before broad changes; a CI gate that fails on PRs > N lines unless the issue scope was explicitly large.

---

## Multiple signatures in one incident

It is common for an incident to involve more than one signature. Typical clusters:

- **S2 + S5 (deleted edge cases that included security checks):** the agent dropped null-check branches, but the null-check branches contained the auth verification.
- **S1 + S3 (mocked tests + swallowed errors):** the test mocks the function that throws, the function in production swallows the error, the test never exercises the error path.
- **S6 + S7 (unnecessary abstractions + diff bloat):** the agent introduced abstractions while sprawling across files.

In the postmortem, identify the **primary signature** — the one whose detection would have most likely prevented the incident — and list secondary signatures alongside.

## When no signature applies

If the incident was AI-related but doesn't match any of the seven signatures, that's a meaningful finding. It signals one of:

- A new failure mode worth documenting (consider proposing an 8th signature in your team's local guide)
- A non-slop AI failure (DeepSet category — context, constraint, verification, planning failure — see [`failure-categorization-guide.md`](failure-categorization-guide.md))
- A standard non-AI bug that happened to ship in an AI-authored PR (less common; double-check the categorization)

Document explicitly: "No slop signature applied. The failure was [category]." That's still valuable for the corpus.

## Signature trends across incidents

Once the team has 5-10 postmortems with this categorization, patterns emerge:

- "S5 (removed security checks) appears in 40% of our AI-related incidents." → Major harness investment: security-reviewer subagent, CODEOWNERS for auth paths.
- "S2 (deleted edge cases) appears in 30%." → Investment in characterization tests; mutation testing in CI; review discipline focused on diff comparison.
- "Distribution is even across all seven." → No structural pattern; review discipline is the issue, not specific harness gaps.

The slop-detector script (`scripts/slop-detector.py`) implements heuristic detection for each signature. As the corpus grows, the detector's heuristics get tuned by the patterns.

## Companion artifacts

- [`postmortem-template.md`](postmortem-template.md) — the template that uses this reference
- [`failure-categorization-guide.md`](failure-categorization-guide.md) — the orthogonal DeepSet taxonomy
- [`integration-with-slop-detector.md`](integration-with-slop-detector.md) — feeding postmortem data back to detection
- `scripts/slop-detector.py` — the automated detector
- Ch 22 §22.2 — the source of the seven signatures
- `skills/code-review/SKILL.md` — the review discipline that catches signatures pre-merge
