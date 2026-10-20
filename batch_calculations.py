import numpy as np


# FR-02 and FR-03 for many flights at once: each argument is a NumPy array.
def calculate_batch(fuel, fuel_flow, time_min, groundspeed, protected):
    arrival = fuel - fuel_flow * (time_min / 60)
    endurance = np.maximum(0, fuel - protected) / fuel_flow
    distance = endurance * groundspeed
    return arrival, endurance, distance
