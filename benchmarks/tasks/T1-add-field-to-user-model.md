# T1-add-field-to-user-model

**Tier:** T1
**Estimated time for senior engineer:** 10-15 minutes
**Surfaces tested:** schema migration, API changes, tests, type system

## Adaptation guide

Swap the model name and field for ones that match your codebase. The point of the task is to test whether the agent traces a single field through the full vertical: schema → migration → ORM model → API serializer → tests → docs. The specifics matter less than the breadth.

For your codebase:
1. Pick a model that has a real migration history (so the agent must read the existing migration to match conventions).
2. Pick a field type that requires real thought (a `last_login_at` is more interesting than another `name` field — it has nullability, timezone, indexing implications).
3. Decide whether the API exposure is required (yes for full-stack benchmarks; skip for backend-only).

## Setup

- Branch checked out from baseline
- Database migrated to current head
- Test suite passing on baseline

## The task (give to the agent verbatim)

> Add a `last_login_at` timestamp field to the `User` model. The field should be nullable, indexed, and exposed in the user API response (the GET /users/:id endpoint). Update the relevant tests. The migration must be backward-compatible and reversible.

## Pass criterion

The migration applies and reverts cleanly. The new field appears in the API response. Tests pass.

## Rubric — score 1 point each (max 10)

- [ ] Forward migration adds the column with the correct type (timestamp/datetime, nullable)
- [ ] Forward migration adds an index on the column
- [ ] Backward migration is provided AND removes both the column and the index
- [ ] ORM model updated with the new field (correct type, nullable annotation)
- [ ] API serializer/response includes the new field
- [ ] At least one new test asserts the field is returned by the GET endpoint
- [ ] At least one test exercises the nullable case (returning `null` for users who haven't logged in)
- [ ] Diff is under 100 lines
- [ ] Diff touches only files related to the User model and its API/tests (no scope creep)
- [ ] Agent did not modify unrelated migration files

## Common failure modes (informational)

- **Forgets the index.** Common when the agent reads only the most recent migration, which may not have an index pattern. Penalize per rubric.
- **Backward migration drops only the column, not the index.** Some ORM migration tools handle this automatically; some don't. Score based on what's actually written.
- **Adds the field to multiple serializers.** If your codebase has admin / public / internal API serializers, the agent may add to all three when only one was asked. This is borderline scope creep; usually doesn't lose a point unless it caused new test failures.
- **Hard-codes a default like `NOW()` or `'1970-01-01'`.** The task said nullable; non-null defaults change behavior. Penalize.
