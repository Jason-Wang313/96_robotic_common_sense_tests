# Child Status 96

Current stage: ICLR main gate terminal
Last update: 2026-06-14 20:39:45 +01:00
PDF: C:/Users/wangz/Downloads/96.pdf
GitHub: https://github.com/Jason-Wang313/96_robotic_common_sense_tests
Submission-hardening version: v4
Terminal decision: KILL_ARCHIVE
ICLR main ready: no

Evidence digest:
- Seven seeds, five tasks, seven assumption families, five splits, nine methods, ablations, stress sweep, paired confidence intervals, and failure cases.
- Strongest non-oracle combined-stress baseline: human_oracle_query_policy with task success 0.633 +/- 0.007.
- Proposed executable tests: task success 0.567 +/- 0.008, unsafe recall 0.419, physical violation 0.318, damage/spill/collision 0.094, zero human burden.
- Paired success difference vs human-query policy: -0.06600 +/- 0.01009 over 245 task/assumption/seed groups.

Reason:
Executable tests improve over pure VLM/LLM/affordance baselines, but human-query policy still wins on success, physical violations, damage, and regret. The proposed method also has high false rejection and is contradicted by `minus_cost_model` and `minus_calibration` ablations.
