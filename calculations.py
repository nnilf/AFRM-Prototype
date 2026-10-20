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
