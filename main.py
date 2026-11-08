# FR-05: read flights.csv and print the results, statuses and warnings as a table.
# FR-06: python main.py routes.csv uses each flight's route when it has one.
import csv
import sys
from pathlib import Path

from calculations import (
    endurance_hours,
    flight_time_hours,
    fuel_at_arrival,
    range_km,
    reserve_margin,
    route_time_and_burn,
)
from status import fuel_status
from validation import validate_inputs, validate_segments

WARNINGS = {
    "CRITICAL": "Arrival fuel is below protected fuel",
    "CAUTION": "Arrival fuel is less than 25% above protected fuel",
    "NORMAL": "-",
}
REQUIRED_COLUMNS = ["flight", "fuel_kg", "fuel_flow_kg_h", "distance_km",
                    "groundspeed_kmh", "protected_kg"]
ROUTE_COLUMNS = ["flight", "distance_km", "groundspeed_kmh", "fuel_flow_kg_h"]


def print_disclaimer():
    print("Prototype")


def print_flight(row, segments=None):
    try:
        fuel, fuel_flow, distance, groundspeed, protected = validate_inputs(
            row["fuel_kg"], row["fuel_flow_kg_h"], row["distance_km"],
            row["groundspeed_kmh"], row["protected_kg"])
        if segments:
            segments = validate_segments(segments)
            if abs(sum(segment[0] for segment in segments) - distance) > 0.001:
                raise ValueError("route distance does not match distance_km")
    except ValueError as error:
        print(f"{row['flight']:<8}INVALID: {error}")
        return

    if segments:
        flight_time, burn = route_time_and_burn(segments)
        arrival = fuel - burn
    else:
        flight_time = flight_time_hours(distance, groundspeed)
        arrival = fuel_at_arrival(fuel, fuel_flow, flight_time)
    endurance = endurance_hours(fuel, protected, fuel_flow)
    available_range = range_km(endurance, groundspeed)
    margin = reserve_margin(arrival, protected)
    status = fuel_status(arrival, protected)

    print(f"{row['flight']:<8}{flight_time:>8.2f}{arrival:>12.0f}{margin:>11.0f}"
          f"{endurance:>10.2f}{available_range:>10.0f}  {status:<10}{WARNINGS[status]}")


def missing_columns(reader, required):
    found = reader.fieldnames or []
    return [name for name in required if name not in found]


# Returns each flight's segments in file order
def load_routes(routes_path):
    routes = {}
    with open(routes_path, newline="") as file:
        reader = csv.DictReader(file)
        missing = missing_columns(reader, ROUTE_COLUMNS)
        if missing:
            raise ValueError(f"routes file is missing columns: {', '.join(missing)}")
        for row in reader:
            if row["flight"] not in routes:
                routes[row["flight"]] = []
            routes[row["flight"]].append(
                (row["distance_km"], row["groundspeed_kmh"], row["fuel_flow_kg_h"]))
    return routes


# Prints one line per flight and returns the flights that had a route
def print_flights(csv_path, routes_path):
    routes = {}
    if routes_path:
        routes = load_routes(routes_path)
    with_route = []
    with open(csv_path, newline="") as file:
        reader = csv.DictReader(file)
        missing = missing_columns(reader, REQUIRED_COLUMNS)
        if missing:
            raise ValueError(f"missing columns: {', '.join(missing)}")
        for row in reader:
            if row["flight"] in routes:
                with_route.append(row["flight"])
            print_flight(row, routes.get(row["flight"]))
    return with_route


def run(csv_path, routes_path=None):
    print_disclaimer()
    print(f"{'Flight':<8}{'Time h':>8}{'Arrival kg':>12}{'Margin kg':>11}"
          f"{'Endur. h':>10}{'Range km':>10}  {'Status':<10}Warning")
    with_route = []
    try:
        with_route = print_flights(csv_path, routes_path)
    except ValueError as error:
        print(f"INVALID FILE: {error}")
    print()
    if with_route:
        print(f"Route used for: {', '.join(with_route)}")
    print_disclaimer()


if __name__ == "__main__":
    routes_path = sys.argv[1] if len(sys.argv) > 1 else None
    run(Path(__file__).parent / "flights.csv", routes_path)
