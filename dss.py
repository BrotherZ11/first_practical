#!/usr/bin/env python3
"""CISO DSS optimizer aligned with NICE Framework.

Commands:
- plan: build an optimized workforce plan under budget.
- gap: compare current vs target workforce and report missing capabilities.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Set

DEFAULT_BUDGET = 250_000.0
DEFAULT_REQUIRED_SCENARIOS = {
    "Ransomware",
    "SupplyChainCompromise",
    "DataLeaks",
    "AuditFailures",
}

FOCUS_PRESETS = {
    "soc": {"tasks": 0.6, "skills": 0.3, "knowledge": 0.1},
    "grc": {"tasks": 0.25, "skills": 0.25, "knowledge": 0.5},
    "custom": None,
}


@dataclass(frozen=True)
class RoleCost:
    role_id: str
    base_salary: float
    training_cost: float
    outsourcing_cost: float
    time_to_hire: float
    criticality_score: float
    risk_impact: float
    certification_bonus_cost: float


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


OPTION_COVERAGE = {"hire": 1.0, "upskill": 0.7, "outsource": 0.85}
PRIORITY_DOMAIN_MULTIPLIER = {"PD": 1.20, "DD": 1.15}


def _first_match(data: dict, keys: Iterable[str], default):
    for key in keys:
        if key in data:
            return data[key]
    return default


def load_nice_tks(path: Path) -> Dict[str, RoleTKS]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    roles = _first_match(raw, ["roles", "work_roles", "data"], raw if isinstance(raw, list) else [])
    if not isinstance(roles, list):
        raise ValueError("Unsupported nice_tks.json structure")

    result: Dict[str, RoleTKS] = {}
    for role in roles:
        role_id = _first_match(role, ["role_id", "Role_ID", "id"], "").strip()
        if not role_id:
            continue
        result[role_id] = RoleTKS(
            role_id=role_id,
            tasks=set(_first_match(role, ["tasks", "Tasks"], [])),
            skills=set(_first_match(role, ["skills", "Skills"], [])),
            knowledge=set(_first_match(role, ["knowledge", "Knowledge"], [])),
        )

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
            "Risk_Impact",
            "Certification_Bonus_Cost",
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
                risk_impact=float(row["Risk_Impact"]),
                certification_bonus_cost=float(row["Certification_Bonus_Cost"]),
            )

    if not result:
        raise ValueError("roles_costs.csv has no data")
    return result


def load_risk_scenarios(path: Path) -> Dict[str, Set[str]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("Unsupported risk_scenarios.json structure")
    scenarios = _first_match(raw, ["scenarios", "threats", "risk_scenarios"], raw)
    if isinstance(scenarios, list):
        mapped = {}
        for item in scenarios:
            name = _first_match(item, ["threat", "name"], "")
            tasks = set(_first_match(item, ["tasks", "mapped_tasks"], []))
            if name:
                mapped[name] = tasks
        scenarios = mapped
    parsed = {k: set(v) for k, v in scenarios.items()}

    missing = DEFAULT_REQUIRED_SCENARIOS - set(parsed)
    if missing:
        raise ValueError(f"risk_scenarios.json missing required scenarios: {sorted(missing)}")
    return parsed


def role_priority_multiplier(role_id: str) -> float:
    domain = role_id.split("-")[0].upper()
    return PRIORITY_DOMAIN_MULTIPLIER.get(domain, 1.0)


def _partial_coverage(items: Set[str], ratio: float) -> Set[str]:
    if ratio >= 1:
        return set(items)
    count = max(1, int(len(items) * ratio)) if items else 0
    return set(sorted(items)[:count])


def _hiring_speed_multiplier(time_to_hire: float) -> float:
    # Penaliza contrataciones lentas: 0.4x (muy lenta) a 1.0x (inmediata)
    return max(0.4, 1 - (time_to_hire / 365.0))


def build_action(role_tks: RoleTKS, cost_data: RoleCost, option: str, weights: Dict[str, float]) -> PlanAction:
    if option == "hire":
        cost = cost_data.base_salary * 2
    elif option == "upskill":
        cost = cost_data.training_cost + cost_data.certification_bonus_cost
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

    score = base_score * cost_data.criticality_score * (1 + cost_data.risk_impact / 10)
    score *= role_priority_multiplier(role_tks.role_id)

    if option == "hire":
        score *= _hiring_speed_multiplier(cost_data.time_to_hire)
    elif option == "outsource":
        score *= 1.05  # respuesta rápida ante exposición operacional

    return PlanAction(role_tks.role_id, option, cost, score, tasks, skills, knowledge)


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
        marginal = (
            (action.covered_tasks - covered_tasks)
            or (action.covered_skills - covered_skills)
            or (action.covered_knowledge - covered_knowledge)
        )
        if not marginal:
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
        covered = len(required_tasks & covered_tasks)
        risk_reduction[threat] = round((covered / len(required_tasks)) * 100, 2) if required_tasks else 0.0

    return PlanResult(
        selected_actions=selected,
        total_cost=round(cost, 2),
        weighted_score=round(total_score, 2),
        covered_tasks=covered_tasks,
        covered_skills=covered_skills,
        covered_knowledge=covered_knowledge,
        risk_reduction=risk_reduction,
    )


def gap_analysis(roles_tks: Dict[str, RoleTKS], current_roles: Set[str], target_roles: Set[str], top_n: int = 10) -> dict:
    missing_roles = sorted(target_roles - current_roles)
    current_tasks = set().union(*(roles_tks[r].tasks for r in current_roles if r in roles_tks))
    target_tasks = set().union(*(roles_tks[r].tasks for r in target_roles if r in roles_tks))
    missing_tasks = sorted(target_tasks - current_tasks)

    ranked = []
    for task in missing_tasks:
        supporting = sorted([r for r in missing_roles if task in roles_tks.get(r, RoleTKS(r, set(), set(), set())).tasks])
        ranked.append({"task": task, "enabled_by_roles": supporting})

    return {
        "current_workforce": sorted(current_roles),
        "target_workforce": sorted(target_roles),
        "missing_roles": missing_roles,
        "task_coverage_current": len(current_tasks),
        "task_coverage_target": len(target_tasks),
        "delta_tasks": len(missing_tasks),
        "top_missing_tasks": ranked[:top_n],
    }


def _weights_from_focus(args: argparse.Namespace) -> Dict[str, float]:
    if args.focus in ("soc", "grc"):
        return FOCUS_PRESETS[args.focus]
    return {"tasks": args.w_tasks, "skills": args.w_skills, "knowledge": args.w_knowledge}


def _dashboard_text(result: PlanResult, budget: float, focus: str) -> str:
    lines = [
        "=== CISO EXECUTIVE DASHBOARD ===",
        f"Focus preset: {focus.upper()}",
        f"Budget used: ${result.total_cost:,.2f} / ${budget:,.2f}",
        f"Weighted score: {result.weighted_score}",
        f"Roles selected: {len(result.selected_actions)}",
        "",
        "Risk Reduction:",
    ]
    for threat, value in sorted(result.risk_reduction.items()):
        lines.append(f"- {threat}: {value}%")
    lines.append("\nActions:")
    for action in result.selected_actions:
        lines.append(f"- {action.role_id}: {action.option} (${action.cost:,.0f})")
    return "\n".join(lines)


def _as_dict(result: PlanResult) -> dict:
    return {
        "total_cost": result.total_cost,
        "weighted_score": result.weighted_score,
        "selected_actions": [
            {"role_id": a.role_id, "option": a.option, "cost": round(a.cost, 2), "score_gain": round(a.score_gain, 2)}
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
    sub = parser.add_subparsers(dest="command")

    plan = sub.add_parser("plan", help="Build optimized plan")
    plan.add_argument("--nice", required=True, type=Path)
    plan.add_argument("--roles", required=True, type=Path)
    plan.add_argument("--risk", required=True, type=Path)
    plan.add_argument("--budget", type=float, default=DEFAULT_BUDGET)
    plan.add_argument("--focus", choices=["soc", "grc", "custom"], default="custom")
    plan.add_argument("--w-tasks", type=float, default=0.5)
    plan.add_argument("--w-skills", type=float, default=0.3)
    plan.add_argument("--w-knowledge", type=float, default=0.2)
    plan.add_argument("--output", type=Path)
    plan.add_argument("--dashboard", action="store_true", help="Print executive dashboard")

    gap = sub.add_parser("gap", help="Gap analysis between current and target workforce")
    gap.add_argument("--nice", required=True, type=Path)
    gap.add_argument("--current", required=True, help="Comma-separated role IDs")
    gap.add_argument("--target", required=True, help="Comma-separated role IDs")
    gap.add_argument("--top-n", type=int, default=10)
    gap.add_argument("--output", type=Path)

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    command = args.command or "plan"

    if command == "gap":
        roles_tks = load_nice_tks(args.nice)
        current = {r.strip() for r in args.current.split(",") if r.strip()}
        target = {r.strip() for r in args.target.split(",") if r.strip()}
        payload = json.dumps(gap_analysis(roles_tks, current, target, args.top_n), indent=2, ensure_ascii=False)
        if args.output:
            args.output.write_text(payload + "\n", encoding="utf-8")
        else:
            print(payload)
        return

    if args.command is None:
        raise SystemExit("Use subcommand: plan or gap")

    weights = _weights_from_focus(args)
    roles_tks = load_nice_tks(args.nice)
    role_costs = load_role_costs(args.roles)
    risk_scenarios = load_risk_scenarios(args.risk)

    result = optimize_plan(roles_tks, role_costs, risk_scenarios, args.budget, weights)
    payload = json.dumps(_as_dict(result), indent=2, ensure_ascii=False)

    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)

    if args.dashboard:
        print()
        print(_dashboard_text(result, args.budget, args.focus))


if __name__ == "__main__":
    main()
