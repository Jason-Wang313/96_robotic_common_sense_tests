"""Paper 96 v5 evidence benchmark: robotic common-sense tests.

This runner tests whether executable physical common-sense probes improve
closed-loop robot action selection beyond strong VLM/LLM, affordance,
active-perception, conformal, repair, and human-query baselines. It is a
deterministic CPU-only local benchmark, not robot hardware validation.
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


BASE_SEED = 96022026
SEEDS = list(range(10))
EPISODES_PER_CELL = 6
STRESS_EPISODES_PER_CELL = 9

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
    "material_fragility_or_thermal",
)

METRICS = (
    "assumption_diagnosis_accuracy",
    "unsafe_affordance_rejection_recall",
    "false_rejection_rate",
    "calibration_error",
    "test_informativeness",
    "assumption_coverage",
    "counterfactual_test_validity",
    "task_success",
    "physical_violation_rate",
    "damage_spill_collision_rate",
    "test_query_cost",
    "human_query_burden",
    "planning_regret_to_oracle",
    "robust_utility",
)


@dataclass(frozen=True)
class Task:
    name: str
    assumption_risk: Sequence[float]
    manipulation_precision: float
    language_dependence: float
    visual_ambiguity: float
    hazard_cost: float
    material_fragility: float


@dataclass(frozen=True)
class Split:
    name: str
    assumption_delta: Sequence[float]
    visual_ambiguity: float
    counterintuitive_physics: float
    language_ambiguity: float
    sensor_noise: float
    tool_geometry_shift: float
    material_shift: float
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
    active_perception: float
    conformal_risk: float
    human_query_rate: float
    repair_memory: float
    conservative_bias: float
    stress_resilience: float
    is_oracle: bool = False


TASKS = (
    Task("stackable_object_placement", (0.58, 0.10, 0.22, 0.12, 0.08, 0.20, 0.36, 0.28), 0.65, 0.22, 0.45, 0.52, 0.36),
    Task("container_liquid_transfer", (0.14, 0.67, 0.24, 0.18, 0.10, 0.16, 0.42, 0.34), 0.72, 0.34, 0.54, 0.72, 0.42),
    Task("tool_use_reachability", (0.12, 0.08, 0.38, 0.63, 0.16, 0.30, 0.28, 0.20), 0.68, 0.46, 0.42, 0.48, 0.24),
    Task("door_drawer_opening", (0.14, 0.06, 0.24, 0.38, 0.67, 0.24, 0.18, 0.22), 0.58, 0.50, 0.36, 0.43, 0.26),
    Task("cluttered_navigation_clearance", (0.22, 0.04, 0.14, 0.20, 0.12, 0.73, 0.24, 0.30), 0.60, 0.28, 0.62, 0.64, 0.34),
    Task("fragile_deformable_packing", (0.32, 0.16, 0.62, 0.28, 0.12, 0.34, 0.30, 0.68), 0.76, 0.40, 0.56, 0.74, 0.78),
)

SPLITS = (
    Split("nominal_household", (0, 0, 0, 0, 0, 0, 0, 0), 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00),
    Split("visual_ambiguity_shift", (0.03, 0.05, 0.06, 0.04, 0.03, 0.10, 0.04, 0.06), 0.43, 0.08, 0.05, 0.18, 0.06, 0.04, 0.04, 0.32),
    Split("counterintuitive_physics_shift", (0.21, 0.28, 0.32, 0.20, 0.13, 0.08, 0.28, 0.28), 0.12, 0.50, 0.10, 0.12, 0.08, 0.18, 0.10, 0.46),
    Split("language_goal_ambiguity_shift", (0.04, 0.05, 0.06, 0.12, 0.15, 0.07, 0.05, 0.06), 0.10, 0.08, 0.50, 0.10, 0.06, 0.04, 0.06, 0.38),
    Split("sensor_noise_shift", (0.05, 0.08, 0.08, 0.10, 0.10, 0.12, 0.10, 0.12), 0.16, 0.12, 0.12, 0.47, 0.08, 0.06, 0.08, 0.42),
    Split("tool_geometry_shift", (0.08, 0.08, 0.18, 0.30, 0.23, 0.25, 0.10, 0.20), 0.20, 0.15, 0.12, 0.16, 0.48, 0.14, 0.11, 0.45),
    Split("low_signal_common_sense_stress", (0.16, 0.20, 0.24, 0.22, 0.20, 0.28, 0.24, 0.30), 0.28, 0.34, 0.32, 0.30, 0.28, 0.24, 0.18, 0.62),
    Split("combined_common_sense_stress", (0.23, 0.29, 0.32, 0.25, 0.22, 0.32, 0.30, 0.36), 0.36, 0.47, 0.42, 0.34, 0.34, 0.32, 0.26, 0.76),
)

METHODS = (
    Method("direct_vlm_action_policy", 0.34, 0.23, 0.43, 0.56, 0.44, 0.00, 0.00, 0.95, 0.08, 0.10, 0.02, 0.00, 0.00, 0.04, 0.00, 0.28),
    Method("llm_common_sense_replanner", 0.52, 0.40, 0.58, 0.84, 0.38, 0.05, 0.22, 0.79, 0.58, 0.24, 0.04, 0.04, 0.00, 0.12, 0.12, 0.40),
    Method("sequential_3d_affordance_reasoner", 0.57, 0.48, 0.63, 0.48, 0.84, 0.12, 0.38, 0.70, 0.38, 0.28, 0.20, 0.08, 0.00, 0.18, 0.10, 0.55),
    Method("uncertainty_threshold_probe", 0.49, 0.66, 0.56, 0.36, 0.52, 0.72, 0.66, 0.36, 0.20, 0.22, 0.10, 0.20, 0.00, 0.10, 0.35, 0.42),
    Method("model_to_model_deliberation", 0.63, 0.56, 0.79, 0.78, 0.62, 0.08, 0.26, 0.82, 0.84, 0.34, 0.10, 0.10, 0.00, 0.22, 0.18, 0.63),
    Method("failure_retrieval_policy", 0.60, 0.62, 0.64, 0.50, 0.57, 0.18, 0.45, 0.66, 0.36, 0.80, 0.12, 0.12, 0.00, 0.46, 0.18, 0.58),
    Method("no_test_calibrated_affordance", 0.58, 0.50, 0.82, 0.60, 0.78, 0.00, 0.00, 0.92, 0.42, 0.28, 0.25, 0.26, 0.00, 0.24, 0.18, 0.65),
    Method("active_perception_planner", 0.70, 0.69, 0.78, 0.62, 0.88, 0.24, 0.58, 0.58, 0.45, 0.34, 0.78, 0.20, 0.00, 0.28, 0.12, 0.74),
    Method("conformal_risk_filter", 0.55, 0.73, 0.90, 0.50, 0.60, 0.35, 0.62, 0.46, 0.32, 0.28, 0.18, 0.92, 0.00, 0.18, 0.42, 0.70),
    Method("human_oracle_query_policy", 0.79, 0.83, 0.88, 0.86, 0.76, 0.15, 0.55, 0.62, 0.48, 0.36, 0.30, 0.40, 0.62, 0.26, 0.10, 0.76),
    Method("policy_repair_from_failed_rollouts", 0.66, 0.69, 0.76, 0.56, 0.67, 0.20, 0.52, 0.68, 0.44, 0.72, 0.30, 0.24, 0.00, 0.84, 0.16, 0.75),
    Method("executable_common_sense_tests_v4", 0.68, 0.76, 0.74, 0.60, 0.68, 0.58, 0.78, 0.60, 0.42, 0.40, 0.18, 0.26, 0.00, 0.24, 0.18, 0.64),
    Method("risk_bounded_executable_common_sense_tests_v5", 0.76, 0.84, 0.84, 0.68, 0.74, 0.62, 0.82, 0.64, 0.46, 0.42, 0.35, 0.45, 0.00, 0.32, 0.19, 0.70),
    Method("oracle_physical_assumption", 0.98, 0.98, 0.96, 0.92, 0.92, 0.28, 0.93, 0.92, 0.80, 0.82, 0.54, 0.70, 0.18, 0.70, 0.04, 0.96, True),
)

METHOD_BY_NAME = {method.name: method for method in METHODS}
V5 = METHOD_BY_NAME["risk_bounded_executable_common_sense_tests_v5"]
ORACLE = METHOD_BY_NAME["oracle_physical_assumption"]

ABLATIONS = (
    replace(V5, name="full_risk_bounded_executable_common_sense_tests_v5"),
    replace(V5, name="minus_executable_probe", executable_test_rate=0.00, test_accuracy=0.00, cost_control=0.95, conformal_risk=0.34),
    replace(V5, name="minus_assumption_parser", diagnosis_skill=0.48, unsafe_recall_skill=0.58, language_reasoning=0.38),
    replace(V5, name="minus_cost_model", executable_test_rate=0.78, cost_control=0.30, conservative_bias=0.34),
    replace(V5, name="minus_calibration", calibration=0.38, conservative_bias=0.34, conformal_risk=0.26),
    replace(V5, name="minus_risk_bound", conformal_risk=0.08, conservative_bias=0.04, unsafe_recall_skill=0.66),
    replace(V5, name="minus_counterfactual_rollout", test_accuracy=0.54, active_perception=0.14, repair_memory=0.12),
    replace(V5, name="language_only_common_sense", diagnosis_skill=0.55, unsafe_recall_skill=0.50, geometry_reasoning=0.20, executable_test_rate=0.04, test_accuracy=0.10, active_perception=0.02),
    replace(V5, name="geometry_only_affordance_tests", diagnosis_skill=0.57, unsafe_recall_skill=0.60, language_reasoning=0.22, executable_test_rate=0.44, test_accuracy=0.62, deliberation=0.14),
    replace(V5, name="active_perception_only", diagnosis_skill=0.62, unsafe_recall_skill=0.66, executable_test_rate=0.18, test_accuracy=0.48, active_perception=0.82, conformal_risk=0.18, cost_control=0.62),
)

HARD_SPLITS = ("low_signal_common_sense_stress", "combined_common_sense_stress")
ABLATION_SPLITS = (
    "counterintuitive_physics_shift",
    "tool_geometry_shift",
    "low_signal_common_sense_stress",
    "combined_common_sense_stress",
)
STRESS_LEVELS = (0.0, 0.2, 0.4, 0.6, 0.8, 1.0)
STRESS_METHODS = (
    "sequential_3d_affordance_reasoner",
    "uncertainty_threshold_probe",
    "model_to_model_deliberation",
    "failure_retrieval_policy",
    "active_perception_planner",
    "conformal_risk_filter",
    "human_oracle_query_policy",
    "policy_repair_from_failed_rollouts",
    "executable_common_sense_tests_v4",
    V5.name,
)
FIXED_RISK_METHODS = (
    V5.name,
    "human_oracle_query_policy",
    "active_perception_planner",
    "conformal_risk_filter",
    "policy_repair_from_failed_rollouts",
    "executable_common_sense_tests_v4",
)
FIXED_RISK_BUDGETS = ("0.00", "0.05", "0.10", "0.15")

RAW_FIELDS = (
    "method",
    "split",
    "task",
    "assumption",
    "seed",
    "episode",
    "true_assumption",
    "predicted_assumption",
    "unsafe",
    "rejected",
    "tested",
    "human_queried",
    "task_success",
    "physical_violation",
    "damage_spill_collision",
    "test_query_cost",
    "planning_regret_to_oracle",
    "robust_utility",
    "risk_score",
)


def clamp(value: np.ndarray | float, lo: float = 0.0, hi: float = 1.0) -> np.ndarray | float:
    return np.clip(value, lo, hi)


def ci95(values: Sequence[float]) -> float:
    if len(values) < 2:
        return 0.0
    return 1.96 * statistics.stdev(values) / math.sqrt(len(values))


def rng_for(*tokens: int) -> np.random.Generator:
    value = BASE_SEED
    for idx, token in enumerate(tokens):
        value += (idx + 3) * 1_000_003 * (token + 31)
    return np.random.default_rng(value % (2**32 - 1))


def wrong_assumption(true_assumption: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    offsets = rng.integers(1, len(ASSUMPTIONS), size=true_assumption.shape[0])
    return (true_assumption + offsets) % len(ASSUMPTIONS)


def scenario_arrays(
    task: Task,
    split: Split,
    seed: int,
    task_idx: int,
    assumption_idx: int,
    split_idx: int,
    episodes: int,
    namespace: int,
) -> Dict[str, np.ndarray]:
    rng = rng_for(namespace, seed, task_idx, assumption_idx, split_idx)
    base = np.asarray(task.assumption_risk) + np.asarray(split.assumption_delta)
    base += 0.05 * task.visual_ambiguity + 0.04 * task.language_dependence + 0.04 * task.hazard_cost
    base += 0.05 * task.material_fragility + 0.08 * split.material_shift
    target_bias = np.zeros(len(ASSUMPTIONS))
    target_bias[assumption_idx] = 0.22 + 0.18 * split.stress
    noise = rng.normal(0.0, 0.052 + 0.026 * split.stress + 0.012 * split.sensor_noise, size=(episodes, len(ASSUMPTIONS)))
    risks = np.clip(base + target_bias + noise, 0.01, 1.80)
    severity = np.max(risks, axis=1)
    true_assumption = np.argmax(risks, axis=1)
    second_assumption = np.argsort(risks, axis=1)[:, -2]
    ambiguity = np.clip(severity - np.take_along_axis(risks, second_assumption[:, None], axis=1).ravel(), 0.0, 1.0)
    unsafe_latent = clamp(
        0.16
        + 0.36 * severity
        + 0.12 * split.counterintuitive_physics
        + 0.10 * split.visual_ambiguity
        + 0.08 * split.sensor_noise
        + 0.08 * split.tool_geometry_shift
        + 0.08 * task.hazard_cost
        + 0.05 * task.material_fragility,
        0.02,
        0.98,
    )
    return {
        "risks": risks,
        "severity": severity,
        "true_assumption": true_assumption,
        "second_assumption": second_assumption,
        "ambiguity": ambiguity,
        "unsafe_latent": unsafe_latent,
        "visual_ambiguity": np.full(episodes, split.visual_ambiguity + task.visual_ambiguity),
        "counterintuitive_physics": np.full(episodes, split.counterintuitive_physics),
        "language_ambiguity": np.full(episodes, split.language_ambiguity + task.language_dependence),
        "sensor_noise": np.full(episodes, split.sensor_noise),
        "tool_geometry_shift": np.full(episodes, split.tool_geometry_shift),
        "material_shift": np.full(episodes, split.material_shift + task.material_fragility),
        "test_cost_pressure": np.full(episodes, split.test_cost_pressure),
        "stress": np.full(episodes, split.stress),
    }


def macro_coverage(predicted: np.ndarray) -> float:
    return float(len(set(int(v) for v in predicted)) / len(ASSUMPTIONS))


def simulate_method(
    method: Method,
    task: Task,
    split: Split,
    scenario: Dict[str, np.ndarray],
    seed: int,
    method_idx: int,
    namespace: int,
) -> Dict[str, np.ndarray | Dict[str, float]]:
    episodes = scenario["severity"].shape[0]
    rng = rng_for(namespace, seed, method_idx, len(method.name))
    severity = scenario["severity"]
    true_assumption = scenario["true_assumption"].astype(int)
    second_assumption = scenario["second_assumption"].astype(int)
    ambiguity = scenario["ambiguity"]
    unsafe_latent = scenario["unsafe_latent"]

    language_penalty = split.language_ambiguity * (1.0 - method.language_reasoning) * (0.15 + 0.08 * task.language_dependence)
    visual_penalty = (split.visual_ambiguity + task.visual_ambiguity) * (1.0 - method.geometry_reasoning) * 0.12
    physics_penalty = split.counterintuitive_physics * (1.0 - method.executable_test_rate * method.test_accuracy) * 0.16
    tool_penalty = split.tool_geometry_shift * (1.0 - max(method.geometry_reasoning, method.active_perception)) * 0.13
    sensor_penalty = split.sensor_noise * (1.0 - 0.55 * method.active_perception) * 0.12
    material_penalty = (split.material_shift + task.material_fragility) * (1.0 - method.executable_test_rate * method.test_accuracy) * 0.07
    stress_penalty = split.stress * (1.0 - method.stress_resilience) * 0.12
    p_diag = clamp(
        method.diagnosis_skill
        + 0.08 * method.deliberation
        + 0.07 * method.retrieval
        + 0.10 * method.active_perception
        + 0.12 * method.human_query_rate
        - language_penalty
        - visual_penalty
        - physics_penalty
        - tool_penalty
        - sensor_penalty
        - material_penalty
        - stress_penalty
        - 0.05 * (1.0 - ambiguity)
        + rng.normal(0.0, 0.025, episodes),
        0.02,
        0.99,
    )
    if method.is_oracle:
        p_diag = np.full(episodes, 0.988)
    diagnosed = rng.random(episodes) < p_diag
    predicted_assumption = np.where(diagnosed, true_assumption, wrong_assumption(true_assumption, rng))
    top2_extra = (~diagnosed) & (rng.random(episodes) < clamp(0.16 + 0.24 * method.unsafe_recall_skill - 0.08 * split.stress, 0.02, 0.92))
    predicted_assumption = np.where(top2_extra, second_assumption, predicted_assumption)

    unsafe = rng.random(episodes) < unsafe_latent
    confidence = clamp(0.10 + 0.82 * method.calibration * p_diag + rng.normal(0.0, 0.055, episodes), 0.02, 0.98)
    calibration_error = abs(float(np.mean(diagnosed)) - float(np.mean(confidence)))

    test_probability = clamp(
        method.executable_test_rate
        * (0.26 + 0.44 * unsafe_latent + 0.17 * (1.0 - confidence) + 0.15 * split.counterintuitive_physics + 0.09 * split.tool_geometry_shift)
        + 0.10 * method.conservative_bias
        + 0.05 * method.active_perception
        - 0.11 * split.test_cost_pressure * method.cost_control,
        0.0,
        0.98,
    )
    human_probability = clamp(
        method.human_query_rate
        * (0.22 + 0.32 * unsafe_latent + 0.22 * split.language_ambiguity + 0.10 * split.stress + 0.05 * task.hazard_cost),
        0.0,
        0.92,
    )
    if method.is_oracle:
        test_probability = clamp(0.16 + 0.20 * unsafe_latent, 0.0, 0.72)
        human_probability = clamp(0.05 + 0.08 * split.language_ambiguity, 0.0, 0.28)

    tested = rng.random(episodes) < test_probability
    human_queried = rng.random(episodes) < human_probability
    test_hit_probability = clamp(
        method.test_accuracy
        - 0.14 * split.sensor_noise
        - 0.10 * split.tool_geometry_shift
        - 0.08 * split.material_shift
        + 0.06 * method.active_perception,
        0.02,
        0.99,
    )
    test_hit = tested & (rng.random(episodes) < test_hit_probability)
    human_hit = human_queried & (rng.random(episodes) < clamp(0.86 + 0.08 * method.language_reasoning - 0.07 * split.language_ambiguity, 0.20, 0.98))

    rejection_score = (
        0.30 * diagnosed.astype(float)
        + 0.35 * test_hit.astype(float)
        + 0.34 * human_hit.astype(float)
        + 0.18 * method.unsafe_recall_skill
        + 0.11 * method.conformal_risk
        + 0.09 * method.conservative_bias
        + 0.06 * method.active_perception
        + 0.05 * method.repair_memory
        - 0.09 * split.counterintuitive_physics * (1.0 - method.executable_test_rate)
        - 0.05 * split.sensor_noise * (1.0 - method.active_perception)
        + rng.normal(0.0, 0.06, episodes)
    )
    rejected = rejection_score > 0.55
    unsafe_rejection_recall = float(np.sum(rejected & unsafe) / max(1, np.sum(unsafe)))
    false_rejection_rate = float(np.sum(rejected & ~unsafe) / max(1, np.sum(~unsafe)))

    test_info = np.where(
        tested,
        0.04 + 0.22 * method.test_accuracy * (0.45 + 0.55 * unsafe_latent) + 0.05 * method.active_perception - 0.06 * split.sensor_noise,
        0.0,
    )
    test_info = clamp(test_info, 0.0, 1.0)
    counterfactual_validity = np.where(
        tested,
        clamp(0.18 + 0.58 * test_hit.astype(float) + 0.14 * diagnosed.astype(float) - 0.12 * split.counterintuitive_physics, 0.0, 1.0),
        clamp(0.08 + 0.18 * method.deliberation + 0.14 * method.repair_memory, 0.0, 1.0),
    )
    test_cost = np.where(
        tested,
        0.030
        * (1.0 + 0.55 * task.manipulation_precision + 0.45 * split.test_cost_pressure + 0.34 * split.stress + 0.22 * split.tool_geometry_shift)
        * (1.25 - method.cost_control),
        0.0,
    )
    human_cost = np.where(human_queried, 0.074 * (1.0 + 0.36 * split.language_ambiguity + 0.22 * split.stress), 0.0)
    active_cost = np.full(episodes, 0.010 * method.active_perception * (0.5 + split.sensor_noise + split.tool_geometry_shift))
    total_cost = test_cost + human_cost + active_cost

    base_failure = clamp(
        0.16
        + 0.34 * unsafe_latent
        + 0.10 * task.manipulation_precision
        + 0.12 * task.hazard_cost
        + 0.10 * split.visual_ambiguity
        + 0.13 * split.counterintuitive_physics
        + 0.08 * split.language_ambiguity
        + 0.08 * split.sensor_noise
        + 0.08 * split.tool_geometry_shift
        + 0.06 * split.material_shift,
        0.02,
        0.97,
    )
    mitigation = (
        0.23 * rejected.astype(float) * unsafe.astype(float)
        + 0.16 * test_hit.astype(float)
        + 0.21 * human_hit.astype(float)
        + 0.10 * method.active_perception
        + 0.11 * method.repair_memory
        + 0.08 * method.conformal_risk
        + 0.07 * method.geometry_reasoning
        + 0.06 * method.language_reasoning
        + 0.06 * method.stress_resilience
    )
    false_rejection_penalty = 0.19 * (rejected & ~unsafe).astype(float)
    cost_penalty = 0.24 * total_cost
    over_probe_penalty = 0.05 * tested.astype(float) * (1.0 - method.cost_control) * (1.0 - unsafe.astype(float))
    failure_probability = clamp(
        base_failure
        - mitigation
        + false_rejection_penalty
        + cost_penalty
        + over_probe_penalty
        + rng.normal(0.0, 0.035, episodes),
        0.01,
        0.98,
    )
    failed = rng.random(episodes) < failure_probability
    success = ~failed

    physical_violation_probability = clamp(
        0.10 * failed.astype(float)
        + 0.17 * unsafe.astype(float)
        + 0.15 * severity
        + 0.08 * task.hazard_cost
        + 0.06 * split.tool_geometry_shift
        - 0.17 * rejected.astype(float) * unsafe.astype(float)
        - 0.08 * method.conformal_risk
        - 0.06 * method.conservative_bias
        - 0.07 * human_hit.astype(float),
        0.0,
        0.92,
    )
    physical_violation = rng.random(episodes) < physical_violation_probability
    damage_probability = clamp(
        0.07 * physical_violation.astype(float)
        + 0.15 * unsafe.astype(float) * task.hazard_cost
        + 0.07 * split.counterintuitive_physics
        + 0.06 * split.material_shift
        - 0.10 * rejected.astype(float) * unsafe.astype(float)
        - 0.06 * human_hit.astype(float)
        - 0.05 * method.conformal_risk,
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
    risk_score = clamp(
        0.24 * failure_probability
        + 0.26 * physical_violation_probability
        + 0.16 * regret
        + 0.10 * unsafe.astype(float)
        + 0.08 * (1.0 - confidence)
        - 0.16 * method.conformal_risk
        - 0.10 * method.calibration
        - 0.08 * test_hit.astype(float)
        - 0.08 * human_hit.astype(float),
        0.0,
        1.0,
    )
    robust_utility = clamp(
        success.astype(float)
        - 1.18 * physical_violation.astype(float)
        - 0.98 * damage.astype(float)
        - 0.68 * regret
        - 0.46 * total_cost
        - 0.16 * (rejected & ~unsafe).astype(float),
        -2.0,
        1.0,
    )

    return {
        "true_assumption": true_assumption,
        "predicted_assumption": predicted_assumption,
        "unsafe": unsafe,
        "rejected": rejected,
        "tested": tested,
        "human_queried": human_queried,
        "success": success,
        "physical_violation": physical_violation,
        "damage": damage,
        "total_cost": total_cost,
        "regret": regret,
        "robust_utility": robust_utility,
        "risk_score": risk_score,
        "metrics": {
            "assumption_diagnosis_accuracy": float(np.mean(diagnosed)),
            "unsafe_affordance_rejection_recall": unsafe_rejection_recall,
            "false_rejection_rate": false_rejection_rate,
            "calibration_error": calibration_error,
            "test_informativeness": float(np.mean(test_info)),
            "assumption_coverage": macro_coverage(predicted_assumption),
            "counterfactual_test_validity": float(np.mean(counterfactual_validity)),
            "task_success": float(np.mean(success)),
            "physical_violation_rate": float(np.mean(physical_violation)),
            "damage_spill_collision_rate": float(np.mean(damage)),
            "test_query_cost": float(np.mean(total_cost)),
            "human_query_burden": float(np.mean(human_queried)),
            "planning_regret_to_oracle": float(np.mean(regret)),
            "robust_utility": float(np.mean(robust_utility)),
        },
    }


def write_csv(path: Path, rows: Sequence[Dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def row_count(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def result_to_raw_rows(
    result: Dict[str, np.ndarray | Dict[str, float]],
    method: str,
    split: str,
    task: str,
    assumption: str,
    seed: int,
) -> Iterable[Dict[str, object]]:
    episodes = len(result["success"])  # type: ignore[arg-type]
    for episode in range(episodes):
        true_idx = int(result["true_assumption"][episode])  # type: ignore[index]
        pred_idx = int(result["predicted_assumption"][episode])  # type: ignore[index]
        yield {
            "method": method,
            "split": split,
            "task": task,
            "assumption": assumption,
            "seed": seed,
            "episode": episode,
            "true_assumption": ASSUMPTIONS[true_idx],
            "predicted_assumption": ASSUMPTIONS[pred_idx],
            "unsafe": int(bool(result["unsafe"][episode])),  # type: ignore[index]
            "rejected": int(bool(result["rejected"][episode])),  # type: ignore[index]
            "tested": int(bool(result["tested"][episode])),  # type: ignore[index]
            "human_queried": int(bool(result["human_queried"][episode])),  # type: ignore[index]
            "task_success": int(bool(result["success"][episode])),  # type: ignore[index]
            "physical_violation": int(bool(result["physical_violation"][episode])),  # type: ignore[index]
            "damage_spill_collision": int(bool(result["damage"][episode])),  # type: ignore[index]
            "test_query_cost": f"{float(result['total_cost'][episode]):.6f}",  # type: ignore[index]
            "planning_regret_to_oracle": f"{float(result['regret'][episode]):.6f}",  # type: ignore[index]
            "robust_utility": f"{float(result['robust_utility'][episode]):.6f}",  # type: ignore[index]
            "risk_score": f"{float(result['risk_score'][episode]):.6f}",  # type: ignore[index]
        }


def run_main() -> List[Dict[str, object]]:
    group_rows: List[Dict[str, object]] = []
    dataset_fields = (
        "seed",
        "split",
        "task",
        "assumption",
        "episode",
        "severity",
        "unsafe_latent",
        "visual_ambiguity",
        "counterintuitive_physics",
        "language_ambiguity",
        "sensor_noise",
        "tool_geometry_shift",
        "material_shift",
        "test_cost_pressure",
        "stress",
    )
    with (RESULTS / "rollouts.csv").open("w", newline="", encoding="utf-8") as raw_handle, (
        RESULTS / "dataset_summary.csv"
    ).open("w", newline="", encoding="utf-8") as data_handle:
        raw_writer = csv.DictWriter(raw_handle, fieldnames=RAW_FIELDS)
        raw_writer.writeheader()
        data_writer = csv.DictWriter(data_handle, fieldnames=dataset_fields)
        data_writer.writeheader()
        for seed in SEEDS:
            for split_idx, split in enumerate(SPLITS):
                for task_idx, task in enumerate(TASKS):
                    for assumption_idx, assumption in enumerate(ASSUMPTIONS):
                        scenario = scenario_arrays(task, split, seed, task_idx, assumption_idx, split_idx, EPISODES_PER_CELL, 10)
                        for episode in range(EPISODES_PER_CELL):
                            data_writer.writerow(
                                {
                                    "seed": seed,
                                    "split": split.name,
                                    "task": task.name,
                                    "assumption": assumption,
                                    "episode": episode,
                                    "severity": f"{float(scenario['severity'][episode]):.6f}",
                                    "unsafe_latent": f"{float(scenario['unsafe_latent'][episode]):.6f}",
                                    "visual_ambiguity": f"{float(scenario['visual_ambiguity'][episode]):.6f}",
                                    "counterintuitive_physics": f"{float(scenario['counterintuitive_physics'][episode]):.6f}",
                                    "language_ambiguity": f"{float(scenario['language_ambiguity'][episode]):.6f}",
                                    "sensor_noise": f"{float(scenario['sensor_noise'][episode]):.6f}",
                                    "tool_geometry_shift": f"{float(scenario['tool_geometry_shift'][episode]):.6f}",
                                    "material_shift": f"{float(scenario['material_shift'][episode]):.6f}",
                                    "test_cost_pressure": f"{float(scenario['test_cost_pressure'][episode]):.6f}",
                                    "stress": f"{float(scenario['stress'][episode]):.6f}",
                                }
                            )
                        for method_idx, method in enumerate(METHODS):
                            result = simulate_method(method, task, split, scenario, seed, method_idx, 20)
                            raw_writer.writerows(result_to_raw_rows(result, method.name, split.name, task.name, assumption, seed))
                            row = {
                                "seed": seed,
                                "split": split.name,
                                "task": task.name,
                                "assumption": assumption,
                                "method": method.name,
                                "episodes": EPISODES_PER_CELL,
                            }
                            row.update({metric: result["metrics"][metric] for metric in METRICS})  # type: ignore[index]
                            group_rows.append(row)
    write_csv(RESULTS / "seed_task_assumption_metrics.csv", group_rows)
    return group_rows


def aggregate_group_rows(rows: Sequence[Dict[str, object]], group_keys: Sequence[str], metrics: Iterable[str]) -> List[Dict[str, object]]:
    grouped: Dict[tuple, List[Dict[str, object]]] = {}
    for row in rows:
        key = tuple(row[k] for k in group_keys)
        grouped.setdefault(key, []).append(row)
    output: List[Dict[str, object]] = []
    for key, group in sorted(grouped.items()):
        out = {field: value for field, value in zip(group_keys, key)}
        out["groups"] = len(group)
        for metric in metrics:
            out[metric] = statistics.mean(float(row[metric]) for row in group)
        output.append(out)
    return output


def metric_long(seed_rows: Sequence[Dict[str, object]], group_keys: Sequence[str], metrics: Iterable[str]) -> List[Dict[str, object]]:
    grouped: Dict[tuple, List[Dict[str, object]]] = {}
    for row in seed_rows:
        key = tuple(row[k] for k in group_keys)
        grouped.setdefault(key, []).append(row)
    output: List[Dict[str, object]] = []
    for key, group in sorted(grouped.items()):
        for metric in metrics:
            values = [float(row[metric]) for row in group]
            out = {field: value for field, value in zip(group_keys, key)}
            out.update({"metric": metric, "mean": statistics.mean(values), "ci95": ci95(values), "n": len(values)})
            output.append(out)
    return output


def lookup_metric(rows: Sequence[Dict[str, object]], keys: Sequence[str]) -> Dict[tuple, Dict[str, object]]:
    return {tuple(row[k] for k in keys) + (row["metric"],): row for row in rows}


def paired_stats(seed_rows: Sequence[Dict[str, object]], split_key: str | None) -> List[Dict[str, object]]:
    baselines = [method.name for method in METHODS if not method.is_oracle and method.name != V5.name]
    output: List[Dict[str, object]] = []
    split_values = sorted({row[split_key] for row in seed_rows}) if split_key else [None]
    for split_value in split_values:
        scoped = [row for row in seed_rows if split_key is None or row[split_key] == split_value]
        for baseline in baselines:
            for metric in METRICS:
                diffs = []
                for seed in SEEDS:
                    v5_row = next(row for row in scoped if row["method"] == V5.name and int(row["seed"]) == seed)
                    b_row = next(row for row in scoped if row["method"] == baseline and int(row["seed"]) == seed)
                    diffs.append(float(v5_row[metric]) - float(b_row[metric]))
                row = {
                    "comparison": f"{V5.name}_minus_{baseline}",
                    "metric": metric,
                    "mean": statistics.mean(diffs),
                    "ci95": ci95(diffs),
                    "lower95": statistics.mean(diffs) - ci95(diffs),
                    "upper95": statistics.mean(diffs) + ci95(diffs),
                    "n": len(diffs),
                    "better_seeds": sum(1 for diff in diffs if diff > 0),
                }
                if split_key:
                    row[split_key] = split_value
                output.append(row)
    return output


def run_ablation() -> List[Dict[str, object]]:
    group_rows: List[Dict[str, object]] = []
    fields = ("ablation",) + RAW_FIELDS[1:]
    with (RESULTS / "ablation_rollouts.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for seed in SEEDS:
            for split_idx, split in enumerate(s for s in SPLITS if s.name in ABLATION_SPLITS):
                for task_idx, task in enumerate(TASKS):
                    for assumption_idx, assumption in enumerate(ASSUMPTIONS):
                        scenario = scenario_arrays(task, split, seed, task_idx, assumption_idx, split_idx, EPISODES_PER_CELL, 30)
                        for ablation_idx, method in enumerate(ABLATIONS):
                            result = simulate_method(method, task, split, scenario, seed, ablation_idx + 100, 40)
                            for raw in result_to_raw_rows(result, method.name, split.name, task.name, assumption, seed):
                                raw = dict(raw)
                                raw["ablation"] = raw.pop("method")
                                writer.writerow(raw)
                            row = {
                                "seed": seed,
                                "split": split.name,
                                "task": task.name,
                                "assumption": assumption,
                                "ablation": method.name,
                                "episodes": EPISODES_PER_CELL,
                            }
                            row.update({metric: result["metrics"][metric] for metric in METRICS})  # type: ignore[index]
                            group_rows.append(row)
    return group_rows


def split_from_stress(level: float) -> Split:
    return Split(
        f"stress_{level:.1f}",
        (0.23 * level, 0.29 * level, 0.32 * level, 0.25 * level, 0.22 * level, 0.32 * level, 0.30 * level, 0.36 * level),
        0.36 * level,
        0.47 * level,
        0.42 * level,
        0.34 * level,
        0.34 * level,
        0.32 * level,
        0.26 * level,
        0.76 * level,
    )


def run_stress() -> List[Dict[str, object]]:
    group_rows: List[Dict[str, object]] = []
    fields = ("stress_level",) + RAW_FIELDS
    methods = [METHOD_BY_NAME[name] for name in STRESS_METHODS]
    with (RESULTS / "stress_sweep_raw.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for level_idx, level in enumerate(STRESS_LEVELS):
            split = split_from_stress(level)
            for seed in SEEDS:
                for task_idx, task in enumerate(TASKS):
                    for assumption_idx, assumption in enumerate(ASSUMPTIONS):
                        scenario = scenario_arrays(task, split, seed, task_idx, assumption_idx, level_idx, STRESS_EPISODES_PER_CELL, 50)
                        for method_idx, method in enumerate(methods):
                            result = simulate_method(method, task, split, scenario, seed, method_idx + 200, 60)
                            for raw in result_to_raw_rows(result, method.name, split.name, task.name, assumption, seed):
                                raw = dict(raw)
                                raw["stress_level"] = f"{level:.1f}"
                                writer.writerow(raw)
                            row = {
                                "seed": seed,
                                "stress_level": f"{level:.1f}",
                                "task": task.name,
                                "assumption": assumption,
                                "method": method.name,
                                "episodes": STRESS_EPISODES_PER_CELL,
                            }
                            row.update({metric: result["metrics"][metric] for metric in METRICS})  # type: ignore[index]
                            group_rows.append(row)
    return group_rows


def run_fixed_risk() -> List[Dict[str, object]]:
    raw_rows: List[Dict[str, object]] = []
    methods = [METHOD_BY_NAME[name] for name in FIXED_RISK_METHODS]
    for split_idx, split in enumerate(s for s in SPLITS if s.name in HARD_SPLITS):
        for seed in SEEDS:
            for task_idx, task in enumerate(TASKS):
                for assumption_idx, assumption in enumerate(ASSUMPTIONS):
                    scenario = scenario_arrays(task, split, seed, task_idx, assumption_idx, split_idx, EPISODES_PER_CELL, 70)
                    for method_idx, method in enumerate(methods):
                        result = simulate_method(method, task, split, scenario, seed, method_idx + 300, 80)
                        for budget in FIXED_RISK_BUDGETS:
                            threshold = float(budget)
                            for episode in range(EPISODES_PER_CELL):
                                accepted = float(result["risk_score"][episode]) <= threshold  # type: ignore[index]
                                raw_rows.append(
                                    {
                                        "split": split.name,
                                        "budget": budget,
                                        "method": method.name,
                                        "task": task.name,
                                        "assumption": assumption,
                                        "seed": seed,
                                        "episode": episode,
                                        "accepted": int(accepted),
                                        "risk_score": f"{float(result['risk_score'][episode]):.6f}",  # type: ignore[index]
                                        "task_success": int(bool(result["success"][episode])),  # type: ignore[index]
                                        "physical_violation_rate": int(bool(result["physical_violation"][episode])),  # type: ignore[index]
                                        "damage_spill_collision_rate": int(bool(result["damage"][episode])),  # type: ignore[index]
                                        "planning_regret_to_oracle": f"{float(result['regret'][episode]):.6f}",  # type: ignore[index]
                                        "robust_utility": f"{float(result['robust_utility'][episode]):.6f}",  # type: ignore[index]
                                        "test_query_cost": f"{float(result['total_cost'][episode]):.6f}",  # type: ignore[index]
                                    }
                                )
    write_csv(RESULTS / "fixed_risk_raw.csv", raw_rows)
    return raw_rows


def fixed_risk_seed_metrics(raw_rows: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    grouped: Dict[tuple, List[Dict[str, object]]] = {}
    for row in raw_rows:
        key = (row["split"], row["budget"], row["method"], str(row["seed"]))
        grouped.setdefault(key, []).append(row)
    output: List[Dict[str, object]] = []
    for key, group in sorted(grouped.items()):
        accepted = [row for row in group if int(row["accepted"]) == 1]

        def accepted_mean(field: str) -> float:
            if not accepted:
                return 0.0
            return statistics.mean(float(row[field]) for row in accepted)

        output.append(
            {
                "split": key[0],
                "budget": key[1],
                "method": key[2],
                "seed": key[3],
                "coverage": len(accepted) / len(group),
                "accepted_success": accepted_mean("task_success"),
                "accepted_safety_violation": accepted_mean("physical_violation_rate"),
                "accepted_damage": accepted_mean("damage_spill_collision_rate"),
                "accepted_regret": accepted_mean("planning_regret_to_oracle"),
                "accepted_utility": accepted_mean("robust_utility"),
            }
        )
    return output


def fixed_risk_metric_long(seed_rows: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    metrics = ("coverage", "accepted_success", "accepted_safety_violation", "accepted_damage", "accepted_regret", "accepted_utility")
    return metric_long(seed_rows, ["split", "budget", "method"], metrics)


def fixed_risk_pairwise(seed_rows: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    metrics = ("coverage", "accepted_success", "accepted_safety_violation", "accepted_damage", "accepted_regret", "accepted_utility")
    baselines = [method for method in FIXED_RISK_METHODS if method != V5.name]
    output: List[Dict[str, object]] = []
    for split in HARD_SPLITS:
        for budget in FIXED_RISK_BUDGETS:
            scoped = [row for row in seed_rows if row["split"] == split and row["budget"] == budget]
            for baseline in baselines:
                for metric in metrics:
                    diffs = []
                    for seed in SEEDS:
                        v5_row = next(row for row in scoped if row["method"] == V5.name and int(row["seed"]) == seed)
                        b_row = next(row for row in scoped if row["method"] == baseline and int(row["seed"]) == seed)
                        diffs.append(float(v5_row[metric]) - float(b_row[metric]))
                    output.append(
                        {
                            "split": split,
                            "budget": budget,
                            "comparison": f"{V5.name}_minus_{baseline}",
                            "metric": metric,
                            "mean": statistics.mean(diffs),
                            "ci95": ci95(diffs),
                            "lower95": statistics.mean(diffs) - ci95(diffs),
                            "upper95": statistics.mean(diffs) + ci95(diffs),
                            "n": len(diffs),
                        }
                    )
    return output


def negative_cases(raw_path: Path) -> List[Dict[str, object]]:
    selected: List[Dict[str, str]] = []
    fallback: List[Dict[str, str]] = []
    with raw_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if row["method"] != V5.name or row["split"] not in HARD_SPLITS:
                continue
            fallback.append(row)
            if row["task_success"] == "0" or row["physical_violation"] == "1" or row["damage_spill_collision"] == "1":
                selected.append(row)
    selected = sorted(selected, key=lambda row: (float(row["robust_utility"]), -float(row["planning_regret_to_oracle"])))
    if len(selected) < 24:
        selected.extend(sorted(fallback, key=lambda row: float(row["robust_utility"]))[: 24 - len(selected)])
    output: List[Dict[str, object]] = []
    for idx, row in enumerate(selected[:24], start=1):
        output.append(
            {
                "case_id": idx,
                "seed": row["seed"],
                "task": row["task"],
                "split": row["split"],
                "assumption": row["assumption"],
                "episode": row["episode"],
                "predicted_assumption": row["predicted_assumption"],
                "true_assumption": row["true_assumption"],
                "unsafe": row["unsafe"],
                "rejected": row["rejected"],
                "success": row["task_success"],
                "physical_violation": row["physical_violation"],
                "damage_spill_collision": row["damage_spill_collision"],
                "regret": row["planning_regret_to_oracle"],
                "utility": row["robust_utility"],
                "failure_mode": "wrong_assumption" if row["predicted_assumption"] != row["true_assumption"] else "over_rejection_or_cost" if row["rejected"] == "1" and row["unsafe"] == "0" else "residual_physical_risk",
            }
        )
    return output


def decide(
    hard_metrics: Sequence[Dict[str, object]],
    hard_pairwise: Sequence[Dict[str, object]],
    ablation_metrics: Sequence[Dict[str, object]],
    stress_metrics: Sequence[Dict[str, object]],
    fixed_metrics: Sequence[Dict[str, object]],
) -> Dict[str, object]:
    hard = lookup_metric(hard_metrics, ["method"])
    all_non_oracle = [method.name for method in METHODS if not method.is_oracle and method.name != V5.name]
    best_success_ref = max(all_non_oracle, key=lambda method: float(hard[(method, "task_success")]["mean"]))
    best_diagnosis_ref = max(all_non_oracle, key=lambda method: float(hard[(method, "assumption_diagnosis_accuracy")]["mean"]))
    best_recall_ref = max(all_non_oracle, key=lambda method: float(hard[(method, "unsafe_affordance_rejection_recall")]["mean"]))
    best_safety_ref = min(all_non_oracle, key=lambda method: float(hard[(method, "physical_violation_rate")]["mean"]))
    best_damage_ref = min(all_non_oracle, key=lambda method: float(hard[(method, "damage_spill_collision_rate")]["mean"]))
    best_regret_ref = min(all_non_oracle, key=lambda method: float(hard[(method, "planning_regret_to_oracle")]["mean"]))
    best_utility_ref = max(all_non_oracle, key=lambda method: float(hard[(method, "robust_utility")]["mean"]))
    pair_lookup = {(row["comparison"], row["metric"]): row for row in hard_pairwise}
    success_comp = pair_lookup[(f"{V5.name}_minus_{best_success_ref}", "task_success")]
    safety_comp = pair_lookup[(f"{V5.name}_minus_{best_safety_ref}", "physical_violation_rate")]
    damage_comp = pair_lookup[(f"{V5.name}_minus_{best_damage_ref}", "damage_spill_collision_rate")]
    regret_comp = pair_lookup[(f"{V5.name}_minus_{best_regret_ref}", "planning_regret_to_oracle")]
    utility_comp = pair_lookup[(f"{V5.name}_minus_{best_utility_ref}", "robust_utility")]

    abl = lookup_metric(ablation_metrics, ["ablation"])
    full = "full_risk_bounded_executable_common_sense_tests_v5"
    best_ablation = max([method.name for method in ABLATIONS], key=lambda name: float(abl[(name, "robust_utility")]["mean"]))
    stress_lookup = lookup_metric(stress_metrics, ["stress_level", "method"])
    max_stress_ref = max([method for method in STRESS_METHODS if method != V5.name], key=lambda method: float(stress_lookup[("1.0", method, "robust_utility")]["mean"]))
    fixed_lookup = lookup_metric(fixed_metrics, ["split", "budget", "method"])
    fixed_coverages = [float(fixed_lookup[(split, "0.05", V5.name, "coverage")]["mean"]) for split in HARD_SPLITS]
    fixed_utilities = [float(fixed_lookup[(split, "0.05", V5.name, "accepted_utility")]["mean"]) for split in HARD_SPLITS]
    best_fixed_utilities = [
        max(float(fixed_lookup[(split, "0.05", method, "accepted_utility")]["mean"]) for method in FIXED_RISK_METHODS if method != V5.name)
        for split in HARD_SPLITS
    ]

    gates = {
        "success_gate": float(success_comp["lower95"]) > 0.0,
        "diagnosis_gate": float(hard[(V5.name, "assumption_diagnosis_accuracy")]["mean"]) >= float(hard[(best_diagnosis_ref, "assumption_diagnosis_accuracy")]["mean"])
        and float(hard[(V5.name, "unsafe_affordance_rejection_recall")]["mean"]) >= float(hard[(best_recall_ref, "unsafe_affordance_rejection_recall")]["mean"]) - 0.015,
        "safety_gate": float(safety_comp["upper95"]) <= 0.0 and float(damage_comp["upper95"]) <= 0.0,
        "regret_gate": float(regret_comp["upper95"]) <= 0.0,
        "utility_gate": float(utility_comp["lower95"]) > 0.0,
        "false_reject_gate": float(hard[(V5.name, "false_rejection_rate")]["mean"]) < 0.18,
        "ablation_gate": best_ablation == full,
        "stress_gate": float(stress_lookup[("1.0", V5.name, "robust_utility")]["mean"]) >= float(stress_lookup[("1.0", max_stress_ref, "robust_utility")]["mean"]),
        "fixed_risk_gate": all(cov > 0.05 for cov in fixed_coverages) and all(v5 >= best - 0.02 for v5, best in zip(fixed_utilities, best_fixed_utilities)),
        "scope_gate": False,
    }
    terminal = "STRONG_REVISE" if all(gates.values()) else "KILL_ARCHIVE"
    return {
        "terminal": terminal,
        "best_success_reference": best_success_ref,
        "best_diagnosis_reference": best_diagnosis_ref,
        "best_recall_reference": best_recall_ref,
        "best_safety_reference": best_safety_ref,
        "best_damage_reference": best_damage_ref,
        "best_regret_reference": best_regret_ref,
        "best_utility_reference": best_utility_ref,
        "best_ablation": best_ablation,
        "max_stress_reference": max_stress_ref,
        "v5_success": float(hard[(V5.name, "task_success")]["mean"]),
        "best_success": float(hard[(best_success_ref, "task_success")]["mean"]),
        "v5_diagnosis": float(hard[(V5.name, "assumption_diagnosis_accuracy")]["mean"]),
        "best_diagnosis": float(hard[(best_diagnosis_ref, "assumption_diagnosis_accuracy")]["mean"]),
        "v5_recall": float(hard[(V5.name, "unsafe_affordance_rejection_recall")]["mean"]),
        "best_recall": float(hard[(best_recall_ref, "unsafe_affordance_rejection_recall")]["mean"]),
        "v5_false_reject": float(hard[(V5.name, "false_rejection_rate")]["mean"]),
        "v5_safety": float(hard[(V5.name, "physical_violation_rate")]["mean"]),
        "best_safety": float(hard[(best_safety_ref, "physical_violation_rate")]["mean"]),
        "v5_damage": float(hard[(V5.name, "damage_spill_collision_rate")]["mean"]),
        "best_damage": float(hard[(best_damage_ref, "damage_spill_collision_rate")]["mean"]),
        "v5_regret": float(hard[(V5.name, "planning_regret_to_oracle")]["mean"]),
        "best_regret": float(hard[(best_regret_ref, "planning_regret_to_oracle")]["mean"]),
        "v5_utility": float(hard[(V5.name, "robust_utility")]["mean"]),
        "best_utility": float(hard[(best_utility_ref, "robust_utility")]["mean"]),
        "fixed_risk_coverages": fixed_coverages,
        "fixed_risk_utilities": fixed_utilities,
        "best_fixed_utilities": best_fixed_utilities,
        **gates,
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


def tex_escape(value: str) -> str:
    return value.replace("_", "\\_")


def build_tables(metrics: Sequence[Dict[str, object]], ablation_metrics: Sequence[Dict[str, object]], hard_pairwise: Sequence[Dict[str, object]]) -> None:
    metric_lookup = lookup_metric(metrics, ["split", "method"])
    combined_rows = []
    for method in [m.name for m in METHODS if not m.is_oracle]:
        key = ("combined_common_sense_stress", method)
        combined_rows.append(
            [
                tex_escape(method),
                f"{float(metric_lookup[key + ('task_success',)]['mean']):.3f}",
                f"{float(metric_lookup[key + ('unsafe_affordance_rejection_recall',)]['mean']):.3f}",
                f"{float(metric_lookup[key + ('physical_violation_rate',)]['mean']):.3f}",
                f"{float(metric_lookup[key + ('damage_spill_collision_rate',)]['mean']):.3f}",
                f"{float(metric_lookup[key + ('robust_utility',)]['mean']):.3f}",
            ]
        )
    write_latex_table(RESULTS / "combined_stress_table.tex", ["Method", "Success", "Recall", "Violation", "Damage", "Utility"], combined_rows)

    abl_lookup = lookup_metric(ablation_metrics, ["ablation"])
    ablation_rows = []
    for method in ABLATIONS:
        key = (method.name,)
        ablation_rows.append(
            [
                tex_escape(method.name),
                f"{float(abl_lookup[key + ('task_success',)]['mean']):.3f}",
                f"{float(abl_lookup[key + ('unsafe_affordance_rejection_recall',)]['mean']):.3f}",
                f"{float(abl_lookup[key + ('physical_violation_rate',)]['mean']):.3f}",
                f"{float(abl_lookup[key + ('robust_utility',)]['mean']):.3f}",
            ]
        )
    write_latex_table(RESULTS / "ablation_table.tex", ["Ablation", "Success", "Recall", "Violation", "Utility"], ablation_rows)

    pairwise_rows = []
    for row in hard_pairwise:
        if row["comparison"].endswith(("human_oracle_query_policy", "active_perception_planner", "policy_repair_from_failed_rollouts", "conformal_risk_filter")):
            if row["metric"] in {"task_success", "physical_violation_rate", "planning_regret_to_oracle", "robust_utility"}:
                pairwise_rows.append(
                    [
                        tex_escape(str(row["comparison"]).replace(f"{V5.name}_minus_", "v5 - ")),
                        tex_escape(str(row["metric"])),
                        f"{float(row['mean']):.4f}",
                        f"{float(row['ci95']):.4f}",
                    ]
                )
    write_latex_table(RESULTS / "pairwise_decision_table.tex", ["Comparison", "Metric", "Diff", "CI95"], pairwise_rows)


def plot_outputs(
    hard_metrics: Sequence[Dict[str, object]],
    ablation_metrics: Sequence[Dict[str, object]],
    stress_metrics: Sequence[Dict[str, object]],
    fixed_metrics: Sequence[Dict[str, object]],
) -> None:
    hard = lookup_metric(hard_metrics, ["method"])
    methods = [method.name for method in METHODS if not method.is_oracle]
    labels = [method.replace("_", "\n") for method in methods]
    x = np.arange(len(methods))

    plt.figure(figsize=(14, 5))
    plt.bar(x - 0.18, [float(hard[(method, "task_success")]["mean"]) for method in methods], 0.36, label="Task success")
    plt.bar(x + 0.18, [float(hard[(method, "planning_regret_to_oracle")]["mean"]) for method in methods], 0.36, label="Regret")
    plt.xticks(x, labels, rotation=35, ha="right", fontsize=7)
    plt.ylim(0, 1)
    plt.title("Hard aggregate success and regret")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "common_sense_hard_success_regret_v5.png", dpi=180)
    plt.close()

    plt.figure(figsize=(14, 5))
    plt.bar(x - 0.25, [float(hard[(method, "assumption_diagnosis_accuracy")]["mean"]) for method in methods], 0.25, label="Diagnosis")
    plt.bar(x, [float(hard[(method, "unsafe_affordance_rejection_recall")]["mean"]) for method in methods], 0.25, label="Unsafe recall")
    plt.bar(x + 0.25, [float(hard[(method, "false_rejection_rate")]["mean"]) for method in methods], 0.25, label="False rejection")
    plt.xticks(x, labels, rotation=35, ha="right", fontsize=7)
    plt.ylim(0, 1)
    plt.title("Assumption-test diagnostic quality")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "common_sense_diagnosis_quality_v5.png", dpi=180)
    plt.close()

    abl = lookup_metric(ablation_metrics, ["ablation"])
    abl_names = [method.name for method in ABLATIONS]
    x = np.arange(len(abl_names))
    plt.figure(figsize=(12, 5))
    plt.bar(x - 0.18, [float(abl[(method, "task_success")]["mean"]) for method in abl_names], 0.36, label="Success")
    plt.bar(x + 0.18, [float(abl[(method, "robust_utility")]["mean"]) for method in abl_names], 0.36, label="Utility")
    plt.xticks(x, [method.replace("_", "\n") for method in abl_names], rotation=30, ha="right", fontsize=7)
    plt.title("Ablation deployment outcomes")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "common_sense_ablation_v5.png", dpi=180)
    plt.close()

    stress_lookup = lookup_metric(stress_metrics, ["stress_level", "method"])
    plt.figure(figsize=(10, 5))
    for method in STRESS_METHODS:
        levels = [float(level) for level in STRESS_LEVELS]
        plt.plot(levels, [float(stress_lookup[(f"{level:.1f}", method, "task_success")]["mean"]) for level in levels], marker="o", label=method.replace("_", " "))
    plt.xlabel("Stress level")
    plt.ylabel("Task success")
    plt.ylim(0, 1)
    plt.title("Common-sense stress sweep")
    plt.legend(fontsize=6, ncol=2)
    plt.tight_layout()
    plt.savefig(FIGURES / "common_sense_stress_sweep_v5.png", dpi=180)
    plt.close()

    fixed_lookup = lookup_metric(fixed_metrics, ["split", "budget", "method"])
    plt.figure(figsize=(10, 5))
    budgets = [float(budget) for budget in FIXED_RISK_BUDGETS]
    for method in FIXED_RISK_METHODS:
        values = [
            statistics.mean(float(fixed_lookup[(split, f"{budget:.2f}", method, "coverage")]["mean"]) for split in HARD_SPLITS)
            for budget in budgets
        ]
        plt.plot(budgets, values, marker="o", label=method.replace("_", " "))
    plt.xlabel("Risk budget")
    plt.ylabel("Coverage")
    plt.ylim(0, 1)
    plt.title("Fixed-risk coverage")
    plt.legend(fontsize=7)
    plt.tight_layout()
    plt.savefig(FIGURES / "common_sense_fixed_risk_v5.png", dpi=180)
    plt.close()

    plt.figure(figsize=(8, 5))
    for method in methods:
        plt.scatter(float(hard[(method, "physical_violation_rate")]["mean"]), float(hard[(method, "task_success")]["mean"]), s=70)
        plt.text(float(hard[(method, "physical_violation_rate")]["mean"]) + 0.002, float(hard[(method, "task_success")]["mean"]), method.replace("_", " "), fontsize=7)
    plt.xlabel("Physical violation")
    plt.ylabel("Task success")
    plt.title("Safety-success frontier")
    plt.tight_layout()
    plt.savefig(FIGURES / "common_sense_pareto_v5.png", dpi=180)
    plt.close()


def write_summary(decision: Dict[str, object], counts: Dict[str, int]) -> None:
    lines = [
        "Paper 96 robotic_common_sense_tests v5 expanded audit",
        f"Terminal recommendation: {decision['terminal']}",
        "ICLR main ready: no",
        "Evidence type: deterministic local executable-common-sense benchmark, not robot hardware validation.",
        "Reason: expanded CPU-only audit tests whether executable common-sense probes convert diagnostic recall into closed-loop deployment gains; v5 improves the assumption-test mechanism but remains non-submittable if human-query, active-perception, repair, conformal, or calibrated-affordance baselines win deployment gates.",
    ]
    for key, value in counts.items():
        lines.append(f"{key}: {value}")
    lines.extend(
        [
            "",
            "Frozen hard-aggregate gate:",
            f"best_success_reference={decision['best_success_reference']}",
            f"best_diagnosis_reference={decision['best_diagnosis_reference']}",
            f"best_recall_reference={decision['best_recall_reference']}",
            f"best_safety_reference={decision['best_safety_reference']}",
            f"best_damage_reference={decision['best_damage_reference']}",
            f"best_regret_reference={decision['best_regret_reference']}",
            f"best_utility_reference={decision['best_utility_reference']}",
            f"best_ablation={decision['best_ablation']}",
            f"max_stress_reference={decision['max_stress_reference']}",
            f"v5_success={decision['v5_success']:.5f}",
            f"best_success={decision['best_success']:.5f}",
            f"v5_diagnosis={decision['v5_diagnosis']:.5f}",
            f"best_diagnosis={decision['best_diagnosis']:.5f}",
            f"v5_recall={decision['v5_recall']:.5f}",
            f"best_recall={decision['best_recall']:.5f}",
            f"v5_false_reject={decision['v5_false_reject']:.5f}",
            f"v5_safety={decision['v5_safety']:.5f}",
            f"best_safety={decision['best_safety']:.5f}",
            f"v5_damage={decision['v5_damage']:.5f}",
            f"best_damage={decision['best_damage']:.5f}",
            f"v5_regret={decision['v5_regret']:.5f}",
            f"best_regret={decision['best_regret']:.5f}",
            f"v5_utility={decision['v5_utility']:.5f}",
            f"best_utility={decision['best_utility']:.5f}",
        ]
    )
    for gate in (
        "success_gate",
        "diagnosis_gate",
        "safety_gate",
        "regret_gate",
        "utility_gate",
        "false_reject_gate",
        "ablation_gate",
        "stress_gate",
        "fixed_risk_gate",
        "scope_gate",
    ):
        lines.append(f"{gate}={decision[gate]}")
    for split, coverage, utility, best_utility in zip(
        HARD_SPLITS,
        decision["fixed_risk_coverages"],
        decision["fixed_risk_utilities"],
        decision["best_fixed_utilities"],
    ):
        lines.append(f"{split}: v5_coverage={coverage:.5f}; v5_accepted_utility={utility:.5f}; best_accepted_utility={best_utility:.5f}")
    lines.append("terminal=" + str(decision["terminal"]))
    (RESULTS / "summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    group_rows = run_main()
    raw_seed_metrics = aggregate_group_rows(group_rows, ["seed", "split", "method"], METRICS)
    write_csv(RESULTS / "raw_seed_metrics.csv", raw_seed_metrics)
    metrics = metric_long(raw_seed_metrics, ["split", "method"], METRICS)
    write_csv(RESULTS / "metrics.csv", metrics)
    per_task_assumption = aggregate_group_rows(group_rows, ["split", "task", "assumption", "method"], METRICS)
    write_csv(RESULTS / "per_task_assumption_metrics.csv", per_task_assumption)
    pairwise = paired_stats(raw_seed_metrics, "split")
    write_csv(RESULTS / "pairwise_stats.csv", pairwise)

    hard_group_rows = [row for row in group_rows if row["split"] in HARD_SPLITS]
    hard_seed = aggregate_group_rows(hard_group_rows, ["seed", "method"], METRICS)
    write_csv(RESULTS / "hard_aggregate_seed_metrics.csv", hard_seed)
    hard_metrics = metric_long(hard_seed, ["method"], METRICS)
    write_csv(RESULTS / "hard_aggregate_metrics.csv", hard_metrics)
    hard_pairwise = paired_stats(hard_seed, None)
    write_csv(RESULTS / "hard_aggregate_pairwise_stats.csv", hard_pairwise)

    ablation_rows = run_ablation()
    ablation_seed = aggregate_group_rows(ablation_rows, ["seed", "ablation"], METRICS)
    write_csv(RESULTS / "ablation_seed_metrics.csv", ablation_seed)
    ablation_metrics = metric_long(ablation_seed, ["ablation"], METRICS)
    write_csv(RESULTS / "ablation_metrics.csv", ablation_metrics)
    write_csv(RESULTS / "ablation_metric_long.csv", ablation_metrics)

    stress_rows = run_stress()
    stress_seed = aggregate_group_rows(stress_rows, ["seed", "stress_level", "method"], METRICS)
    write_csv(RESULTS / "stress_sweep_seed_metrics.csv", stress_seed)
    stress_metrics = metric_long(stress_seed, ["stress_level", "method"], METRICS)
    write_csv(RESULTS / "stress_sweep.csv", stress_metrics)
    write_csv(RESULTS / "stress_sweep_metric_long.csv", stress_metrics)
    write_csv(FIGURES / "stress_curve_data.csv", stress_metrics)

    fixed_raw = run_fixed_risk()
    fixed_seed = fixed_risk_seed_metrics(fixed_raw)
    write_csv(RESULTS / "fixed_risk_seed_metrics.csv", fixed_seed)
    fixed_metrics = fixed_risk_metric_long(fixed_seed)
    write_csv(RESULTS / "fixed_risk_metrics.csv", fixed_metrics)
    fixed_pair = fixed_risk_pairwise(fixed_seed)
    write_csv(RESULTS / "fixed_risk_pairwise.csv", fixed_pair)

    negatives = negative_cases(RESULTS / "rollouts.csv")
    write_csv(RESULTS / "negative_cases.csv", negatives)
    write_csv(RESULTS / "failure_cases.csv", negatives)

    decision = decide(hard_metrics, hard_pairwise, ablation_metrics, stress_metrics, fixed_metrics)
    build_tables(metrics, ablation_metrics, hard_pairwise)
    plot_outputs(hard_metrics, ablation_metrics, stress_metrics, fixed_metrics)
    counts = {
        "Main rollout rows": row_count(RESULTS / "rollouts.csv"),
        "Dataset summary rows": row_count(RESULTS / "dataset_summary.csv"),
        "Main seed-metric rows": len(raw_seed_metrics),
        "Main metric rows": len(metrics),
        "Main pairwise rows": len(pairwise),
        "Hard aggregate seed rows": len(hard_seed),
        "Hard aggregate metric rows": len(hard_metrics),
        "Hard aggregate pairwise rows": len(hard_pairwise),
        "Ablation rollout rows": row_count(RESULTS / "ablation_rollouts.csv"),
        "Ablation seed rows": len(ablation_seed),
        "Ablation metric rows": len(ablation_metrics),
        "Stress raw rows": row_count(RESULTS / "stress_sweep_raw.csv"),
        "Stress seed rows": len(stress_seed),
        "Stress metric rows": len(stress_metrics),
        "Fixed-risk raw rows": len(fixed_raw),
        "Fixed-risk seed rows": len(fixed_seed),
        "Fixed-risk metric rows": len(fixed_metrics),
        "Fixed-risk pairwise rows": len(fixed_pair),
        "Negative cases": len(negatives),
    }
    write_summary(decision, counts)
    print(f"Paper 96 v5 expanded audit complete: {decision['terminal']}")
    print(RESULTS / "summary.txt")


if __name__ == "__main__":
    main()
