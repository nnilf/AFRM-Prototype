# Test Plan

This plan tests the AFRM baseline (tag `V1.0.0`). I wrote it before adding any new tests so that the pass criteria were decided before I saw the results.

AFRM is a prototype that uses simulated data, so the priorities and targets below are my own judgement and are not certified requirements.

## Test priorities

I ranked each failure by how misleading it would be. A result that looks safe when it isn't matters more than one that is too cautious, because the cautious result would at least get checked.

| Failure | Why it matters | Priority | How I will test it |
|---|---|---|---|
| Arrival fuel too high | Looks like there is more fuel than there really is | High | Hand-worked answers and property tests |
| False NORMAL status | A low fuel state gets no warning | High | Boundary tests at ratios 1.00 and 1.25 |
| Invalid value accepted | The result is meaningless but still looks real | High | Invalid input tests |
| Wrong CSV columns | Data can't be read properly | High | CSV tests through `main.py` |
| Wrong CSV units | Numbers are wrong but look fine | High | Can't be tested from the values, see Limitations |
| Python and NumPy disagree | Two different answers for one flight | High | Compare both, plus hand-worked answers |
| Missing or unclear warning | A low fuel state could be missed or misread | High | Output tests through `main.py` |
| False CRITICAL or CAUTION | Too cautious, but it would get checked | Medium | Boundary tests |
| Slow batch calculations | Inconvenient, but the results are still right | Low | Benchmark |

## Tests

The README already lists the existing tests for each requirement. These are the new tests I plan to add, each one named by its test ID. Expected values come from the requirements or from working them out by hand, not from running the code.

| Requirement | New tests | Method | Pass if |
|---|---|---|---|
| FR-01 | `test_fr01_rejects_blank`, `test_fr01_rejects_none`, `test_fr01_rejects_negative_infinity` | Invalid inputs | `ValueError` is raised |
| FR-02 | `test_fr02_zero_distance_keeps_all_fuel`, `test_fr02_arrival_exactly_zero` | Boundary values | Results match my hand calculations |
| FR-03 | `test_fr03_fuel_equal_to_protected_gives_zero` | Boundary value | Endurance is 0 |
| FR-02, FR-03 | `test_fr02_fr03_numpy_matches_hand_values`, `test_fr02_fr03_numpy_matches_python_for_any_flight` | Known answers and comparison | NumPy matches the hand values, and Python to within 0.000001 |
| FR-05 | `test_fr05_critical_warning`, `test_fr05_caution_warning`, `test_fr05_normal_has_no_warning` | CSV through `main.py` | The right status and warning are printed |
| FR-05 | `test_fr05_invalid_row_does_not_stop_later_rows`, `test_fr05_disclaimer_before_and_after_table` | CSV through `main.py` | The bad row prints `INVALID`, the rest still run, and the disclaimer prints twice |
| FR-05 | `test_fr05_missing_column_gives_clear_error`, `test_fr05_renamed_column_gives_clear_error` | CSV through `main.py` | A clear error is printed instead of a crash, and the disclaimer still prints |

While planning these tests I found a real defect, DEF-001. A CSV with a missing or renamed column crashed `main.py` with a `KeyError`, and the closing disclaimer was not printed. The two column tests reproduced it before I fixed it, and that failure is saved in `evidence/def-001_traceback.txt`.

I also plan one challenge test, `test_challenge.py`, which runs a two-leg route with different speeds and fuel flows. I chose it on purpose to test the constant speed and fuel flow assumption, so it shows a limit of the model and not a bug.

## Targets

- **Performance:** NumPy must process 100,000 flights in a median under 10 ms over 5 repeats. Assignment 1 measured a median of 3.26 ms, so this leaves room for normal variation.
- **Requirements coverage:** FR-01 to FR-05 all have at least one automated test.
- **Code coverage:** 100% statement and branch for `validation.py`, `calculations.py`, `status.py` and `batch_calculations.py`, and at least 90% for `main.py`, which mostly handles input and output. `benchmark.py` and `generate_flights.py` are left out because they are tools and not part of the requirements.

## When testing starts and finishes

Testing can start once the baseline is tagged, the pinned requirements are installed and the expected results are written down.

Testing is finished when all the tests above pass, Ruff reports no problems, GitHub Actions passes, and the results are saved in `evidence/`. If a target is missed, I will record it and explain why.

## Limitations

- Python and NumPy agreeing doesn't prove either is right, as both could share a mistake, so I also check against hand-worked answers.
- A value in the wrong unit looks like any other number, so I can only check the column names.
- Coverage shows which code ran, not that the answers were correct.

## How to run

The Hypothesis seed is fixed so the same inputs are generated each time.

```powershell
python -m ruff check .
python -m pytest -v --hypothesis-seed=42
python benchmark.py
```
