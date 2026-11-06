# Times plain Python against NumPy on 1,000 and 100,000 made-up flights.
# Each timing is repeated 5 times and saved to benchmark_results.csv.
# It then prints the median and standard deviation and checks the target.
import csv
import random
import statistics
import time
from pathlib import Path

import numpy as np

from batch_calculations import calculate_batch
from calculations import endurance_hours, flight_time_hours, fuel_at_arrival, range_km
from generate_flights import make_flight

REPEATS = 5
TARGET_SECONDS = 0.010


def run_python(rows):
    for fuel, fuel_flow, distance, groundspeed, protected in rows:
        fuel_at_arrival(fuel, fuel_flow, flight_time_hours(distance, groundspeed))
        range_km(endurance_hours(fuel, protected, fuel_flow), groundspeed)


def run_numpy(columns):
    fuel, fuel_flow, distance, groundspeed, protected = columns
    calculate_batch(fuel, fuel_flow, distance, groundspeed, protected)


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

print()
for count in [1000, 100000]:
    for method in ["python", "numpy"]:
        times = [row[3] for row in results if row[0] == count and row[1] == method]
        median = statistics.median(times)
        print(f"{count:>7} flights  {method:<7} median {median:.6f} s  "
              f"st dev {statistics.stdev(times):.6f} s")
        if count == 100000 and method == "numpy":
            outcome = "PASS" if median < TARGET_SECONDS else "FAIL"
            print(f"Target median under 10 ms: {outcome}")
