"""Gap analysis between current and target workforce."""

from __future__ import annotations

from typing import Dict, Set

from .models import RoleTKS


def gap_analysis(
    roles_tks: Dict[str, RoleTKS],
    current_roles: Set[str],
    target_roles: Set[str],
    top_n: int = 10
) -> dict:
    """
    Perform gap analysis between current and target workforce.
    
    Args:
        roles_tks: Dictionary of role TKS mappings
        current_roles: Set of current role IDs
        target_roles: Set of target role IDs
        top_n: Number of top missing tasks to report
    
    Returns:
        Dictionary containing gap analysis results
    """
    missing_roles = sorted(target_roles - current_roles)
    current_tasks = set().union(
        *(roles_tks[r].tasks for r in current_roles if r in roles_tks)
    )
    target_tasks = set().union(
        *(roles_tks[r].tasks for r in target_roles if r in roles_tks)
    )
    missing_tasks = sorted(target_tasks - current_tasks)

    ranked = []
    for task in missing_tasks:
        supporting = sorted([
            r for r in missing_roles
            if task in roles_tks.get(r, RoleTKS(r, set(), set(), set())).tasks
        ])
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
