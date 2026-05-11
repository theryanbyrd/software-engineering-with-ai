"""Orders handler. Demonstrates Pydantic boundary validation, Result types,
and integer-cents money handling.
"""

from __future__ import annotations

import time
from itertools import count
from typing import Annotated

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from starter.shared import Err, Ok, Result, err, format_usd, ok

router = APIRouter(prefix="/orders", tags=["orders"])

_counter = count(1)


class CreateOrderInput(BaseModel):
    """Input schema for creating an order. Validation at the boundary."""

    amount_cents: Annotated[int, Field(ge=0, description="Amount in integer cents")]
    customer_id: Annotated[str, Field(min_length=1, description="Customer identifier")]


class Order(BaseModel):
    """Public order shape returned to clients."""

    id: str
    amount_cents: int
    customer_id: str
    formatted_amount: str
    created_at: float


def create_order(amount_cents: int, customer_id: str) -> Result[Order, str]:
    """Create an order with explicit validation. Returns a Result.

    Returns Err for expected validation failures (negative amount, blank customer
    id). Raises only for unexpected programmer errors.
    """
    if not isinstance(amount_cents, int) or isinstance(amount_cents, bool):
        return err("amount_cents must be an integer (cents)")
    if amount_cents < 0:
        return err("amount_cents must be non-negative")
    if not customer_id or not customer_id.strip():
        return err("customer_id is required")

    order = Order(
        id=f"ord_{int(time.time())}_{next(_counter)}",
        amount_cents=amount_cents,
        customer_id=customer_id,
        formatted_amount=format_usd(amount_cents),
        created_at=time.time(),
    )
    return ok(order)


@router.post("", response_model=Order, status_code=201)
async def post_order(payload: CreateOrderInput) -> Order:
    """HTTP boundary for order creation."""
    result = create_order(payload.amount_cents, payload.customer_id)
    if isinstance(result, Err):
        raise HTTPException(status_code=400, detail=result.error)
    # mypy: result is Ok[Order] here
    assert isinstance(result, Ok)
    return result.value
