# Claims

## Claim Tested

Executable common-sense tests are useful if a robot can convert physical assumptions into low-cost action probes that reject unsafe affordances before committing to manipulation or navigation.

The v5 claim is stronger than the original draft: `risk_bounded_executable_common_sense_tests_v5` should improve closed-loop task success, safety, regret, and robust utility under hard common-sense stress, not merely produce an interpretable test.

## Supported Claims

- The v5 benchmark is reproducible and paper-specific: 10 seeds, 6 tasks, 8 assumption families, 8 distribution splits, 14 methods, ablations, stress curves, fixed-risk deployment, paired comparisons, and negative cases.
- The final audit generated 322,560 main rollout rows, 115,200 ablation rollouts, 259,200 stress rows, 138,240 fixed-risk rows, and 24 mined negative cases.
- The full v5 mechanism beats its stripped ablations on the internal ablation suite.
- The canonical PDF is 30 pages, validates successfully, and has bright boxed clickable citations.

## Measured Negative Claim

The method does not clear the ICLR-main gate:

- Task success: 0.54514 for v5 vs 0.68351 for `executable_common_sense_tests_v4`.
- Diagnosis: 0.65052 for v5 vs 0.74601 for `human_oracle_query_policy`.
- Unsafe recall: 0.44944 for v5 vs 0.51299 for `human_oracle_query_policy`.
- False rejection rate: 0.50990 for v5.
- Physical violation: 0.37830 for v5 vs 0.19549 for `conformal_risk_filter`.
- Damage/spill/collision: 0.05642 for v5 vs 0.03038 for `conformal_risk_filter`.
- Planning regret: 0.20551 for v5 vs 0.17437 for `human_oracle_query_policy`.
- Robust utility: -0.10301 for v5 vs 0.20773 for `conformal_risk_filter`.
- Fixed-risk budget 0.05 does not uniformly rescue accepted utility.
- Scope remains local deterministic simulation, not real robot or high-fidelity simulator validation.

## Unsupported Claims Explicitly Avoided

- No claim of ICLR-main submission readiness.
- No claim of real-robot validation.
- No claim of high-fidelity simulator validation.
- No claim that executable common-sense tests beat human-in-the-loop recovery.
- No claim that high unsafe-rejection recall is sufficient for deployment.
- No claim of state-of-the-art embodied reasoning or affordance testing.
