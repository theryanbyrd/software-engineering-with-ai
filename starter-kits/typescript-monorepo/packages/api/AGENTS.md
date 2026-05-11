# packages/api

Example API service. Demonstrates validation at boundaries, integer-cents money handling, and the test patterns this repo uses.

## Rules for this package

- Validate all inputs at the HTTP boundary (or wherever inputs enter from outside).
- Money is integer cents only. Never floats.
- Webhook handlers must be idempotent.
- Auth checks go in `src/auth/` (CODEOWNER required).
- Billing logic goes in `src/billing/` (CODEOWNER required).

## Verification

```bash
npm test -- packages/api
```
