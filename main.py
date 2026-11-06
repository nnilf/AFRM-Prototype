# FR-05: read flights.csv and print the results, statuses and warnings as a table.
import csv
from pathlib import Path

from calculations import (
    endurance_hours,
    flight_time_hours,
    fuel_at_arrival,
    range_km,
    reserve_margin,
)
from status import fuel_status
from validation import validate_inputs

WARNINGS = {
    "CRITICAL": "Arrival fuel is below protected fuel",
    "CAUTION": "Arrival fuel is less than 25% above protected fuel",
    "NORMAL": "-",
}
REQUIRED_COLUMNS = ["flight", "fuel_kg", "fuel_flow_kg_h", "distance_km",
                    "groundspeed_kmh", "protected_kg"]


def print_disclaimer():
    print("Prototype")


def print_flight(row):
    try:
        fuel, fuel_flow, distance, groundspeed, protected = validate_inputs(
            row["fuel_kg"], row["fuel_flow_kg_h"], row["distance_km"],
            row["groundspeed_kmh"], row["protected_kg"])
    except ValueError as error:
        print(f"{row['flight']:<8}INVALID: {error}")
        return

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


def run(csv_path):
    print_disclaimer()
    print(f"{'Flight':<8}{'Time h':>8}{'Arrival kg':>12}{'Margin kg':>11}"
          f"{'Endur. h':>10}{'Range km':>10}  {'Status':<10}Warning")
    with open(csv_path, newline="") as file:
        reader = csv.DictReader(file)
        missing = missing_columns(reader, REQUIRED_COLUMNS)
        if missing:
            print(f"INVALID FILE: missing columns: {', '.join(missing)}")
        else:
            for row in reader:
                print_flight(row)
    print()
    print_disclaimer()


if __name__ == "__main__":
    run(Path(__file__).parent / "flights.csv")
