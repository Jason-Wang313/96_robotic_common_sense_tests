# ICLR Main Gate

Paper: 96 robotic_common_sense_tests

Submission-hardening version: v5 expanded hostile-review audit

Gate verdict: KILL_ARCHIVE

Evidence digest: deterministic executable-common-sense benchmark, 10 seeds, 6 tasks, 8 assumption families, 8 splits, 14 methods, raw rollouts, ablations, stress sweep, fixed-risk deployment, paired confidence intervals, and negative cases.

Fatal blockers:

- `success_gate=False`: v5 success is 0.54514; the best non-oracle success baseline is `executable_common_sense_tests_v4` at 0.68351.
- `diagnosis_gate=False`: v5 diagnosis and recall trail `human_oracle_query_policy`.
- `safety_gate=False`: v5 physical violation is 0.37830; `conformal_risk_filter` is 0.19549.
- `regret_gate=False`: v5 regret is 0.20551; `human_oracle_query_policy` is 0.17437.
- `utility_gate=False`: v5 utility is -0.10301; `conformal_risk_filter` is 0.20773.
- `false_reject_gate=False`: v5 false rejection is 0.50990.
- `fixed_risk_gate=False`: budget 0.05 does not uniformly rescue accepted utility.
- `scope_gate=False`: the evidence is local deterministic simulation rather than real robot or high-fidelity simulator validation.

Positive but insufficient:

- `ablation_gate=True`: the full v5 mechanism is internally useful relative to stripped variants.
- `stress_gate=True`: v5 survives the maximum stress comparison used by the stress gate.

The only honest main-conference-safe decision is to archive rather than overclaim.
