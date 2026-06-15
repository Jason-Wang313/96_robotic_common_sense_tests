# Paper 96 Terminal Audit

Date: 2026-06-15

Paper: `96_robotic_common_sense_tests`

Decision: KILL_ARCHIVE

ICLR main-conference readiness: NO

## Execution

- Created plan-first continuation document: `docs/paper96_iclr_submission_execution_plan_20260615.md`.
- Compiled experiment script with `python -m py_compile src/run_experiment.py`.
- Reran full benchmark with seven seeds, five tasks, seven assumption families, five splits, nine methods, ablations, stress sweep, paired comparisons, and failure cases.
- Rerun log: `C:/Users/wangz/robotics_massive_pool_paper_factory/logs/96_robotic_common_sense_tests_continuation_rerun_20260615.log`.

## Evidence

The rerun reproduced the previous negative decision:

- Proposed combined-stress task success: `0.56725 +/- 0.00807`.
- Human-query combined-stress task success: `0.63326 +/- 0.00658`.
- Paired proposed-minus-human success: `-0.06600 +/- 0.01009`.
- Proposed physical violation: `0.31846` versus `0.29184` for human-query policy.
- Proposed damage/spill/collision: `0.09397` versus `0.07871` for human-query policy.
- Proposed planning regret: `0.21702` versus `0.18558` for human-query policy.
- Proposed unsafe recall: `0.41866` versus `0.45736` for human-query policy.
- `minus_cost_model` and `minus_calibration` beat the full method on success.

## Artifact Status

- Canonical PDF: `C:/Users/wangz/Downloads/96.pdf`.
- PDF SHA256: `631C8D84934B02A5C06B19E6A9E13A68E5011DE83BEF1739806FBE4BB96373B5`.
- PDF size: `546185` bytes.
- Visible Desktop PDF: absent in verification.
- LaTeX log: clean except harmless `rerunfilecheck` package metadata line.
- GitHub: `https://github.com/Jason-Wang313/96_robotic_common_sense_tests`.

## Terminal Rationale

Executable common-sense tests are useful relative to no-human reasoning baselines, but the ICLR-main claim requires a stronger closed-loop result. The proposed method loses the main success/safety/regret gate to human-query policy and fails the internal ablation gate, so archiving is the honest terminal action.
