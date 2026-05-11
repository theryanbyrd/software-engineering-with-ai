"""Tests for starter.shared."""

from __future__ import annotations

import pytest

from starter.shared import Err, Ok, err, format_usd, ok


class TestFormatUsd:
    def test_formats_whole_dollars(self) -> None:
        assert format_usd(10000) == "$100.00"

    def test_formats_with_cents(self) -> None:
        assert format_usd(12345) == "$123.45"

    def test_pads_single_digit_cents_with_leading_zero(self) -> None:
        assert format_usd(105) == "$1.05"

    def test_formats_zero(self) -> None:
        assert format_usd(0) == "$0.00"

    def test_formats_negative_with_leading_minus(self) -> None:
        assert format_usd(-12345) == "-$123.45"

    def test_rejects_float(self) -> None:
        with pytest.raises(TypeError, match="integer"):
            format_usd(99.5)  # type: ignore[arg-type]

    def test_rejects_bool(self) -> None:
        with pytest.raises(TypeError, match="integer"):
            format_usd(True)  # type: ignore[arg-type]


class TestResultHelpers:
    def test_ok_wraps_a_value(self) -> None:
        result = ok(42)
        assert isinstance(result, Ok)
        assert result.ok
        assert result.value == 42

    def test_err_wraps_an_error(self) -> None:
        result = err("boom")
        assert isinstance(result, Err)
        assert not result.ok
        assert result.error == "boom"
