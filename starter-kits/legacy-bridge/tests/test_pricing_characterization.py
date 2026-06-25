from legacy_sample import legacy_price


def test_basic_total():
    assert legacy_price(100, 3) == 300


def test_bulk_discount_at_ten():
    # Pins the 10% bulk discount that kicks in at qty>=10.
    assert legacy_price(100, 10) == 900


def test_coupon_can_drive_total_negative():
    # Characterizes a known wart: SAVE5 is unconditional and can go negative.
    assert legacy_price(100, 1, "save5") == -400
