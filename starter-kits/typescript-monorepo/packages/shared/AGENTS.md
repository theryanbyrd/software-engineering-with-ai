# packages/shared

Shared library — utilities and types used across packages.

## Rules for this package

- This is a **leaf** package. It cannot import from `@starter/api` or any other service-specific package.
- All exports go through `src/index.ts`. Internal modules are not re-exported.
- Functions here should be pure or near-pure (no I/O, no global state).
- Public functions must have JSDoc explaining purpose and edge cases.

## Verification

```bash
npm test -- packages/shared
```
