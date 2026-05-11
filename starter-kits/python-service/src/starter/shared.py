"""Pure utilities and types shared across the service.

Leaf module: cannot import from `starter.api` or any framework adapter.
No I/O, no global state, no network or filesystem access.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")
E = TypeVar("E")


def format_usd(cents: int) -> str:
    """Format an integer cents value as a USD currency string.

    Args:
        cents: Amount in integer cents (e.g., 12345 for $123.45).

    Returns:
        Formatted string with two decimal places and a leading $.

    Raises:
        TypeError: if ``cents`` is not an int (bool is rejected too).
    """
    # bool is an int subclass; reject explicitly to avoid format_usd(True) silently working.
    if isinstance(cents, bool) or not isinstance(cents, int):
        raise TypeError("amount must be an integer (cents)")

    sign = "-" if cents < 0 else ""
    abs_cents = abs(cents)
    dollars = abs_cents // 100
    remainder = abs_cents % 100
    return f"{sign}${dollars}.{remainder:02d}"


@dataclass(frozen=True)
class Ok(Generic[T]):
    """Successful result. Use ``ok()`` to construct."""

    value: T
    ok: bool = True


@dataclass(frozen=True)
class Err(Generic[E]):
    """Failed result. Use ``err()`` to construct."""

    error: E
    ok: bool = False


Result = Ok[T] | Err[E]


def ok(value: T) -> Ok[T]:
    """Construct a successful Result."""
    return Ok(value=value)


def err(error: E) -> Err[E]:
    """Construct a failed Result."""
    return Err(error=error)
