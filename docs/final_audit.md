# Final Audit

1. Chosen thesis: Robotic Common-Sense Tests evaluates whether executable probes of physical assumptions improve robot action selection.
2. ICLR-main decision: KILL_ARCHIVE.
3. Submission-hardening version: v4.1 rerun audit.
4. Last update: 2026-06-15 13:49:29 +01:00.
5. Evidence: deterministic local executable-common-sense benchmark with seven seeds, five tasks, seven assumption families, five splits, nine methods, ablations, stress sweeps, paired confidence intervals, and failure cases; rerun on 2026-06-15 without reducing experimental quality.
6. Strongest non-oracle baseline: human_oracle_query_policy.
7. Combined-stress evidence: human-query policy reaches 0.633 +/- 0.007 task success; the proposed method reaches 0.567 +/- 0.008.
8. Paired task/assumption/seed result: proposed minus human-query policy is -0.06600 +/- 0.01009 for success, +0.02662 +/- 0.00856 for physical violations, +0.01526 +/- 0.00538 for damage, -0.02483 +/- 0.00070 for cost, -0.37695 +/- 0.00643 for human burden, +0.03144 +/- 0.00281 for regret, and -0.03870 +/- 0.01062 for unsafe recall.
9. Main failure mode: executable tests reduce reliance on humans and beat non-human reasoning baselines, but they do not match human-query success/safety and have high false rejections.
10. Ablation failure: `minus_cost_model` and `minus_calibration` beat full on task success.
11. Closest hostile prior work: see `docs/hostile_prior_work.md`, `docs/hostile_prior_work_100_cards.csv`, and `docs/hostile_reviewer_response.md`.
12. Reproducibility: `python src/run_experiment.py` regenerates the CSVs, figures, LaTeX tables, and terminal decision.
13. Claim-validity status: ICLR-main claim killed; archive retained as a negative evidence report.
14. Exact Downloads PDF path: `C:/Users/wangz/Downloads/96.pdf`.
15. GitHub URL: https://github.com/Jason-Wang313/96_robotic_common_sense_tests.
16. Confirmation: no visible Desktop PDF copy was requested or made.
