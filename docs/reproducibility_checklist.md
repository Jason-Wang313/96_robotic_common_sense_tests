# Reproducibility Checklist

## What Reproduces

- [x] `python -m py_compile src/run_experiment.py`
- [x] `python src/run_experiment.py`
- [x] `results/metrics.csv`
- [x] `results/per_task_assumption_metrics.csv`
- [x] `results/seed_task_assumption_metrics.csv`
- [x] `results/ablation_metrics.csv`
- [x] `results/ablation_seed_metrics.csv`
- [x] `results/stress_sweep.csv`
- [x] `results/stress_sweep_seed_metrics.csv`
- [x] `results/pairwise_stats.csv`
- [x] `results/failure_cases.csv`
- [x] `results/combined_stress_table.tex`
- [x] `results/ablation_table.tex`
- [x] `results/pairwise_decision_table.tex`
- [x] `figures/common_sense_diagnosis_quality.png`
- [x] `figures/common_sense_task_outcomes.png`
- [x] `figures/common_sense_cost_regret.png`
- [x] `figures/common_sense_ablation.png`
- [x] `figures/common_sense_stress_sweep.png`
- [x] `paper/main.tex`
- [x] Canonical PDF target: `C:/Users/wangz/Downloads/96.pdf`

## What Does Not Reproduce

- [ ] Real robot results.
- [ ] High-fidelity simulator runs.
- [ ] Trained model checkpoints.
- [ ] Integrated external baseline codebases.
- [ ] Hardware videos.

This is reproducible as a negative evidence audit and archive memo, not as an ICLR-main robotics system paper.
