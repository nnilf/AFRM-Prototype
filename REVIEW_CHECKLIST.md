> AI (Claude) was used to format this document.

# CR-001 Review Checklist

I wrote this checklist before implementing CR-001, so the review is judged against points decided in advance. I will complete it against the final diff before merging.

This is a self-review, as I am the only developer. It is less independent than a peer review.

Reviewed against `git diff V1.0.1 0490411`: 7 code and data files, 250 lines added and 26 removed.

| # | Check | Result | Finding | Action |
|---|---|---|---|---|
| 1 | Units are km, km/h, kg/h and kg throughout, matching `flights.csv` | Pass | `routes.csv` uses the same column names and units as `flights.csv`. A value in the wrong unit still can't be detected, as noted in `TEST_PLAN.md` | Accepted as a limitation |
| 2 | Zero, negative, non-numeric and empty segment input is rejected | Pass | Covered by `test_cr001_invalid_segments_rejected`. I also checked a blank and a `nan` value by hand, and both print `INVALID` | None |
| 3 | Route distance must match the flight distance within 0.001 km | Pass | Covered by `test_cr001_route_distance_must_match`. By hand, 0.0005 km off was accepted and 0.002 km off was rejected. No automated test checks the 0.001 km edge | Accepted as a limitation |
| 4 | Code uses exactly the formula in `CR-001.md` | Pass | `route_time_and_burn` and `calculate_route_batch` both use time = d / g, burn = flow × time, arrival = fuel − burn | None |
| 5 | One segment gives the same results as `V1.0.1` | Pass | `test_cr001_single_segment_matches_baseline` passes: 2400 kg | None |
| 6 | `python main.py` without routes gives byte-identical output to `V1.0.1` | Pass | Same SHA-256 (`evidence/release_main_unchanged.txt`) | Checked again after the fixes, still identical |
| 7 | Status and warnings use the route arrival fuel, and the thresholds are unchanged | Pass | `status.py` has no changes since `V1.0.1`. Margin and status use the route arrival fuel, which `test_cr001_cli_uses_route` checks | None |
| 8 | Endurance and range keep their original meaning, as documented | Pass | They still use the `flights.csv` fuel flow and groundspeed (1.88 h and 1312 km in the CLI test). The printed table does not say this, so a reader could think they come from the route | Accepted as a limitation. Documented in `CR-001.md` |
| 9 | NumPy route results match plain Python and the hand values | Pass | `test_cr001_numpy_matches_python` passes on two hand-worked routes. There is no Hypothesis test for routes, unlike the original NumPy function | Accepted as a limitation |
| 10 | All CR-001 acceptance tests exist and pass | Pass | 8/8 pass (`evidence/release_tests.txt`). They failed first in CI run `42391614707` | None |
| 11 | All original tests pass without being changed | Pass | 41/41 pass, and `git diff V1.0.1` on the original test files is empty | One test was added to `test_main.py` in `4141291`. The 41 original tests are unchanged |
| 12 | Coverage targets in `TEST_PLAN.md` are still met | Pass | Calculation modules 100%, `main.py` 95%. Line 72, the error for a routes file with a missing column, has no automated test | Fixed in `4141291`. `main.py` is now 97% |
| 13 | Performance targets are met | Pass | NumPy medians: 2.918 ms for flights, 4.272 ms for 3-segment routes, both under 10 ms (`evidence/comparison.md`) | None |
| 14 | FR-06 is documented in `README.md`, `TEST_PLAN.md` and `CHANGELOG.md` | Pass | All three updated in `cecb690` | Updated again for the fixes in `96aebcd` |
| 15 | The code is simple and readable, with no unneeded comments | Pass | Each new function is under 20 lines and reuses existing functions. `print_flight` reuses the name `segments` for the checked values | None |
| 16 | CI passes on the branch | Pass | Latest run `42511439668` on `0490411` passed | The fix commits must also pass CI on the pull request before merging |

**Result** is Pass or Fail. **Action** is what I did about each finding.

## Other findings

These were not on the checklist but I found them during the review.

| # | Finding | Action |
|---|---|---|
| A | A route for a flight that is not in `flights.csv` is ignored without a message. I tested this with FLT999 | Accepted as a limitation |
| B | "Route used for" also lists flights whose route was rejected as `INVALID`, so the route was not actually used | Fixed in `e16e6df`, with the test `test_cr001_rejected_route_not_listed_as_used` |
| C | AFRM only checks fuel at arrival, so running out partway through a route would not be noticed if the total is fine | Accepted as a limitation |

## Final decision

| | |
|---|---|
| Decision (accept / accept with limitations / reject) | Accept with limitations |
| Remaining risks | Findings A and C. The 0.001 km edge and random NumPy route inputs are not tested automatically (#3, #9). Endurance and range ignore the route without saying so in the table (#8). Units can't be checked (#1). This is a self-review, and branch protection is off |
| Reviewed by | Flinn Mort |
| Date | 2026-11-08 |
