#!/usr/bin/env python3
"""CISO DSS optimizer aligned with NICE Framework.

Inputs:
- nice_tks.json: NICE tasks/knowledge/skills by role.
- roles_costs.csv: organizational cost and criticality data.
- risk_scenarios.json: threat -> required NICE tasks.

Outputs:
- Recommended 2-year staffing/training/outsourcing plan under budget.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Set, Tuple


DEFAULT_BUDGET = 250_000.0


@dataclass(frozen=True)
class RoleCost:
    role_id: str
    base_salary: float
    training_cost: float
    outsourcing_cost: float
    time_to_hire: float
    criticality_score: float


@dataclass(frozen=True)
class RoleTKS:
    role_id: str
    tasks: Set[str]
    skills: Set[str]
    knowledge: Set[str]


@dataclass(frozen=True)
class PlanAction:
    role_id: str
    option: str
    cost: float
    score_gain: float
    covered_tasks: Set[str]
    covered_skills: Set[str]
    covered_knowledge: Set[str]


@dataclass
class PlanResult:
    selected_actions: List[PlanAction]
    total_cost: float
    weighted_score: float
    covered_tasks: Set[str]
    covered_skills: Set[str]
    covered_knowledge: Set[str]
    risk_reduction: Dict[str, float]


OPTION_COVERAGE = {
    "hire": 1.0,
    "upskill": 0.7,
    "outsource": 0.85,
}

PRIORITY_DOMAIN_MULTIPLIER = {
    "PD": 1.20,  # Protection & Defense
    "DD": 1.15,  # Design & Development
}


def _first_match(data: dict, keys: Iterable[str], default):
    for key in keys:
        if key in data:
            return data[key]
    return default


def load_nice_tks(path: Path) -> Dict[str, RoleTKS]:
    raw = json.loads(path.read_text(encoding="utf-8"))

    if isinstance(raw, dict):
        roles = _first_match(raw, ["roles", "work_roles", "data"], [])
    elif isinstance(raw, list):
        roles = raw
    else:
        raise ValueError("Unsupported nice_tks.json structure")

    result: Dict[str, RoleTKS] = {}
    for role in roles:
        role_id = _first_match(role, ["role_id", "Role_ID", "id"], "").strip()
        if not role_id:
            continue

        tasks = set(_first_match(role, ["tasks", "Tasks"], []))
        skills = set(_first_match(role, ["skills", "Skills"], []))
        knowledge = set(_first_match(role, ["knowledge", "Knowledge"], []))
        result[role_id] = RoleTKS(role_id, tasks, skills, knowledge)

    if not result:
        raise ValueError("No valid roles found in nice_tks.json")
    return result


def load_role_costs(path: Path) -> Dict[str, RoleCost]:
    result: Dict[str, RoleCost] = {}
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        expected = {
            "Role_ID",
            "Base_Salary",
            "Training_Cost",
            "Outsourcing_Cost",
            "Time_to_Hire",
            "Criticality_Score",
        }
        missing = expected - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"roles_costs.csv missing columns: {sorted(missing)}")

        for row in reader:
            role_id = row["Role_ID"].strip()
            result[role_id] = RoleCost(
                role_id=role_id,
                base_salary=float(row["Base_Salary"]),
                training_cost=float(row["Training_Cost"]),
                outsourcing_cost=float(row["Outsourcing_Cost"]),
                time_to_hire=float(row["Time_to_Hire"]),
                criticality_score=float(row["Criticality_Score"]),
            )

    if not result:
        raise ValueError("roles_costs.csv has no data")
    return result


def load_risk_scenarios(path: Path) -> Dict[str, Set[str]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(raw, dict):
        scenarios = _first_match(raw, ["scenarios", "threats", "risk_scenarios"], raw)
        if isinstance(scenarios, list):
            mapped = {}
            for item in scenarios:
                name = _first_match(item, ["threat", "name"], "")
                tasks = set(_first_match(item, ["tasks", "mapped_tasks"], []))
                if name:
                    mapped[name] = tasks
            return mapped
        return {k: set(v) for k, v in scenarios.items()}
    raise ValueError("Unsupported risk_scenarios.json structure")


def role_priority_multiplier(role_id: str) -> float:
    domain = role_id.split("-")[0].upper()
    return PRIORITY_DOMAIN_MULTIPLIER.get(domain, 1.0)


def _partial_coverage(items: Set[str], ratio: float) -> Set[str]:
    if ratio >= 1:
        return set(items)
    count = max(1, int(len(items) * ratio)) if items else 0
    return set(sorted(items)[:count])


def build_action(role_tks: RoleTKS, cost_data: RoleCost, option: str, weights: Dict[str, float]) -> PlanAction:
    if option == "hire":
        cost = cost_data.base_salary * 2  # 2-year horizon
    elif option == "upskill":
        cost = cost_data.training_cost
    elif option == "outsource":
        cost = cost_data.outsourcing_cost * 2
    else:
        raise ValueError(f"Unknown option: {option}")

    coverage = OPTION_COVERAGE[option]
    tasks = _partial_coverage(role_tks.tasks, coverage)
    skills = _partial_coverage(role_tks.skills, coverage)
    knowledge = _partial_coverage(role_tks.knowledge, coverage)

    base_score = (
        weights["tasks"] * len(tasks)
        + weights["skills"] * len(skills)
        + weights["knowledge"] * len(knowledge)
    )
    score = base_score * cost_data.criticality_score * role_priority_multiplier(role_tks.role_id)

    return PlanAction(
        role_id=role_tks.role_id,
        option=option,
        cost=cost,
        score_gain=score,
        covered_tasks=tasks,
        covered_skills=skills,
        covered_knowledge=knowledge,
    )


def optimize_plan(
    roles_tks: Dict[str, RoleTKS],
    role_costs: Dict[str, RoleCost],
    risk_scenarios: Dict[str, Set[str]],
    budget: float,
    weights: Dict[str, float],
) -> PlanResult:
    available_roles = sorted(set(roles_tks) & set(role_costs))
    if not available_roles:
        raise ValueError("No overlapping Role_ID values between NICE data and roles_costs.csv")

    candidates: List[PlanAction] = []
    for role_id in available_roles:
        for option in ("hire", "upskill", "outsource"):
            candidates.append(build_action(roles_tks[role_id], role_costs[role_id], option, weights))

    candidates.sort(key=lambda a: (a.score_gain / max(a.cost, 1), a.score_gain), reverse=True)

    selected: List[PlanAction] = []
    selected_roles: Set[str] = set()
    cost = 0.0
    covered_tasks: Set[str] = set()
    covered_skills: Set[str] = set()
    covered_knowledge: Set[str] = set()
    total_score = 0.0

    for action in candidates:
        if action.role_id in selected_roles:
            continue
        if cost + action.cost > budget:
            continue

        marginal_tasks = action.covered_tasks - covered_tasks
        marginal_skills = action.covered_skills - covered_skills
        marginal_knowledge = action.covered_knowledge - covered_knowledge
        if not (marginal_tasks or marginal_skills or marginal_knowledge):
            continue

        selected.append(action)
        selected_roles.add(action.role_id)
        cost += action.cost
        covered_tasks |= action.covered_tasks
        covered_skills |= action.covered_skills
        covered_knowledge |= action.covered_knowledge
        total_score += action.score_gain

    risk_reduction = {}
    for threat, required_tasks in risk_scenarios.items():
        if not required_tasks:
            risk_reduction[threat] = 0.0
            continue
        covered = len(required_tasks & covered_tasks)
        risk_reduction[threat] = round((covered / len(required_tasks)) * 100, 2)

    return PlanResult(
        selected_actions=selected,
        total_cost=round(cost, 2),
        weighted_score=round(total_score, 2),
        covered_tasks=covered_tasks,
        covered_skills=covered_skills,
        covered_knowledge=covered_knowledge,
        risk_reduction=risk_reduction,
    )


def as_dict(result: PlanResult) -> dict:
    return {
        "total_cost": result.total_cost,
        "weighted_score": result.weighted_score,
        "selected_actions": [
            {
                "role_id": a.role_id,
                "option": a.option,
                "cost": round(a.cost, 2),
                "score_gain": round(a.score_gain, 2),
            }
            for a in result.selected_actions
        ],
        "coverage": {
            "tasks": sorted(result.covered_tasks),
            "skills": sorted(result.covered_skills),
            "knowledge": sorted(result.covered_knowledge),
        },
        "risk_reduction_percent": result.risk_reduction,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CISO DSS optimizer (NICE aligned)")
    parser.add_argument("--nice", required=True, type=Path, help="Path to NICE TKS JSON")
    parser.add_argument("--roles", required=True, type=Path, help="Path to roles_costs.csv")
    parser.add_argument("--risk", required=True, type=Path, help="Path to risk_scenarios.json")
    parser.add_argument("--budget", type=float, default=DEFAULT_BUDGET, help="2-year budget cap")
    parser.add_argument("--w-tasks", type=float, default=0.5, help="Weight for task coverage")
    parser.add_argument("--w-skills", type=float, default=0.3, help="Weight for skill coverage")
    parser.add_argument("--w-knowledge", type=float, default=0.2, help="Weight for knowledge coverage")
    parser.add_argument("--output", type=Path, help="Optional output JSON file")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    weights = {"tasks": args.w_tasks, "skills": args.w_skills, "knowledge": args.w_knowledge}

    roles_tks = load_nice_tks(args.nice)
    role_costs = load_role_costs(args.roles)
    risk_scenarios = load_risk_scenarios(args.risk)

    result = optimize_plan(
        roles_tks=roles_tks,
        role_costs=role_costs,
        risk_scenarios=risk_scenarios,
        budget=args.budget,
        weights=weights,
    )

    output = as_dict(result)
    payload = json.dumps(output, indent=2, ensure_ascii=False)

    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)


if __name__ == "__main__":
    main()
