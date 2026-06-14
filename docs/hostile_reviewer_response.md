# Hostile Reviewer Response

Paper: 96 Robotic Common-Sense Tests

## Strongest Technical Threats

- Cosmos-Reason1 and broader embodied physical-reasoning models.
- SeqAfford and sequential 3D affordance reasoning via multimodal LLMs.
- Large Action Models with physical world knowledge.
- Human-in-the-loop robot action replanning with LLM common-sense reasoning.
- Cross-environment failure reasoning data for vision-language manipulation.
- Robot common-sense embeddings and physical reasoning benchmarks.
- Model-to-model safety deliberation.
- Gesture-driven affordance transfer and task-aware grasping.

## Hostile ICLR-Main Response

A hostile reviewer should reject this as an ICLR-main submission. The v4 rebuild replaces the shared template experiment with a paper-specific executable-common-sense benchmark, but the central claim still fails.

The proposed method is useful relative to non-human reasoning baselines, but it loses to human-query policy:

- Task success: 0.567 +/- 0.008 vs 0.633 +/- 0.007 for human-query policy.
- Physical violation: 0.318 vs 0.292.
- Damage/spill/collision: 0.094 vs 0.079.
- Planning regret: 0.217 vs 0.186.
- Unsafe recall: 0.419 vs 0.457.

The proposed method is cheaper and avoids human burden, but that is not enough for the terminal gate because the central claim requires success and safety gains, not only autonomy.

## Honest Action

The paper is marked `KILL_ARCHIVE`. This avoids converting a generated robotics idea into an overstated main-conference claim.

## What Would Be Needed To Revive

- Real robot or high-fidelity benchmark experiments.
- Implemented VLM/LLM, sequential affordance, deliberation, retrieval, human-query, and executable-test baselines.
- Evidence that executable tests beat human-query/recovery or achieve comparable safety with much lower burden.
- Lower false-rejection rates and ablations that support the full mechanism.
- Manual full-paper related-work audit and qualitative rollouts.
