---
name: write-tests
description: Use when writing tests for new or existing code. Follows test-first prompt pattern. Targets behavior, not implementation. Avoids mocks-of-everything anti-pattern.
allowed_tools: Read, Edit, Write, Bash
---

# Write Tests

You are writing tests. The goal is to catch a class of regression, not to hit a coverage number.

## Process

1. **Read the code under test.** Understand inputs, outputs, side effects.
2. **Identify behaviors, not branches.** A test should describe a behavior the user / caller cares about. "returns the user when found" not "if-statement on line 42."
3. **Write the test name as a sentence.** `test_returns_none_when_user_not_found` over `test_user_not_found`.
4. **Use real implementations where possible.** Mock at boundaries only (network, filesystem, time, randomness). Do not mock the code you're testing.
5. **Assert on outputs and observable side effects.** Not on internal calls.
6. **Run the test.** Confirm it actually fails when the code is broken.

## pytest patterns for this repo

```python
import pytest
from starter.api.orders import create_order

class TestCreateOrder:
    def test_returns_order_when_input_is_valid(self) -> None:
        result = create_order(amount_cents=100, customer_id="c_1")
        assert result.ok
        assert result.value.amount_cents == 100

    def test_rejects_negative_amount(self) -> None:
        result = create_order(amount_cents=-1, customer_id="c_1")
        assert not result.ok
        assert "non-negative" in result.error

    @pytest.mark.parametrize("bad_id", ["", "   ", None])
    def test_rejects_invalid_customer_id(self, bad_id: str | None) -> None:
        result = create_order(amount_cents=100, customer_id=bad_id)
        assert not result.ok
```

## FastAPI testing

```python
from fastapi.testclient import TestClient
from starter.api.main import app

def test_orders_endpoint_creates_order() -> None:
    client = TestClient(app)
    response = client.post("/orders", json={"amount_cents": 100, "customer_id": "c_1"})
    assert response.status_code == 201
    assert response.json()["amount_cents"] == 100
```

## What this skill does NOT do

- Write tests that mock the code under test.
- Write tests that assert on private internals.
- Add `@pytest.mark.skip` to existing tests.
- Reduce coverage thresholds to make CI pass.
