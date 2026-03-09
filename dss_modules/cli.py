"""Command-line interface for CISO DSS optimizer."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict

from .dashboard import dashboard_text, generate_html_dashboard, plan_to_dict
from .gap_analysis import gap_analysis
from .loaders import (
    load_baseline_workforce,
    load_nice_tks,
    load_risk_scenarios,
    load_role_costs,
)
from .models import DEFAULT_BUDGET, FOCUS_PRESETS
from .optimizer import optimize_plan


def weights_from_focus(args: argparse.Namespace) -> Dict[str, float]:
    """Extract weight configuration from command-line arguments."""
    if args.focus in ("soc", "grc"):
        return FOCUS_PRESETS[args.focus]
    return {
        "tasks": args.w_tasks,
        "skills": args.w_skills,
        "knowledge": args.w_knowledge
    }


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="CISO DSS optimizer (NICE aligned)")
    sub = parser.add_subparsers(dest="command")

    # Plan subcommand
    plan = sub.add_parser("plan", help="Build optimized plan")
    plan.add_argument("--nice", required=True, type=Path)
    plan.add_argument("--roles", required=True, type=Path)
    plan.add_argument("--risk", required=True, type=Path)
    plan.add_argument("--baseline-workforce", required=True, type=Path)
    plan.add_argument("--budget", type=float, default=DEFAULT_BUDGET)
    plan.add_argument("--focus", choices=["soc", "grc", "custom"], default="custom")
    plan.add_argument("--w-tasks", type=float, default=0.5)
    plan.add_argument("--w-skills", type=float, default=0.3)
    plan.add_argument("--w-knowledge", type=float, default=0.2)
    plan.add_argument("--output", type=Path)
    plan.add_argument("--dashboard", action="store_true", help="Print executive dashboard")
    plan.add_argument("--dashboard-file", type=Path, help="Generate HTML dashboard to file")

    # Gap analysis subcommand
    gap = sub.add_parser("gap", help="Gap analysis between current and target workforce")
    gap.add_argument("--nice", required=True, type=Path)
    gap.add_argument("--current", required=True, help="Comma-separated role IDs")
    gap.add_argument("--target", required=True, help="Comma-separated role IDs")
    gap.add_argument("--top-n", type=int, default=10)
    gap.add_argument("--output", type=Path)

    return parser.parse_args()


def run_gap_command(args: argparse.Namespace) -> None:
    """Execute gap analysis command."""
    roles_tks = load_nice_tks(args.nice)
    current = {r.strip() for r in args.current.split(",") if r.strip()}
    target = {r.strip() for r in args.target.split(",") if r.strip()}
    payload = json.dumps(
        gap_analysis(roles_tks, current, target, args.top_n),
        indent=2,
        ensure_ascii=False
    )
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)


def run_plan_command(args: argparse.Namespace) -> None:
    """Execute plan optimization command."""
    weights = weights_from_focus(args)
    roles_tks = load_nice_tks(args.nice)
    role_costs = load_role_costs(args.roles)
    risk_scenarios = load_risk_scenarios(args.risk)
    baseline_roles = load_baseline_workforce(args.baseline_workforce)

    result = optimize_plan(
        roles_tks,
        role_costs,
        risk_scenarios,
        baseline_roles,
        args.budget,
        weights
    )
    
    payload = json.dumps(plan_to_dict(result), indent=2, ensure_ascii=False)

    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)

    if args.dashboard:
        print()
        print(dashboard_text(result, args.budget, args.focus))

    if hasattr(args, 'dashboard_file') and args.dashboard_file:
        html_content = generate_html_dashboard(
            result,
            args.budget,
            args.focus,
            baseline_roles,
            roles_tks,
            role_costs
        )
        args.dashboard_file.write_text(html_content, encoding='utf-8')
        print(f"\n✅ Professional HTML dashboard generated: {args.dashboard_file}")


def main() -> None:
    """Main entry point for CLI."""
    args = parse_args()
    command = args.command or "plan"

    if command == "gap":
        run_gap_command(args)
    elif command == "plan":
        run_plan_command(args)
    else:
        raise SystemExit("Use subcommand: plan or gap")
