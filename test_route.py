# CR-001 acceptance tests, written before the route code exists.
# A segment is (distance km, groundspeed km/h, fuel flow kg/h).
import numpy as np
import pytest

import batch_calculations
import calculations
import main
import validation
from status import fuel_status
from test_main import HEADER

TWO_SEGMENTS = [(400, 800, 2400), (600, 600, 3000)]
THREE_SEGMENTS = [(300, 600, 2000), (400, 800, 2400), (500, 500, 3000)]
ROUTE_HEADER = "flight,distance_km,groundspeed_kmh,fuel_flow_kg_h\n"
FLIGHTS = "FLT001,Test,6000,2400,1000,700,1500\nFLT002,Test,6000,2400,1200,800,1500\n"


def run_with_routes(route_rows, tmp_path, capsys):
    flights = tmp_path / "flights.csv"
    flights.write_text(HEADER + FLIGHTS)
    routes = tmp_path / "routes.csv"
    routes.write_text(ROUTE_HEADER + route_rows)
    main.run(flights, routes)
    return capsys.readouterr().out


def flight_line(output, flight):
    return next(line for line in output.splitlines() if line.startswith(flight))


def test_cr001_single_segment_matches_baseline():
    time, burn = calculations.route_time_and_burn([(1200, 800, 2400)])
    baseline_time = calculations.flight_time_hours(1200, 800)
    assert time == baseline_time
    assert 6000 - burn == calculations.fuel_at_arrival(6000, 2400, baseline_time)
    assert 6000 - burn == 2400


def test_cr001_two_segments_matches_hand_values():
    # 0.5 h x 2400 = 1200 kg, then 1 h x 3000 = 3000 kg
    assert calculations.route_time_and_burn(TWO_SEGMENTS) == (1.5, 4200)


def test_cr001_three_segments_matches_hand_values():
    # 0.5 h x 2000 = 1000 kg, 0.5 h x 2400 = 1200 kg, then 1 h x 3000 = 3000 kg
    assert calculations.route_time_and_burn(THREE_SEGMENTS) == (2, 5200)


def test_cr001_invalid_segments_rejected():
    assert validation.validate_segments([("400", "800", "2400")]) == [(400, 800, 2400)]
    bad_routes = [
        [],
        [(0, 800, 2400)],
        [(400, -800, 2400)],
        [(400, 800, "abc")],
        [(400, 800, 2400), (600, 0, 3000)],
    ]
    for segments in bad_routes:
        with pytest.raises(ValueError):
            validation.validate_segments(segments)


def test_cr001_segment_status_correct():
    # Burn is 4200 kg, so arrival is 1499, 1500 and 1875 kg against 1500 protected
    burn = calculations.route_time_and_burn(TWO_SEGMENTS)[1]
    assert fuel_status(5699 - burn, 1500) == "CRITICAL"
    assert fuel_status(5700 - burn, 1500) == "CAUTION"
    assert fuel_status(6075 - burn, 1500) == "NORMAL"


def test_cr001_numpy_matches_python():
    # Row 2 is the two-segment route with its second leg split in half
    routes = [THREE_SEGMENTS, [(400, 800, 2400), (300, 600, 3000), (300, 600, 3000)]]
    fuel = np.array([6000.0, 6000.0])
    distances = np.array([[s[0] for s in route] for route in routes], dtype=float)
    groundspeeds = np.array([[s[1] for s in route] for route in routes], dtype=float)
    fuel_flows = np.array([[s[2] for s in route] for route in routes], dtype=float)

    arrival = batch_calculations.calculate_route_batch(fuel, distances, groundspeeds, fuel_flows)

    for i, route in enumerate(routes):
        burn = calculations.route_time_and_burn(route)[1]
        assert abs(arrival[i] - (fuel[i] - burn)) < 0.000001
    assert abs(arrival[0] - 800) < 0.000001
    assert abs(arrival[1] - 1800) < 0.000001


def test_cr001_route_distance_must_match(tmp_path, capsys):
    # FLT001 is 1000 km but its route only adds up to 400 km
    output = run_with_routes("FLT001,400,800,2400\n", tmp_path, capsys)
    assert "INVALID" in flight_line(output, "FLT001")
    assert "NORMAL" in flight_line(output, "FLT002")


def test_cr001_cli_uses_route(tmp_path, capsys):
    output = run_with_routes("FLT001,400,800,2400\nFLT001,600,600,3000\n", tmp_path, capsys)
    # Route: 1.5 h, 6000 - 4200 = 1800 kg, margin 300. Endurance stays (6000 - 1500) / 2400
    assert flight_line(output, "FLT001").split()[1:7] == [
        "1.50", "1800", "300", "1.88", "1312", "CAUTION"]
    # FLT002 has no route, so it keeps the original result: 6000 - 2400 x 1.5 = 2400
    assert flight_line(output, "FLT002").split()[1:3] == ["1.50", "2400"]
