# ICLR Main Gate

Paper: 96 robotic_common_sense_tests

Submission-hardening version: v4

Gate verdict: KILL_ARCHIVE

Evidence digest: v4 deterministic executable-common-sense benchmark, seven seeds, five tasks, seven assumption families, five splits, nine methods, ablations, stress sweep, paired confidence intervals, and failure cases.

Fatal blockers:

- The proposed method loses combined-stress task success to human-query policy.
- Proposed task success is 0.567 +/- 0.008 vs 0.633 +/- 0.007 for human-query policy.
- Proposed physical violation is 0.318 vs 0.292.
- Proposed planning regret is 0.217 vs 0.186.
- Proposed false rejection rate is 0.427.
- Two ablations beat the full method on task success.
- The evidence is local simulation rather than real robot or high-fidelity simulator validation.

The only honest main-conference-safe decision is to archive rather than overclaim.
