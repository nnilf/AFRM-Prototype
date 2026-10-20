from calculations import (
    endurance_hours,
    flight_time_hours,
    fuel_at_arrival,
    range_km,
    reserve_margin,
)


def test_fr02_flight_time():
    # 1200 km / 800 km/h = 1.5 h
    assert flight_time_hours(1200, 800) == 1.5


def test_fr02_fuel_at_arrival():
    # 6000 - 2400 x 1.5 = 2400
    assert fuel_at_arrival(6000, 2400, 1.5) == 2400


def test_fr03_endurance_and_range():
    # (6000 - 1875) / 2400 = 1.71875 h, then x 800 km/h = 1375 km
    endurance = endurance_hours(6000, 1875, 2400)
    assert endurance == 1.71875
    assert range_km(endurance, 800) == 1375


def test_fr03_no_usable_fuel_below_protected():
    assert endurance_hours(1500, 1875, 2400) == 0


def test_fr04_reserve_margin():
    # 2400 - 1875 = 525
    assert reserve_margin(2400, 1875) == 525
