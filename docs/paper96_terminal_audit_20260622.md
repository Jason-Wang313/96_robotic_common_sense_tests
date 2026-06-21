# Paper 96 Terminal Audit - 2026-06-22

Paper: `96_robotic_common_sense_tests`

Terminal decision: `KILL_ARCHIVE`

## Final Commands Run

- `python -m py_compile src\run_experiment.py`
- `python src\run_experiment.py`
- `python -m py_compile scripts\generate_manuscript.py scripts\validate_submission_artifacts.py`
- `python scripts\generate_manuscript.py`
- `pdflatex`, `bibtex`, and final `pdflatex` passes in `paper/`
- `Copy-Item -LiteralPath paper\main.pdf -Destination C:\Users\wangz\Downloads\96.pdf -Force`
- `python scripts\validate_submission_artifacts.py`
- `pdftoppm` visual render of `C:\Users\wangz\Downloads\96.pdf`

## Final Validator Result

`validated Paper 96 artifacts: pages=30, sha256=492889C4112439872136EF409497C19C991C833C7A825D3533D2828D62D4DFD2`

## Visual QA

- Page 1: title, abstract, terminal decision, and bright green citation boxes are legible.
- Page 3: hard aggregate table and hard success/regret figure are legible.
- Page 7: fixed-risk table and coverage plot are legible.
- Page 14: citation wall is chunked into local bright green boxes without page-sized border artifacts.
- Page 15: citation wall continuation is legible.
- Page 30: bibliography tail and blue URL boxes are legible.

## Downloads/Desktop Constraint

- Required numbered PDF exists at `C:/Users/wangz/Downloads/96.pdf`.
- No visible Desktop copy exists at `C:/Users/wangz/Desktop/96.pdf`.

## Publication State

Repo target: `https://github.com/Jason-Wang313/96_robotic_common_sense_tests`

Root ledgers must be updated only after the Paper 96 repo is committed, pushed, and verified public.
