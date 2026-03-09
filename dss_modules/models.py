"""Data models and constants for the CISO DSS optimizer."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Set

DEFAULT_BUDGET = 250_000.0
DEFAULT_REQUIRED_SCENARIOS = {
    "Ransomware",
    "SupplyChainCompromise",
    "DataLeaks",
    "AuditFailures",
}

FOCUS_PRESETS = {
    "soc": {"tasks": 1.0, "skills": 0.6, "knowledge": 0.3},
    "grc": {"tasks": 0.4, "skills": 0.8, "knowledge": 1.0},
    "custom": None,
}

OPTION_COVERAGE = {"hire": 1.0, "upskill": 0.7, "outsource": 0.85}
PRIORITY_DOMAIN_MULTIPLIER = {"PD": 1.20, "DD": 1.15}


@dataclass(frozen=True)
class RoleCost:
    """Cost and timing data for a cybersecurity role."""
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
    """Tasks, Knowledge, and Skills for a NICE Framework role."""
    role_id: str
    tasks: Set[str]
    skills: Set[str]
    knowledge: Set[str]


@dataclass(frozen=True)
class PlanAction:
    """A single action in the workforce plan."""
    role_id: str
    option: str
    cost: float
    score_gain: float
    covered_tasks: Set[str]
    covered_skills: Set[str]
    covered_knowledge: Set[str]


@dataclass
class PlanResult:
    """Complete result of a workforce optimization plan."""
    selected_actions: List[PlanAction]
    total_cost: float
    weighted_score: float
    covered_tasks: Set[str]
    covered_skills: Set[str]
    covered_knowledge: Set[str]
    risk_reduction: Dict[str, float]
