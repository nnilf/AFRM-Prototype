# Property tests: Hypothesis tries hundreds of random valid inputs for each test.
from hypothesis import given
from hypothesis import strategies as st

from calculations import flight_time_hours, fuel_at_arrival, endurance_hours, range_km
from status import fuel_status

fuel_values = st.floats(min_value=0, max_value=200000)
fuel_flow_values = st.floats(min_value=100, max_value=20000)
distance_values = st.floats(min_value=0, max_value=10000)
groundspeed_values = st.floats(min_value=100, max_value=1300)
protected_values = st.floats(min_value=1, max_value=50000)
extra_flow_values = st.floats(min_value=0, max_value=10000)


@given(fuel_values, protected_values, groundspeed_values, fuel_flow_values, extra_flow_values)
def test_fr03_more_fuel_flow_never_increases_range(fuel, protected, groundspeed, fuel_flow, extra_flow):
    range_before = range_km(endurance_hours(fuel, protected, fuel_flow), groundspeed)
    range_after = range_km(endurance_hours(fuel, protected, fuel_flow + extra_flow), groundspeed)
    assert range_after <= range_before


@given(fuel_values, fuel_flow_values, distance_values, groundspeed_values)
def test_fr02_arrival_fuel_never_more_than_current_fuel(fuel, fuel_flow, distance, groundspeed):
    flight_time = flight_time_hours(distance, groundspeed)
    assert fuel_at_arrival(fuel, fuel_flow, flight_time) <= fuel


@given(fuel_values, protected_values, fuel_flow_values)
def test_fr03_endurance_never_negative(fuel, protected, fuel_flow):
    assert endurance_hours(fuel, protected, fuel_flow) >= 0


@given(fuel_values, protected_values)
def test_fr04_status_is_always_one_of_three(arrival, protected):
    assert fuel_status(arrival, protected) in ("CRITICAL", "CAUTION", "NORMAL")
