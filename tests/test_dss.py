import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


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
