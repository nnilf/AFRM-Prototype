import numpy as np


# FR-02 and FR-03 for many flights at once: each argument is a NumPy array.
def calculate_batch(fuel, fuel_flow, distance, groundspeed, protected):
    flight_time = distance / groundspeed
    arrival = fuel - fuel_flow * flight_time
    endurance = np.maximum(0, fuel - protected) / fuel_flow
    available_range = endurance * groundspeed
    return flight_time, arrival, endurance, available_range


# FR-06 for many routes at once: one row per flight and one column per segment.
def calculate_route_batch(fuel, distances, groundspeeds, fuel_flows):
    burn = (fuel_flows * (distances / groundspeeds)).sum(axis=1)
    return fuel - burn
