# Final Audit

1. Chosen thesis: Robotic Common-Sense Tests evaluates whether executable probes of physical assumptions improve robot action selection.
2. ICLR-main decision: KILL_ARCHIVE.
3. Submission-hardening version: v5 expanded hostile-review audit.
4. Last update: 2026-06-22.
5. Evidence: deterministic local executable-common-sense benchmark with 10 seeds, 6 tasks, 8 assumption families, 8 splits, 14 methods, ablations, stress sweeps, fixed-risk deployment, paired confidence intervals, and negative cases.
6. Main rows: 322,560 rollouts, 23,040 dataset rows, 1,120 seed-metric rows, 1,568 aggregate metric rows, and 1,344 paired rows.
7. Additional rows: 115,200 ablation rollouts, 259,200 stress-sweep rows, 138,240 fixed-risk rows, and 24 negative cases.
8. Strongest hard-aggregate success baseline: `executable_common_sense_tests_v4` at 0.68351 task success.
9. Strongest hard-aggregate safety/utility baseline: `conformal_risk_filter` at 0.19549 physical violation and 0.20773 robust utility.
10. Strongest hard-aggregate diagnosis/recall/regret reference: `human_oracle_query_policy` at 0.74601 diagnosis, 0.51299 unsafe recall, and 0.17437 regret.
11. V5 hard-aggregate evidence: success 0.54514, diagnosis 0.65052, recall 0.44944, false rejection 0.50990, violation 0.37830, regret 0.20551, utility -0.10301.
12. Gate status: success false, diagnosis false, safety false, regret false, utility false, false-reject false, ablation true, stress true, fixed-risk false, scope false.
13. Closest hostile prior work: see `docs/hostile_prior_work.md`, `docs/hostile_prior_work_100_cards.csv`, and `docs/hostile_reviewer_response.md`.
14. Reproducibility: `python src/run_experiment.py`, `python scripts/generate_manuscript.py`, and `python scripts/validate_submission_artifacts.py`.
15. Claim-validity status: ICLR-main claim killed; archive retained as a negative evidence report.
16. Exact Downloads PDF path: `C:/Users/wangz/Downloads/96.pdf`.
17. PDF SHA256: `492889C4112439872136EF409497C19C991C833C7A825D3533D2828D62D4DFD2`.
18. GitHub URL: https://github.com/Jason-Wang313/96_robotic_common_sense_tests.
19. Confirmation: no visible Desktop PDF copy was requested or made.
