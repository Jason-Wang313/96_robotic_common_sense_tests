# Submission Attack Log

Paper: 96 robotic_common_sense_tests

This v4/v4.1 pass applies the ICLR main-conference bar with a paper-specific executable-common-sense benchmark. The result is an honest archive decision, not a workshop resubmission.

## Attack 1: Human-query policy may beat executable tests.

Verdict: Confirmed.

Evidence: human_oracle_query_policy reaches 0.633 +/- 0.007 task success under combined stress; proposed_executable_common_sense_tests reaches 0.567 +/- 0.008. Paired proposed-minus-human success difference is -0.06600 +/- 0.01009 over 245 task/assumption/seed groups.

Action: Kill/archive. Lower human burden does not compensate for lower success and safety under the stated gate.

## Attack 2: Executable tests may have high false rejections.

Verdict: Confirmed.

Evidence: proposed false rejection rate is 0.427 under combined stress. `minus_cost_model` increases recall and success by over-testing, showing the cost/rejection tradeoff is not solved.

Action: Do not claim a reliable test-selection policy.

## Attack 3: The full mechanism may be contradicted by ablations.

Verdict: Confirmed.

Evidence: `minus_cost_model` reaches 0.608 task success and `minus_calibration` reaches 0.580, both above the full method's 0.573 ablation-run success.

Action: Kill/archive. Ablation contradictions are fatal for an ICLR-main mechanism claim.

## Attack 4: Sequential affordance, deliberation, and retrieval baselines may already cover much of the space.

Verdict: Partly mitigated.

Evidence: proposed tests beat sequential affordance reasoning, model deliberation, LLM replanning, retrieval, uncertainty probing, and direct VLM under combined stress.

Action: Preserve this as a useful negative/partial-positive result, but do not claim ICLR-main readiness.

## Attack 5: The evidence is local simulation only.

Verdict: Still true.

Evidence: the v4/v4.1 benchmark is reproducible and paper-specific, but it is not real robot or high-fidelity simulator validation.

Action: Frame as a negative evidence audit, not a submission.

## Attack 6: Prior work already covers embodied physical reasoning and common-sense affordances.

Verdict: Still true.

Evidence: hostile pool includes Cosmos-Reason1, SeqAfford, Large Action Models, LLM replanning, failure reasoning data, common-sense embeddings, physical reasoning benchmarks, and model deliberation.

Action: Do not claim novelty from common-sense reasoning alone.

## Attack 7: No meaningful recoverable ICLR-main issue remains after the negative result.

Verdict: Terminal condition reached.

Action: Mark KILL_ARCHIVE and stop Paper 96 after public repo/PDF/report updates.

## Attack 8: Continuation rerun might change the terminal decision.

Verdict: Not changed.

Evidence: the 2026-06-15 rerun regenerated the full CSV set and again found task success `0.56725 +/- 0.00807` for the proposed method versus `0.63326 +/- 0.00658` for human-query policy, with worse violation, damage, recall, and regret. `minus_cost_model` and `minus_calibration` still beat the full method.

Action: Keep KILL_ARCHIVE.
