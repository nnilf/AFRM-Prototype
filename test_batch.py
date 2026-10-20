import random

import numpy as np

from batch_calculations import calculate_batch
from calculations import fuel_at_arrival, endurance_hours, range_nm
from generate_flights import make_flight


def test_fr02_fr03_numpy_matches_plain_python():
    # Each row is: fuel, fuel_flow, time_min, groundspeed, protected
    rows = [
        [6000, 2400, 90, 450, 1875],  # the known-answer example
        [1500, 2400, 90, 450, 1875],  # fuel below protected fuel
    ]
    random.seed(42)
    for number in range(1, 51):
        rows.append(make_flight(number)[2:])  # [2:] skips the flight id and aircraft name

    fuel, fuel_flow, time_min, groundspeed, protected = np.array(rows, dtype=float).T
    arrival, endurance, distance = calculate_batch(fuel, fuel_flow, time_min, groundspeed, protected)

    for i in range(len(rows)):
        assert arrival[i] == fuel_at_arrival(fuel[i], fuel_flow[i], time_min[i])
        assert endurance[i] == endurance_hours(fuel[i], protected[i], fuel_flow[i])
        assert distance[i] == range_nm(endurance[i], groundspeed[i])
