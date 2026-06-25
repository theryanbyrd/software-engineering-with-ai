"""Characterizes a strangler seam: the new code path must match legacy output
exactly before legacy is removed. See .claude/skills/strangler-pattern/SKILL.md.
"""
from legacy_sample import legacy_price


def new_price(cents: int, qty: int, coupon: str = "") -> int:
    """Candidate replacement — must be behavior-identical at the seam for now."""
    total = cents * qty
    if qty >= 10:
        total = int(total * 0.9)
    if coupon.upper() == "SAVE5":
        total -= 500
    return total


def test_seam_parity_across_inputs():
    cases = [(100, 1, ""), (100, 10, ""), (250, 12, "SAVE5"), (99, 3, "save5")]
    for cents, qty, coupon in cases:
        assert new_price(cents, qty, coupon) == legacy_price(cents, qty, coupon)
