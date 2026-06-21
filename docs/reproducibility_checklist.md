# Reproducibility Checklist

## What Reproduces

- [x] `python -m py_compile src/run_experiment.py`
- [x] `python src/run_experiment.py`
- [x] `results/rollouts.csv`
- [x] `results/dataset_summary.csv`
- [x] `results/raw_seed_metrics.csv`
- [x] `results/metrics.csv`
- [x] `results/pairwise_stats.csv`
- [x] `results/hard_aggregate_seed_metrics.csv`
- [x] `results/hard_aggregate_metrics.csv`
- [x] `results/hard_aggregate_pairwise_stats.csv`
- [x] `results/ablation_rollouts.csv`
- [x] `results/ablation_metrics.csv`
- [x] `results/stress_sweep_raw.csv`
- [x] `results/stress_sweep.csv`
- [x] `results/fixed_risk_raw.csv`
- [x] `results/fixed_risk_metrics.csv`
- [x] `results/negative_cases.csv`
- [x] `figures/common_sense_hard_success_regret_v5.png`
- [x] `figures/common_sense_diagnosis_quality_v5.png`
- [x] `figures/common_sense_ablation_v5.png`
- [x] `figures/common_sense_stress_sweep_v5.png`
- [x] `figures/common_sense_fixed_risk_v5.png`
- [x] `figures/common_sense_pareto_v5.png`
- [x] `python scripts/generate_manuscript.py`
- [x] `paper/main.tex`
- [x] `paper/references.bib`
- [x] `python scripts/validate_submission_artifacts.py`
- [x] Canonical PDF target: `C:/Users/wangz/Downloads/96.pdf`
- [x] Final PDF SHA256: `492889C4112439872136EF409497C19C991C833C7A825D3533D2828D62D4DFD2`

## What Does Not Reproduce

- [ ] Real robot results.
- [ ] High-fidelity simulator runs.
- [ ] Trained model checkpoints.
- [ ] Integrated external baseline codebases.
- [ ] Hardware videos.

This is reproducible as a negative evidence audit and archive memo, not as an ICLR-main robotics system paper.
