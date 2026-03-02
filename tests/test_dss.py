import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_cli_generates_plan_under_budget(tmp_path):
    out = tmp_path / "plan.json"
    cmd = [
        sys.executable,
        str(ROOT / "dss.py"),
        "--nice",
        str(ROOT / "fixtures" / "nice_tks.json"),
        "--roles",
        str(ROOT / "fixtures" / "roles_costs.csv"),
        "--risk",
        str(ROOT / "fixtures" / "risk_scenarios.json"),
        "--output",
        str(out),
    ]
    completed = subprocess.run(cmd, capture_output=True, text=True, check=True)
    assert completed.returncode == 0

    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["total_cost"] <= 250000
    assert payload["weighted_score"] > 0
    assert payload["risk_reduction_percent"]["Ransomware"] >= 0
    assert any(action["role_id"].startswith("PD") for action in payload["selected_actions"])
