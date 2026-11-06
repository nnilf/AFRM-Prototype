import random

import numpy as np
from hypothesis import given

from batch_calculations import calculate_batch
from calculations import endurance_hours, flight_time_hours, fuel_at_arrival, range_km
from generate_flights import make_flight
from test_properties import (
    distance_values,
    fuel_flow_values,
    fuel_values,
    groundspeed_values,
    protected_values,
)


def test_fr02_fr03_numpy_matches_plain_python():
    # Each row is: fuel, fuel_flow, distance, groundspeed, protected
    rows = [
        [6000, 2400, 1200, 800, 1875],  # the known-answer example
        [1500, 2400, 1200, 800, 1875],  # fuel below protected fuel
    ]
    random.seed(42)
    for number in range(1, 51):
        rows.append(make_flight(number)[2:])  # [2:] skips the flight id and aircraft name

    fuel, fuel_flow, distance, groundspeed, protected = np.array(rows, dtype=float).T
    flight_time, arrival, endurance, available_range = calculate_batch(
        fuel, fuel_flow, distance, groundspeed, protected)

    for i in range(len(rows)):
        assert flight_time[i] == flight_time_hours(distance[i], groundspeed[i])
        assert arrival[i] == fuel_at_arrival(fuel[i], fuel_flow[i], flight_time[i])
        assert endurance[i] == endurance_hours(fuel[i], protected[i], fuel_flow[i])
        assert available_range[i] == range_km(endurance[i], groundspeed[i])


def test_fr02_fr03_numpy_matches_hand_values():
    # Each row is: fuel, fuel_flow, distance, groundspeed, protected
    rows = [
        [6000, 2400, 1200, 800, 1875],
        [1500, 2400, 1200, 800, 1875],
        [5000, 2000, 1000, 500, 1000],
    ]
    # Each row is: time h, arrival kg, endurance h, range km
    expected = [
        [1.5, 2400, 1.71875, 1375],  # 6000 - 3600, then 4125 / 2400 and x 800
        [1.5, -2100, 0, 0],  # 1500 - 3600, and fuel is below protected fuel
        [2, 1000, 2, 1000],  # 5000 - 4000, then 4000 / 2000 and x 500
    ]

    fuel, fuel_flow, distance, groundspeed, protected = np.array(rows, dtype=float).T
    flight_time, arrival, endurance, available_range = calculate_batch(
        fuel, fuel_flow, distance, groundspeed, protected)

    for i in range(len(rows)):
        assert [flight_time[i], arrival[i], endurance[i], available_range[i]] == expected[i]


@given(fuel_values, fuel_flow_values, distance_values, groundspeed_values, protected_values)
def test_fr02_fr03_numpy_matches_python_for_any_flight(fuel, fuel_flow, distance, groundspeed, protected):
    flight_time, arrival, endurance, available_range = calculate_batch(
        np.array([fuel]), np.array([fuel_flow]), np.array([distance]),
        np.array([groundspeed]), np.array([protected]))

    python_time = flight_time_hours(distance, groundspeed)
    python_endurance = endurance_hours(fuel, protected, fuel_flow)

    assert abs(flight_time[0] - python_time) < 0.000001
    assert abs(arrival[0] - fuel_at_arrival(fuel, fuel_flow, python_time)) < 0.000001
    assert abs(endurance[0] - python_endurance) < 0.000001
    assert abs(available_range[0] - range_km(python_endurance, groundspeed)) < 0.000001
