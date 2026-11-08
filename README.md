# AFRM Prototype

A small command-line prototype for Aircraft Fuel and Range Management (AFRM), written for a university assignment.

## Setup (Windows PowerShell, Python 3.13)

```powershell
py -3.13 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Reproduce everything

Run these in order from the project folder with the venv active.

```powershell
python generate_flights.py   # makes flights.csv (the same 50 flights every time)
python main.py               # prints the results table, statuses and warnings
python main.py routes.csv    # the same, but flights listed in routes.csv use their route (FR-06)
python -m ruff check .       # checks code quality with Ruff
python -m pytest -v --cov --cov-report=term-missing --hypothesis-seed=42   # runs all the tests and shows coverage
python benchmark.py          # times plain Python against NumPy for flights and 1, 3 and 5 segment routes, saves benchmark_results.csv, prints the medians and target results
```

`routes.csv` has one row per segment, in order, with the columns `flight,distance_km,groundspeed_kmh,fuel_flow_kg_h`. A flight's segments must add up to its `distance_km`. Flights without a route use the original calculation. See `CR-001.md` for the full rules.

The benchmark times depend on the computer, so they will be slightly different on each run.

GitHub Actions runs the Ruff check and all the tests automatically on every push (see `.github/workflows/tests.yml`).

## Files

| File | What it does |
|---|---|
| `validation.py` | Checks the inputs (FR-01) and route segments (FR-06) |
| `calculations.py` | Flight time, fuel at arrival, endurance, range and reserve margin for one flight (FR-02, FR-03, FR-04), and time and burn over a route (FR-06) |
| `status.py` | CRITICAL, CAUTION or NORMAL status (FR-04) |
| `main.py` | Prints the results table, warnings and disclaimer (FR-05), using routes when given (FR-06) |
| `generate_flights.py` | Makes the simulated flight data |
| `batch_calculations.py` | The FR-02 and FR-03 formulae for many flights at once with NumPy, and arrival fuel for many routes (FR-06) |
| `benchmark.py` | Times plain Python against NumPy |
| `routes.csv` | Sample routes for FLT009 and FLT012, checked by hand |

## Which tests cover each requirement

| Requirement | Tests |
|---|---|
| FR-01 Validate inputs | `test_validation.py`: `test_fr01_accepts_valid_inputs`, `test_fr01_rejects_negative`, `test_fr01_rejects_zero_fuel_flow`, `test_fr01_rejects_zero_groundspeed`, `test_fr01_rejects_zero_protected`, `test_fr01_rejects_non_numeric`, `test_fr01_rejects_nan`, `test_fr01_rejects_infinity`, `test_fr01_rejects_blank`, `test_fr01_rejects_none`, `test_fr01_rejects_negative_infinity` |
| FR-02 Flight time and fuel at arrival | `test_calculations.py`: `test_fr02_flight_time`, `test_fr02_fuel_at_arrival`, `test_fr02_zero_distance_keeps_all_fuel`, `test_fr02_arrival_exactly_zero`<br>`test_properties.py`: `test_fr02_arrival_fuel_never_more_than_current_fuel`<br>`test_batch.py`: `test_fr02_fr03_numpy_matches_plain_python`, `test_fr02_fr03_numpy_matches_hand_values`, `test_fr02_fr03_numpy_matches_python_for_any_flight` |
| FR-03 Endurance and range | `test_calculations.py`: `test_fr03_endurance_and_range`, `test_fr03_no_usable_fuel_below_protected`, `test_fr03_fuel_equal_to_protected_gives_zero`<br>`test_properties.py`: `test_fr03_more_fuel_flow_never_increases_range`, `test_fr03_endurance_never_negative`<br>`test_batch.py`: `test_fr02_fr03_numpy_matches_plain_python`, `test_fr02_fr03_numpy_matches_hand_values`, `test_fr02_fr03_numpy_matches_python_for_any_flight` |
| FR-04 Reserve margin and fuel status | `test_calculations.py`: `test_fr04_reserve_margin`<br>`test_status.py`: `test_fr04_just_below_1_00_is_critical`, `test_fr04_exactly_1_00_is_caution`, `test_fr04_just_below_1_25_is_caution`, `test_fr04_exactly_1_25_is_normal`, `test_fr04_negative_arrival_fuel_is_critical`<br>`test_properties.py`: `test_fr04_status_is_always_one_of_three` |
| FR-05 Understandable results and warnings | `test_main.py`: `test_fr05_critical_warning`, `test_fr05_caution_warning`, `test_fr05_normal_has_no_warning`, `test_fr05_invalid_row_does_not_stop_later_rows`, `test_fr05_disclaimer_before_and_after_table`, `test_fr05_missing_column_gives_clear_error`, `test_fr05_renamed_column_gives_clear_error`, `test_fr05_routes_file_missing_column_gives_clear_error` |
| FR-06 Multi-segment routes (CR-001) | `test_route.py`: `test_cr001_single_segment_matches_baseline`, `test_cr001_two_segments_matches_hand_values`, `test_cr001_three_segments_matches_hand_values`, `test_cr001_invalid_segments_rejected`, `test_cr001_segment_status_correct`, `test_cr001_numpy_matches_python`, `test_cr001_route_distance_must_match`, `test_cr001_rejected_route_not_listed_as_used`, `test_cr001_cli_uses_route` |
| Planned challenge (known model limit, not a requirement) | `test_challenge.py`: `test_challenge_leg_by_leg_matches_hand_value`, `test_challenge_simple_average_changes_status`, `test_challenge_weighted_average_matches_hand_value` |
