# Paper 96 Submission Readiness Audit v5

Date: 2026-06-22

Decision: KILL_ARCHIVE

ICLR-main ready: no

## Evidence Scale

- Seeds: 10.
- Tasks: 6.
- Assumption families: 8.
- Splits: 8.
- Methods: 14.
- Main rollout rows: 322,560.
- Dataset summary rows: 23,040.
- Main seed-metric rows: 1,120.
- Main aggregate metric rows: 1,568.
- Main paired rows: 1,344.
- Hard aggregate seed rows: 140.
- Hard aggregate metric rows: 196.
- Hard aggregate paired rows: 168.
- Ablation rollout rows: 115,200.
- Stress raw rows: 259,200.
- Fixed-risk raw rows: 138,240.
- Negative cases: 24.

## Hard-Aggregate Gate

- best_success_reference=`executable_common_sense_tests_v4`
- best_diagnosis_reference=`human_oracle_query_policy`
- best_recall_reference=`human_oracle_query_policy`
- best_safety_reference=`conformal_risk_filter`
- best_damage_reference=`conformal_risk_filter`
- best_regret_reference=`human_oracle_query_policy`
- best_utility_reference=`conformal_risk_filter`
- best_ablation=`full_risk_bounded_executable_common_sense_tests_v5`
- max_stress_reference=`human_oracle_query_policy`

## V5 Versus Best References

- v5_success=0.54514; best_success=0.68351.
- v5_diagnosis=0.65052; best_diagnosis=0.74601.
- v5_recall=0.44944; best_recall=0.51299.
- v5_false_reject=0.50990.
- v5_safety=0.37830; best_safety=0.19549.
- v5_damage=0.05642; best_damage=0.03038.
- v5_regret=0.20551; best_regret=0.17437.
- v5_utility=-0.10301; best_utility=0.20773.

## Gate Outcomes

- success_gate=False.
- diagnosis_gate=False.
- safety_gate=False.
- regret_gate=False.
- utility_gate=False.
- false_reject_gate=False.
- ablation_gate=True.
- stress_gate=True.
- fixed_risk_gate=False.
- scope_gate=False.

## Artifact Validation

- Canonical PDF: `C:/Users/wangz/Downloads/96.pdf`.
- PDF pages: 30.
- PDF SHA256: `492889C4112439872136EF409497C19C991C833C7A825D3533D2828D62D4DFD2`.
- Desktop PDF leak: none.
- Validator: `python scripts/validate_submission_artifacts.py` passed.
- Visual QA: title/abstract, hard table, fixed-risk page, citation-wall pages, and bibliography tail rendered legibly.

## Terminal Reason

Risk-bounded executable common-sense tests are internally meaningful, but they do not survive the external ICLR-main deployment gate. The paper should be archived rather than submitted.
