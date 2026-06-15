# Paper 96 ICLR-Main Continuation Execution Plan

Date: 2026-06-15

Paper: `96_robotic_common_sense_tests`

Repository: `C:/Users/wangz/robotics_massive_pool_paper_factory/96_robotic_common_sense_tests`

Canonical PDF target: `C:/Users/wangz/Downloads/96.pdf`

Desktop policy: no copy of `96.pdf` may exist on the visible Desktop.

## Objective

Re-audit Paper 96 as a real ICLR-main-target submission candidate rather than trusting the prior terminal state. The paper can be called submission-ready only if the rerun evidence supports a decisive closed-loop contribution for executable physical common-sense tests under hostile prior-work pressure.

## RAM-Light Execution Policy

- Run only this paper's experiment process while auditing Paper 96.
- Do not reduce seeds, tasks, assumptions, splits, baselines, ablations, stress levels, or episodes to save RAM.
- Prefer streaming logs to the root `logs/` directory and inspect CSV artifacts after completion instead of loading large files into the editor.

## Evidence To Rerun

1. Compile the experiment script with `python -m py_compile src/run_experiment.py`.
2. Rerun `python src/run_experiment.py` from the child repository.
3. Confirm regenerated outputs:
   - `results/metrics.csv`
   - `results/per_task_assumption_metrics.csv`
   - `results/seed_task_assumption_metrics.csv`
   - `results/ablation_metrics.csv`
   - `results/ablation_seed_metrics.csv`
   - `results/stress_sweep.csv`
   - `results/stress_sweep_seed_metrics.csv`
   - `results/pairwise_stats.csv`
   - `results/failure_cases.csv`
   - LaTeX tables and figures consumed by `paper/main.tex`

## Required ICLR-Main Gates

The paper may only move upward to `STRONG_REVISE` if the rerun evidence shows all of the following:

- Proposed executable common-sense tests beat the strongest non-oracle closed-loop baseline on combined-stress task success.
- Proposed tests do not lose the safety gate: physical violations and damage/spill/collision must be no worse than the strongest safety baseline within uncertainty.
- Proposed unsafe-affordance rejection recall must be competitive with or better than the best non-oracle recall baseline.
- Paired confidence intervals over task/assumption/seed groups must support the direction of the claim rather than overlap a practical loss.
- The full method must beat its ablations; no ablation may match or exceed the full system on the main success/safety/regret gate.
- Stress-sweep behavior at maximum stress must not reverse the claimed advantage.
- The manuscript must clearly state the evidence type, limitations, and hostile prior-work boundary.

## Terminal Failure Criteria

Mark `KILL_ARCHIVE` if any of these remain true after rerun:

- Human-query policy or another non-oracle baseline wins combined-stress task success, safety, or regret.
- The proposed method's lower human burden is bought by materially worse success/safety.
- False rejection remains high enough to weaken the closed-loop claim.
- Ablations such as `minus_cost_model` or `minus_calibration` match or beat the full method.
- Evidence remains local deterministic simulation without enough high-fidelity or robot validation to support an ICLR-main submission.

## Artifact Updates

After the rerun and audit:

- Add a continuation audit document with row counts, coverage, decision metrics, and terminal decision.
- Update child docs and manuscript only to reflect what the rerun proves.
- Rebuild `paper/main.pdf` cleanly and copy only to `C:/Users/wangz/Downloads/96.pdf`.
- Commit and push the child repository to the matching public GitHub repo.
- Update root ledgers: `GLOBAL_POOL_STATUS.md`, `BATCH_STATUS.md`, `SUBMISSION_STATUS.md`, `MASTER_REPORT.md`, `MASTER_SUBMISSION_REPORT.md`.

## Stop Condition Before Moving To Paper 97

Paper 96 is terminal only after all of the following are verified:

- Child repository is clean and local `HEAD` equals `origin/main`.
- GitHub repo is public.
- `C:/Users/wangz/Downloads/96.pdf` exists with recorded SHA256 and size.
- `C:/Users/wangz/Desktop/96.pdf` is absent.
- LaTeX log has no substantive warnings/errors.
- Root ledgers agree with the child decision and PDF artifact.
