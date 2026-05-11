---
name: write-tests
description: Use when writing tests for new or existing code. Follows test-first prompt pattern. Targets behavior, not implementation. Avoids mocks-of-everything anti-pattern.
allowed_tools: Read, Edit, Write, Bash
---

# Write Tests

You are writing tests. The goal is to catch a class of regression, not to hit a coverage number.

## Process

1. **Read the code under test.** Understand inputs, outputs, side effects.
2. **Identify behaviors, not branches.** A test should describe a behavior the user / caller cares about. "Returns the user when found" not "if-statement on line 42."
3. **Write the test name as a sentence.** `should return null when the user is not found` over `test_user_not_found`.
4. **Use real implementations where possible.** Mock at boundaries only (network, filesystem, time, randomness). Do not mock the code you're testing.
5. **Assert on outputs and observable side effects.** Not on internal calls.
6. **Run the test.** Confirm it actually fails when the code is broken (mutation test it manually if unsure).

## Vitest patterns for this repo

```typescript
import { describe, it, expect } from "vitest";
import { createOrder } from "../src/orders.js";

describe("createOrder", () => {
  it("returns the order id when the input is valid", () => {
    const result = createOrder({ amount: 100, customerId: "c_1" });
    expect(result.id).toBeDefined();
  });

  it("throws when the amount is negative", () => {
    expect(() => createOrder({ amount: -1, customerId: "c_1" }))
      .toThrow(/amount must be non-negative/);
  });
});
```

## What this skill does NOT do

- Write tests that mock the code under test.
- Write tests that assert on private internals.
- Add `.skip()` to existing tests.
- Reduce coverage thresholds to make CI pass.
