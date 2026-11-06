# Planned challenge: one route with two different legs, chosen on purpose.
# AFRM takes one speed and fuel flow per flight, so this shows a model limit, not a bug.
# Leg 1: 400 km at 800 km/h and 2400 kg/h. Leg 2: 600 km at 600 km/h and 3000 kg/h.
from calculations import flight_time_hours, fuel_at_arrival
from status import fuel_status

FUEL = 6000
PROTECTED = 1500


def test_challenge_leg_by_leg_matches_hand_value():
    # Leg 1: 0.5 h x 2400 = 1200 kg, leg 2: 1 h x 3000 = 3000 kg, so 6000 - 4200 = 1800
    after_leg_1 = fuel_at_arrival(FUEL, 2400, flight_time_hours(400, 800))
    arrival = fuel_at_arrival(after_leg_1, 3000, flight_time_hours(600, 600))
    assert arrival == 1800
    assert fuel_status(arrival, PROTECTED) == "CAUTION"  # ratio 1.2


def test_challenge_simple_average_changes_status():
    # Averages are 700 km/h and 2700 kg/h over 1000 km, which hides 343 kg of burn
    arrival = fuel_at_arrival(FUEL, 2700, flight_time_hours(1000, 700))
    assert round(arrival, 2) == 2142.86
    assert fuel_status(arrival, PROTECTED) == "NORMAL"  # ratio 1.43


def test_challenge_weighted_average_matches_hand_value():
    # Total time 1.5 h and burn 4200 kg give 1000 / 1.5 km/h and 2800 kg/h
    arrival = fuel_at_arrival(FUEL, 2800, flight_time_hours(1000, 1000 / 1.5))
    assert round(arrival, 2) == 1800
    assert fuel_status(arrival, PROTECTED) == "CAUTION"
