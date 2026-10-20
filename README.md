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
python -m pytest -v          # runs all the tests
python benchmark.py          # times plain Python against NumPy, saves benchmark_results.csv
```

The benchmark times depend on the computer, so they will be slightly different on each run.

## Files

| File | What it does |
|---|---|
| `validation.py` | Checks the inputs (FR-01) |
| `calculations.py` | Fuel at arrival, endurance and range for one flight (FR-02, FR-03) |
| `status.py` | CRITICAL, CAUTION or NORMAL status (FR-04) |
| `main.py` | Prints the results table, warnings and disclaimer (FR-05) |
| `generate_flights.py` | Makes the simulated flight data |
| `batch_calculations.py` | The FR-02 and FR-03 formulae for many flights at once with NumPy |
| `benchmark.py` | Times plain Python against NumPy |

## Which tests cover each requirement

| Requirement | Tests |
|---|---|
| FR-01 Validate inputs | `test_validation.py`: `test_fr01_accepts_valid_inputs`, `test_fr01_rejects_negative`, `test_fr01_rejects_zero_fuel_flow`, `test_fr01_rejects_zero_protected`, `test_fr01_rejects_non_numeric`, `test_fr01_rejects_nan`, `test_fr01_rejects_infinity` |
| FR-02 Fuel at arrival | `test_calculations.py`: `test_fr02_fuel_at_arrival`<br>`test_properties.py`: `test_fr02_arrival_fuel_never_more_than_current_fuel`<br>`test_batch.py`: `test_fr02_fr03_numpy_matches_plain_python` |
| FR-03 Endurance and range | `test_calculations.py`: `test_fr03_endurance_and_range`, `test_fr03_no_usable_fuel_below_protected`<br>`test_properties.py`: `test_fr03_more_fuel_flow_never_increases_range`, `test_fr03_endurance_never_negative`<br>`test_batch.py`: `test_fr02_fr03_numpy_matches_plain_python` |
| FR-04 Fuel status | `test_status.py`: `test_fr04_just_below_1_00_is_critical`, `test_fr04_exactly_1_00_is_caution`, `test_fr04_just_below_1_25_is_caution`, `test_fr04_exactly_1_25_is_normal`, `test_fr04_negative_arrival_fuel_is_critical`<br>`test_properties.py`: `test_fr04_status_is_always_one_of_three` |
| FR-05 Understandable results and warnings | No automated test. Checked by running `python main.py` and reading the output. |
