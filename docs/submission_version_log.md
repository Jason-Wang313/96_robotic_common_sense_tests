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
- Recompiled and reran the full benchmark without reducing experimental quality.
- Audited regenerated CSV row counts, coverage, paired statistics, ablations, maximum-stress results, and failure cases.
- Reconfirmed KILL_ARCHIVE: the proposed method remains lower-cost/no-human-burden but loses success, safety, recall, and regret to human-query policy, and two ablations beat the full method.
