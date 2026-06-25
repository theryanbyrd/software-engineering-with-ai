"""Golden-master style test: snapshot current outputs across many inputs so a
refactor that changes ANY of them fails loudly. See scripts/golden-master-record.sh.
"""
from legacy_sample import legacy_price, legacy_grade


def test_pricing_grid_snapshot():
    grid = {(c, q): legacy_price(c, q) for c in (50, 100) for q in (1, 9, 10)}
    assert grid == {
        (50, 1): 50, (50, 9): 450, (50, 10): 450,
        (100, 1): 100, (100, 9): 900, (100, 10): 900,
    }


def test_grade_curve_snapshot():
    assert [legacy_grade(s) for s in range(0, 101, 20)] == ["F", "F", "F", "F", "B", "A"]
