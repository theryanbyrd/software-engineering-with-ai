# Exercise 01 — The Charged Customer

**Primary smell:** S1 (tests mock the implementation).
**Difficulty:** Easy. Single-signature.
**Pacing:** 5 minutes review, 3 minutes debrief.

## Scenario

The PR description:

> **Title:** Add `charge_customer` method to PaymentService
>
> Adds a method on `PaymentService` that charges a customer's default payment method via Stripe. Includes a unit test. Per the team's CLAUDE.md, no new direct Stripe API calls outside the `payment_service` module.
>
> Tagged: `[AI-authored]`

The issue (one line):

> "Add a `charge_customer(customer, amount)` method to `PaymentService` that charges the customer's default card. Surface errors to the caller."

## The diff

```python
# payments/payment_service.py
class PaymentService:
    def __init__(self, stripe_client):
        self._stripe_client = stripe_client

    def charge_customer(self, customer, amount):
        """Charge a customer's default card."""
+       charge = self._stripe_client.charges.create(
+           customer=customer.stripe_id,
+           amount=amount,
+           currency="usd",
+       )
+       return charge
```

```python
# tests/test_payment_service.py
+ from unittest.mock import MagicMock
+ from payments.payment_service import PaymentService
+
+ def test_charge_customer_charges_default_card():
+     stripe_client = MagicMock()
+     stripe_client.charges.create.return_value = {"id": "ch_1", "status": "succeeded"}
+     service = PaymentService(stripe_client=stripe_client)
+
+     customer = MagicMock()
+     customer.stripe_id = "cus_1"
+
+     service.charge_customer(customer, amount=100)
+
+     stripe_client.charges.create.assert_called_once_with(
+         customer="cus_1",
+         amount=100,
+         currency="usd",
+     )
```

## Trainee task

Review this diff. Write the comments you would leave on the PR. Do not read the instructor key until you have written your comments.

Suggested time: 5 minutes.

---

## Instructor key

### Planted smells

**S1 (primary, blatant).** The test `test_charge_customer_charges_default_card` mocks the Stripe client, mocks the customer, calls the function under test, and asserts that the mock was called with specific arguments. Per the catch heuristic in [`../ai-code-smell-checklist.md`](../ai-code-smell-checklist.md):

> Does this test fail if the implementation is wrong?

If `charge_customer` were:

```python
def charge_customer(self, customer, amount):
    self._stripe_client.charges.create(customer=customer.stripe_id, amount=amount, currency="usd")
    # forgot to return; no actual charge sent for any failed retry
```

— the test would still pass (the mock doesn't care about the return value, and `assert_called_once_with` only checks the call arguments). If the implementation were:

```python
def charge_customer(self, customer, amount):
    self._stripe_client.charges.create(customer=customer.stripe_id, amount=amount, currency="usd")
    raise StripeError("simulated")
```

— the test would still pass. The test verifies nothing about the system's observable behavior.

### Reference comments (what the experienced reviewer leaves)

**Inline on the test:**

> S1: this test mocks `stripe_client.charges.create` and then asserts on the mock's call arguments. The test passes whether or not the function actually returns the charge or handles errors. Specifically: if the function body were `pass`, this test would still pass. Suggest replacing with a test that asserts on `result.id` and `result.status`, against either a real Stripe test-mode customer or a recorded VCR fixture.

**Inline on the implementation:**

> The issue says "surface errors to the caller." The current implementation passes errors through naturally, which is correct — but there are no tests for the failure path. Add at least one test for the case where Stripe returns a card-decline error, asserting that the caller sees the error.

**Summary comment:**

> S1 in the unit test. The test verifies the implementation, not the behavior. Replace with a behavior-asserting test before merge. Also missing: error-path coverage. Happy to pair on either.

### Trainee may have also flagged

- **"This should be in a try/except."** Trainee may flag the lack of error handling. The PR description says "surface errors to the caller," which is what happens by default in Python — the exception propagates up. This is *not* S3 (silent error swallowing); it's the opposite, and it's correct. Small precision penalty if the trainee flagged this as a smell.
- **"This should be async."** Trainee may have stylistic preferences. Not a smell. Don't penalize, but also don't credit.
- **"`amount` should be a `Decimal`, not an `int`."** Real concern but not one of the seven signatures. Credit as a bonus finding, but the smell-spotting score doesn't include it.

### What an L2-ready trainee writes

The trainee names S1 explicitly, points to the specific lines, articulates the diagnostic question ("would this test fail if the implementation were `pass`?"), and proposes the fix (behavior-asserting test against test-mode Stripe or a VCR fixture). Bonus points for also noting the missing error-path coverage.

### What a not-yet-ready trainee writes

- Vague: "This test feels weak."
- Missed: trainee approves the PR with a +1.
- Mis-flagged: trainee flags the missing try/except, missing the actual S1.

Per [`../evaluation-rubric.md`](../evaluation-rubric.md), the L2-ready response scores 4 on S1; the vague version scores 1-2; the missed version scores 0.

## Debrief prompts

For the workshop facilitator running this exercise:

1. **"Who spotted S1?"** Hands.
2. **"What's the diagnostic question that makes S1 obvious?"** Looking for: "would this test fail if the implementation were wrong?"
3. **"What would a behavior-asserting test look like for this function?"** Looking for: a test that constructs a real customer (or test-mode), calls the function, and asserts on observable state — the returned charge, the customer's balance, a side effect on the ledger.
4. **"What did anyone flag that wasn't S1?"** Surface the precision side — distinguish real smells from style preferences.

## Why this is exercise 01

It's the most common AI-slop signature (per Ch 7 §7.5 — "the #1 AI slop signature"). It's the one engineers learn to spot first, and the one that builds confidence for the harder exercises. If a trainee can't spot this one cold, they're not ready for the multi-smell exercises.

## Companion artifacts

- [`../ai-code-smell-checklist.md`](../ai-code-smell-checklist.md#s1) — the deep reference for S1
- [`02-deleted-edge-cases.md`](02-deleted-edge-cases.md) — the next exercise
- [`../evaluation-rubric.md`](../evaluation-rubric.md) — how this would be scored on the calibration set
- Ch 2 §2.2 — source
