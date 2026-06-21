# Submission Readiness Decision

Decision: KILL_ARCHIVE

ICLR main-conference readiness: NO.

## Why It Fails

The strongest defensible claim was that executable physical common-sense tests should improve closed-loop robot action selection beyond strong active-perception, repair, conformal, human-query, and prior executable-test baselines. The expanded v5 benchmark does not support that claim.

The v5 audit is not too small: it uses 10 seeds, 6 tasks, 8 assumption families, 8 splits, 14 methods, 322,560 main rollout rows, 115,200 ablation rollouts, 259,200 stress rows, 138,240 fixed-risk rows, paired seed tests, and negative-case mining.

The method fails the hard aggregate:

- V5 task success: 0.54514 vs 0.68351 for `executable_common_sense_tests_v4`.
- V5 diagnosis: 0.65052 vs 0.74601 for `human_oracle_query_policy`.
- V5 unsafe recall: 0.44944 vs 0.51299 for `human_oracle_query_policy`.
- V5 false rejection rate: 0.50990.
- V5 physical violation: 0.37830 vs 0.19549 for `conformal_risk_filter`.
- V5 robust utility: -0.10301 vs 0.20773 for `conformal_risk_filter`.
- Fixed-risk budget 0.05 does not uniformly rescue accepted utility.

## Honest Terminal Action

Archive/kill for ICLR main. Do not submit this paper to ICLR main in its current form.

## Revival Condition

The idea would need a substantially new empirical project:

- Real robot or high-fidelity simulator evidence across physical common-sense tasks.
- Implemented VLM/LLM, affordance, active-perception, conformal, repair, and human-query baselines.
- A test-selection mechanism with much lower false rejection and better success/safety/utility than v4 and conformal references.
- Pre-registered fixed-risk budgets with accepted utility that leads the frontier.
- Manual related-work synthesis and qualitative rollouts.
- A new terminal gate showing the full method beats ablations and strong external baselines under maximum stress.
