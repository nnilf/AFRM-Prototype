import random

import numpy as np

from batch_calculations import calculate_batch
from calculations import endurance_hours, flight_time_hours, fuel_at_arrival, range_km
from generate_flights import make_flight


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
