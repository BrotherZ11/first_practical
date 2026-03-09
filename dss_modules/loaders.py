"""Data loading functions for NICE Framework and related data."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Dict, Iterable, Set

from .models import RoleCost, RoleTKS, DEFAULT_REQUIRED_SCENARIOS


def _first_match(data: dict, keys: Iterable[str], default):
    """Return the first matching key value from a dictionary."""
    for key in keys:
        if key in data:
            return data[key]
    return default


def load_nice_tks(path: Path) -> Dict[str, RoleTKS]:
    """Load NICE Framework role TKS mappings from JSON file."""
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
    """Load role cost and criticality data from CSV file."""
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
    """Load risk scenario to task mappings from JSON file."""
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


def load_baseline_workforce(path: Path) -> Set[str]:
    """Load current baseline workforce role IDs from JSON file."""
    raw = json.loads(path.read_text(encoding="utf-8"))

    entries = _first_match(raw, ["baseline_workforce", "roles", "work_roles", "data"], raw)
    if not isinstance(entries, list):
        raise ValueError("Unsupported baseline_workforce structure")

    baseline_roles = set()
    for entry in entries:
        if isinstance(entry, str):
            role_id = entry.strip()
        elif isinstance(entry, dict):
            role_id = _first_match(entry, ["role_id", "Role_ID", "id"], "").strip()
        else:
            role_id = ""

        if role_id:
            baseline_roles.add(role_id)

    if not baseline_roles:
        raise ValueError("baseline_workforce has no valid role IDs")
    return baseline_roles
