# Submission Readiness Audit v4.1

Date: 2026-06-15

Decision: KILL_ARCHIVE

ICLR main-conference readiness: NO

## Rerun Command

```powershell
python -m py_compile src\run_experiment.py
python src\run_experiment.py
```

The continuation rerun completed successfully and wrote `results/summary.txt` with terminal decision `KILL_ARCHIVE`.

## CSV Integrity

- `metrics.csv`: 45 rows.
- `per_task_assumption_metrics.csv`: 1575 rows.
- `seed_task_assumption_metrics.csv`: 11025 rows.
- `pairwise_stats.csv`: 7 rows.
- `ablation_metrics.csv`: 7 rows.
- `ablation_seed_metrics.csv`: 1715 rows.
- `stress_sweep.csv`: 42 rows.
- `stress_sweep_seed_metrics.csv`: 10290 rows.
- `failure_cases.csv`: 5 rows.

Coverage: seven seeds (`0` through `6`), five tasks, seven physical-assumption families, five splits, nine methods, seven ablations, and six stress levels.

## Main Combined-Stress Gate

The proposed executable-test method is the best no-human method, but it does not beat the strongest non-oracle baseline.

| Method | Success | Unsafe recall | Violation | Damage | Cost | Human burden | Regret |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| human_oracle_query_policy | 0.63326 +/- 0.00658 | 0.45736 | 0.29184 | 0.07871 | 0.03973 | 0.37695 | 0.18558 |
| proposed_executable_common_sense_tests | 0.56725 +/- 0.00807 | 0.41866 | 0.31846 | 0.09397 | 0.01490 | 0.00000 | 0.21702 |

Paired proposed-minus-human differences over 245 task/assumption/seed groups:

- Task success: `-0.06600 +/- 0.01009`.
- Physical violation: `+0.02662 +/- 0.00856`.
- Damage/spill/collision: `+0.01526 +/- 0.00538`.
- Test/query cost: `-0.02483 +/- 0.00070`.
- Human-query burden: `-0.37695 +/- 0.00643`.
- Planning regret to oracle: `+0.03144 +/- 0.00281`.
- Unsafe-affordance rejection recall: `-0.03870 +/- 0.01062`.

The lower-cost/no-human-burden result is real, but it is bought with worse success, safety, recall, and regret.

## Ablation Gate

The full method is not the best version of itself:

- `minus_cost_model`: success `0.60835 +/- 0.00669`, violation `0.27955`, regret `0.19110`.
- `minus_calibration`: success `0.57992 +/- 0.00670`, violation `0.30000`, regret `0.20677`.
- Full proposed method in the ablation run: success `0.57263 +/- 0.00721`, violation `0.31688`, regret `0.21453`.

This is a fatal mechanism-support failure.

## Stress Gate

At maximum stress (`1.0`), the result does not reverse:

- human-query policy: success `0.63163 +/- 0.00836`, violation `0.28776`, regret `0.18394`.
- proposed executable tests: success `0.56279 +/- 0.00873`, violation `0.31531`, regret `0.21577`.

## Terminal Decision

Paper 96 remains `KILL_ARCHIVE`. The continuation audit confirms a useful partial-positive result against autonomous reasoning baselines, but the paper is not an honest ICLR-main submission because the core closed-loop claim loses to human-query policy and is contradicted by ablations.

