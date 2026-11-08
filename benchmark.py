# Times plain Python against NumPy on 1,000 and 100,000 made-up flights,
# then on 100,000 routes of 1, 3 and 5 segments.
# Each timing is repeated 5 times and saved to benchmark_results.csv.
# It then prints the median and standard deviation and checks the targets.
import csv
import random
import statistics
import time
from pathlib import Path

import numpy as np

from batch_calculations import calculate_batch, calculate_route_batch
from calculations import (
    endurance_hours,
    flight_time_hours,
    fuel_at_arrival,
    range_km,
    route_time_and_burn,
)
from generate_flights import make_flight

REPEATS = 5
TARGET_SECONDS = 0.010
SEGMENT_COUNTS = [1, 3, 5]


def run_python(rows):
    for fuel, fuel_flow, distance, groundspeed, protected in rows:
        fuel_at_arrival(fuel, fuel_flow, flight_time_hours(distance, groundspeed))
        range_km(endurance_hours(fuel, protected, fuel_flow), groundspeed)


def run_numpy(columns):
    fuel, fuel_flow, distance, groundspeed, protected = columns
    calculate_batch(fuel, fuel_flow, distance, groundspeed, protected)


def run_python_routes(data):
    fuel, routes = data
    for flight_fuel, segments in zip(fuel, routes):
        flight_fuel - route_time_and_burn(segments)[1]


def run_numpy_routes(arrays):
    calculate_route_batch(*arrays)


# Random segments: only the timing matters here, not the distances adding up
def make_route(segment_count):
    return [(random.uniform(50, 500), random.uniform(400, 900), random.uniform(500, 7000))
            for _ in range(segment_count)]


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

fuel = [row[0] for row in rows]  # rows still holds the 100,000 flights
for segment_count in SEGMENT_COUNTS:
    routes = [make_route(segment_count) for _ in fuel]
    segments = np.array(routes)  # flights x segments x 3 values
    arrays = (np.array(fuel, dtype=float),
              segments[:, :, 0], segments[:, :, 1], segments[:, :, 2])
    for repeat in range(1, REPEATS + 1):
        results.append([100000, f"python_route_{segment_count}", repeat,
                        seconds_taken(run_python_routes, (fuel, routes))])
        results.append([100000, f"numpy_route_{segment_count}", repeat,
                        seconds_taken(run_numpy_routes, arrays)])

with open(Path(__file__).parent / "benchmark_results.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["flights", "method", "repeat", "seconds"])
    for count, method, repeat, seconds in results:
        writer.writerow([count, method, repeat, f"{seconds:.6f}"])
        print(f"{count:>7} flights  {method:<7} repeat {repeat}  {seconds:.6f} s")

print()
groups = []
for count, method, repeat, seconds in results:
    if [count, method] not in groups:
        groups.append([count, method])
for count, method in groups:
    times = [row[3] for row in results if row[0] == count and row[1] == method]
    median = statistics.median(times)
    print(f"{count:>7} flights  {method:<7} median {median:.6f} s  "
          f"st dev {statistics.stdev(times):.6f} s")
    if count == 100000 and method in ["numpy", "numpy_route_3"]:
        outcome = "PASS" if median < TARGET_SECONDS else "FAIL"
        print(f"Target median under 10 ms: {outcome}")
