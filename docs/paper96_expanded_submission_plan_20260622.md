# Paper 96 Expanded Submission-Readiness Plan

Date frozen: 2026-06-22

Paper: `96_robotic_common_sense_tests`

Target venue posture: ICLR-main hostile-review audit. The goal is not to make executable common-sense tests look good. The goal is to test whether a stronger, risk-bounded version survives strong baselines, stress, ablations, fixed-risk deployment, and reviewer attack.

## Core Question

Can a robot convert natural physical common-sense assumptions into executable affordance tests that improve closed-loop task success, safety, regret, and utility under ambiguous perception, counterintuitive physics, language ambiguity, tool-geometry shift, and low-signal common-sense stress?

The v4.1 audit found that executable tests were the best no-human baseline but still lost to the human-query policy on success, physical violations, damage, and regret. The v5 audit must test a stronger version without relaxing the acceptance standard.

## Method Under Audit

`risk_bounded_executable_common_sense_tests_v5`

The v5 method may use:

- Assumption-family parsing from language and scene context.
- Low-cost executable probes for support, containment, rigidity, reach, articulation, clearance, mass, and material/fragility assumptions.
- Counterfactual rollout scoring before committing to action.
- Cost-calibrated test selection.
- Calibration and fixed-risk abstention.
- Risk-bounded rejection of unsafe affordances.

The method is not allowed to win by silently discarding success, over-rejecting valid actions, hiding test cost, using human queries, or weakening strong active-perception, repair, conformal, and human-query baselines.

## CPU/RAM-Light Expanded Protocol

Main evaluation:

- Seeds: 10.
- Tasks: 6.
- Assumption families: 8.
- Splits: 8.
- Methods: 14.
- Episodes per cell: 6.
- Expected main rollout rows: 322,560.
- Expected dataset summary rows: 23,040.
- Expected seed-metric rows: 1,120.
- Expected aggregate metric rows: 1,568.
- Expected paired rows: 1,344.

Tasks:

- stackable_object_placement
- container_liquid_transfer
- tool_use_reachability
- door_drawer_opening
- cluttered_navigation_clearance
- fragile_deformable_packing

Assumption families:

- support_stability
- containment_or_leakage
- rigidity_or_deformation
- tool_reach_and_contact
- articulation_direction
- clearance_and_collision
- mass_or_inertia
- material_fragility_or_thermal

Splits:

- nominal_household
- visual_ambiguity_shift
- counterintuitive_physics_shift
- language_goal_ambiguity_shift
- sensor_noise_shift
- tool_geometry_shift
- low_signal_common_sense_stress
- combined_common_sense_stress

Methods:

- direct_vlm_action_policy
- llm_common_sense_replanner
- sequential_3d_affordance_reasoner
- uncertainty_threshold_probe
- model_to_model_deliberation
- failure_retrieval_policy
- no_test_calibrated_affordance
- active_perception_planner
- conformal_risk_filter
- human_oracle_query_policy
- policy_repair_from_failed_rollouts
- executable_common_sense_tests_v4
- risk_bounded_executable_common_sense_tests_v5
- oracle_physical_assumption

## Metrics

Diagnostic and test metrics:

- assumption_diagnosis_accuracy
- unsafe_affordance_rejection_recall
- false_rejection_rate
- calibration_error
- test_informativeness
- assumption_coverage
- counterfactual_test_validity

Deployment metrics:

- task_success
- physical_violation_rate
- damage_spill_collision_rate
- test_query_cost
- human_query_burden
- planning_regret_to_oracle
- robust_utility

## Ablations

Run 10 ablations/variants on the four hard splits:

- full_risk_bounded_executable_common_sense_tests_v5
- minus_executable_probe
- minus_assumption_parser
- minus_cost_model
- minus_calibration
- minus_risk_bound
- minus_counterfactual_rollout
- language_only_common_sense
- geometry_only_affordance_tests
- active_perception_only

Expected ablation rollout rows: 115,200.

## Stress Sweep

Run a six-level stress sweep over visual ambiguity, counterintuitive physics, language ambiguity, sensor noise, tool-geometry shift, material fragility, and test-cost pressure.

Expected stress raw rows: 259,200.

Stress gate:

- V5 must not be dominated at maximum stress by human-query, active perception, conformal risk filtering, policy repair, deliberation, or v4.
- If tests improve recall but reduce utility through over-rejection or cost, report the negative mechanism honestly.

## Fixed-Risk Deployment

Budgets:

- 0.00
- 0.05
- 0.10
- 0.15

Hard splits:

- low_signal_common_sense_stress
- combined_common_sense_stress

Methods:

- risk_bounded_executable_common_sense_tests_v5
- human_oracle_query_policy
- active_perception_planner
- conformal_risk_filter
- policy_repair_from_failed_rollouts
- executable_common_sense_tests_v4

Expected fixed-risk raw rows: 138,240.

Fixed-risk gate:

- At budget 0.05, V5 must have nonzero useful coverage.
- Accepted success and accepted utility must not trail the strongest accepted baseline.
- If coverage collapses or accepted utility is poor, mark the gate failed.

## Required Gates

V5 can only be `STRONG_REVISE` if all of these pass:

- `success_gate`: V5 beats the best non-oracle hard-split success baseline by a practical margin or a paired positive lower bound.
- `diagnosis_gate`: V5 is best or statistically tied-best on assumption diagnosis and unsafe rejection recall.
- `safety_gate`: V5 does not increase physical violations or damage relative to the strongest safe baseline.
- `regret_gate`: V5 does not increase regret relative to active-perception, repair, human-query, or conformal baselines.
- `utility_gate`: V5 is on the hard robust-utility frontier.
- `false_reject_gate`: V5 does not win safety by rejecting too many valid actions.
- `ablation_gate`: the full method is necessary; stripped variants cannot match or beat it on the deployment objective.
- `stress_gate`: V5 survives maximum stress without being dominated.
- `fixed_risk_gate`: V5 has useful coverage and accepted performance at budget 0.05.
- `scope_gate`: evidence is not overclaimed as real robot or high-fidelity validation.

If any critical deployment gate fails, the terminal state must be `KILL_ARCHIVE` unless the evidence supports only a clearly bounded `STRONG_REVISE`.

## Manuscript Requirements

- 25+ page ICLR-style PDF.
- Bright boxed clickable citations routed to the bibliography.
- 120+ bibliography entries from `docs/deep_read_250.csv`.
- Formal problem setup for executable assumption tests and risk-bounded affordance rejection.
- Theory notes showing why executable tests and high recall alone are insufficient for closed-loop improvement.
- Tables for row counts, hard aggregate, paired tests, ablations, stress, fixed risk, split frontiers, baseline rejection, and negative cases.
- Honest limitations: local deterministic benchmark, no real robot, no high-fidelity simulator, no learned checkpoint release, no independent reproduction.

## Artifact Requirements

- Numbered PDF only at `C:/Users/wangz/Downloads/96.pdf`.
- No visible Desktop PDF.
- `scripts/generate_manuscript.py`.
- `scripts/validate_submission_artifacts.py`.
- Updated README/status/checklist/audit docs.
- Public GitHub repo pushed and verified.
- Root ledgers updated only after Paper 96 repo validation and push.

## Frozen Decision Rule

Report all predefined results honestly. Do not optimize for pretty results. Optimize for a result that survives hostile review.

If V5 improves diagnostic recall but human-query, active-perception, repair, conformal, or calibrated-affordance baselines remain better for success, safety, regret, robust utility, fixed-risk coverage, or ablation necessity, the correct terminal decision is `KILL_ARCHIVE`.
