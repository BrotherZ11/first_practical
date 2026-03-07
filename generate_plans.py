#!/usr/bin/env python3
"""Script de ejemplo para generar múltiples planes de optimización.

Este script genera planes con diferentes configuraciones (SOC, GRC) y los guarda
en la carpeta output/ para comparación.
"""

import subprocess
import sys
from pathlib import Path


def run_plan(focus: str, budget: float = 250000):
    """Ejecuta un plan de optimización con la configuración especificada."""
    output_json = f"output/{focus}_plan.json"
    output_html = f"output/{focus}_dashboard.html"
    
    cmd = [
        sys.executable,
        "dss.py",
        "plan",
        "--nice", "fixtures/nice_tks.json",
        "--roles", "fixtures/roles_costs.csv",
        "--risk", "fixtures/risk_scenarios.json",
        "--baseline-workforce", "fixtures/baseline_workforce.json",
        "--focus", focus,
        "--budget", str(budget),
        "--output", output_json,
        "--dashboard-file", output_html,
    ]
    
    print(f"\n{'='*60}")
    print(f"Generando plan {focus.upper()} con presupuesto ${budget:,.0f}")
    print(f"{'='*60}")
    
    result = subprocess.run(cmd, capture_output=False, text=True)
    
    if result.returncode == 0:
        print(f"✅ Plan {focus.upper()} generado exitosamente:")
        print(f"   📄 JSON: {output_json}")
        print(f"   🌐 HTML: {output_html}")
    else:
        print(f"❌ Error generando plan {focus.upper()}")
    
    return result.returncode == 0


def main():
    """Genera múltiples planes para comparación."""
    print("🚀 CISO DSS Optimizer - Generador de Planes\n")
    
    # Crear carpeta output si no existe
    Path("output").mkdir(exist_ok=True)
    
    # Configuraciones a generar
    configs = [
        ("soc", 250000),
        ("grc", 250000),
        ("soc", 1800000),  # SOC con más presupuesto
    ]
    
    success_count = 0
    for focus, budget in configs:
        if run_plan(focus, budget):
            success_count += 1
    
    print(f"\n{'='*60}")
    print(f"✨ Resumen: {success_count}/{len(configs)} planes generados exitosamente")
    print(f"📁 Revisa la carpeta 'output/' para ver los resultados")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
