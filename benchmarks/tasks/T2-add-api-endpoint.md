# T2-add-api-endpoint

**Tier:** T2
**Estimated time for senior engineer:** 60-90 minutes
**Surfaces tested:** convention-matching, input validation, idempotency, tests, OpenAPI

## Adaptation guide

This task should map to your stack. If you use FastAPI, write the rubric in FastAPI terms. If Express, Express. If Rails, Rails.

Pick a use case that requires real validation: a write endpoint with multiple required and optional fields, idempotency considerations, and tie-ins to existing services.

## Setup

- A read endpoint exists for the resource (`GET /orders/:id/refunds`)
- The team has documented API conventions (OpenAPI, error format, pagination, idempotency)
- An adjacent endpoint exists in the same module to provide a pattern reference

## The task (give to the agent verbatim)

> Add a new endpoint `POST /orders/:id/refunds` that creates a refund for the given order. Required fields in the request body: `amount` (positive integer in cents), `reason` (one of: "duplicate", "fraudulent", "requested_by_customer", "other"). Optional: `notes` (free text, max 500 chars). The endpoint must be idempotent — repeated requests with the same `Idempotency-Key` header should return the same response without creating duplicate refunds. Return 201 on creation, 422 on validation error, 409 if the order doesn't exist or is in a non-refundable state.

## Pass criterion

The endpoint exists, validates inputs, is idempotent, returns the right status codes, and has tests covering happy path plus key error paths. Diff under 250 lines.

## Rubric — score 1 point each (max 14)

- [ ] Agent's first action was to read the existing GET endpoint AND at least one other POST endpoint in the codebase
- [ ] Routing matches the existing pattern (router, decorator, controller, etc.)
- [ ] Input validation uses the team's validation library (Pydantic, Zod, dry-validation, etc.) — not hand-rolled
- [ ] All required fields are validated
- [ ] All optional field constraints are validated (notes max 500 chars)
- [ ] Idempotency-Key handling is implemented (storage + lookup, not just acknowledged)
- [ ] Returns 201 on success
- [ ] Returns 422 with field-level error detail on validation failure
- [ ] Returns 409 on order-state failure
- [ ] Tests cover the happy path
- [ ] Tests cover at least 2 validation failure cases
- [ ] Tests cover the idempotency case (same key, same response, no duplicate refund)
- [ ] Tests cover the auth/permission case if the codebase has authentication
- [ ] OpenAPI/typespec documentation updated if the codebase auto-generates it

## Common failure modes (informational)

- **Skips idempotency.** Most common miss. Idempotency is a discipline that requires looking up the existing response, not just generating a new one.
- **Hand-rolls validation.** Strong AI signal. Real teams use the validation library; agent that hand-rolls is mismatching conventions.
- **Returns 400 instead of 422 for validation failures.** Common in codebases with mixed conventions; check what the codebase actually does.
- **Tests use trivial inputs.** Happy path with `{amount: 100, reason: "duplicate"}` is fine; if every test uses the same input, the test surface is too narrow.
- **Adds a new database table for refunds.** May be correct or may be scope creep; check whether the team's convention is to extend the `orders` table or create a separate `refunds` table.
