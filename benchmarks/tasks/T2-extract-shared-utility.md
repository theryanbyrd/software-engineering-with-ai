# T2-extract-shared-utility

**Tier:** T2
**Estimated time for senior engineer:** 45-75 minutes
**Surfaces tested:** refactor discipline, test preservation, scope discipline, dependency reasoning

## Adaptation guide

Set up the fixture: identify a utility function that is duplicated (with minor variations) across 3-5 files in your codebase. The variations should be small enough that ONE shared utility can replace all callers, but real enough that the agent has to make decisions about parameterization.

## Setup

- 3-5 files contain near-duplicate implementations of `format_currency_with_symbol(amount, currency_code)` (or your equivalent)
- The variations differ slightly: some round to nearest cent, some use locale-specific formatting, one has a bug
- Existing tests call into each duplicate independently

## The task (give to the agent verbatim)

> The function `format_currency_with_symbol` (or close variants) is duplicated across `app/billing/invoice.py`, `app/billing/refund.py`, `app/orders/receipt.py`, and `app/admin/report.py`. Extract a single shared implementation into the `app/shared/formatting.py` module. Update all four call sites to use the shared utility. Preserve the behavior of each existing call site exactly — if a call site has a bug or quirk, document it but do NOT fix it as part of this refactor. Add tests for the shared utility.

## Pass criterion

All four call sites use the shared utility. Behavior at each call site is preserved exactly. The shared utility has tests. Diff under 300 lines. No mixing of refactor with bug fixes.

## Rubric — score 1 point each (max 12)

- [ ] Agent's first action was to read all four duplicate implementations to identify the differences
- [ ] Shared utility's signature accommodates the variations through parameters (not by inlining variant-specific logic)
- [ ] Each call site updated to use shared utility with the correct parameters to preserve behavior
- [ ] Existing tests still pass (no behavior change to any caller)
- [ ] Bug or quirk in one of the variants is documented (e.g., as a TODO with reasoning) but NOT fixed
- [ ] No "while you're in there" improvements introduced (e.g., changing unrelated code in the touched files)
- [ ] New tests for the shared utility cover all variant behaviors
- [ ] New tests include the buggy/quirky case from the existing duplicate
- [ ] Diff stays under 300 lines
- [ ] Touched files are limited to the four call sites + the new shared module + its tests
- [ ] Agent ran the test suite to verify no regressions
- [ ] Documentation comment on the shared utility explains the parameterization

## Common failure modes (informational)

- **Mixes the refactor with a bug fix.** The most common mistake. The instruction is explicit; penalize.
- **Designs an over-parameterized utility.** Adds 6 boolean flags to handle every variant. Should rather pick a clean abstraction even if one call site has to do small adaptation work.
- **Misses one call site.** Often happens if the agent stops at the first 3 found by grep without doing a comprehensive search.
- **"Improves" the formatting library while at it.** E.g., switches from `format()` to f-strings in adjacent code. Scope creep.
