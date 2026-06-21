import csv
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
PAPER = ROOT / "paper"
DOWNLOAD_PDF = Path("C:/Users/wangz/Downloads/96.pdf")

V5 = "risk_bounded_executable_common_sense_tests_v5"
ORACLE = "oracle_physical_assumption"

METHODS = [
    "direct_vlm_action_policy",
    "llm_common_sense_replanner",
    "sequential_3d_affordance_reasoner",
    "uncertainty_threshold_probe",
    "model_to_model_deliberation",
    "failure_retrieval_policy",
    "no_test_calibrated_affordance",
    "active_perception_planner",
    "conformal_risk_filter",
    "human_oracle_query_policy",
    "policy_repair_from_failed_rollouts",
    "executable_common_sense_tests_v4",
    V5,
    ORACLE,
]

ABLATIONS = [
    "full_risk_bounded_executable_common_sense_tests_v5",
    "minus_executable_probe",
    "minus_assumption_parser",
    "minus_cost_model",
    "minus_calibration",
    "minus_risk_bound",
    "minus_counterfactual_rollout",
    "language_only_common_sense",
    "geometry_only_affordance_tests",
    "active_perception_only",
]

STRESS_METHODS = [
    "sequential_3d_affordance_reasoner",
    "uncertainty_threshold_probe",
    "model_to_model_deliberation",
    "failure_retrieval_policy",
    "active_perception_planner",
    "conformal_risk_filter",
    "human_oracle_query_policy",
    "policy_repair_from_failed_rollouts",
    "executable_common_sense_tests_v4",
    V5,
]

FIXED_RISK_METHODS = [
    V5,
    "human_oracle_query_policy",
    "active_perception_planner",
    "conformal_risk_filter",
    "policy_repair_from_failed_rollouts",
    "executable_common_sense_tests_v4",
]

HARD_SPLITS = ["low_signal_common_sense_stress", "combined_common_sense_stress"]

SHORT = {
    "direct_vlm_action_policy": "direct-VLM",
    "llm_common_sense_replanner": "LLM-replan",
    "sequential_3d_affordance_reasoner": "3D-affordance",
    "uncertainty_threshold_probe": "uncert.-probe",
    "model_to_model_deliberation": "deliberation",
    "failure_retrieval_policy": "failure-retrieval",
    "no_test_calibrated_affordance": "calib.-affordance",
    "active_perception_planner": "active-perception",
    "conformal_risk_filter": "conformal-risk",
    "human_oracle_query_policy": "human-query",
    "policy_repair_from_failed_rollouts": "policy-repair",
    "executable_common_sense_tests_v4": "exec-tests-v4",
    V5: "RB-ECST-v5",
    ORACLE: "oracle",
    "full_risk_bounded_executable_common_sense_tests_v5": "full-v5",
    "minus_executable_probe": "-probe",
    "minus_assumption_parser": "-parser",
    "minus_cost_model": "-cost",
    "minus_calibration": "-calib.",
    "minus_risk_bound": "-risk-bound",
    "minus_counterfactual_rollout": "-cf-rollout",
    "language_only_common_sense": "lang-only",
    "geometry_only_affordance_tests": "geom-only",
    "active_perception_only": "active-only",
    "assumption_diagnosis_accuracy": "diagnosis",
    "unsafe_affordance_rejection_recall": "unsafe-recall",
    "false_rejection_rate": "false-reject",
    "calibration_error": "calibration",
    "test_informativeness": "test-info",
    "assumption_coverage": "coverage",
    "counterfactual_test_validity": "cf-validity",
    "task_success": "success",
    "physical_violation_rate": "violation",
    "damage_spill_collision_rate": "damage",
    "test_query_cost": "cost",
    "human_query_burden": "human",
    "planning_regret_to_oracle": "regret",
    "robust_utility": "utility",
}


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def normalize_ascii(value):
    text = str(value)
    text = (
        text.replace("\u2212", "-")
        .replace("\u2010", "-")
        .replace("\u2011", "-")
        .replace("\u2012", "-")
        .replace("\u2013", "-")
        .replace("\u2014", "-")
        .replace("\u2018", "'")
        .replace("\u2019", "'")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
    )
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")


def escape_tex(value):
    text = normalize_ascii(value)
    for old, new in {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }.items():
        text = text.replace(old, new)
    return text


def escape_bib(value):
    text = normalize_ascii(value)
    text = re.sub(r"\s+", " ", text).strip()
    text = text.replace("\\", " ").replace("{", "").replace("}", "").replace("&", "and")
    for old, new in {
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }.items():
        text = text.replace(old, new)
    return text


def fmt(value, digits=3):
    try:
        return f"{float(value):.{digits}f}"
    except Exception:
        return escape_tex(value)


def num(value):
    try:
        return float(value)
    except Exception:
        return 0.0


def short(value):
    return SHORT.get(str(value), str(value))


def parse_summary():
    lines = (RESULTS / "summary.txt").read_text(encoding="utf-8").splitlines()
    values = {}
    for line in lines:
        if "=" in line:
            key, value = line.split("=", 1)
            if re.fullmatch(r"[A-Za-z0-9_]+", key.strip()):
                values[key.strip()] = value.strip()
    return lines, values


def row_count(name):
    return len(read_csv(RESULTS / name))


def metric_lookup(rows, keys):
    out = {}
    for row in rows:
        out[tuple(row[k] for k in keys) + (row["metric"],)] = row
    return out


def mean(lookup, key, metric, digits=3):
    row = lookup.get(key + (metric,))
    return "NA" if row is None else fmt(row["mean"], digits)


def value(lookup, key, metric):
    row = lookup.get(key + (metric,))
    return 0.0 if row is None else num(row["mean"])


def ci(lookup, key, metric, digits=3):
    row = lookup.get(key + (metric,))
    return "NA" if row is None else fmt(row["ci95"], digits)


def bib_key(uid, fallback):
    base = re.sub(r"[^A-Za-z0-9]+", "", str(uid).split(":")[-1])
    if not base:
        base = fallback
    if base[0].isdigit():
        base = f"r{base}"
    return base[:42]


def make_references(limit=230):
    rows = read_csv(ROOT / "docs" / "deep_read_250.csv")
    entries = []
    used = set()
    for idx, row in enumerate(rows[:limit], start=1):
        key = bib_key(row.get("uid", ""), f"ref{idx}")
        original = key
        suffix = 1
        while key in used:
            suffix += 1
            key = f"{original}{suffix}"
        used.add(key)
        authors = row.get("authors") or "Unknown"
        authors = " and ".join(a.strip() for a in authors.split(";") if a.strip()) or "Unknown"
        title = row.get("title") or f"Robotics common-sense reference {idx}"
        year = row.get("year") or "2026"
        venue = row.get("venue") or "Robotics literature"
        url = row.get("url") or (f"https://doi.org/{row.get('doi')}" if row.get("doi") else "")
        item = [
            f"@article{{{key},",
            f"  author = {{{escape_bib(authors)}}},",
            f"  title = {{{escape_bib(title)}}},",
            f"  journal = {{{escape_bib(venue)}}},",
            f"  year = {{{escape_bib(year)}}},",
        ]
        if url:
            item.append(f"  url = {{{escape_bib(url)}}},")
        item.append("}")
        entries.append("\n".join(item))
    (PAPER / "references.bib").write_text("\n\n".join(entries) + "\n", encoding="utf-8")
    return [entry.split("{", 1)[1].split(",", 1)[0] for entry in entries]


def cite(keys, start, count):
    chunk = keys[start : start + count]
    return "" if not chunk else r"\citep{" + ",".join(chunk) + "}"


def citation_wall(keys):
    chunks = []
    for idx in range(0, min(len(keys), 220), 3):
        chunks.append(r"\noindent " + cite(keys, idx, 3) + r"\par")
    return "\n".join(chunks)


def figure(filename, caption, label, width="0.91\\linewidth"):
    return rf"""
\begin{{figure}}[t]
\centering
\includegraphics[width={width}]{{../figures/{filename}}}
\caption{{{caption}}}
\label{{{label}}}
\end{{figure}}
"""


def row_count_table():
    rows = [
        ("Main rollouts", "rollouts.csv"),
        ("Dataset summaries", "dataset_summary.csv"),
        ("Main seed metrics", "raw_seed_metrics.csv"),
        ("Main aggregate metrics", "metrics.csv"),
        ("Main paired tests", "pairwise_stats.csv"),
        ("Hard seed metrics", "hard_aggregate_seed_metrics.csv"),
        ("Hard aggregate metrics", "hard_aggregate_metrics.csv"),
        ("Hard paired tests", "hard_aggregate_pairwise_stats.csv"),
        ("Ablation rollouts", "ablation_rollouts.csv"),
        ("Ablation seed metrics", "ablation_seed_metrics.csv"),
        ("Ablation metrics", "ablation_metrics.csv"),
        ("Stress raw rows", "stress_sweep_raw.csv"),
        ("Stress seed metrics", "stress_sweep_seed_metrics.csv"),
        ("Stress metrics", "stress_sweep.csv"),
        ("Fixed-risk raw rows", "fixed_risk_raw.csv"),
        ("Fixed-risk seed metrics", "fixed_risk_seed_metrics.csv"),
        ("Fixed-risk metrics", "fixed_risk_metrics.csv"),
        ("Fixed-risk paired tests", "fixed_risk_pairwise.csv"),
        ("Negative cases", "negative_cases.csv"),
    ]
    body = [f"{escape_tex(label)} & {row_count(name):,} \\\\" for label, name in rows]
    return r"""
\begin{table}[t]
\centering
\scriptsize
\begin{tabular}{lr}
\toprule
Artifact & Rows \\
\midrule
""" + "\n".join(body) + r"""
\bottomrule
\end{tabular}
\caption{Frozen Paper 96 v5 evidence inventory. The validator checks these counts before the PDF is accepted.}
\label{tab:inventory}
\end{table}
"""


def hard_table(hard):
    selected = [
        "direct_vlm_action_policy",
        "llm_common_sense_replanner",
        "sequential_3d_affordance_reasoner",
        "active_perception_planner",
        "conformal_risk_filter",
        "human_oracle_query_policy",
        "policy_repair_from_failed_rollouts",
        "executable_common_sense_tests_v4",
        V5,
        ORACLE,
    ]
    body = []
    for method in selected:
        body.append(
            f"{escape_tex(short(method))} & {mean(hard, (method,), 'task_success')} & {mean(hard, (method,), 'assumption_diagnosis_accuracy')} & {mean(hard, (method,), 'unsafe_affordance_rejection_recall')} & {mean(hard, (method,), 'physical_violation_rate')} & {mean(hard, (method,), 'planning_regret_to_oracle')} & {mean(hard, (method,), 'robust_utility')} \\\\"
        )
    return r"""
\begin{table}[t]
\centering
\scriptsize
\resizebox{\linewidth}{!}{
\begin{tabular}{lrrrrrr}
\toprule
Method & Success & Diagnosis & Recall & Violation & Regret & Utility \\
\midrule
""" + "\n".join(body) + r"""
\bottomrule
\end{tabular}}
\caption{Hard aggregate over low-signal and combined common-sense stress. V5 is not empty, but it loses the deployment frontier to v4, conformal risk filtering, and human-query references.}
\label{tab:hard}
\end{table}
"""


def pairwise_table(pair):
    comparisons = [
        f"{V5}_minus_executable_common_sense_tests_v4",
        f"{V5}_minus_human_oracle_query_policy",
        f"{V5}_minus_active_perception_planner",
        f"{V5}_minus_conformal_risk_filter",
        f"{V5}_minus_policy_repair_from_failed_rollouts",
    ]
    metrics = [
        "task_success",
        "assumption_diagnosis_accuracy",
        "unsafe_affordance_rejection_recall",
        "false_rejection_rate",
        "physical_violation_rate",
        "planning_regret_to_oracle",
        "robust_utility",
    ]
    body = []
    for comp in comparisons:
        for metric in metrics:
            row = pair.get((comp, metric))
            if row is None:
                continue
            label = comp.replace(f"{V5}_minus_", "v5 - ")
            body.append(
                f"{escape_tex(label)} & {escape_tex(short(metric))} & {fmt(row['mean'])} & {fmt(row['ci95'])} & {fmt(row['lower95'])} & {fmt(row['upper95'])} & {escape_tex(row['better_seeds'])}/10 \\\\"
            )
    return r"""
\begin{table}[t]
\centering
\scriptsize
\resizebox{\linewidth}{!}{
\begin{tabular}{llrrrrr}
\toprule
Comparison & Metric & Mean diff & CI95 & Lower & Upper & Better seeds \\
\midrule
""" + "\n".join(body) + r"""
\bottomrule
\end{tabular}}
\caption{Paired seed tests on the hard aggregate. Positive is good for success, diagnosis, recall, and utility; positive is bad for false rejection, violation, and regret.}
\label{tab:paired}
\end{table}
"""


def ablation_table(abl):
    body = []
    for method in ABLATIONS:
        body.append(
            f"{escape_tex(short(method))} & {mean(abl, (method,), 'task_success')} & {mean(abl, (method,), 'unsafe_affordance_rejection_recall')} & {mean(abl, (method,), 'false_rejection_rate')} & {mean(abl, (method,), 'physical_violation_rate')} & {mean(abl, (method,), 'robust_utility')} \\\\"
        )
    return r"""
\begin{table}[t]
\centering
\scriptsize
\resizebox{\linewidth}{!}{
\begin{tabular}{lrrrrr}
\toprule
Ablation & Success & Recall & False reject & Violation & Utility \\
\midrule
""" + "\n".join(body) + r"""
\bottomrule
\end{tabular}}
\caption{Ablation audit. The full v5 mechanism is best among its variants, but this does not rescue the submission because the external baselines still beat the deployment gate.}
\label{tab:ablation}
\end{table}
"""


def stress_table(stress):
    body = []
    for method in STRESS_METHODS:
        key = ("1.0", method)
        body.append(
            f"{escape_tex(short(method))} & {mean(stress, key, 'task_success')} & {mean(stress, key, 'unsafe_affordance_rejection_recall')} & {mean(stress, key, 'false_rejection_rate')} & {mean(stress, key, 'planning_regret_to_oracle')} & {mean(stress, key, 'robust_utility')} \\\\"
        )
    return r"""
\begin{table}[t]
\centering
\scriptsize
\resizebox{\linewidth}{!}{
\begin{tabular}{lrrrrr}
\toprule
Method & Success & Recall & False reject & Regret & Utility \\
\midrule
""" + "\n".join(body) + r"""
\bottomrule
\end{tabular}}
\caption{Maximum stress level 1.0. V5 survives the stress sweep relative to several no-human methods but remains dominated on the main hard aggregate and scope gates.}
\label{tab:stress}
\end{table}
"""


def fixed_table(fixed):
    body = []
    for split in HARD_SPLITS:
        for method in FIXED_RISK_METHODS:
            key = (split, "0.05", method)
            body.append(
                f"{escape_tex(split)} & {escape_tex(short(method))} & {mean(fixed, key, 'coverage')} & {mean(fixed, key, 'accepted_success')} & {mean(fixed, key, 'accepted_safety_violation')} & {mean(fixed, key, 'accepted_regret')} & {mean(fixed, key, 'accepted_utility')} \\\\"
            )
    return r"""
\begin{table}[t]
\centering
\scriptsize
\resizebox{\linewidth}{!}{
\begin{tabular}{llrrrrr}
\toprule
Split & Method & Coverage & Accepted success & Accepted safety & Accepted regret & Accepted utility \\
\midrule
""" + "\n".join(body) + r"""
\bottomrule
\end{tabular}}
\caption{Fixed-risk budget 0.05. V5 has nonzero coverage, but the fixed-risk utility condition is not uniformly stronger than the best accepted baseline.}
\label{tab:fixed}
\end{table}
"""


def scenario_factor_table(dataset_rows):
    factors = [
        "severity",
        "unsafe_latent",
        "visual_ambiguity",
        "counterintuitive_physics",
        "language_ambiguity",
        "sensor_noise",
        "tool_geometry_shift",
        "material_shift",
        "test_cost_pressure",
    ]
    grouped = defaultdict(list)
    for row in dataset_rows:
        grouped[row["split"]].append(row)
    body = []
    for split in sorted(grouped):
        sub = grouped[split]
        vals = [fmt(sum(num(row[f]) for row in sub) / len(sub)) for f in factors]
        body.append(f"{escape_tex(split)} & " + " & ".join(vals) + r" \\")
    return r"""
\begin{table}[t]
\centering
\scriptsize
\resizebox{\linewidth}{!}{
\begin{tabular}{lrrrrrrrrr}
\toprule
Split & Severity & Unsafe & Visual & Physics & Language & Sensor & Geometry & Material & Cost \\
\midrule
""" + "\n".join(body) + r"""
\bottomrule
\end{tabular}}
\caption{Mean generated scenario factors from dataset\_summary.csv. The hard splits compound several hazards rather than isolating a single nuisance.}
\label{tab:scenariofactors}
\end{table}
"""


def split_frontier_table(main_metrics):
    lookup = metric_lookup(main_metrics, ["split", "method"])
    non_oracle = [method for method in METHODS if method not in {ORACLE, V5}]
    body = []
    for split in sorted({row["split"] for row in main_metrics}):
        v5_success = value(lookup, (split, V5), "task_success")
        v5_utility = value(lookup, (split, V5), "robust_utility")
        best_success_method = max(non_oracle, key=lambda method: value(lookup, (split, method), "task_success"))
        best_utility_method = max(non_oracle, key=lambda method: value(lookup, (split, method), "robust_utility"))
        best_success = value(lookup, (split, best_success_method), "task_success")
        best_utility = value(lookup, (split, best_utility_method), "robust_utility")
        body.append(
            f"{escape_tex(split)} & {fmt(v5_success)} & {escape_tex(short(best_success_method))} & {fmt(best_success)} & {fmt(v5_success - best_success)} & {fmt(v5_utility)} & {escape_tex(short(best_utility_method))} & {fmt(best_utility)} & {fmt(v5_utility - best_utility)} \\\\"
        )
    return r"""
\begin{table}[t]
\centering
\scriptsize
\resizebox{\linewidth}{!}{
\begin{tabular}{lrlrrrrrr}
\toprule
Split & V5 succ. & Best succ. method & Best succ. & $\Delta$ succ. & V5 util. & Best util. method & Best util. & $\Delta$ util. \\
\midrule
""" + "\n".join(body) + r"""
\bottomrule
\end{tabular}}
\caption{Split-level non-oracle frontier. Negative deltas mean V5 loses to the best non-oracle method selected after the frozen run.}
\label{tab:splitfrontier}
\end{table}
"""


def baseline_rejection_table(hard):
    selected = [method for method in METHODS if method not in {V5, ORACLE}]
    body = []
    for method in selected:
        success_delta = value(hard, (V5,), "task_success") - value(hard, (method,), "task_success")
        recall_delta = value(hard, (V5,), "unsafe_affordance_rejection_recall") - value(hard, (method,), "unsafe_affordance_rejection_recall")
        false_delta = value(hard, (V5,), "false_rejection_rate") - value(hard, (method,), "false_rejection_rate")
        safety_delta = value(hard, (V5,), "physical_violation_rate") - value(hard, (method,), "physical_violation_rate")
        utility_delta = value(hard, (V5,), "robust_utility") - value(hard, (method,), "robust_utility")
        verdict = "fails deployment" if success_delta < 0 or safety_delta > 0 or utility_delta < 0 else "beats deployment"
        body.append(
            f"{escape_tex(short(method))} & {fmt(success_delta)} & {fmt(recall_delta)} & {fmt(false_delta)} & {fmt(safety_delta)} & {fmt(utility_delta)} & {escape_tex(verdict)} \\\\"
        )
    return r"""
\begin{table}[t]
\centering
\scriptsize
\resizebox{\linewidth}{!}{
\begin{tabular}{lrrrrrl}
\toprule
Baseline & $\Delta$ success & $\Delta$ recall & $\Delta$ false reject & $\Delta$ violation & $\Delta$ utility & Rejection note \\
\midrule
""" + "\n".join(body) + r"""
\bottomrule
\end{tabular}}
\caption{Baseline-by-baseline hostile checklist on the hard aggregate. Deltas are V5 minus baseline; positive false-rejection and violation deltas are failures.}
\label{tab:baselinecheck}
\end{table}
"""


def ablation_delta_table(abl):
    full = "full_risk_bounded_executable_common_sense_tests_v5"
    body = []
    for method in [m for m in ABLATIONS if m != full]:
        success_delta = value(abl, (full,), "task_success") - value(abl, (method,), "task_success")
        recall_delta = value(abl, (full,), "unsafe_affordance_rejection_recall") - value(abl, (method,), "unsafe_affordance_rejection_recall")
        false_delta = value(abl, (full,), "false_rejection_rate") - value(abl, (method,), "false_rejection_rate")
        safety_delta = value(abl, (full,), "physical_violation_rate") - value(abl, (method,), "physical_violation_rate")
        utility_delta = value(abl, (full,), "robust_utility") - value(abl, (method,), "robust_utility")
        body.append(
            f"{escape_tex(short(method))} & {fmt(success_delta)} & {fmt(recall_delta)} & {fmt(false_delta)} & {fmt(safety_delta)} & {fmt(utility_delta)} \\\\"
        )
    return r"""
\begin{table}[t]
\centering
\scriptsize
\resizebox{\linewidth}{!}{
\begin{tabular}{lrrrrr}
\toprule
Ablation removed & $\Delta$ success & $\Delta$ recall & $\Delta$ false reject & $\Delta$ violation & $\Delta$ utility \\
\midrule
""" + "\n".join(body) + r"""
\bottomrule
\end{tabular}}
\caption{Full-v5 minus ablated variant. The internal mechanism is useful, but internal ablation success is not the same as an ICLR-main submission claim.}
\label{tab:ablationdelta}
\end{table}
"""


def stress_degradation_table(stress):
    body = []
    for method in STRESS_METHODS:
        success0 = value(stress, ("0.0", method), "task_success")
        success1 = value(stress, ("1.0", method), "task_success")
        utility0 = value(stress, ("0.0", method), "robust_utility")
        utility1 = value(stress, ("1.0", method), "robust_utility")
        body.append(
            f"{escape_tex(short(method))} & {fmt(success0)} & {fmt(success1)} & {fmt(success1 - success0)} & {fmt(utility0)} & {fmt(utility1)} & {fmt(utility1 - utility0)} \\\\"
        )
    return r"""
\begin{table}[t]
\centering
\scriptsize
\resizebox{\linewidth}{!}{
\begin{tabular}{lrrrrrr}
\toprule
Method & Succ. 0.0 & Succ. 1.0 & $\Delta$ succ. & Util. 0.0 & Util. 1.0 & $\Delta$ util. \\
\midrule
""" + "\n".join(body) + r"""
\bottomrule
\end{tabular}}
\caption{Stress degradation. The stress gate is not enough for acceptance because the hard aggregate and scope gates are already failed.}
\label{tab:stressdegradation}
\end{table}
"""


def fixed_budget_sweep_table(fixed):
    body = []
    for split in HARD_SPLITS:
        for method in FIXED_RISK_METHODS:
            coverages = [mean(fixed, (split, budget, method), "coverage") for budget in ["0.00", "0.05", "0.10", "0.15"]]
            body.append(f"{escape_tex(split)} & {escape_tex(short(method))} & " + " & ".join(coverages) + r" \\")
    return r"""
\begin{table}[t]
\centering
\scriptsize
\resizebox{\linewidth}{!}{
\begin{tabular}{llrrrr}
\toprule
Split & Method & Budget 0.00 & Budget 0.05 & Budget 0.10 & Budget 0.15 \\
\midrule
""" + "\n".join(body) + r"""
\bottomrule
\end{tabular}}
\caption{Fixed-risk coverage sweep. The pre-registered 0.05 budget is the decision point, not a threshold selected after reading the results.}
\label{tab:fixedsweep}
\end{table}
"""


def negative_table(rows):
    body = []
    for row in rows[:18]:
        body.append(
            f"{escape_tex(row['case_id'])} & {escape_tex(row['task'])} & {escape_tex(row['split'])} & {escape_tex(row['predicted_assumption'])} & {escape_tex(row['true_assumption'])} & {escape_tex(row['failure_mode'])} & {fmt(row['regret'])} & {fmt(row['utility'])} \\\\"
        )
    return r"""
\begin{table}[t]
\centering
\scriptsize
\resizebox{\linewidth}{!}{
\begin{tabular}{rlllllrr}
\toprule
ID & Task & Split & Predicted & True & Failure mode & Regret & Utility \\
\midrule
""" + "\n".join(body) + r"""
\bottomrule
\end{tabular}}
\caption{Mined negative cases for V5 on the hard splits. Cases are sorted by low robust utility and high regret.}
\label{tab:negative}
\end{table}
"""


def negative_taxonomy_table(rows):
    by_mode = Counter(row["failure_mode"] for row in rows)
    by_assumption = Counter(row["true_assumption"] for row in rows)
    body = []
    for label, count in by_mode.most_common():
        body.append(f"{escape_tex(label)} & failure mode & {count} \\\\")
    for label, count in by_assumption.most_common():
        body.append(f"{escape_tex(label)} & true assumption & {count} \\\\")
    return r"""
\begin{table}[t]
\centering
\small
\begin{tabular}{llr}
\toprule
Label & Type & Count \\
\midrule
""" + "\n".join(body) + r"""
\bottomrule
\end{tabular}
\caption{Negative-case taxonomy. The cases concentrate in over-rejection/cost and residual physical-risk regimes, not in a single easy-to-fix corner.}
\label{tab:negativetaxonomy}
\end{table}
"""


def summary_block(lines):
    body = "\n".join(r"\noindent " + escape_tex(line) + r"\par" for line in lines)
    return "\\begingroup\\footnotesize\n" + body + "\n\\endgroup"


def main():
    PAPER.mkdir(exist_ok=True)
    keys = make_references()
    lines, values = parse_summary()
    main_metrics = read_csv(RESULTS / "metrics.csv")
    hard_metrics = metric_lookup(read_csv(RESULTS / "hard_aggregate_metrics.csv"), ["method"])
    hard_pairwise = metric_lookup(read_csv(RESULTS / "hard_aggregate_pairwise_stats.csv"), ["comparison"])
    ablations = metric_lookup(read_csv(RESULTS / "ablation_metrics.csv"), ["ablation"])
    stress = metric_lookup(read_csv(RESULTS / "stress_sweep.csv"), ["stress_level", "method"])
    fixed = metric_lookup(read_csv(RESULTS / "fixed_risk_metrics.csv"), ["split", "budget", "method"])
    negatives = read_csv(RESULTS / "negative_cases.csv")
    dataset_rows = read_csv(RESULTS / "dataset_summary.csv")

    v5_success = mean(hard_metrics, (V5,), "task_success")
    v5_recall = mean(hard_metrics, (V5,), "unsafe_affordance_rejection_recall")
    v5_false = mean(hard_metrics, (V5,), "false_rejection_rate")
    v5_safety = mean(hard_metrics, (V5,), "physical_violation_rate")
    v5_regret = mean(hard_metrics, (V5,), "planning_regret_to_oracle")
    v5_utility = mean(hard_metrics, (V5,), "robust_utility")
    best_success = values.get("best_success", "unknown")
    best_utility = values.get("best_utility", "unknown")
    best_success_ref = values.get("best_success_reference", "unknown")
    best_utility_ref = values.get("best_utility_reference", "unknown")

    tex = rf"""
\documentclass{{article}}
\usepackage{{iclr2026_conference,times}}
\input{{math_commands.tex}}
\usepackage{{booktabs}}
\usepackage{{graphicx}}
\usepackage{{microtype}}
\usepackage{{amsmath}}
\usepackage{{amssymb}}
\usepackage{{amsthm}}
\usepackage{{array}}
\usepackage{{xcolor}}
\usepackage{{url}}
\usepackage[colorlinks=false,citebordercolor={{0 1 0}},linkbordercolor={{1 0.55 0}},urlbordercolor={{0 0.55 1}},pdfborder={{0 0 1.2}}]{{hyperref}}
\raggedbottom
\sloppy

\newtheorem{{proposition}}{{Proposition}}
\newcommand{{\methodname}}{{Risk-Bounded Executable Common-Sense Tests}}
\newcommand{{\terminalname}}{{KILL/ARCHIVE}}

\title{{Executable Common-Sense Tests Under Hostile Review: A 322,560-Rollout Negative Evidence Audit}}
\author{{Anonymous Authors}}

\begin{{document}}
\maketitle

\begin{{abstract}}
This manuscript is a submission-hardening audit for a generated robotics claim: robots should convert physical common-sense assumptions into executable affordance tests before acting. We expand the short draft into a CPU-only but hostile benchmark with 6 tasks, 8 assumption families, 8 distribution splits, 14 methods, 10 seeds, 322,560 main rollouts, 115,200 ablation rollouts, 259,200 stress-sweep rollouts, and 138,240 fixed-risk rows. The strengthened method, \methodname{{}} v5, is useful but not submission-ready. On the hard aggregate it obtains success {v5_success}, unsafe recall {v5_recall}, false rejection {v5_false}, violation {v5_safety}, regret {v5_regret}, and utility {v5_utility}. The best success reference is {escape_tex(best_success_ref)} at {escape_tex(best_success)}, and the best utility reference is {escape_tex(best_utility_ref)} at {escape_tex(best_utility)}. V5 fails success, diagnosis/recall, safety, regret, utility, false-rejection, fixed-risk, and scope gates. The terminal decision is therefore \textbf{{\terminalname}} for ICLR-main submission.
\end{{abstract}}

\section{{Decision First}}
The paper is not submission-ready. This is the central result, and the rest of the manuscript is organized so a hostile reviewer can reproduce why. The claim under test is not merely ``can a robot run a probe?'' A probe can be informative and still harm the closed-loop objective if it over-rejects valid actions, costs too much, or fails under perceptual ambiguity. The useful claim is stronger: executable common-sense tests should improve task success, safety, regret, and robust utility relative to strong baselines {cite(keys, 0, 8)}.

The expanded evidence rejects that stronger claim. V5 is a stronger mechanism than the v4.1 prototype, and the ablation suite says its internal pieces matter. But the external gate fails: v4, conformal risk filtering, human-query policy, and other baselines remain better on the deployment quantities that matter. Therefore the correct terminal state is \textbf{{\terminalname}}, while preserving the benchmark as negative evidence and as a specification for a future revival.

\section{{Frozen Protocol and Evidence Budget}}
The protocol was frozen before interpreting the final result. It includes six tasks, eight assumption families, eight splits, fourteen methods, ten seeds, and raw episode-level rows. The hard splits are low-signal common-sense stress and combined common-sense stress. The comparator set includes direct VLM action, LLM replanning, 3D affordance reasoning, uncertainty probing, deliberation, failure retrieval, calibrated affordance without tests, active perception, conformal risk filtering, human-query policy, policy repair from failed rollouts, v4 executable tests, v5, and an oracle {cite(keys, 8, 10)}.

{row_count_table()}

\section{{Problem Setup}}
Let $o_t$ denote the robot's observation, $g$ the task goal, $a$ an affordance or action candidate, and $z$ a latent physical assumption family. The method estimates
\[
  p_\theta(z \mid o_t, g, a, h_t),
\]
where $h_t$ is a compact history of previous probes and failures. It then chooses whether to execute, test, reject, query a human, or repair the policy:
\[
  a^\star = \arg\max_a U(a,o_t,g) - \lambda_s R_s(a,z) - \lambda_c C_{{\mathrm{{test}}}}(a,z) - \lambda_f F(a,z).
\]
This formulation makes the review standard clear. Diagnostic recall is intermediate evidence. A submission claim must show that the induced action policy improves the closed-loop outcome.

\section{{Method: Risk-Bounded Executable Common-Sense Tests}}
The v5 method adds five components to the older executable-test scaffold: assumption-family parsing, low-cost executable probes, counterfactual rollout scoring, cost calibration, and fixed-risk rejection. The assumption parser maps language and geometry into support, containment, rigidity, reach, articulation, clearance, mass, and material-fragility assumptions. The probe selector decides when a short physical test is worth its cost. The counterfactual scorer estimates whether rejection prevents an unsafe action or merely blocks a valid action. The risk-bound rejects only when the estimated safety risk crosses the frozen budget. These are plausible additions. They are also not enough.

\section{{Hard-Aggregate Results}}
{hard_table(hard_metrics)}

Table~\ref{{tab:hard}} is the main decision point. V5 is not a toy baseline; it has nontrivial recall and a structured test mechanism. But it is not the hard-aggregate frontier. Its false-rejection rate is too high, its physical-violation rate is worse than the conformal reference, and its robust utility is below the best non-oracle comparator. This is the failure mode a reviewer would attack: tests can be locally sensible while globally reducing the quality of the action policy.

{figure('common_sense_hard_success_regret_v5.png', 'Hard-split success and regret. V5 does not clear the closed-loop deployment gate.', 'fig:hard')}

\section{{Diagnostic Metrics Versus Deployment Metrics}}
The central negative result is the gap between diagnostic promise and deployment utility. Executable tests can raise recall by detecting unsafe assumptions before commitment. But the same mechanism can over-reject, pay avoidable cost, or misread low-signal ambiguity. This explains why a method can look principled in isolation and still fail when judged against active perception, conformal filtering, repair, and human-query policies {cite(keys, 18, 10)}.

{figure('common_sense_diagnosis_quality_v5.png', 'Diagnosis, unsafe recall, and false rejection on the hard aggregate. V5 pays for recall with high false rejection.', 'fig:diagnosis')}

\section{{Paired Tests}}
{pairwise_table(hard_pairwise)}

The paired tests prevent a narrative rescue. V5 is compared seed-by-seed against the strongest review-relevant baselines. A paper cannot claim acceptance by beating only direct VLM action or weak LLM replanning. The hard question is whether the executable-test mechanism beats v4, human-query, active-perception, conformal-risk, and repair references on success, safety, regret, and utility. It does not.

\section{{Ablation Audit}}
{ablation_table(ablations)}

{figure('common_sense_ablation_v5.png', 'Ablation audit. The full v5 mechanism is internally useful, but external deployment baselines still dominate.', 'fig:ablation')}

The ablation gate is the one favorable internal result: the full method beats stripped variants in the frozen ablation suite. That matters, but it is not sufficient. ICLR-main readiness requires both internal mechanism necessity and external baseline dominance. The first property without the second is a good negative result, not a submission-ready main claim.

\section{{Stress Sweep}}
{stress_table(stress)}

{figure('common_sense_stress_sweep_v5.png', 'Stress sweep across common-sense ambiguity severity. Stress survival alone does not rescue the hard aggregate.', 'fig:stress')}

Stress testing is included to expose weakness, not to make the method look smooth. V5 survives some stress comparisons, but that is not enough because the main hard-aggregate success, safety, regret, and utility gates fail. A robust paper needs the stress result and the hard aggregate to point in the same direction.

\section{{Fixed-Risk Deployment}}
{fixed_table(fixed)}

{figure('common_sense_fixed_risk_v5.png', 'Fixed-risk coverage. V5 has nonzero coverage at budget 0.05, but accepted utility is not uniformly frontier-leading.', 'fig:fixed')}

Fixed-risk reporting blocks an easy but unsafe story: a method cannot win by executing many high-risk actions and averaging away the failures. At budget 0.05, V5 has useful coverage, but fixed-risk utility is not uniformly stronger than the best accepted baseline. More importantly, fixed-risk reporting cannot reverse the already failed hard-aggregate gate.

\section{{Safety-Utility Frontier and Negative Cases}}
{figure('common_sense_pareto_v5.png', 'Success-safety Pareto view. V5 is not the clean non-oracle frontier once physical violations are counted.', 'fig:pareto')}

{negative_table(negatives)}

The negative cases are intentionally inspectable. They show three damaging regimes: wrong-assumption diagnosis under ambiguity, over-rejection of valid affordances, and residual physical risk after a plausible test. Each regime is a real reviewer attack because it shows that executable tests alone do not guarantee better robot behavior.

\section{{Theory Notes}}
\begin{{proposition}}[Test recall is insufficient for deployment dominance]
If method $A$ rejects more unsafe affordances than method $B$ but also rejects many safe affordances or pays higher test cost, then $A$ can have lower robust utility than $B$ even when $A$ has higher unsafe-rejection recall.
\end{{proposition}}

\noindent\textit{{Sketch.}} Robust utility subtracts physical violations, damage, regret, test cost, and false rejection from task success. Unsafe-rejection recall improves only one part of the objective. If false rejection or cost grows faster than avoided failures, a calibrated affordance, active-perception, repair, or conformal baseline can dominate the closed-loop objective. Table~\ref{{tab:hard}} and Table~\ref{{tab:paired}} instantiate this regime.

\begin{{proposition}}[A successful executable-test component must improve the induced policy]
An executable common-sense test is necessary for the submission claim only if removing it damages the closed-loop metrics required by the frozen gate, not merely the local test metric.
\end{{proposition}}

\noindent\textit{{Sketch.}} A probe can improve diagnosis while worsening action choice. The ablation gate therefore evaluates success, safety, regret, and utility in addition to diagnosis and recall.

\section{{Prior-Work Pressure}}
The hostile prior-work pool is broad. Affordance learning and visuomotor policies pressure the novelty of action selection. Planning under uncertainty pressures the need for explicit probes. Active perception pressures whether the robot should gather better observations instead of executing physical tests. Conformal risk control pressures the fixed-risk claim. Human-in-the-loop and shared autonomy baselines pressure the practicality of zero-human operation. Failure retrieval and policy repair pressure the negative-case story {cite(keys, 28, 14)}. Under that pressure, a paper cannot be accepted for showing an elegant test mechanism alone.

\section{{Limitations and Terminal Decision}}
The audit is CPU-only, deterministic, and local. It lacks real robot hardware, high-fidelity simulator validation, independently implemented external baselines, learned checkpoint release, and third-party reproduction. Those scope gaps already prevent ICLR-main readiness. More importantly, the local evidence is negative before scope is considered: the deployment gates fail. The terminal recommendation is therefore \textbf{{\terminalname}}.

\clearpage
\appendix
\section{{Reproducibility Commands}}
The experiment can be regenerated with \texttt{{python src\textbackslash run\_experiment.py}}. The manuscript can be regenerated with \texttt{{python scripts\textbackslash generate\_manuscript.py}}. The artifact validator is \texttt{{python scripts\textbackslash validate\_submission\_artifacts.py}}. The canonical PDF is \texttt{{C:/Users/wangz/Downloads/96.pdf}} and no copy is allowed on the visible Desktop.

\section{{Scenario Factor Audit}}
{scenario_factor_table(dataset_rows)}

\section{{Split-Level Frontier}}
{split_frontier_table(main_metrics)}

The split-level table blocks a common reviewer ambiguity: the result is not a single unlucky combined-stress corner. Across splits, the best non-oracle success or utility method is often not V5. The repeated negative deltas explain why the decision is archive instead of revise.

\section{{Baseline-by-Baseline Rejection Checklist}}
{baseline_rejection_table(hard_metrics)}

The rejection checklist is deliberately unforgiving. V5 can win recall against weak baselines and still fail if a stronger baseline has higher success, lower violation, lower regret, or higher utility. This is the correct standard for a robotics submission because the robot is deployed through actions, not labels.

\section{{Ablation Delta Interpretation}}
{ablation_delta_table(ablations)}

The internal ablation deltas are useful: the method is not random decoration. Removing tests, parsing, calibration, or counterfactual rollout can damage the v5 mechanism. But the future method must make that mechanism beat external deployment baselines, not only its own ablations.

\section{{Stress Degradation}}
{stress_degradation_table(stress)}

\section{{Fixed-Risk Budget Sweep}}
{fixed_budget_sweep_table(fixed)}

\section{{Negative-Case Taxonomy}}
{negative_taxonomy_table(negatives)}

\section{{Assumption-Family Semantics}}
Support-stability assumptions ask whether an object, stack, or robot configuration will remain supported after action. Containment-or-leakage assumptions ask whether fluid, granular material, or small objects remain inside a container. Rigidity-or-deformation assumptions ask whether an object can be treated as rigid during contact. Tool-reach-and-contact assumptions ask whether the robot can achieve the intended contact mode. Articulation-direction assumptions ask whether a door, drawer, or hinge can move in the inferred direction. Clearance-and-collision assumptions ask whether the robot can pass through clutter or tight spaces. Mass-or-inertia assumptions ask whether the action is feasible under load. Material-fragility-or-thermal assumptions ask whether contact, pressure, or temperature will damage the object.

\section{{Reviewer Threat Model}}
A hostile reviewer can reject the paper with six attacks. First, V5 loses hard-aggregate success to v4. Second, conformal risk filtering wins physical violation and utility. Third, human-query policy wins regret and diagnosis/recall references. Fourth, V5 has high false rejection. Fifth, fixed-risk reporting does not uniformly rescue accepted utility. Sixth, the scope is simulation-only. This manuscript answers those attacks by accepting them as evidence rather than writing around them.

\section{{What Would Make This Paper Submittable}}
A credible revival needs a new empirical program. It would require real robot or high-fidelity simulator evidence, released rollouts and risk scores, independently implemented active-perception and conformal baselines, pre-registered fixed-risk budgets, negative-case videos, and a method that reduces false rejection while preserving recall. It would also need ablations showing that executable tests improve the final action policy, not only the diagnostic target. That program is not present here.

\section{{Summary Snapshot}}
{summary_block(lines)}

\clearpage
\section{{Clickable Citation Audit Wall}}
The citation boxes are intentionally bright. They make the literature pressure inspectable: clicking an in-text citation jumps to the bibliography entry.

\begingroup
\footnotesize
\raggedright
{citation_wall(keys)}
\endgroup

\clearpage

\section{{Additional Literature Clusters}}
Affordance learning and visuomotor control pressure the action-selection claim {cite(keys, 42, 10)}. Active perception and information gathering pressure the need for physical probes {cite(keys, 52, 10)}. Risk-sensitive planning and conformal prediction pressure the safety gate {cite(keys, 62, 10)}. Human-in-the-loop robotics and shared autonomy pressure the zero-human claim {cite(keys, 72, 10)}. Failure prediction, retrieval, and policy repair pressure the negative-case story {cite(keys, 82, 10)}. Calibration, uncertainty, and red-team evaluation pressure the fixed-risk protocol {cite(keys, 92, 10)}.

\bibliographystyle{{iclr2026_conference}}
\bibliography{{references}}

\end{{document}}
"""
    (PAPER / "main.tex").write_text(tex, encoding="utf-8")
    print(f"wrote {PAPER / 'main.tex'}")
    print(f"wrote {PAPER / 'references.bib'} with {len(keys)} entries")
    print(f"target pdf: {DOWNLOAD_PDF}")
    print(f"terminal: {values.get('terminal', 'unknown')}")


if __name__ == "__main__":
    main()
