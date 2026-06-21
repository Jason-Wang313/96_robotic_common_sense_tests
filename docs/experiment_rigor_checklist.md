# Experiment Rigor Checklist

## Completed In v5 Expanded Audit

- [x] Bulletproof expanded submission-readiness plan before executing v5.
- [x] Hostile prior-work pressure from the shared robotics literature pool.
- [x] Paper-specific executable common-sense affordance benchmark.
- [x] Six tasks: stackable object placement, liquid transfer, tool reachability, door/drawer opening, cluttered navigation, and fragile/deformable packing.
- [x] Eight physical assumption families.
- [x] Eight splits: nominal household, visual ambiguity, counterintuitive physics, language ambiguity, sensor noise, tool geometry, low-signal stress, and combined common-sense stress.
- [x] Fourteen methods including direct VLM, LLM replanning, sequential 3D affordance reasoning, uncertainty probing, model deliberation, failure retrieval, calibrated affordance without tests, active perception, conformal risk filtering, human-query policy, policy repair, v4, v5, and oracle.
- [x] Ten deterministic seeds.
- [x] Raw episode-level main rollout evidence: 322,560 rows.
- [x] Per-seed, per-split, per-method aggregate metrics.
- [x] 95 percent confidence intervals.
- [x] Paired seed comparisons against all non-oracle baselines.
- [x] Ablations for executable probe, assumption parser, cost model, calibration, risk bound, counterfactual rollout, language-only, geometry-only, and active-perception-only variants.
- [x] Stress sweep across six stress levels.
- [x] Fixed-risk deployment at budgets 0.00, 0.05, 0.10, and 0.15.
- [x] Negative-case mining over hard splits.
- [x] Numeric hygiene audit through `scripts/validate_submission_artifacts.py`.
- [x] Paper-specific figures and LaTeX tables.
- [x] 30-page ICLR-style PDF with bright boxed clickable citations.

## Still Missing For ICLR Main

- [ ] Real robot validation.
- [ ] High-fidelity simulator benchmark.
- [ ] Trained model checkpoints.
- [ ] Integrated external baseline codebases.
- [ ] Independent third-party reproduction.
- [ ] Hardware videos or qualitative rollouts.

Decision: KILL_ARCHIVE. The local benchmark is rigorous enough to falsify the generated claim, not enough to revive it as an ICLR-main submission.
