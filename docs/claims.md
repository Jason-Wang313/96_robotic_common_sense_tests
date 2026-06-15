# Claims

## Claim Tested

Executable common-sense tests are useful when a robot converts physical assumptions into low-cost action probes that falsify unsafe affordances before committing to manipulation or navigation.

## Supported Claims

- The v4/v4.1 benchmark is reproducible and paper-specific: five tasks, seven assumption families, five distribution shifts, nine methods, seven seeds, ablations, stress curves, paired comparisons, and failure cases.
- The 2026-06-15 v4.1 continuation rerun reproduces the negative decision with regenerated CSVs, figures, LaTeX tables, and summary evidence.
- The proposed method improves over direct VLM action, LLM replanning, sequential 3D affordance reasoning, model deliberation, failure retrieval, and uncertainty probes on combined-stress task success.
- The proposed method avoids human-query burden and has lower cost than the human-query baseline.

## Measured Negative Claim

The method does not clear the ICLR-main gate:

- Task success: 0.567 +/- 0.008 vs 0.633 +/- 0.007 for human-query policy.
- Physical violation: 0.318 vs 0.292.
- Damage/spill/collision: 0.094 vs 0.079.
- Planning regret: 0.217 vs 0.186.
- Unsafe recall: 0.419 vs 0.457.
- False rejection rate: 0.427.
- `minus_cost_model` and `minus_calibration` beat the full method on success.

## Unsupported Claims Explicitly Avoided

- No claim of ICLR-main submission readiness.
- No claim of real-robot validation.
- No claim of high-fidelity simulator validation.
- No claim that executable common-sense tests beat human-in-the-loop recovery.
- No claim of state-of-the-art embodied reasoning or affordance testing.
