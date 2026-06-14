# Paper 96 Rebuild Plan: Robotic Common-Sense Tests

Timestamp: 2026-06-14 20:29:40 +01:00

## Starting Point

Paper 96 is currently a v3 archive. The original research bet is:

> Turn common-sense physical assumptions into executable affordance tests.

The current repo contains a generic synthetic probability scaffold, not a robotics common-sense benchmark. The hostile prior-work pressure is strong: embodied physical-reasoning models, sequential 3D affordance reasoning, large action models, LLM replanning, cross-environment failure reasoning, robot common-sense embeddings, physical reasoning benchmarks, and safety deliberation already cover much of the obvious territory. The rebuild cannot claim novelty from "common sense" or "affordance tests." It must show that executable physical tests change robot action choices and outcomes beyond strong VLM/LLM, affordance, uncertainty, and recovery baselines.

## Rebuilt Claim Under Test

The strongest defensible claim is:

> Executable common-sense tests are useful when a robot converts physical assumptions into low-cost action probes that falsify unsafe affordances before committing to manipulation or navigation.

This is a local evidence audit, not hardware validation.

## Benchmark Design

I will replace the template scaffold with a deterministic common-sense affordance benchmark. Each episode samples a scene, task, hidden physical assumption, and action set. Methods choose whether to run executable tests, deliberate, ask for help, or directly act. The benchmark measures whether the tests prevent common-sense physical failures without excessive cost or false rejection.

Tasks:

1. `stackable_object_placement`
2. `container_liquid_transfer`
3. `tool_use_reachability`
4. `door_drawer_opening`
5. `cluttered_navigation_clearance`

Assumption families:

1. `support_stability`
2. `containment_or_leakage`
3. `rigidity_or_deformation`
4. `tool_reach_and_contact`
5. `articulation_direction`
6. `clearance_and_collision`
7. `mass_or_inertia`

Splits:

1. `nominal_household`
2. `visual_ambiguity_shift`
3. `counterintuitive_physics_shift`
4. `language_goal_ambiguity_shift`
5. `combined_common_sense_stress`

## Methods To Compare

Strong baselines:

1. `direct_vlm_action_policy`
2. `llm_common_sense_replanner`
3. `sequential_3d_affordance_reasoner`
4. `uncertainty_threshold_probe`
5. `model_to_model_deliberation`
6. `failure_retrieval_policy`
7. `human_oracle_query_policy`
8. `proposed_executable_common_sense_tests`
9. `oracle_physical_assumption`

## Metrics

Reasoning/test metrics:

1. Assumption-family diagnosis accuracy.
2. Unsafe-affordance rejection recall.
3. False rejection rate.
4. Calibration error.
5. Test informativeness.

Closed-loop metrics:

1. Task success.
2. Physical violation rate.
3. Damage/spill/collision rate.
4. Test/query cost.
5. Human-query burden.
6. Planning regret to oracle.

Statistics:

1. Seven deterministic seeds.
2. Per-task and per-assumption means with 95 percent confidence intervals.
3. Paired seed/task/assumption comparison against the strongest non-oracle baseline.
4. Explicit terminal decision in `results/summary.txt`.

## Ablations

The full method must beat stripped variants:

1. `full_executable_common_sense_tests`
2. `minus_executable_probe`
3. `minus_assumption_family_parser`
4. `minus_cost_model`
5. `minus_calibration`
6. `language_only_common_sense`
7. `geometry_only_affordance_tests`

If stripped variants match or beat full on closed-loop success, violation reduction, or regret, the mechanism is not supported.

## Stress Tests

Stress axes:

1. Visual ambiguity.
2. Counterintuitive physics.
3. Language-goal ambiguity.
4. Sensor noise / partial observation.
5. Test-cost budget.
6. Combined maximum stress.

The stress sweep must show whether executable tests remain useful when VLM/LLM reasoning, sequential affordance reasoning, deliberation, retrieval, and human-query policies degrade or become costly.

## Paper Rewrite Requirements

After experiments:

1. Rewrite `paper/main.tex` as either a strong-revise evidence report or a negative evidence audit.
2. Replace template claims with measured claims only.
3. Include tables for combined stress, ablations, pairwise decision, and failure cases.
4. Include figures for diagnosis quality, closed-loop outcomes, cost/regret, ablations, and stress curves.
5. Update README, child status, claims, final audit, and submission-readiness docs.
6. Build only `C:/Users/wangz/Downloads/96.pdf`; do not copy anything to Desktop.
7. Commit and push to `https://github.com/Jason-Wang313/96_robotic_common_sense_tests`.

## Terminal Gate

Mark `STRONG_REVISE` only if all of the following are true:

1. `proposed_executable_common_sense_tests` beats the strongest non-oracle baseline on combined-stress task success and physical-violation reduction.
2. It also improves unsafe-affordance rejection recall or assumption diagnosis without excessive false rejections, test cost, or human burden.
3. Core ablations degrade in expected directions.
4. Maximum-stress curves do not reverse in favor of sequential 3D affordance reasoning, LLM replanning, model deliberation, failure retrieval, or human-query policies.
5. The paper honestly states the evidence is local/simulated and not robot hardware validation.

Otherwise mark `KILL_ARCHIVE`. Executable common-sense tests that are matched or beaten by affordance reasoning, deliberation, retrieval, or human queries are not ICLR-main ready.
