import numpy as np


# FR-02 and FR-03 for many flights at once: each argument is a NumPy array.
def calculate_batch(fuel, fuel_flow, distance, groundspeed, protected):
    flight_time = distance / groundspeed
    arrival = fuel - fuel_flow * flight_time
    endurance = np.maximum(0, fuel - protected) / fuel_flow
    available_range = endurance * groundspeed
    return flight_time, arrival, endurance, available_range
