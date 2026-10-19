# FR-05: read flights.csv and print the results, statuses and warnings as a table.
import csv
from pathlib import Path

from calculations import fuel_at_arrival, endurance_hours, range_nm
from status import fuel_status
from validation import validate_inputs

WARNINGS = {
    "CRITICAL": "Arrival fuel is below protected fuel",
    "CAUTION": "Arrival fuel is less than 25% above protected fuel",
    "NORMAL": "-",
}


def print_disclaimer():
    print("PROTOTYPE ONLY - NOT FOR OPERATIONAL USE. All flight data is simulated.")
    print("Statuses are illustrative prototype bands, not MINIMUM FUEL or MAYDAY FUEL declarations.")
    print()


def print_flight(row):
    try:
        fuel, fuel_flow, time_min, groundspeed, protected = validate_inputs(
            row["fuel_kg"], row["fuel_flow_kg_h"], row["time_min"],
            row["groundspeed_kt"], row["protected_kg"])
    except ValueError as error:
        print(f"{row['flight']:<8}INVALID: {error}")
        return

    arrival = fuel_at_arrival(fuel, fuel_flow, time_min)
    endurance = endurance_hours(fuel, protected, fuel_flow)
    distance = range_nm(endurance, groundspeed)
    status = fuel_status(arrival, protected)

    print(f"{row['flight']:<8}{arrival:>12.0f}{endurance:>12.2f}{distance:>10.0f}  {status:<10}{WARNINGS[status]}")


print_disclaimer()
print(f"{'Flight':<8}{'Arrival kg':>12}{'Endur. h':>12}{'Range NM':>10}  {'Status':<10}Warning")
with open(Path(__file__).parent / "flights.csv", newline="") as file:
    for row in csv.DictReader(file):
        print_flight(row)
print()
print_disclaimer()
