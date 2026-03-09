"""Workforce plan optimization using multiple-choice knapsack algorithm."""

from __future__ import annotations

from typing import Dict, List, Set, Tuple

from .models import (
    PlanAction,
    PlanResult,
    RoleCost,
    RoleTKS,
    OPTION_COVERAGE,
    PRIORITY_DOMAIN_MULTIPLIER,
)


def role_priority_multiplier(role_id: str) -> float:
    """Calculate priority multiplier based on role domain (PD, DD, etc.)."""
    domain = role_id.split("-")[0].upper()
    return PRIORITY_DOMAIN_MULTIPLIER.get(domain, 1.0)


def _partial_coverage(items: Set[str], ratio: float) -> Set[str]:
    """Return a subset of items based on coverage ratio."""
    if ratio >= 1:
        return set(items)
    count = max(1, int(len(items) * ratio)) if items else 0
    return set(sorted(items)[:count])


def _hiring_speed_multiplier(time_to_hire: float) -> float:
    """Calculate multiplier for hiring speed (penalizes slow hiring)."""
    return max(0.4, 1 - (time_to_hire / 365.0))


def build_action(
    role_tks: RoleTKS,
    cost_data: RoleCost,
    option: str,
    weights: Dict[str, float]
) -> PlanAction:
    """Build a workforce plan action with cost and score calculations."""
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

    # Strategic multipliers (moderate adjustments to focus weights)
    strategic_multiplier = 1.0
    strategic_multiplier += max(0.0, cost_data.criticality_score - 1.0) * 0.20
    strategic_multiplier += max(0.0, cost_data.risk_impact) * 0.10
    strategic_multiplier += max(0.0, role_priority_multiplier(role_tks.role_id) - 1.0) * 0.25

    score = base_score * strategic_multiplier

    if option == "hire":
        score *= 0.8 + (0.2 * _hiring_speed_multiplier(cost_data.time_to_hire))
    elif option == "outsource":
        score *= 1.03  # slight advantage for speed

    return PlanAction(role_tks.role_id, option, cost, score, tasks, skills, knowledge)


def optimize_plan(
    roles_tks: Dict[str, RoleTKS],
    role_costs: Dict[str, RoleCost],
    risk_scenarios: Dict[str, Set[str]],
    baseline_roles: Set[str],
    budget: float,
    weights: Dict[str, float],
) -> PlanResult:
    """Optimize workforce plan using multiple-choice knapsack algorithm."""
    available_roles = sorted(set(roles_tks) & set(role_costs))
    if not available_roles:
        raise ValueError("No overlapping Role_ID values between NICE data and roles_costs.csv")

    role_actions: List[List[PlanAction]] = []
    for role_id in available_roles:
        options = ("upskill",) if role_id in baseline_roles else ("hire", "outsource")
        actions = [
            build_action(roles_tks[role_id], role_costs[role_id], option, weights)
            for option in options
        ]
        role_actions.append(actions)

    budget_cents = int(round(budget * 100))

    # Multiple-choice knapsack: at most one action per role
    # State: accumulated cost -> (total score, selected actions)
    dp: Dict[int, Tuple[float, List[PlanAction]]] = {0: (0.0, [])}

    for actions in role_actions:
        next_dp = dict(dp)  # option to not select this role
        for used_cost, (used_score, used_actions) in dp.items():
            for action in actions:
                action_cost = int(round(action.cost * 100))
                new_cost = used_cost + action_cost
                if new_cost > budget_cents:
                    continue

                new_score = used_score + action.score_gain
                new_actions = used_actions + [action]
                current = next_dp.get(new_cost)
                if current is None or new_score > current[0]:
                    next_dp[new_cost] = (new_score, new_actions)
        dp = next_dp

    # Best combination by score; tie-break by higher budget usage
    best_cost_cents, (total_score, selected) = max(
        dp.items(), key=lambda item: (item[1][0], item[0])
    )
    cost = best_cost_cents / 100

    covered_tasks: Set[str] = set()
    covered_skills: Set[str] = set()
    covered_knowledge: Set[str] = set()
    for action in selected:
        covered_tasks |= action.covered_tasks
        covered_skills |= action.covered_skills
        covered_knowledge |= action.covered_knowledge

    risk_reduction = {}
    for threat, required_tasks in risk_scenarios.items():
        covered = len(required_tasks & covered_tasks)
        risk_reduction[threat] = (
            round((covered / len(required_tasks)) * 100, 2) if required_tasks else 0.0
        )

    return PlanResult(
        selected_actions=selected,
        total_cost=round(cost, 2),
        weighted_score=round(total_score, 2),
        covered_tasks=covered_tasks,
        covered_skills=covered_skills,
        covered_knowledge=covered_knowledge,
        risk_reduction=risk_reduction,
    )
