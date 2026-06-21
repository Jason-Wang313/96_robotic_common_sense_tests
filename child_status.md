# Child Status 96

Current stage: ICLR main v5 expanded hostile-review audit terminal
Last update: 2026-06-22
PDF: C:/Users/wangz/Downloads/96.pdf
PDF SHA256: 492889C4112439872136EF409497C19C991C833C7A825D3533D2828D62D4DFD2
GitHub: https://github.com/Jason-Wang313/96_robotic_common_sense_tests
Submission-hardening version: v5 expanded audit
Terminal decision: KILL_ARCHIVE
ICLR main ready: no

Evidence digest:

- 10 seeds, 6 tasks, 8 physical assumption families, 8 splits, 14 methods.
- 322,560 main rollout rows, 115,200 ablation rollout rows, 259,200 stress-sweep rows, 138,240 fixed-risk rows, and 24 mined negative cases.
- 30-page ICLR-style PDF with bright boxed clickable citations.
- Strongest hard-aggregate success reference: `executable_common_sense_tests_v4` with task success 0.68351.
- Strongest hard-aggregate utility reference: `conformal_risk_filter` with robust utility 0.20773.
- V5: task success 0.54514, diagnosis 0.65052, unsafe recall 0.44944, false rejection 0.50990, physical violation 0.37830, regret 0.20551, robust utility -0.10301.

Reason:

Risk-bounded executable common-sense tests improve the mechanism relative to stripped ablations, but the final claim still fails. V5 loses success, diagnosis/recall, safety, regret, utility, false-rejection, fixed-risk, and scope gates. The archive decision is evidence-based, not a page-count or formatting failure.
