import pytest
from legacy_sample import legacy_grade


@pytest.mark.parametrize("score,grade", [(95, "A"), (85, "B"), (75, "C"), (60, "F")])
def test_grade_bands(score, grade):
    assert legacy_grade(score) == grade


def test_no_d_grade_is_preserved():
    # Historical quirk: 65 returns F, not D. Pinned on purpose.
    assert legacy_grade(65) == "F"
