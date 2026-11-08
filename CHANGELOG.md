# Changelog

## Unreleased (planned V1.1.0)

CR-001: multi-segment routes. The tag and date are added on release.

### Added

- FR-06: a flight can have a route of segments, each with its own distance, groundspeed and fuel flow
- `validate_segments`, `route_time_and_burn` and `calculate_route_batch`
- `python main.py routes.csv`, with a sample `routes.csv`
- CR-001 acceptance tests in `test_route.py`, written before the route code
- Route timings for 1, 3 and 5 segments in `benchmark.py`
- `CR-001.md` and `REVIEW_CHECKLIST.md`
- Fixed Hypothesis seed in CI

### Unchanged

- Plain `python main.py` output is byte-identical to `V1.0.1`.
- The existing calculation functions, status thresholds, and the meaning of endurance and range.

## V1.0.1 - 2026-11-07

The calculations are the same as `V1.0.0`.

### Added

- Test plan with priorities, targets and start and finish criteria
- Branch coverage reporting in CI
- Known-answer and boundary tests
- Automated FR-05 output and CSV tests
- Hand-worked and Hypothesis checks for NumPy
- Benchmark median, standard deviation and target check
- Planned challenge test for a two-leg route
- Baseline evidence in `evidence/`

### Changed

- `main.py` now runs through `run(csv_path)`, so tests can import it. Normal output is unchanged.

### Fixed

- DEF-001: a CSV with a missing or renamed column crashed with a `KeyError`. It now prints a clear error and the closing disclaimer.

## V1.0.0 - 2026-11-01

Assignment 1 prototype.

- Input validation (FR-01)
- Flight time and arrival fuel (FR-02)
- Endurance and range (FR-03)
- Reserve margin and fuel status (FR-04)
- Results table, warnings and disclaimer (FR-05)
- Simulated flight data, NumPy batch calculations and benchmark
- Ruff and tests in GitHub Actions
