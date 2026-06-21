# Submission Version Log

## v1 - Generated Draft

- Original continuation-batch generated paper and toy single-seed experiment.

## v2 - Submission Hardening

- Added hostile reviewer attack log and response docs.
- Replaced the toy experiment with seven-seed metrics, stronger baselines, ablations, stress tests, and negative cases.
- Narrowed claims to synthetic diagnostic evidence.
- Recompiled canonical PDF at `C:/Users/wangz/Downloads/96.pdf`.
- Terminal decision: WORKSHOP_ONLY.

## v3 - ICLR Main Gate Archive

- Applied the stricter ICLR-main-conference standard.
- Re-read local paper, docs, experiments, prior-work artifacts, PDF state, and repo state.
- Determined that missing real-robot/high-fidelity evidence, template-generated experiments, and unresolved novelty threats were not recoverable from local artifacts.
- Recompiled the canonical PDF with `Submission-hardening version: v3`.
- Terminal decision: KILL_ARCHIVE.

## v4 - Paper-Specific Evidence Audit

- Added a concrete Paper 96 rebuild plan before experiments.
- Replaced the generic probability scaffold with a deterministic executable-common-sense benchmark.
- Tested five tasks, seven assumption families, five splits, nine methods, seven seeds, ablations, stress sweeps, paired comparisons, and failure cases.
- Generated paper-specific figures and LaTeX tables.
- Found that executable tests beat non-human baselines but lose to human-query policy and are contradicted by ablations.
- Terminal decision remains: KILL_ARCHIVE.

## v4.1 - Continuation Rerun Audit

- Added `docs/paper96_iclr_submission_execution_plan_20260615.md` before rerunning.
- Recompiled and reran the full v4 benchmark without reducing experimental quality.
- Reconfirmed KILL_ARCHIVE.

## v5 - Expanded Hostile-Review Audit

- Added `docs/paper96_expanded_submission_plan_20260622.md` before execution.
- Expanded to 10 seeds, 6 tasks, 8 assumption families, 8 splits, and 14 methods.
- Added raw rollout evidence, hard aggregates, paired tests, ablations, stress sweep, fixed-risk deployment, and negative-case mining.
- Generated 322,560 main rollouts, 115,200 ablation rollouts, 259,200 stress rows, and 138,240 fixed-risk rows.
- Added `scripts/generate_manuscript.py` and `scripts/validate_submission_artifacts.py`.
- Generated a 30-page PDF with bright boxed clickable citations.
- Final PDF SHA256: `492889C4112439872136EF409497C19C991C833C7A825D3533D2828D62D4DFD2`.
- Reconfirmed KILL_ARCHIVE: v5 fails success, diagnosis/recall, safety, regret, utility, false-rejection, fixed-risk, and scope gates.
