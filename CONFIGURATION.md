# Configuration Register

This records which files are under version control, which versions can be recovered, and how changes are controlled in this solo project.

## Controlled items

| Item | Files |
|---|---|
| Source code | `calculations.py`, `validation.py`, `status.py`, `batch_calculations.py`, `main.py` |
| Tools | `generate_flights.py`, `benchmark.py` |
| Tests | `test_*.py` |
| Test plan and evidence | `TEST_PLAN.md`, `evidence/` |
| Sample data | `flights.csv`, `benchmark_results.csv` |
| Pinned dependencies | `requirements.txt` |
| Coverage and CI configuration | `.coveragerc`, `.github/workflows/tests.yml` |
| Documentation | `README.md`, `CHANGELOG.md`, `CONFIGURATION.md` |

## Baselines

| Tag | Full commit SHA | What it is | CI run |
|---|---|---|---|
| `V1.0.0` | `35d06451a305afb47b3a02e439672d1ba4edc389` | Assignment 1 prototype | `41910393157`, passed |
| `V1.0.1` | `8aa72ace49d481659272f1ba8424d17bf338f42d` | Tested baseline with the same calculations, new tests and the DEF-001 fix | `42356813449`, passed |

The evidence in `evidence/` was recorded on commit `deaab54f7199e1b89e795a7f50ce65385c94d816`, CI run `42300852815`, which passed. `V1.0.1` is the next commit, which only added that evidence and the updated run commands.

To recover a baseline and repeat its tests:

```powershell
git switch --detach V1.0.1
python -m pip install -r requirements.txt
python -m pytest -v --cov --cov-report=term-missing --hypothesis-seed=42
```

## Change controls

- Each change is a small commit, and GitHub Actions runs Ruff and all the tests on every push.
- Algorithm changes need a written change request, a branch and a pull request before merging.
- Each baseline or release gets a tag and an entry in `CHANGELOG.md`.

## Limitations

- I am the only developer, so I approve my own changes and nobody independently reviews them.
- Git history shows what changed, but it does not show that a change was approved.
- Branch protection is not turned on for `main`, so CI reports failures but nothing stops a merge. I have to check the result myself.
- The DEF-001 fix went directly onto `main` without a branch or pull request. It was small and has test evidence, but it did not go through the full change process.
