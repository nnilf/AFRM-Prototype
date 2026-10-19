# FR-04: fuel status from the ratio of arrival fuel to protected fuel.
def fuel_status(arrival, protected):
    ratio = arrival / protected
    if ratio < 1.00:
        return "CRITICAL"
    if ratio < 1.25:
        return "CAUTION"
    return "NORMAL"
