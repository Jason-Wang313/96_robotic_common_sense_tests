# 96 Robotic Common-Sense Tests

Submission-hardening version: v5 expanded hostile-review audit

Terminal decision: KILL_ARCHIVE for ICLR main conference.

This repository is a negative evidence audit for the generated robotics idea:

> Turn common-sense physical assumptions into executable affordance tests.

The v5 rebuild tests a stronger version of the idea: a robot should parse physical assumptions, run low-cost executable probes, score counterfactual outcomes, apply cost calibration, and reject unsafe affordances under a fixed-risk gate before committing to manipulation or navigation.

The method is useful, but it does not clear the ICLR-main gate. Under the hard aggregate over `low_signal_common_sense_stress` and `combined_common_sense_stress`, v5 has nontrivial recall but loses the deployment frontier:

| Method | Task success | Diagnosis | Unsafe recall | Physical violation | Regret | Robust utility |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| executable_common_sense_tests_v4 | 0.684 | 0.586 | 0.205 | 0.318 | 0.223 | 0.044 |
| conformal_risk_filter | 0.598 | 0.255 | 0.310 | 0.195 | 0.184 | 0.208 |
| human_oracle_query_policy | 0.610 | 0.746 | 0.513 | 0.232 | 0.174 | 0.126 |
| risk_bounded_executable_common_sense_tests_v5 | 0.545 | 0.651 | 0.449 | 0.378 | 0.206 | -0.103 |

Expanded evidence inventory:

- Main rollout rows: 322,560.
- Dataset summary rows: 23,040.
- Main seed-metric rows: 1,120.
- Main aggregate metric rows: 1,568.
- Main paired rows: 1,344.
- Hard aggregate seed rows: 140.
- Hard aggregate metric rows: 196.
- Hard aggregate paired rows: 168.
- Ablation rollout rows: 115,200.
- Stress raw rows: 259,200.
- Fixed-risk raw rows: 138,240.
- Negative cases: 24.

Frozen gate failures:

- `success_gate=False`
- `diagnosis_gate=False`
- `safety_gate=False`
- `regret_gate=False`
- `utility_gate=False`
- `false_reject_gate=False`
- `fixed_risk_gate=False`
- `scope_gate=False`

The correct terminal decision is archive/kill. The benchmark is useful as a negative result and as a revival specification, but the paper should not be submitted to ICLR main in this state.

## Reproduce

```powershell
python src\run_experiment.py
python scripts\generate_manuscript.py
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
cd ..
Copy-Item -LiteralPath paper\main.pdf -Destination C:\Users\wangz\Downloads\96.pdf -Force
python scripts\validate_submission_artifacts.py
```

Canonical local PDF: `C:/Users/wangz/Downloads/96.pdf`

Final PDF SHA256: `492889C4112439872136EF409497C19C991C833C7A825D3533D2828D62D4DFD2`

No PDF should be copied to the visible Desktop.
