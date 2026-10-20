# Times plain Python against NumPy on 1,000 and 100,000 made-up flights.
# Each timing is repeated 5 times and saved to benchmark_results.csv.
import csv
import random
import time
from pathlib import Path

import numpy as np

from batch_calculations import calculate_batch
from calculations import fuel_at_arrival, endurance_hours, range_nm
from generate_flights import make_flight

REPEATS = 5


def run_python(rows):
    for fuel, fuel_flow, time_min, groundspeed, protected in rows:
        fuel_at_arrival(fuel, fuel_flow, time_min)
        range_nm(endurance_hours(fuel, protected, fuel_flow), groundspeed)


def run_numpy(columns):
    fuel, fuel_flow, time_min, groundspeed, protected = columns
    calculate_batch(fuel, fuel_flow, time_min, groundspeed, protected)


def seconds_taken(function, data):
    start = time.perf_counter()
    function(data)
    return time.perf_counter() - start


random.seed(42)
results = []
for count in [1000, 100000]:
    rows = [make_flight(number)[2:] for number in range(1, count + 1)]
    columns = np.array(rows, dtype=float).T  # one array per input, e.g. all the fuel values
    for repeat in range(1, REPEATS + 1):
        results.append([count, "python", repeat, seconds_taken(run_python, rows)])
        results.append([count, "numpy", repeat, seconds_taken(run_numpy, columns)])

with open(Path(__file__).parent / "benchmark_results.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["flights", "method", "repeat", "seconds"])
    for count, method, repeat, seconds in results:
        writer.writerow([count, method, repeat, f"{seconds:.6f}"])
        print(f"{count:>7} flights  {method:<7} repeat {repeat}  {seconds:.6f} s")
