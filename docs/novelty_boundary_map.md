# Novelty Boundary Map

## Crowded Territory

- Generic common-sense reasoning.
- VLM/LLM affordance selection.
- Sequential 3D affordance reasoning.
- Model-to-model deliberation.
- Failure-retrieval policies.
- Human-in-the-loop replanning.
- New benchmark only.

## Claimed Boundary Tested

The only plausible boundary was executable common-sense testing: convert a physical assumption into a low-cost action probe that falsifies unsafe affordances before the robot commits to the action.

## Falsification Result

The boundary is not defensible for ICLR main. The proposed method beats non-human reasoning baselines, but human-query policy still has higher success, lower physical violations, lower damage, and lower regret. The full method is also contradicted by calibration and cost-model ablations.

Decision: KILL_ARCHIVE. A future revival would need executable tests that match human-query safety or clearly dominate it under a human-burden-aware objective.
