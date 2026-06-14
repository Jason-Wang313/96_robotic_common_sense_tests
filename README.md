# 96 Robotic Common-Sense Tests

Submission-hardening version: v4

Terminal decision: KILL_ARCHIVE for ICLR main conference.

This repository is a negative evidence audit for the generated robotics idea:

> Turn common-sense physical assumptions into executable affordance tests.

The v4 rebuild tests the strongest defensible version of the idea: a robot should convert physical assumptions into low-cost executable probes that reject unsafe affordances before committing to manipulation or navigation.

The tests help relative to pure VLM/LLM/affordance baselines, but they do not clear the ICLR-main gate. Under combined common-sense stress, the human-query policy has higher success, lower violations, lower damage, and lower regret:

| Method | Task success | Unsafe recall | Physical violation | Damage/spill/collision | Cost | Human burden |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| human_oracle_query_policy | 0.633 +/- 0.007 | 0.457 | 0.292 | 0.079 | 0.040 | 0.377 |
| proposed_executable_common_sense_tests | 0.567 +/- 0.008 | 0.419 | 0.318 | 0.094 | 0.015 | 0.000 |

Paired comparison against human-query policy over 245 task/assumption/seed groups:

- Task success diff: -0.06600 +/- 0.01009.
- Physical-violation diff: +0.02662 +/- 0.00856.
- Damage/spill/collision diff: +0.01526 +/- 0.00538.
- Test/query cost diff: -0.02483 +/- 0.00070.
- Human-query burden diff: -0.37695 +/- 0.00643.
- Planning-regret diff: +0.03144 +/- 0.00281.
- Unsafe-recall diff: -0.03870 +/- 0.01062.

The proposed method is lower-cost and avoids human burden, but it loses the main success/safety/regret gate and has high false rejections. It is therefore archived rather than submitted.

## Reproduce

```powershell
python src\run_experiment.py
```

The script writes:

- `results/metrics.csv`
- `results/per_task_assumption_metrics.csv`
- `results/seed_task_assumption_metrics.csv`
- `results/ablation_metrics.csv`
- `results/stress_sweep.csv`
- `results/pairwise_stats.csv`
- `results/failure_cases.csv`
- `figures/common_sense_*.png`

## Rebuild Archive PDF

```powershell
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Canonical local PDF: `C:/Users/wangz/Downloads/96.pdf`

No PDF should be copied to the visible Desktop.
