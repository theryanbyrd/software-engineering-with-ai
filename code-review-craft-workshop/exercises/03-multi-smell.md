# Exercise 03 — The "Cleanup" Refund Handler

**Planted smells:** S4 (weakened validation), S5 (removed security checks), S7 (diff bloat). Also a dose of S1 in the test.
**Difficulty:** Hard. Multi-smell. For trainees past the first two exercises.
**Pacing:** 7 minutes review, 5 minutes debrief.

## Scenario

The PR description:

> **Title:** Clean up refund handling
>
> Refactors the refund handler into a new endpoint (`refund_v2`) with cleaner validation and a more permissive amount range to support partial refunds. Old endpoint is deprecated, will be removed in v3. Also tidied up some adjacent code I noticed.
>
> Tagged: `[AI-authored]`

The issue (one line):

> "Refund processing: support partial refunds. Currently we can only refund the full charge amount; finance needs to be able to refund a portion."

This is a billing/payments path. Per [`../do-not-automate-catalog/tier-1-never-autonomous.md`](../do-not-automate-catalog/tier-1-never-autonomous.md), Tier 1 applies — these changes are never to be merged on AI authorship alone.

## The diff

```python
# billing/handlers.py

# BEFORE (existing, NOT shown in the diff — visible via git show HEAD^)
- @require_auth
- @rate_limit(per_minute=5)
- @csrf_protect
- @require_role("billing_admin")
- def refund(request):
-     charge_id = request.json["charge_id"]
-     amount = request.json.get("amount")
-     charge = get_charge(charge_id)
-     if amount is None:
-         amount = charge.amount
-     if amount <= 0 or amount > charge.amount:
-         return error(400, "invalid amount")
-     if charge.refunded_amount + amount > charge.amount:
-         return error(400, "exceeds charge amount")
-     audit_log("refund_initiated", user=request.user, charge_id=charge_id, amount=amount)
-     refund = stripe.refunds.create(charge=charge.stripe_id, amount=amount)
-     audit_log("refund_completed", user=request.user, charge_id=charge_id, refund_id=refund.id)
-     return ok(refund)

# AFTER (the diff shows this added; the old handler also remains, marked deprecated)
+ def refund_v2(request):
+     """Cleaner refund handler. Supports partial refunds."""
+     charge_id = request.json["charge_id"]
+     amount = request.json.get("amount", 0)
+     charge = get_charge(charge_id)
+     if amount > 0:
+         refund = stripe.refunds.create(charge=charge.stripe_id, amount=amount)
+     else:
+         refund = stripe.refunds.create(charge=charge.stripe_id)
+     return ok(refund)
```

```python
# billing/routes.py
  routes = [
      Route("/refund", refund, methods=["POST"]),
+     Route("/refund_v2", refund_v2, methods=["POST"]),
      Route("/charges/<id>", get_charge_handler, methods=["GET"]),
  ]
```

```python
# tests/test_refund.py
+ def test_refund_v2_creates_refund():
+     stripe.refunds = MagicMock()
+     stripe.refunds.create.return_value = MagicMock(id="re_1")
+
+     request = MagicMock()
+     request.json = {"charge_id": "ch_1", "amount": 50}
+
+     response = refund_v2(request)
+
+     stripe.refunds.create.assert_called_once_with(charge="ch_1_stripe", amount=50)
+     assert response.status == 200
```

```python
# billing/utils.py — also touched by this PR
- def format_currency(amount, currency="USD"):
-     """Format an amount as a currency string."""
-     return f"{currency} {amount / 100:.2f}"

+ def format_currency(amount: int, currency: str = "USD") -> str:
+     """Format an amount as a currency string."""
+     return f"{currency} {amount / 100:.2f}"

# Renamed throughout 4 other files: `format_currency` → `formatCurrency` (camelCase)
# 80 lines of rename-only changes follow in:
#   - billing/invoices.py
#   - billing/reports.py
#   - billing/email_templates.py
#   - billing/audit.py
```

Total diff: 12 files, 350 lines.

## Trainee task

Review this diff. Write the comments you would leave on the PR. Suggested time: 7 minutes.

Note: this PR touches the billing path. Per [`../do-not-automate-catalog/tier-1-never-autonomous.md`](../do-not-automate-catalog/tier-1-never-autonomous.md), the bar is higher than a normal PR.

---

## Instructor key

### Planted smells

**S5 (primary, severe).** The new `refund_v2` handler is missing four decorators that the original `refund` had:

- `@require_auth` — anyone can hit this endpoint, authenticated or not
- `@rate_limit(per_minute=5)` — unlimited refund attempts allowed
- `@csrf_protect` — vulnerable to CSRF
- `@require_role("billing_admin")` — any logged-in user can refund any charge

The blast radius is "any user can issue refunds to any charge for any amount." This is the worst kind of S5: a new endpoint that quietly omits security infrastructure that the old endpoint had. The reviewer must compare the two handlers, not just read the new one.

**S4 (severe, billing-specific).** The new handler dropped four pieces of validation:

1. `if amount <= 0 or amount > charge.amount` — the new handler accepts negative amounts (Stripe may reject them, but the handler doesn't validate; if Stripe's behavior changes or someone routes around Stripe, this is unsafe)
2. `if charge.refunded_amount + amount > charge.amount` — the new handler allows refunding more than the charge. Cumulative refunds could exceed the original charge.
3. The `amount is None` → `charge.amount` default — the new handler defaults `amount` to 0, then passes `amount=0` to Stripe as a "full refund" via the else branch. The behavior is plausibly equivalent but subtly different (and the test doesn't cover it).
4. The audit logging — `audit_log("refund_initiated", ...)` and `audit_log("refund_completed", ...)` are both absent. Per Tier 1 ("Anything that touches the customer of record without a transaction log"; see [`../do-not-automate-catalog/tier-1-never-autonomous.md`](../do-not-automate-catalog/tier-1-never-autonomous.md)), this is a compliance failure.

**S7 (severe).** The PR scope is "support partial refunds." The diff includes:

- The new endpoint (intended, ~15 lines)
- The route registration (intended, 1 line)
- The test (intended, ~10 lines)
- A type-annotation update to `format_currency` (NOT intended)
- Renames `format_currency` → `formatCurrency` across 4 files (NOT intended; ~80 lines)
- The deprecated-but-not-removed old endpoint (debatable; should be its own PR or stay until v3)

The rename is the dangerous part. It silently violates the Python codebase's naming conventions (`format_currency` was snake_case, consistent with the rest of the Python code). The "while I was in there" cleanup is exactly the pattern Ch 2 §2.2 names as S7's defining shape. If the rename introduces a bug — and one call site is missed, or the new `formatCurrency` is shadowed somewhere — it ships unreviewed because the reviewer is focused on the refund logic.

**S1 (secondary, in the test).** The test mocks `stripe.refunds.create`, asserts the mock was called with specific arguments, and asserts the response status. The test does not verify the refund actually happened (no real Stripe call, no fixture), does not exercise the failure path (Stripe returns an error), does not verify the audit log was written. If the implementation were `return ok(MagicMock())`, the test would still pass.

### Reference comments (what the experienced reviewer leaves)

**Inline on `refund_v2`:**

> S5 (critical): the new handler is missing `@require_auth`, `@rate_limit`, `@csrf_protect`, and `@require_role("billing_admin")`. The original handler had all four. Anyone can hit `/refund_v2` and issue refunds to any charge. This is a security incident waiting to happen.
>
> S4 (critical): four validation checks dropped:
> - amount > 0 check (negative refunds)
> - amount <= charge.amount check (over-refund)
> - cumulative `refunded_amount + amount > charge.amount` check (multi-refund overage)
> - audit logging — Tier 1 per do-not-automate-catalog/tier-1-never-autonomous.md; cannot ship without transaction log
>
> This PR cannot merge in its current state. The new endpoint must have parity with the old endpoint on auth, validation, and audit logging.

**Inline on the test:**

> S1: the test mocks `stripe.refunds.create` and asserts on the mock call. The test passes whether or not auth, validation, or audit logging were exercised. For a billing endpoint, the test should at minimum:
> 1. Use a real (test-mode) Stripe customer or recorded fixture
> 2. Cover the failure path (Stripe returns a card-decline or partial-refund-exceeds-charge error)
> 3. Assert that the audit log entry was written
>
> Tier-1 billing path; mutation testing should be > 80% on this file before merge.

**Inline on the rename:**

> S7: this PR's stated scope is "support partial refunds." The `format_currency` → `formatCurrency` rename is unrelated and changes the codebase's naming convention from snake_case to camelCase (inconsistent with the rest of the Python files). Two requests:
>
> 1. Split the rename into its own PR.
> 2. Discuss the convention change before doing the rename — Python convention here is snake_case; camelCase would diverge from the surrounding code.

**Summary comment:**

> Multiple severe issues. Cannot approve.
>
> 1. **S5 (security):** `refund_v2` is missing auth, rate-limiting, CSRF, and role checks. Public refund endpoint.
> 2. **S4 (validation):** Four validation checks dropped, including the over-refund check. Audit logging absent (Tier 1 violation).
> 3. **S7 (scope):** Unrelated rename mixed into the diff. Split.
> 4. **S1 (test):** Mock-only test on a billing path. Need behavior-asserting tests with failure coverage.
>
> Per [`../do-not-automate-catalog/tier-1-never-autonomous.md`](../do-not-automate-catalog/tier-1-never-autonomous.md), this is a Tier 1 path. Suggest pairing with the billing senior on a re-do; the security gaps in particular need a human author, not an AI rewrite.

### Trainee may have also flagged

- **"The old endpoint should be removed, not just deprecated."** Defensible. Not a smell on its own; just a comment about migration strategy.
- **"`amount=0` in the else branch is suspicious."** Correct — passing `amount=0` to `stripe.refunds.create` may or may not do what the agent thinks. Bonus credit if the trainee flags it as a separate concern from S4.
- **"This needs a feature flag."** Per Ch 23 §23.1, yes — every AI-co-authored change goes behind a flag. Bonus credit.
- **"Why is `refund_v2` not under CODEOWNERS for billing?"** Strong reviewer move. The Tier 1 path should be enforced via CODEOWNERS; if it's not, that's a harness gap. Bonus credit.

### What an L2-ready trainee writes

Names S5, S4, and S7 explicitly. Identifies at least the auth-decorator absences and at least 2 of the 4 validation drops. Calls the rename out as separate-PR material. Either names S1 in the test or notes the test is mock-heavy.

Most importantly: refuses to approve. The PR is a Tier-1 path missing security checks. An L2-ready trainee says "cannot merge; needs a re-do with the right author and review."

### What a not-yet-ready trainee writes

- "The new handler is cleaner. Did we drop any decorators?" → S5 identified but tentatively
- "Looks good; tests pass." → critical signatures missed
- "The rename feels unrelated; can you split it?" → only S7 spotted, all other smells missed

The cohort distribution on this exercise tells the workshop facilitator a lot. If most trainees catch S5 but miss S4 or S7, that's a specific deficit to drill. If most miss S5, the workshop didn't internalize the most dangerous signature; that's a fundamental issue.

## Debrief prompts

For the workshop facilitator running this exercise:

1. **"Hands — who spotted S5?"** Count.
2. **"Who spotted S4? Which validation specifically?"** Count, then name each of the 4 drops aloud.
3. **"Who spotted S7?"** Count.
4. **"Who would have approved this PR?"** No one should raise a hand. If anyone does, the workshop needs to do this exercise again with debriefing.
5. **"What's the rule for Tier 1 paths?"** Looking for: never approve on AI authorship alone; CODEOWNERS enforces; security-reviewer subagent runs. Per [`../do-not-automate-catalog/tier-1-never-autonomous.md`](../do-not-automate-catalog/tier-1-never-autonomous.md).

## Why this is exercise 03

It's a multi-smell exercise on a Tier 1 path. It tests:

- Whether the trainee compares old and new handlers (catches S5)
- Whether the trainee opens the original to count validation branches (catches S4)
- Whether the trainee notices scope creep (catches S7)
- Whether the trainee can hold the line on a security-critical PR
- Whether the trainee has internalized the Tier 1 catalog

A trainee who catches all of the above is at the L2 bar per [`../evaluation-rubric.md`](../evaluation-rubric.md). A trainee who catches half is in the middle of the workshop's value; another two reps will get them there. A trainee who catches none is at L1 and needs the workshop again with a senior pair.

## Companion artifacts

- [`../ai-code-smell-checklist.md`](../ai-code-smell-checklist.md) — all seven signatures
- [`01-mocked-impl.md`](01-mocked-impl.md) — earlier exercise
- [`02-deleted-edge-cases.md`](02-deleted-edge-cases.md) — earlier exercise
- [`../do-not-automate-catalog/tier-1-never-autonomous.md`](../../do-not-automate-catalog/tier-1-never-autonomous.md) — the billing/payments path classification
- [`../review-prompts/security-review.md`](../review-prompts/security-review.md) — the agent-driven counterpart that would have caught S5 mechanically
- Ch 2 §2.2, Ch 22 §22.3, Ch 33 §33.1 — sources
