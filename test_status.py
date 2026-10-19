from status import fuel_status


def test_fr04_just_below_1_00_is_critical():
    assert fuel_status(999, 1000) == "CRITICAL"  # ratio 0.999


def test_fr04_exactly_1_00_is_caution():
    assert fuel_status(1000, 1000) == "CAUTION"  # ratio 1.00


def test_fr04_just_below_1_25_is_caution():
    assert fuel_status(1249, 1000) == "CAUTION"  # ratio 1.249


def test_fr04_exactly_1_25_is_normal():
    assert fuel_status(1250, 1000) == "NORMAL"  # ratio 1.25


def test_fr04_negative_arrival_fuel_is_critical():
    assert fuel_status(-500, 1000) == "CRITICAL"  # flight cannot reach destination
