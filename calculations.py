# FR-02: hours left until we reach the destination
def flight_time_hours(distance, groundspeed):
    return distance / groundspeed


# FR-02: fuel left when we arrive (kg)
def fuel_at_arrival(fuel, fuel_flow, flight_time):
    return fuel - fuel_flow * flight_time


# FR-03: hours we can fly using only the fuel above the protected amount
def endurance_hours(fuel, protected, fuel_flow):
    usable = max(0, fuel - protected)
    return usable / fuel_flow


# FR-03: distance we can fly before reaching protected fuel (km)
def range_km(endurance, groundspeed):
    return endurance * groundspeed


# FR-04: how much fuel we arrive with above the protected amount (kg)
def reserve_margin(arrival, protected):
    return arrival - protected


# FR-06: total hours and fuel burned (kg) over a route, one segment at a time
def route_time_and_burn(segments):
    total_time = 0
    total_burn = 0
    for distance, groundspeed, fuel_flow in segments:
        time = flight_time_hours(distance, groundspeed)
        total_time += time
        total_burn += fuel_flow * time
    return total_time, total_burn
