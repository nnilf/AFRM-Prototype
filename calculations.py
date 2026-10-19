# FR-02: fuel left when we arrive (kg)
def fuel_at_arrival(fuel, fuel_flow, time_min):
    return fuel - fuel_flow * (time_min / 60)


# FR-03: hours we can fly using only the fuel above the protected amount
def endurance_hours(fuel, protected, fuel_flow):
    usable = max(0, fuel - protected)
    return usable / fuel_flow


# FR-03: distance we can fly (NM)
def range_nm(endurance, groundspeed):
    return endurance * groundspeed
