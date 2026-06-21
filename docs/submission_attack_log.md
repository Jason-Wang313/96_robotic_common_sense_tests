# Submission Attack Log

Paper: 96 robotic_common_sense_tests

This v5 pass applies the ICLR main-conference bar with an expanded paper-specific executable-common-sense benchmark. The result is an honest archive decision, not a workshop resubmission.

## Attack 1: v4 or another non-oracle baseline may beat the stronger v5 method.

Verdict: Confirmed.

Evidence: `executable_common_sense_tests_v4` reaches 0.68351 hard-aggregate task success; v5 reaches 0.54514.

Action: Kill/archive. A new version cannot claim progress if the prior executable-test baseline wins the success gate.

## Attack 2: Executable tests may have high false rejections.

Verdict: Confirmed.

Evidence: v5 hard-aggregate false rejection is 0.50990.

Action: Do not claim a reliable deployment test-selection policy.

## Attack 3: Conformal risk filtering may dominate the safety and utility frontier.

Verdict: Confirmed.

Evidence: `conformal_risk_filter` reaches 0.19549 physical violation and 0.20773 robust utility; v5 reaches 0.37830 physical violation and -0.10301 utility.

Action: Kill/archive. Safety and utility are central robotics gates.

## Attack 4: Human-query policy may still be the diagnosis, recall, and regret reference.

Verdict: Confirmed.

Evidence: `human_oracle_query_policy` reaches 0.74601 diagnosis, 0.51299 unsafe recall, and 0.17437 regret. V5 reaches 0.65052, 0.44944, and 0.20551.

Action: Do not claim that no-human executable tests match the strongest review-relevant recovery baseline.

## Attack 5: The full mechanism may be contradicted by ablations.

Verdict: Partly mitigated.

Evidence: `best_ablation=full_risk_bounded_executable_common_sense_tests_v5`, so internal ablation necessity is improved relative to v4.1.

Action: Preserve this as a useful mechanism result, but do not submit because external baselines still dominate.

## Attack 6: Fixed-risk reporting may not rescue deployment.

Verdict: Confirmed.

Evidence: At budget 0.05, v5 coverage is nonzero, but accepted utility is not uniformly stronger than the best accepted baseline. The frozen `fixed_risk_gate=False`.

Action: Do not tune the budget after reading the results.

## Attack 7: The evidence is local simulation only.

Verdict: Still true.

Evidence: the v5 benchmark is deterministic, local, and CPU-only. It is not real robot or high-fidelity simulator validation.

Action: Frame as a negative evidence audit, not a submission.

## Attack 8: No meaningful recoverable ICLR-main issue remains after the expanded negative result.

Verdict: Terminal condition reached.

Action: Mark KILL_ARCHIVE and stop Paper 96 after public repo/PDF/report updates.
