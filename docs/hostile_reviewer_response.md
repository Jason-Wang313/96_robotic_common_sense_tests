# Hostile Reviewer Response

Paper: 96 Robotic Common-Sense Tests

## Strongest Technical Threats

- Executable tests may be dominated by active perception, conformal risk filtering, policy repair, or human-query recovery.
- High unsafe-rejection recall may be purchased with false rejection and test cost.
- v4 executable tests may already capture the useful part of the mechanism.
- Common-sense affordance testing may be covered by embodied physical-reasoning, sequential affordance, and language-conditioned robotics prior work.
- Local deterministic simulation may be too weak for ICLR-main robotics claims.

## Hostile ICLR-Main Response

A hostile reviewer should reject this as an ICLR-main submission. The v5 rebuild is much stronger than the short draft and v4.1 rerun, but the central claim still fails.

Hard-aggregate evidence:

- V5 task success: 0.54514 vs 0.68351 for `executable_common_sense_tests_v4`.
- V5 physical violation: 0.37830 vs 0.19549 for `conformal_risk_filter`.
- V5 robust utility: -0.10301 vs 0.20773 for `conformal_risk_filter`.
- V5 regret: 0.20551 vs 0.17437 for `human_oracle_query_policy`.
- V5 false rejection: 0.50990.

The method is internally meaningful because the full v5 ablation wins its stripped variants. That does not rescue the submission because the external baselines beat the deployment gate.

## Honest Action

The paper is marked `KILL_ARCHIVE`. This avoids converting a generated robotics idea into an overstated main-conference claim.

## What Would Be Needed To Revive

- Real robot or high-fidelity benchmark experiments.
- Implemented active-perception, conformal-risk, policy-repair, human-query, and executable-test baselines.
- Evidence that executable tests beat v4 and external deployment baselines on success, safety, regret, and utility.
- Lower false-rejection rates and fixed-risk utility that leads the accepted frontier.
- Manual full-paper related-work audit and qualitative rollouts.
