---
name: add-api-endpoint
description: Use when the user asks for a new HTTP endpoint, route, or API method. Scaffolds the endpoint following existing conventions, validates inputs at the boundary, returns errors as Result types or HTTP error responses (matching codebase style), and writes tests for happy path plus key error paths.
allowed_tools: Read, Edit, Write, Bash, Grep
---

# Add API endpoint

## When to use this skill

The user requests a new endpoint. Examples: "add a POST /orders endpoint," "create a route for fetching user preferences," "add a GraphQL query for X."

## Procedure

1. **Read existing endpoints in the same module.** Match conventions: routing, validation, error format, response shape, naming.
2. **Read the relevant ADR or architecture doc** (if it exists) for API conventions: pagination, versioning, auth requirements, idempotency, rate limits.
3. **State the plan to the user.** Files to create or edit, response shape, validation rules, error cases. Wait for approval.
4. **Implement:**
   - Validate inputs at the boundary (use the team's validation library: Pydantic, Zod, etc.)
   - Reuse existing error types/middleware
   - Match the existing handler pattern (Express middleware, FastAPI route, Rails controller, etc.)
   - Add OpenAPI/typespec docs if the codebase uses them
5. **Write tests:**
   - Happy path with realistic request body
   - At least 2 validation-failure cases
   - Auth/permission case if the endpoint requires authentication
   - Idempotency case if the endpoint is a write that should be idempotent
6. **Run `verify`.** Must pass.
7. **Update relevant documentation.** README mentions the endpoint, OpenAPI spec is regenerated, etc.

## Output

The diff with:
- The new handler
- Tests
- Documentation updates
- A summary listing the conventions matched and any deviations (with explanation)

## Forbidden

- Do not invent a new convention if one exists. Match what's there.
- Do not add the endpoint without input validation. Boundary validation is mandatory.
- Do not skip tests because "the endpoint is simple."
- Do not modify auth or billing endpoints without explicit approval (these are restricted paths).
- Do not invent response shapes. Match the existing shape used by similar endpoints.

## References

- Chapter 6 — repo legibility (find existing patterns first)
- Chapter 13 §13.x — skill conventions
- The codebase's `docs/api-conventions.md` (if it exists; if it doesn't, ASK whether to create one)
