import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dss import RoleCost, RoleTKS, optimize_plan


def _run_plan(focus: str, out_path: Path):
    cmd = [
        sys.executable,
        str(ROOT / "dss.py"),
        "plan",
        "--nice",
        str(ROOT / "fixtures" / "nice_tks.json"),
        "--roles",
        str(ROOT / "fixtures" / "roles_costs.csv"),
        "--risk",
        str(ROOT / "fixtures" / "risk_scenarios.json"),
        "--baseline-workforce",
        str(ROOT / "fixtures" / "baseline_workforce.json"),
        "--focus",
        focus,
        "--output",
        str(out_path),
    ]
    subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(out_path.read_text(encoding="utf-8"))


def test_plan_cli_with_soc_focus_and_dashboard(tmp_path):
    out = tmp_path / "plan.json"
    cmd = [
        sys.executable,
        str(ROOT / "dss.py"),
        "plan",
        "--nice",
        str(ROOT / "fixtures" / "nice_tks.json"),
        "--roles",
        str(ROOT / "fixtures" / "roles_costs.csv"),
        "--risk",
        str(ROOT / "fixtures" / "risk_scenarios.json"),
        "--baseline-workforce",
        str(ROOT / "fixtures" / "baseline_workforce.json"),
        "--focus",
        "soc",
        "--output",
        str(out),
        "--dashboard",
    ]
    completed = subprocess.run(cmd, capture_output=True, text=True, check=True)
    assert "CISO EXECUTIVE DASHBOARD" in completed.stdout

    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["total_cost"] <= 250000
    assert payload["weighted_score"] > 0
    assert "DataLeaks" in payload["risk_reduction_percent"]
    assert any(action["role_id"] == "PD-WRL-006" for action in payload["selected_actions"])


def test_gap_command_returns_top_missing_tasks(tmp_path):
    out = tmp_path / "gap.json"
    cmd = [
        sys.executable,
        str(ROOT / "dss.py"),
        "gap",
        "--nice",
        str(ROOT / "fixtures" / "nice_tks.json"),
        "--current",
        "PD-WRL-001,DD-WRL-002",
        "--target",
        "PD-WRL-001,PD-WRL-003,PD-WRL-006,DD-WRL-002,IO-WRL-005",
        "--output",
        str(out),
    ]
    subprocess.run(cmd, capture_output=True, text=True, check=True)
    payload = json.loads(out.read_text(encoding="utf-8"))

    assert payload["delta_tasks"] > 0
    assert payload["missing_roles"] == ["IO-WRL-005", "PD-WRL-003", "PD-WRL-006"]
    assert len(payload["top_missing_tasks"]) > 0


def test_soc_and_grc_presets_produce_different_scores(tmp_path):
    soc_payload = _run_plan("soc", tmp_path / "soc.json")
    grc_payload = _run_plan("grc", tmp_path / "grc.json")

    assert soc_payload["weighted_score"] != grc_payload["weighted_score"]




def test_focus_preset_changes_hiring_decision(tmp_path):
    soc_payload = _run_plan("soc", tmp_path / "soc_plan.json")
    grc_payload = _run_plan("grc", tmp_path / "grc_plan.json")

    soc_hires = sorted([a["role_id"] for a in soc_payload["selected_actions"] if a["option"] == "hire"])
    grc_hires = sorted([a["role_id"] for a in grc_payload["selected_actions"] if a["option"] == "hire"])

    assert soc_hires != grc_hires

def test_optimizer_maximizes_score_with_budget_constraint():
    roles_tks = {
        "R1": RoleTKS(role_id="R1", tasks={"T1", "T2"}, skills={"S1"}, knowledge={"K1"}),
        "R2": RoleTKS(role_id="R2", tasks={"T3"}, skills={"S2"}, knowledge={"K2"}),
    }
    role_costs = {
        "R1": RoleCost(
            role_id="R1",
            base_salary=100,
            training_cost=40,
            outsourcing_cost=80,
            time_to_hire=20,
            criticality_score=8,
            risk_impact=8,
            certification_bonus_cost=10,
        ),
        "R2": RoleCost(
            role_id="R2",
            base_salary=80,
            training_cost=30,
            outsourcing_cost=70,
            time_to_hire=20,
            criticality_score=1,
            risk_impact=1,
            certification_bonus_cost=5,
        ),
    }
    risk_scenarios = {
        "Ransomware": {"T1"},
        "SupplyChainCompromise": {"T2"},
        "DataLeaks": {"T3"},
        "AuditFailures": {"T3"},
    }

    result = optimize_plan(
        roles_tks=roles_tks,
        role_costs=role_costs,
        risk_scenarios=risk_scenarios,
        baseline_roles={"R1"},
        budget=80,
        weights={"tasks": 1.0, "skills": 1.0, "knowledge": 1.0},
    )

    assert result.total_cost <= 80
    # Verifica que no se elige la opción más barata globalmente, sino la de mayor score bajo presupuesto.
    assert [(a.role_id, a.option) for a in result.selected_actions] == [("R1", "upskill")]
