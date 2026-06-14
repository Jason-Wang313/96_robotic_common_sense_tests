# Submission Readiness Decision

Decision: KILL_ARCHIVE

ICLR main-conference readiness: NO.

## Why It Fails

The strongest defensible claim was that executable physical common-sense tests should improve closed-loop robot action selection beyond strong reasoning and recovery baselines. The benchmark does not support that claim.

The proposed method beats non-human baselines, but the human-query policy still wins the main gate:

- human_oracle_query_policy task success: 0.633 +/- 0.007.
- proposed_executable_common_sense_tests task success: 0.567 +/- 0.008.
- Paired proposed-minus-human success difference: -0.06600 +/- 0.01009.
- Proposed physical violations are higher: 0.318 vs 0.292.
- Proposed planning regret is higher: 0.217 vs 0.186.
- Proposed false rejection rate is high: 0.427.
- Two ablations beat the full method on task success.

## Honest Terminal Action

Archive/kill for ICLR main. Do not submit this paper to ICLR main in its current form.

## Revival Condition

The idea would need a substantially new empirical project:

- Real robot or high-fidelity simulator evidence across physical common-sense tasks.
- Implemented VLM/LLM, affordance, deliberation, retrieval, and human-query baselines.
- A test-selection mechanism with lower false rejection and better success/safety than human-in-the-loop recovery.
- Manual related-work synthesis and qualitative rollouts.
- A new terminal gate showing the full method beats ablations and strong baselines under maximum stress.
