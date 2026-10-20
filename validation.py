import math


# FR-01: turn a value into a number, or raise an error explaining what is wrong
def check_number(name, value, allow_zero=True):
    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{name} must be a number")
    if not math.isfinite(number):  # rejects nan, inf and -inf
        raise ValueError(f"{name} must be a finite number")
    if number < 0:
        raise ValueError(f"{name} must not be negative")
    if number == 0 and not allow_zero:
        raise ValueError(f"{name} must be greater than zero")
    return number


# FR-01: check all inputs for one flight.
# Fuel flow, groundspeed and protected fuel cannot be zero because we divide by them.
def validate_inputs(fuel, fuel_flow, distance, groundspeed, protected):
    return (
        check_number("fuel", fuel),
        check_number("fuel_flow", fuel_flow, allow_zero=False),
        check_number("distance", distance),
        check_number("groundspeed", groundspeed, allow_zero=False),
        check_number("protected", protected, allow_zero=False),
    )
