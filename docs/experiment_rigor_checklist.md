# Experiment Rigor Checklist

## Completed In v4

- [x] Concrete pre-execution rebuild plan.
- [x] Hostile prior-work pressure from the shared robotics literature pool.
- [x] Paper-specific executable common-sense affordance benchmark.
- [x] Five tasks: stackable object placement, liquid transfer, tool reachability, door/drawer opening, and cluttered navigation.
- [x] Seven physical assumption families.
- [x] Five splits: nominal household, visual ambiguity, counterintuitive physics, language-goal ambiguity, and combined common-sense stress.
- [x] Nine methods including direct VLM policy, LLM replanning, sequential 3D affordance reasoning, uncertainty probing, model-to-model deliberation, failure retrieval, human-query policy, proposed executable tests, and oracle.
- [x] Seven deterministic seeds.
- [x] Per-task/per-assumption/per-seed metrics.
- [x] 95 percent confidence intervals.
- [x] Paired task/assumption/seed comparison against the strongest non-oracle baseline.
- [x] Ablations for executable probe, assumption parser, cost model, calibration, language-only, and geometry-only variants.
- [x] Stress sweep across visual ambiguity, counterintuitive physics, language ambiguity, sensor noise, test cost, and combined maximum stress.
- [x] Failure-case analysis.
- [x] Numeric hygiene audit: no NaN or Inf values in generated CSVs.
- [x] Paper-specific figures and LaTeX tables.

## Still Missing For ICLR Main

- [ ] Real robot validation.
- [ ] High-fidelity simulator benchmark.
- [ ] Trained model checkpoints.
- [ ] Integrated external baseline codebases.
- [ ] Manual full-paper related-work synthesis beyond the local hostile pool.
- [ ] Hardware videos or qualitative rollouts.

Decision: KILL_ARCHIVE. The local benchmark is rigorous enough to falsify the generated claim, not enough to revive it as an ICLR-main submission.
