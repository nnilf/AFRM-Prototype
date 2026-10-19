from calculations import fuel_at_arrival, endurance_hours, range_nm


def test_fr02_fuel_at_arrival():
    # 6000 - 2400 x (90 / 60) = 2400
    assert fuel_at_arrival(6000, 2400, 90) == 2400


def test_fr03_endurance_and_range():
    # (6000 - 1875) / 2400 = 1.71875 h, then x 450 kt = 773.44 NM
    endurance = endurance_hours(6000, 1875, 2400)
    assert endurance == 1.71875
    assert round(range_nm(endurance, 450), 2) == 773.44


def test_fr03_no_usable_fuel_below_protected():
    assert endurance_hours(1500, 1875, 2400) == 0
