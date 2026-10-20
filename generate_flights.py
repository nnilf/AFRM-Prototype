# Makes flights.csv: 50 made-up flights for testing the program.
# I used Claude (an AI assistant) to help pick aircraft types and fuel levels.
# Figures are rough, in line with open models such as OpenAP, not real data.
# Fuel flow varies by up to 10% and wind by up to 90 km/h.
# Flights are 100 to 1500 km from destination with 45 min of protected fuel.
# The seed is fixed so the file is the same every time.

import csv
import random
from pathlib import Path

# aircraft: (cruise fuel flow kg/h, cruise speed km/h)
AIRCRAFT = {
    "TP-70 turboprop": (700, 500),
    "RJ-90 regional jet": (1700, 780),
    "NB-180 narrowbody": (2500, 830),
    "WB-300 widebody": (6500, 890),
}
PROTECTED_MINUTES = 45


def make_flight(number):
    aircraft = random.choice(list(AIRCRAFT))
    cruise_flow, cruise_speed = AIRCRAFT[aircraft]

    fuel_flow = round(cruise_flow * random.uniform(0.9, 1.1))
    wind = random.uniform(-90, 90)
    groundspeed = round(cruise_speed + wind)
    distance = random.randint(100, 1500)
    protected = round(fuel_flow * PROTECTED_MINUTES / 60)

    # Pick arrival fuel first so we get a mix of CRITICAL, CAUTION and NORMAL
    arrival = protected * random.uniform(0.8, 1.6)
    fuel = round(arrival + fuel_flow * distance / groundspeed)

    return [f"FLT{number:03d}", aircraft, fuel, fuel_flow, distance, groundspeed, protected]


if __name__ == "__main__":
    random.seed(42)
    with open(Path(__file__).parent / "flights.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["flight", "aircraft", "fuel_kg", "fuel_flow_kg_h",
                         "distance_km", "groundspeed_kmh", "protected_kg"])
        for number in range(1, 51):
            writer.writerow(make_flight(number))
