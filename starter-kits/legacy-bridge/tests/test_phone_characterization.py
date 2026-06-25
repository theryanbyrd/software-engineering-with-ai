import pytest
from legacy_sample import normalize_phone


@pytest.mark.parametrize("raw,out", [
    ("(415) 555-1234", "4155551234"),
    ("1-415-555-1234", "4155551234"),
    ("415.555.1234", "4155551234"),
])
def test_normalizes_to_ten_digits(raw, out):
    assert normalize_phone(raw) == out
