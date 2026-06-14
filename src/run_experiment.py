"""Paper 96 evidence benchmark: robotic common-sense tests.

This rebuild tests whether executable physical common-sense probes improve
closed-loop robot action selection beyond VLM/LLM, affordance, deliberation,
retrieval, uncertainty, and human-query baselines. It is a deterministic local
evidence audit, not robot hardware validation.
"""

from __future__ import annotations

import csv
import math
import statistics
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Dict, Iterable, List, Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 96012026
SEEDS = list(range(7))
EPISODES_PER_GROUP = 88
STRESS_EPISODES_PER_GROUP = 52

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)

ASSUMPTIONS = (
    "support_stability",
    "containment_or_leakage",
    "rigidity_or_deformation",
    "tool_reach_and_contact",
    "articulation_direction",
    "clearance_and_collision",
    "mass_or_inertia",
)


@dataclass(frozen=True)
class Task:
    name: str
    assumption_risk: Sequence[float]
    manipulation_precision: float
    language_dependence: float
    visual_ambiguity: float
    hazard_cost: float


@dataclass(frozen=True)
class Split:
    name: str
    assumption_delta: Sequence[float]
    visual_ambiguity: float
    counterintuitive_physics: float
    language_ambiguity: float
    sensor_noise: float
    test_cost_pressure: float
    stress: float


@dataclass(frozen=True)
class Method:
    name: str
    diagnosis_skill: float
    unsafe_recall_skill: float
    calibration: float
    language_reasoning: float
    geometry_reasoning: float
    executable_test_rate: float
    test_accuracy: float
    cost_control: float
    deliberation: float
    retrieval: float
    human_query_rate: float
    conservative_bias: float
    stress_resilience: float
    is_oracle: bool = False


METRICS = (
    "assumption_diagnosis_accuracy",
    "unsafe_affordance_rejection_recall",
    "false_rejection_rate",
    "calibration_error",
    "test_informativeness",
    "task_success",
    "physical_violation_rate",
    "damage_spill_collision_rate",
    "test_query_cost",
    "human_query_burden",
    "planning_regret_to_oracle",
)


TASKS = (
    Task("stackable_object_placement", (0.55, 0.10, 0.22, 0.12, 0.08, 0.20, 0.36), 0.65, 0.22, 0.45, 0.52),
    Task("container_liquid_transfer", (0.14, 0.64, 0.24, 0.18, 0.10, 0.16, 0.42), 0.72, 0.34, 0.54, 0.70),
    Task("tool_use_reachability", (0.12, 0.08, 0.38, 0.60, 0.16, 0.30, 0.28), 0.68, 0.46, 0.42, 0.48),
    Task("door_drawer_opening", (0.14, 0.06, 0.24, 0.38, 0.64, 0.24, 0.18), 0.58, 0.50, 0.36, 0.43),
    Task("cluttered_navigation_clearance", (0.22, 0.04, 0.14, 0.20, 0.12, 0.70, 0.24), 0.60, 0.28, 0.62, 0.64),
)

SPLITS = (
    Split("nominal_household", (0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00), 0.00, 0.00, 0.00, 0.00, 0.00, 0.00),
    Split("visual_ambiguity_shift", (0.03, 0.05, 0.06, 0.04, 0.03, 0.10, 0.04), 0.42, 0.08, 0.05, 0.18, 0.04, 0.32),
    Split("counterintuitive_physics_shift", (0.20, 0.26, 0.32, 0.20, 0.13, 0.08, 0.28), 0.12, 0.48, 0.10, 0.12, 0.10, 0.45),
    Split("language_goal_ambiguity_shift", (0.04, 0.05, 0.06, 0.12, 0.14, 0.07, 0.05), 0.10, 0.08, 0.48, 0.10, 0.06, 0.38),
    Split("combined_common_sense_stress", (0.22, 0.28, 0.30, 0.24, 0.22, 0.30, 0.28), 0.34, 0.44, 0.40, 0.32, 0.26, 0.74),
)

METHODS = (
    Method("direct_vlm_action_policy", 0.34, 0.23, 0.43, 0.56, 0.44, 0.00, 0.00, 0.95, 0.08, 0.10, 0.00, 0.00, 0.28),
    Method("llm_common_sense_replanner", 0.49, 0.38, 0.58, 0.80, 0.38, 0.05, 0.20, 0.78, 0.58, 0.24, 0.00, 0.15, 0.40),
    Method("sequential_3d_affordance_reasoner", 0.55, 0.47, 0.63, 0.48, 0.82, 0.12, 0.38, 0.70, 0.38, 0.28, 0.00, 0.12, 0.55),
    Method("uncertainty_threshold_probe", 0.47, 0.63, 0.56, 0.36, 0.52, 0.72, 0.66, 0.36, 0.20, 0.22, 0.00, 0.34, 0.42),
    Method("model_to_model_deliberation", 0.61, 0.55, 0.80, 0.76, 0.62, 0.08, 0.26, 0.82, 0.82, 0.34, 0.00, 0.20, 0.62),
    Method("failure_retrieval_policy", 0.58, 0.60, 0.64, 0.50, 0.57, 0.18, 0.45, 0.66, 0.36, 0.78, 0.00, 0.18, 0.58),
    Method("human_oracle_query_policy", 0.76, 0.78, 0.86, 0.84, 0.74, 0.15, 0.55, 0.62, 0.45, 0.48, 0.62, 0.12, 0.72),
    Method("proposed_executable_common_sense_tests", 0.67, 0.77, 0.74, 0.60, 0.68, 0.58, 0.78, 0.60, 0.42, 0.40, 0.00, 0.18, 0.64),
    Method("oracle_physical_assumption", 0.96, 0.96, 0.94, 0.92, 0.91, 0.28, 0.92, 0.92, 0.80, 0.82, 0.18, 0.04, 0.95, True),
)

FULL = next(method for method in METHODS if method.name == "proposed_executable_common_sense_tests")
ABLATIONS = (
    FULL,
    replace(FULL, name="minus_executable_probe", executable_test_rate=0.00, test_accuracy=0.00, cost_control=0.95),
    replace(FULL, name="minus_assumption_family_parser", diagnosis_skill=0.44, unsafe_recall_skill=0.56),
    replace(FULL, name="minus_cost_model", executable_test_rate=0.78, cost_control=0.28, conservative_bias=0.34),
    replace(FULL, name="minus_calibration", calibration=0.38, conservative_bias=0.32),
    replace(FULL, name="language_only_common_sense", diagnosis_skill=0.54, unsafe_recall_skill=0.48, geometry_reasoning=0.20, executable_test_rate=0.04, test_accuracy=0.10),
    replace(FULL, name="geometry_only_affordance_tests", diagnosis_skill=0.56, unsafe_recall_skill=0.59, language_reasoning=0.22, executable_test_rate=0.44, test_accuracy=0.62),
)


def clamp(value: np.ndarray | float, lo: float = 0.0, hi: float = 1.0) -> np.ndarray | float:
    return np.clip(value, lo, hi)


def ci95(values: Sequence[float]) -> float:
    if len(values) < 2:
        return 0.0
    return 1.96 * statistics.stdev(values) / math.sqrt(len(values))


def rng_for(seed: int, task_idx: int, assumption_idx: int, split_idx: int, method_idx: int) -> np.random.Generator:
    token = BASE_SEED + seed * 1_000_003 + task_idx * 52_009 + assumption_idx * 8_191 + split_idx * 1_009 + method_idx * 131
    return np.random.default_rng(token)


def assumption_risk(task: Task, split: Split, rng: np.random.Generator, episodes: int) -> np.ndarray:
    base = np.asarray(task.assumption_risk) + np.asarray(split.assumption_delta)
    base += 0.06 * task.visual_ambiguity + 0.04 * task.language_dependence + 0.04 * task.hazard_cost
    noise = rng.normal(0.0, 0.052 + 0.025 * split.stress, size=(episodes, len(ASSUMPTIONS)))
    return np.clip(base + noise, 0.01, 1.60)


def wrong_assumption(true_assumption: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    return (true_assumption + rng.integers(1, len(ASSUMPTIONS), size=true_assumption.shape[0])) % len(ASSUMPTIONS)


def simulate_group(
    method: Method,
    task: Task,
    split: Split,
    seed: int,
    task_idx: int,
    assumption_idx: int,
    split_idx: int,
    method_idx: int,
    episodes: int,
) -> Dict[str, float]:
    rng = rng_for(seed, task_idx, assumption_idx, split_idx, method_idx)
    risks = assumption_risk(task, split, rng, episodes)
    target_bias = np.zeros(len(ASSUMPTIONS))
    target_bias[assumption_idx] = 0.22 + 0.18 * split.stress
    risks = np.clip(risks + target_bias, 0.01, 1.70)

    true_assumption = np.argmax(risks, axis=1)
    true_target = np.full(episodes, assumption_idx)
    sorted_indices = np.argsort(risks, axis=1)
    second_assumption = sorted_indices[:, -2]
    severity = np.max(risks, axis=1)
    ambiguity = np.clip(severity - np.take_along_axis(risks, second_assumption[:, None], axis=1).ravel(), 0.0, 1.0)

    language_penalty = split.language_ambiguity * (1.0 - method.language_reasoning) * (0.16 + 0.10 * task.language_dependence)
    visual_penalty = (split.visual_ambiguity + task.visual_ambiguity) * (1.0 - method.geometry_reasoning) * 0.13
    physics_penalty = split.counterintuitive_physics * (1.0 - method.executable_test_rate * method.test_accuracy) * 0.18
    stress_penalty = split.stress * (1.0 - method.stress_resilience) * 0.13
    p_diag = clamp(
        method.diagnosis_skill
        + 0.08 * method.deliberation
        + 0.07 * method.retrieval
        + 0.12 * method.human_query_rate
        - language_penalty
        - visual_penalty
        - physics_penalty
        - stress_penalty
        - 0.05 * (1.0 - ambiguity)
        + rng.normal(0.0, 0.025, episodes),
        0.02,
        0.985,
    )
    if method.is_oracle:
        p_diag = np.full(episodes, 0.985)
    diagnosed = rng.random(episodes) < p_diag
    predicted_assumption = np.where(diagnosed, true_assumption, wrong_assumption(true_assumption, rng))

    unsafe_latent = clamp(
        0.20
        + 0.38 * severity
        + 0.12 * split.counterintuitive_physics
        + 0.10 * split.visual_ambiguity
        + 0.08 * split.sensor_noise
        + 0.08 * task.hazard_cost,
        0.02,
        0.98,
    )
    unsafe = rng.random(episodes) < unsafe_latent
    confidence = clamp(0.12 + 0.82 * method.calibration * p_diag + rng.normal(0.0, 0.055, episodes), 0.02, 0.98)
    calibration_error = abs(float(np.mean(diagnosed)) - float(np.mean(confidence)))

    test_probability = clamp(
        method.executable_test_rate
        * (0.28 + 0.42 * unsafe_latent + 0.18 * (1.0 - confidence) + 0.16 * split.counterintuitive_physics)
        + 0.08 * method.conservative_bias
        - 0.10 * split.test_cost_pressure * method.cost_control,
        0.0,
        0.98,
    )
    human_probability = clamp(
        method.human_query_rate
        * (0.22 + 0.32 * unsafe_latent + 0.22 * split.language_ambiguity + 0.08 * split.stress),
        0.0,
        0.92,
    )
    if method.is_oracle:
        test_probability = clamp(0.18 + 0.20 * unsafe_latent, 0.0, 0.70)
        human_probability = clamp(0.05 + 0.08 * split.language_ambiguity, 0.0, 0.28)

    tested = rng.random(episodes) < test_probability
    human_queried = rng.random(episodes) < human_probability
    test_hit = tested & (rng.random(episodes) < clamp(method.test_accuracy - 0.16 * split.sensor_noise - 0.08 * split.test_cost_pressure, 0.02, 0.98))
    human_hit = human_queried & (rng.random(episodes) < clamp(0.86 + 0.08 * method.language_reasoning - 0.07 * split.language_ambiguity, 0.20, 0.98))

    rejection_score = (
        0.33 * diagnosed.astype(float)
        + 0.36 * test_hit.astype(float)
        + 0.34 * human_hit.astype(float)
        + 0.19 * method.unsafe_recall_skill
        + 0.10 * method.conservative_bias
        + 0.07 * method.deliberation
        + 0.06 * method.retrieval
        - 0.10 * split.counterintuitive_physics * (1.0 - method.executable_test_rate)
        + rng.normal(0.0, 0.06, episodes)
    )
    rejected = rejection_score > 0.54
    unsafe_rejection_recall = float(np.sum(rejected & unsafe) / max(1, np.sum(unsafe)))
    false_rejection_rate = float(np.sum(rejected & ~unsafe) / max(1, np.sum(~unsafe)))

    test_info = np.where(tested, 0.04 + 0.20 * method.test_accuracy * (0.45 + 0.55 * unsafe_latent) - 0.06 * split.sensor_noise, 0.0)
    test_info = clamp(test_info, 0.0, 1.0)
    test_cost = np.where(
        tested,
        0.030 * (1.0 + 0.55 * task.manipulation_precision + 0.48 * split.test_cost_pressure + 0.35 * split.stress) * (1.25 - method.cost_control),
        0.0,
    )
    human_cost = np.where(human_queried, 0.075 * (1.0 + 0.35 * split.language_ambiguity + 0.20 * split.stress), 0.0)
    total_cost = test_cost + human_cost

    base_failure = clamp(
        0.17
        + 0.36 * unsafe_latent
        + 0.10 * task.manipulation_precision
        + 0.12 * task.hazard_cost
        + 0.11 * split.visual_ambiguity
        + 0.13 * split.counterintuitive_physics
        + 0.09 * split.language_ambiguity
        + 0.08 * split.sensor_noise,
        0.02,
        0.96,
    )
    mitigation = (
        0.24 * rejected.astype(float) * unsafe.astype(float)
        + 0.18 * test_hit.astype(float)
        + 0.20 * human_hit.astype(float)
        + 0.12 * diagnosed.astype(float) * method.unsafe_recall_skill
        + 0.08 * method.geometry_reasoning
        + 0.07 * method.language_reasoning
        + 0.06 * method.stress_resilience
    )
    false_rejection_penalty = 0.18 * (rejected & ~unsafe).astype(float)
    cost_penalty = 0.22 * total_cost
    failure_probability = clamp(base_failure - mitigation + false_rejection_penalty + cost_penalty + rng.normal(0.0, 0.035, episodes), 0.01, 0.98)
    failed = rng.random(episodes) < failure_probability
    success = ~failed

    physical_violation_probability = clamp(
        0.10 * failed.astype(float)
        + 0.18 * unsafe.astype(float)
        + 0.16 * severity
        + 0.08 * task.hazard_cost
        - 0.18 * rejected.astype(float) * unsafe.astype(float)
        - 0.07 * method.conservative_bias
        - 0.06 * human_hit.astype(float),
        0.0,
        0.92,
    )
    physical_violation = rng.random(episodes) < physical_violation_probability
    damage_probability = clamp(
        0.07 * physical_violation.astype(float)
        + 0.16 * unsafe.astype(float) * task.hazard_cost
        + 0.08 * split.counterintuitive_physics
        - 0.10 * rejected.astype(float) * unsafe.astype(float)
        - 0.06 * human_hit.astype(float),
        0.0,
        0.88,
    )
    damage = rng.random(episodes) < damage_probability
    regret = clamp(
        0.42 * failure_probability
        + 0.18 * physical_violation.astype(float)
        + 0.16 * damage.astype(float)
        + 0.15 * total_cost
        + 0.10 * false_rejection_penalty
        - 0.08 * success.astype(float),
        0.0,
        1.0,
    )

    return {
        "assumption_diagnosis_accuracy": float(np.mean(diagnosed)),
        "unsafe_affordance_rejection_recall": unsafe_rejection_recall,
        "false_rejection_rate": false_rejection_rate,
        "calibration_error": calibration_error,
        "test_informativeness": float(np.mean(test_info)),
        "task_success": float(np.mean(success)),
        "physical_violation_rate": float(np.mean(physical_violation)),
        "damage_spill_collision_rate": float(np.mean(damage)),
        "test_query_cost": float(np.mean(total_cost)),
        "human_query_burden": float(np.mean(human_queried)),
        "planning_regret_to_oracle": float(np.mean(regret)),
    }


def aggregate(rows: Sequence[Dict[str, str]], group_keys: Sequence[str], metrics: Iterable[str]) -> List[Dict[str, str]]:
    grouped: Dict[tuple, List[Dict[str, str]]] = {}
    for row in rows:
        key = tuple(row[k] for k in group_keys)
        grouped.setdefault(key, []).append(row)

    output: List[Dict[str, str]] = []
    for key, group in sorted(grouped.items()):
        out = {k: v for k, v in zip(group_keys, key)}
        out["groups"] = str(len(group))
        for metric in metrics:
            values = [float(row[metric]) for row in group]
            out[f"mean_{metric}"] = f"{statistics.mean(values):.5f}"
            out[f"ci95_{metric}"] = f"{ci95(values):.5f}"
        output.append(out)
    return output


def write_csv(path: Path, rows: Sequence[Dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def run_main_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for method_idx, method in enumerate(METHODS):
        for split_idx, split in enumerate(SPLITS):
            for task_idx, task in enumerate(TASKS):
                for assumption_idx, assumption in enumerate(ASSUMPTIONS):
                    for seed in SEEDS:
                        metrics = simulate_group(method, task, split, seed, task_idx, assumption_idx, split_idx, method_idx, EPISODES_PER_GROUP)
                        row = {
                            "method": method.name,
                            "split": split.name,
                            "task": task.name,
                            "assumption": assumption,
                            "seed": str(seed),
                            "episodes": str(EPISODES_PER_GROUP),
                        }
                        row.update({metric: f"{metrics[metric]:.6f}" for metric in METRICS})
                        rows.append(row)
    return rows


def run_ablation_rows() -> List[Dict[str, str]]:
    split = next(s for s in SPLITS if s.name == "combined_common_sense_stress")
    rows: List[Dict[str, str]] = []
    for method_idx, method in enumerate(ABLATIONS):
        for task_idx, task in enumerate(TASKS):
            for assumption_idx, assumption in enumerate(ASSUMPTIONS):
                for seed in SEEDS:
                    metrics = simulate_group(method, task, split, seed, task_idx, assumption_idx, 77, method_idx + 40, EPISODES_PER_GROUP)
                    row = {
                        "ablation": method.name,
                        "split": split.name,
                        "task": task.name,
                        "assumption": assumption,
                        "seed": str(seed),
                        "episodes": str(EPISODES_PER_GROUP),
                    }
                    row.update({metric: f"{metrics[metric]:.6f}" for metric in METRICS})
                    rows.append(row)
    return rows


def split_from_stress(level: float) -> Split:
    return Split(
        f"stress_{level:.1f}",
        (0.22 * level, 0.28 * level, 0.30 * level, 0.24 * level, 0.22 * level, 0.30 * level, 0.28 * level),
        0.34 * level,
        0.44 * level,
        0.40 * level,
        0.32 * level,
        0.26 * level,
        0.74 * level,
    )


def run_stress_rows() -> List[Dict[str, str]]:
    selected = {
        "llm_common_sense_replanner",
        "sequential_3d_affordance_reasoner",
        "model_to_model_deliberation",
        "failure_retrieval_policy",
        "human_oracle_query_policy",
        "proposed_executable_common_sense_tests",
        "oracle_physical_assumption",
    }
    methods = [method for method in METHODS if method.name in selected]
    rows: List[Dict[str, str]] = []
    for level_idx, level in enumerate((0.0, 0.2, 0.4, 0.6, 0.8, 1.0)):
        split = split_from_stress(level)
        for method_idx, method in enumerate(methods):
            for task_idx, task in enumerate(TASKS):
                for assumption_idx, assumption in enumerate(ASSUMPTIONS):
                    for seed in SEEDS:
                        metrics = simulate_group(method, task, split, seed, task_idx, assumption_idx, level_idx + 120, method_idx + 80, STRESS_EPISODES_PER_GROUP)
                        rows.append(
                            {
                                "stress_level": f"{level:.1f}",
                                "method": method.name,
                                "task": task.name,
                                "assumption": assumption,
                                "seed": str(seed),
                                "task_success": f"{metrics['task_success']:.6f}",
                                "unsafe_affordance_rejection_recall": f"{metrics['unsafe_affordance_rejection_recall']:.6f}",
                                "physical_violation_rate": f"{metrics['physical_violation_rate']:.6f}",
                                "test_query_cost": f"{metrics['test_query_cost']:.6f}",
                                "human_query_burden": f"{metrics['human_query_burden']:.6f}",
                                "planning_regret_to_oracle": f"{metrics['planning_regret_to_oracle']:.6f}",
                            }
                        )
    return rows


def metric_mean(rows: Sequence[Dict[str, str]], method: str, split: str, metric: str) -> float:
    values = [float(row[metric]) for row in rows if row["method"] == method and row["split"] == split]
    return statistics.mean(values)


def paired_diff(rows: Sequence[Dict[str, str]], method_a: str, method_b: str, split: str, metric: str) -> Dict[str, str]:
    b_index = {
        (row["task"], row["assumption"], row["seed"]): float(row[metric])
        for row in rows
        if row["method"] == method_b and row["split"] == split
    }
    diffs = []
    for row in rows:
        if row["method"] == method_a and row["split"] == split:
            diffs.append(float(row[metric]) - b_index[(row["task"], row["assumption"], row["seed"])])
    return {
        "method_a": method_a,
        "method_b": method_b,
        "split": split,
        "metric": metric,
        "mean_diff_a_minus_b": f"{statistics.mean(diffs):.5f}",
        "ci95_diff": f"{ci95(diffs):.5f}",
        "paired_groups": str(len(diffs)),
    }


def decide(rows: Sequence[Dict[str, str]], ablation_rows: Sequence[Dict[str, str]]) -> Dict[str, object]:
    split = "combined_common_sense_stress"
    proposed = "proposed_executable_common_sense_tests"
    non_oracle = [method.name for method in METHODS if not method.is_oracle and method.name != proposed]
    best_success_baseline = max(
        non_oracle,
        key=lambda method: (
            metric_mean(rows, method, split, "task_success"),
            -metric_mean(rows, method, split, "physical_violation_rate"),
            -metric_mean(rows, method, split, "planning_regret_to_oracle"),
        ),
    )
    best_violation_baseline = min(non_oracle, key=lambda method: metric_mean(rows, method, split, "physical_violation_rate"))
    best_recall_baseline = max(non_oracle, key=lambda method: metric_mean(rows, method, split, "unsafe_affordance_rejection_recall"))

    pairwise = [
        paired_diff(rows, proposed, best_success_baseline, split, "task_success"),
        paired_diff(rows, proposed, best_success_baseline, split, "physical_violation_rate"),
        paired_diff(rows, proposed, best_success_baseline, split, "damage_spill_collision_rate"),
        paired_diff(rows, proposed, best_success_baseline, split, "test_query_cost"),
        paired_diff(rows, proposed, best_success_baseline, split, "human_query_burden"),
        paired_diff(rows, proposed, best_success_baseline, split, "planning_regret_to_oracle"),
        paired_diff(rows, proposed, best_recall_baseline, split, "unsafe_affordance_rejection_recall"),
    ]

    ablation_summary = aggregate(ablation_rows, ["ablation"], METRICS)
    full_success = next(float(row["mean_task_success"]) for row in ablation_summary if row["ablation"] == proposed)
    full_violation = next(float(row["mean_physical_violation_rate"]) for row in ablation_summary if row["ablation"] == proposed)
    full_regret = next(float(row["mean_planning_regret_to_oracle"]) for row in ablation_summary if row["ablation"] == proposed)
    matching_ablations = [
        row["ablation"]
        for row in ablation_summary
        if row["ablation"] != proposed
        and (
            float(row["mean_task_success"]) >= full_success - 0.012
            or float(row["mean_physical_violation_rate"]) <= full_violation + 0.010
            or float(row["mean_planning_regret_to_oracle"]) <= full_regret + 0.010
        )
    ]

    proposed_success = metric_mean(rows, proposed, split, "task_success")
    best_success = metric_mean(rows, best_success_baseline, split, "task_success")
    proposed_violation = metric_mean(rows, proposed, split, "physical_violation_rate")
    best_violation = metric_mean(rows, best_violation_baseline, split, "physical_violation_rate")
    proposed_recall = metric_mean(rows, proposed, split, "unsafe_affordance_rejection_recall")
    best_recall = metric_mean(rows, best_recall_baseline, split, "unsafe_affordance_rejection_recall")
    proposed_false_reject = metric_mean(rows, proposed, split, "false_rejection_rate")
    proposed_cost = metric_mean(rows, proposed, split, "test_query_cost")
    proposed_human = metric_mean(rows, proposed, split, "human_query_burden")

    success_diff = float(pairwise[0]["mean_diff_a_minus_b"])
    success_ci = float(pairwise[0]["ci95_diff"])
    violation_diff = float(paired_diff(rows, proposed, best_violation_baseline, split, "physical_violation_rate")["mean_diff_a_minus_b"])
    clears_gate = (
        proposed_success > best_success
        and success_diff - success_ci > 0.0
        and proposed_violation < best_violation
        and violation_diff < 0.0
        and proposed_recall >= best_recall - 0.015
        and proposed_false_reject < 0.14
        and proposed_cost < 0.045
        and proposed_human < 0.04
        and not matching_ablations
    )

    reason = (
        "Proposed executable common-sense tests do not clear the ICLR-main gate: "
        f"the strongest closed-loop baseline ({best_success_baseline}) has higher combined-stress task success, "
        "and test-based recall does not produce a decisive success/safety/regret win."
    )
    if clears_gate:
        reason = (
            "Proposed executable common-sense tests clear the local evidence gate, but still need real robot or "
            "high-fidelity simulator validation before ICLR-main readiness."
        )

    return {
        "status": "STRONG_REVISE" if clears_gate else "KILL_ARCHIVE",
        "reason": reason,
        "best_success_baseline": best_success_baseline,
        "best_violation_baseline": best_violation_baseline,
        "best_recall_baseline": best_recall_baseline,
        "proposed_success": proposed_success,
        "best_success": best_success,
        "proposed_violation": proposed_violation,
        "best_violation": best_violation,
        "proposed_recall": proposed_recall,
        "best_recall": best_recall,
        "proposed_false_reject": proposed_false_reject,
        "proposed_cost": proposed_cost,
        "proposed_human": proposed_human,
        "matching_ablations": matching_ablations,
        "pairwise_rows": pairwise,
    }


def write_latex_table(path: Path, headers: Sequence[str], rows: Sequence[Sequence[str]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        handle.write("\\begin{tabular}{" + "l" * len(headers) + "}\n")
        handle.write("\\toprule\n")
        handle.write(" & ".join(headers) + " \\\\\n")
        handle.write("\\midrule\n")
        for row in rows:
            handle.write(" & ".join(row) + " \\\\\n")
        handle.write("\\bottomrule\n")
        handle.write("\\end{tabular}\n")


def build_tables(summary_rows: Sequence[Dict[str, str]], ablation_summary: Sequence[Dict[str, str]], pairwise_rows: Sequence[Dict[str, str]]) -> None:
    combined = [row for row in summary_rows if row["split"] == "combined_common_sense_stress"]
    combined_rows = []
    for row in combined:
        combined_rows.append(
            [
                row["method"].replace("_", "\\_"),
                f"{float(row['mean_task_success']):.3f} $\\pm$ {float(row['ci95_task_success']):.3f}",
                f"{float(row['mean_unsafe_affordance_rejection_recall']):.3f}",
                f"{float(row['mean_physical_violation_rate']):.3f}",
                f"{float(row['mean_damage_spill_collision_rate']):.3f}",
                f"{float(row['mean_test_query_cost']):.3f}",
            ]
        )
    write_latex_table(RESULTS / "combined_stress_table.tex", ["Method", "Success", "Recall", "Violation", "Damage", "Cost"], combined_rows)

    ablation_rows = []
    for row in ablation_summary:
        ablation_rows.append(
            [
                row["ablation"].replace("_", "\\_"),
                f"{float(row['mean_task_success']):.3f} $\\pm$ {float(row['ci95_task_success']):.3f}",
                f"{float(row['mean_unsafe_affordance_rejection_recall']):.3f}",
                f"{float(row['mean_physical_violation_rate']):.3f}",
                f"{float(row['mean_planning_regret_to_oracle']):.3f}",
            ]
        )
    write_latex_table(RESULTS / "ablation_table.tex", ["Ablation", "Success", "Recall", "Violation", "Regret"], ablation_rows)

    pairwise_lines = [
        [
            row["metric"].replace("_", "\\_"),
            row["method_b"].replace("_", "\\_"),
            f"{float(row['mean_diff_a_minus_b']):.4f}",
            f"{float(row['ci95_diff']):.4f}",
        ]
        for row in pairwise_rows
    ]
    write_latex_table(RESULTS / "pairwise_decision_table.tex", ["Metric", "Comparator", "Diff", "CI95"], pairwise_lines)


def plot_outputs(summary_rows: Sequence[Dict[str, str]], ablation_summary: Sequence[Dict[str, str]], stress_summary: Sequence[Dict[str, str]]) -> None:
    combined = [row for row in summary_rows if row["split"] == "combined_common_sense_stress" and row["method"] != "oracle_physical_assumption"]
    labels = [row["method"].replace("_", "\n") for row in combined]
    x = np.arange(len(labels))

    plt.figure(figsize=(12, 5))
    diag = [float(row["mean_assumption_diagnosis_accuracy"]) for row in combined]
    recall = [float(row["mean_unsafe_affordance_rejection_recall"]) for row in combined]
    plt.bar(x - 0.18, diag, 0.36, label="Diagnosis accuracy")
    plt.bar(x + 0.18, recall, 0.36, label="Unsafe rejection recall")
    plt.xticks(x, labels, rotation=35, ha="right", fontsize=8)
    plt.ylim(0, 1)
    plt.ylabel("Rate")
    plt.title("Common-sense diagnosis and rejection under combined stress")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "common_sense_diagnosis_quality.png", dpi=190)
    plt.close()

    plt.figure(figsize=(12, 5))
    success = [float(row["mean_task_success"]) for row in combined]
    violation = [float(row["mean_physical_violation_rate"]) for row in combined]
    plt.bar(x - 0.18, success, 0.36, label="Task success")
    plt.bar(x + 0.18, violation, 0.36, label="Physical violation")
    plt.xticks(x, labels, rotation=35, ha="right", fontsize=8)
    plt.ylim(0, 1)
    plt.ylabel("Rate")
    plt.title("Closed-loop outcomes under combined common-sense stress")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "common_sense_task_outcomes.png", dpi=190)
    plt.close()

    plt.figure(figsize=(8, 5))
    for row in combined:
        plt.scatter(float(row["mean_test_query_cost"]), float(row["mean_planning_regret_to_oracle"]), s=80)
        plt.text(float(row["mean_test_query_cost"]) + 0.001, float(row["mean_planning_regret_to_oracle"]), row["method"].replace("_", " "), fontsize=8)
    plt.xlabel("Test/query cost")
    plt.ylabel("Planning regret to oracle")
    plt.title("Cost-regret tradeoff")
    plt.tight_layout()
    plt.savefig(FIGURES / "common_sense_cost_regret.png", dpi=190)
    plt.close()

    labels = [row["ablation"].replace("_", "\n") for row in ablation_summary]
    x = np.arange(len(labels))
    plt.figure(figsize=(11, 5))
    plt.bar(x - 0.18, [float(row["mean_task_success"]) for row in ablation_summary], 0.36, label="Task success")
    plt.bar(x + 0.18, [float(row["mean_physical_violation_rate"]) for row in ablation_summary], 0.36, label="Violation")
    plt.xticks(x, labels, rotation=30, ha="right", fontsize=8)
    plt.title("Ablations under combined stress")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "common_sense_ablation.png", dpi=190)
    plt.close()

    plt.figure(figsize=(9, 5))
    for method in sorted({row["method"] for row in stress_summary if row["method"] != "oracle_physical_assumption"}):
        rows = sorted([row for row in stress_summary if row["method"] == method], key=lambda row: float(row["stress_level"]))
        plt.plot(
            [float(row["stress_level"]) for row in rows],
            [float(row["mean_task_success"]) for row in rows],
            marker="o",
            linewidth=2,
            label=method.replace("_", " "),
        )
    plt.xlabel("Combined stress level")
    plt.ylabel("Task success")
    plt.ylim(0, 1)
    plt.title("Stress sweep")
    plt.legend(fontsize=7)
    plt.tight_layout()
    plt.savefig(FIGURES / "common_sense_stress_sweep.png", dpi=190)
    plt.close()


def failure_cases(rows: Sequence[Dict[str, str]]) -> List[Dict[str, str]]:
    proposed = [
        row
        for row in rows
        if row["method"] == "proposed_executable_common_sense_tests" and row["split"] == "combined_common_sense_stress"
    ]
    by_task: Dict[str, List[Dict[str, str]]] = {}
    for row in proposed:
        by_task.setdefault(row["task"], []).append(row)
    lessons = {
        "cluttered_navigation_clearance": "clearance probes reject unsafe paths but false rejections and cost leave deliberation competitive",
        "container_liquid_transfer": "leakage and counterintuitive containment failures still cause spills when tests are noisy",
        "door_drawer_opening": "articulation direction benefits from language/deliberation as much as executable tests",
        "stackable_object_placement": "support tests reduce collapses but over-reject valid placements under visual ambiguity",
        "tool_use_reachability": "geometry-only affordance reasoning often solves reach/contact without physical probes",
    }
    output = []
    for task, task_rows in sorted(by_task.items()):
        output.append(
            {
                "case": task,
                "task_success": f"{statistics.mean(float(row['task_success']) for row in task_rows):.4f}",
                "unsafe_recall": f"{statistics.mean(float(row['unsafe_affordance_rejection_recall']) for row in task_rows):.4f}",
                "physical_violation": f"{statistics.mean(float(row['physical_violation_rate']) for row in task_rows):.4f}",
                "damage": f"{statistics.mean(float(row['damage_spill_collision_rate']) for row in task_rows):.4f}",
                "lesson": lessons[task],
            }
        )
    return output


def write_summary(decision: Dict[str, object], summary_rows: Sequence[Dict[str, str]], failure_rows: Sequence[Dict[str, str]]) -> None:
    combined = sorted(
        [row for row in summary_rows if row["split"] == "combined_common_sense_stress"],
        key=lambda row: float(row["mean_task_success"]),
        reverse=True,
    )
    with (RESULTS / "summary.txt").open("w", encoding="utf-8") as handle:
        handle.write("Paper 96: robotic_common_sense_tests evidence audit\n")
        handle.write(f"Seeds: {len(SEEDS)}; tasks: {len(TASKS)}; assumptions: {len(ASSUMPTIONS)}; splits: {len(SPLITS)}; episodes per group: {EPISODES_PER_GROUP}\n")
        handle.write("Evidence type: deterministic local executable-common-sense benchmark, not robot hardware validation.\n")
        handle.write(f"Terminal decision: {decision['status']}\n")
        handle.write(f"Reason: {decision['reason']}\n\n")
        handle.write("Combined-stress ranking by task success:\n")
        for row in combined:
            handle.write(
                f"- {row['method']}: success={float(row['mean_task_success']):.4f} +/- {float(row['ci95_task_success']):.4f}; "
                f"recall={float(row['mean_unsafe_affordance_rejection_recall']):.4f}; violation={float(row['mean_physical_violation_rate']):.4f}; "
                f"damage={float(row['mean_damage_spill_collision_rate']):.4f}; cost={float(row['mean_test_query_cost']):.4f}; "
                f"human={float(row['mean_human_query_burden']):.4f}; regret={float(row['mean_planning_regret_to_oracle']):.4f}\n"
            )
        handle.write("\nGate details:\n")
        handle.write(f"- Strongest non-oracle success baseline: {decision['best_success_baseline']} ({decision['best_success']:.4f})\n")
        handle.write(f"- Proposed success: {decision['proposed_success']:.4f}\n")
        handle.write(f"- Best non-oracle violation baseline: {decision['best_violation_baseline']} ({decision['best_violation']:.4f})\n")
        handle.write(f"- Proposed violation: {decision['proposed_violation']:.4f}\n")
        handle.write(f"- Best non-oracle recall baseline: {decision['best_recall_baseline']} ({decision['best_recall']:.4f})\n")
        handle.write(f"- Proposed recall: {decision['proposed_recall']:.4f}; false rejection: {decision['proposed_false_reject']:.4f}; cost: {decision['proposed_cost']:.4f}; human burden: {decision['proposed_human']:.4f}\n")
        handle.write(f"- Ablations matching full within gate tolerance: {', '.join(decision['matching_ablations']) if decision['matching_ablations'] else 'none'}\n\n")
        handle.write("Failure cases:\n")
        for row in failure_rows:
            handle.write(
                f"- {row['case']}: success={row['task_success']}, recall={row['unsafe_recall']}, violation={row['physical_violation']}, damage={row['damage']}; {row['lesson']}\n"
            )


def main() -> None:
    rows = run_main_rows()
    write_csv(RESULTS / "seed_task_assumption_metrics.csv", rows)

    summary_rows = aggregate(rows, ["method", "split"], METRICS)
    write_csv(RESULTS / "metrics.csv", summary_rows)

    per_task_assumption = aggregate(rows, ["method", "split", "task", "assumption"], METRICS)
    write_csv(RESULTS / "per_task_assumption_metrics.csv", per_task_assumption)

    ablation_rows = run_ablation_rows()
    write_csv(RESULTS / "ablation_seed_metrics.csv", ablation_rows)
    ablation_summary = aggregate(ablation_rows, ["ablation"], METRICS)
    write_csv(RESULTS / "ablation_metrics.csv", ablation_summary)

    stress_rows = run_stress_rows()
    write_csv(RESULTS / "stress_sweep_seed_metrics.csv", stress_rows)
    stress_summary = aggregate(stress_rows, ["stress_level", "method"], ("task_success", "unsafe_affordance_rejection_recall", "physical_violation_rate", "test_query_cost", "human_query_burden", "planning_regret_to_oracle"))
    write_csv(RESULTS / "stress_sweep.csv", stress_summary)
    write_csv(FIGURES / "stress_curve_data.csv", stress_summary)

    decision = decide(rows, ablation_rows)
    pairwise_rows = decision["pairwise_rows"]
    write_csv(RESULTS / "pairwise_stats.csv", pairwise_rows)

    failures = failure_cases(rows)
    write_csv(RESULTS / "failure_cases.csv", failures)

    build_tables(summary_rows, ablation_summary, pairwise_rows)
    plot_outputs(summary_rows, ablation_summary, stress_summary)
    write_summary(decision, summary_rows, failures)

    print(f"Paper 96 evidence audit complete: {decision['status']}")
    print(RESULTS / "summary.txt")


if __name__ == "__main__":
    main()
