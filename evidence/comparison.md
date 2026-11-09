> AI (Claude) was used to format this document.

# Baseline vs release comparison

| | Baseline | Release candidate |
|---|---|---|
| Version | `V1.0.1` (`8aa72ac`), evidence recorded at `deaab54` | `cr-001-route-segments`, with the two review fixes |
| CI run | `42300852815`, passed | `42490799450` on `cecb690`, passed, 49 tests, seed 42 (before the review fixes) |

Both were run on the same machine with Python 3.13.16 and the same pinned packages (`requirements.txt` has not changed since `V1.0.1`). See `environment.txt`.

The review found two small problems, which I fixed before merging. I then re-recorded `release_tests.txt` and `release_main_unchanged.txt`. The benchmark, routes output and `pip-audit` results were recorded at `cecb690`. The fixes only changed `main.py` and the tests, so they don't affect those results, and the routes output was checked again and is the same.

## Tests and coverage

| | Baseline | Release |
|---|---|---|
| Tests | 41 passed, 0 failed | 51 passed, 0 failed |
| Original tests changed | | None. The 41 original tests are unchanged, and one new test was added to `test_main.py` |
| Requirements with automated tests | 5/5 (FR-01 to FR-05) | 6/6 (FR-01 to FR-06) |
| Statement coverage | 78/79 (98.7%) | 132/134 (98.5%) |
| Branch coverage | 15/16 (93.8%) | 39/40 (97.5%) |
| Calculation modules | 100% | 100% |
| `main.py` | 96% | 97% |

All the coverage targets in `TEST_PLAN.md` are still met. The only lines not covered are 115 to 116 in `main.py`, which only run when it is started as a script.

## Expected vs observed

Expected values were worked out by hand before the code was written.

| Check | Expected | Observed |
|---|---|---|
| One segment (1200 km, 800 km/h, 2400 kg/h, fuel 6000) | Arrival 2400 kg, same as `V1.0.1` | Pass |
| Two segments | 1.5 h, burn 4200 kg | Pass |
| Three segments | 2 h, burn 5200 kg | Pass |
| Invalid segments and empty route | `ValueError` | Pass |
| Status with protected 1500 kg | 5699 CRITICAL, 5700 CAUTION, 6075 NORMAL | Pass |
| NumPy routes | 800 and 1800 kg, and matches Python within 0.000001 | Pass |
| Route that doesn't match the flight distance | `INVALID` | Pass |
| Command line with a route | 1.50 h, 1800 kg, margin 300, CAUTION, endurance 1.88 h | Pass |
| Rejected route (review fix) | Not listed in "Route used for" | Pass |
| Routes file with a missing column (review fix) | Clear error and closing disclaimer, no crash | Pass |
| `routes.csv` FLT009 | 1.15 h, burn 3000 kg, arrival 2153 kg | 1.15 h, 2153 kg (`release_routes_output.txt`) |
| `routes.csv` FLT012 | 2.14 h, burn 4828 kg, arrival 1211 kg | 2.14 h, 1211 kg (`release_routes_output.txt`) |
| `python main.py` without routes | Byte-identical to `V1.0.1` | Identical, same SHA-256 (`release_main_unchanged.txt`) |

## Status changes

Statuses only change when `routes.csv` is used. The other 48 flights print exactly the same lines.

| Flight | Without route | With route | Reason |
|---|---|---|---|
| FLT009 | 2522 kg, NORMAL | 2153 kg, CAUTION | Slower segments add 0.16 h, and the climb burns 3000 kg/h, more than the single rate of 2665 kg/h |
| FLT012 | 1771 kg, CAUTION | 1211 kg, CRITICAL | Slower climb and descent add 0.31 h, and the climb burns 3000 kg/h |

This is the intended effect of CR-001. A single average rate can hide fuel burned in slower or thirstier segments, as the challenge test showed. Endurance and range do not change, as documented in `CR-001.md`.

## Performance

These are 100,000 flights, 5 repeats, in milliseconds. I ran `V1.0.1` again just before the release benchmark, so the two can be compared under the same conditions.

| Run | Method | Median | Range | Target |
|---|---|---|---|---|
| Baseline evidence (`deaab54`, 2026-11-07) | NumPy | 2.506 | 2.375 to 2.988 | Under 10 ms: met |
| | Python | 47.110 | 46.686 to 47.260 | |
| `V1.0.1` rerun (2026-11-08) | NumPy | 2.446 | 2.091 to 3.379 | Under 10 ms: met |
| | Python | 45.789 | 44.928 to 57.141 | |
| Release (2026-11-08) | NumPy | 2.918 | 2.504 to 3.483 | Under 10 ms: met |
| | Python | 46.838 | 46.183 to 48.249 | |
| | NumPy, 1-segment routes | 1.037 | 0.970 to 1.322 | |
| | NumPy, 3-segment routes | 4.272 | 4.135 to 6.125 | Under 10 ms: met |
| | NumPy, 5-segment routes | 4.749 | 4.681 to 4.837 | |
| | Python, 1-segment routes | 34.529 | 34.277 to 35.959 | |
| | Python, 3-segment routes | 64.395 | 62.422 to 77.374 | |
| | Python, 5-segment routes | 86.531 | 86.317 to 90.140 | |

- Both performance targets were met. Even the slowest 3-segment run, 6.125 ms, was under 10 ms.
- The original NumPy median was 0.47 ms higher on the release than on the `V1.0.1` rerun. `calculate_batch` has not changed and the ranges overlap, so I treat this as normal variation and not a regression.
- Route time grows with the number of segments, but 5 segments took only a little longer than 3. With only 5 repeats I would not read much into that.

## Security

`pip-audit` found no known vulnerabilities in `requirements.txt` on 2026-11-08 (`release_pip_audit.txt`).

## Limitations

- All the timings come from one machine, with no warm-up run and only 5 repeats. Other programs running in the background were not controlled.
- The benchmark routes use random segments that do not add up to a flight distance. Only the timing matters there.
- A route in `routes.csv` for a flight that is not in `flights.csv` is ignored without a message.
