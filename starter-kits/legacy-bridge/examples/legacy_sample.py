"""A tiny stand-in for the kind of untested legacy code this kit wraps.

These are intentionally gnarly pure functions: the point of the
characterization tests in ../tests is to PIN current behavior (warts and all)
before any refactor, per the characterize-then-refactor skill. Replace this
with imports from your real legacy module.
"""


def legacy_price(cents: int, qty: int, coupon: str = "") -> int:
    """Original pricing logic. Quirks preserved deliberately."""
    total = cents * qty
    if qty >= 10:
        total = int(total * 0.9)          # bulk discount
    if coupon.upper() == "SAVE5":
        total -= 500                       # flat $5 off, can go negative (!)
    return total


def legacy_grade(score: int) -> str:
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    return "F"                              # note: no D, by historical accident


def normalize_phone(raw: str) -> str:
    digits = "".join(c for c in raw if c.isdigit())
    if len(digits) == 11 and digits[0] == "1":
        digits = digits[1:]
    return digits
