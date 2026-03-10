"""Dashboard generation for CISO DSS plans (text and HTML formats)."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Set

from .models import PlanResult, RoleCost, RoleTKS


def dashboard_text(result: PlanResult, budget: float, focus: str) -> str:
    """Generate a simple text dashboard for the plan."""
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


def generate_html_dashboard(
    result: PlanResult,
    budget: float,
    focus: str,
    baseline_roles: Set[str],
    roles_tks: Dict[str, RoleTKS],
    role_costs: Dict[str, RoleCost]
) -> str:
    """Generate professional HTML dashboard with before/after gap analysis."""
    
    # Calculate BEFORE metrics
    before_tasks = set()
    before_skills = set()
    before_knowledge = set()
    before_cost = 0.0
    
    for role_id in baseline_roles:
        if role_id in roles_tks:
            before_tasks |= roles_tks[role_id].tasks
            before_skills |= roles_tks[role_id].skills
            before_knowledge |= roles_tks[role_id].knowledge
        if role_id in role_costs:
            before_cost += role_costs[role_id].base_salary
    
    # Calculate AFTER metrics
    after_roles = set(baseline_roles)
    for action in result.selected_actions:
        if action.option in ("hire", "outsource"):
            after_roles.add(action.role_id)
    
    # Budget utilization
    budget_used_pct = (result.total_cost / budget * 100) if budget > 0 else 0
    
    # Actions breakdown
    actions_by_type = {"hire": 0, "upskill": 0, "outsource": 0}
    for action in result.selected_actions:
        actions_by_type[action.option] += 1
    
    html_template = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CISO Executive Dashboard - Cybersecurity Workforce Optimization</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .case-study {{
            background: #f8f9fa;
            padding: 30px 40px;
            border-left: 5px solid #667eea;
            margin: 30px 40px;
            border-radius: 10px;
        }}
        
        .case-study h2 {{
            color: #1e3c72;
            margin-bottom: 15px;
            font-size: 1.8em;
        }}
        
        .case-study p {{
            line-height: 1.8;
            color: #555;
            margin-bottom: 10px;
        }}
        
        .case-study .highlight {{
            background: #fff3cd;
            padding: 2px 6px;
            border-radius: 3px;
            font-weight: 600;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 40px;
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        
        .metric-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        }}
        
        .metric-card h3 {{
            font-size: 0.9em;
            opacity: 0.9;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .metric-card .value {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .metric-card .subtext {{
            font-size: 0.85em;
            opacity: 0.8;
        }}
        
        .section {{
            padding: 40px;
        }}
        
        .section h2 {{
            color: #1e3c72;
            margin-bottom: 25px;
            font-size: 2em;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .comparison-container {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }}
        
        .comparison-box {{
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        
        .before-box {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }}
        
        .after-box {{
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        }}
        
        .comparison-box h3 {{
            color: #1e3c72;
            margin-bottom: 15px;
            font-size: 1.5em;
        }}
        
        .comparison-box .stat {{
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid rgba(0,0,0,0.1);
        }}
        
        .comparison-box .stat:last-child {{
            border-bottom: none;
        }}
        
        .comparison-box .label {{
            font-weight: 600;
            color: #555;
        }}
        
        .comparison-box .value {{
            font-weight: bold;
            color: #1e3c72;
        }}
        
        .chart-container {{
            position: relative;
            height: 400px;
            margin-bottom: 40px;
            padding: 20px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        
        .actions-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border-radius: 12px;
            overflow: hidden;
        }}
        
        .actions-table thead {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        
        .actions-table th {{
            padding: 15px;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.85em;
            letter-spacing: 1px;
        }}
        
        .actions-table td {{
            padding: 15px;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .actions-table tbody tr:hover {{
            background: #f5f7fa;
        }}
        
        .badge {{
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            text-transform: uppercase;
        }}
        
        .badge-hire {{
            background: #28a745;
            color: white;
        }}
        
        .badge-upskill {{
            background: #ffc107;
            color: #333;
        }}
        
        .badge-outsource {{
            background: #17a2b8;
            color: white;
        }}
        
        .improvement {{
            color: #28a745;
            font-weight: bold;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 20px 40px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }}
        
        @media (max-width: 768px) {{
            .comparison-container {{
                grid-template-columns: 1fr;
            }}
            
            .metrics-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        /* ===== ANIMACIONES ===== */
        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(40px); }}
            to   {{ opacity: 1; transform: translateY(0); }}
        }}
        @keyframes fadeInDown {{
            from {{ opacity: 0; transform: translateY(-40px); }}
            to   {{ opacity: 1; transform: translateY(0); }}
        }}
        @keyframes slideInLeft {{
            from {{ opacity: 0; transform: translateX(-60px); }}
            to   {{ opacity: 1; transform: translateX(0); }}
        }}
        @keyframes slideInRight {{
            from {{ opacity: 0; transform: translateX(60px); }}
            to   {{ opacity: 1; transform: translateX(0); }}
        }}
        @keyframes scaleIn {{
            from {{ opacity: 0; transform: scale(0.8); }}
            to   {{ opacity: 1; transform: scale(1); }}
        }}
        @keyframes pulseValue {{
            0%   {{ transform: scale(1); }}
            50%  {{ transform: scale(1.08); }}
            100% {{ transform: scale(1); }}
        }}
        @keyframes shimmer {{
            0%   {{ background-position: -200% center; }}
            100% {{ background-position:  200% center; }}
        }}
        @keyframes progressFill {{
            from {{ width: 0; }}
            to   {{ width: var(--target-width); }}
        }}

        /* Ocultar hasta que IntersectionObserver dispare .visible */
        .anim-fadeup    {{ opacity: 0; }}
        .anim-left      {{ opacity: 0; }}
        .anim-right     {{ opacity: 0; }}
        .anim-scale     {{ opacity: 0; }}
        .anim-fadedown  {{ opacity: 0; }}

        .anim-fadeup.visible   {{ animation: fadeInUp    0.7s ease forwards; }}
        .anim-left.visible     {{ animation: slideInLeft 0.7s ease forwards; }}
        .anim-right.visible    {{ animation: slideInRight 0.7s ease forwards; }}
        .anim-scale.visible    {{ animation: scaleIn     0.6s ease forwards; }}
        .anim-fadedown.visible {{ animation: fadeInDown  0.7s ease forwards; }}

        /* Retardos escalonados para las metric-card */
        .metric-card:nth-child(1) {{ animation-delay: 0.0s; }}
        .metric-card:nth-child(2) {{ animation-delay: 0.15s; }}
        .metric-card:nth-child(3) {{ animation-delay: 0.30s; }}
        .metric-card:nth-child(4) {{ animation-delay: 0.45s; }}

        /* Shimmer en el header */
        .header-shimmer {{
            background: linear-gradient(90deg,
                rgba(255,255,255,0) 0%,
                rgba(255,255,255,0.25) 50%,
                rgba(255,255,255,0) 100%);
            background-size: 200% auto;
            animation: shimmer 3s linear infinite;
            position: absolute; inset: 0; border-radius: inherit;
            pointer-events: none;
        }}
        header {{ position: relative; overflow: hidden; }}

        /* Pulse en los counters de las tarjetas */
        .metric-card.visible .value {{
            animation: pulseValue 0.5s ease 0.8s both;
        }}

        /* Barra de progreso animada de presupuesto */
        .budget-bar-wrap {{
            background: rgba(255,255,255,0.25);
            border-radius: 20px;
            height: 8px;
            margin-top: 8px;
            overflow: hidden;
        }}
        .budget-bar {{
            height: 100%;
            border-radius: 20px;
            background: #fff;
            width: 0;
            transition: none;
        }}
        .budget-bar.animate {{
            animation: progressFill 1.2s ease 0.5s forwards;
        }}

        /* Hover en chart-container */
        .chart-container {{
            transition: box-shadow 0.3s ease, transform 0.3s ease;
        }}
        .chart-container:hover {{
            transform: translateY(-4px);
            box-shadow: 0 12px 35px rgba(0,0,0,0.15);
        }}

        /* Grid de gráficas lado a lado */
        .charts-row {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 40px;
        }}
        @media (max-width: 900px) {{
            .charts-row {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header class="anim-fadedown visible">
            <div class="header-shimmer"></div>
            <h1>🛡️ CISO Executive Dashboard</h1>
            <p>Cybersecurity Workforce Optimization Plan</p>
        </header>
        
        <div class="case-study">
            <h2>📊 Case Study: FinTech Corp Security Transformation</h2>
            <p><strong>Company:</strong> Mid-sized financial technology company with 500 employees</p>
            <p><strong>Challenge:</strong> Limited cybersecurity team struggling to manage increasing threats including <span class="highlight">ransomware attacks</span>, <span class="highlight">supply chain compromises</span>, <span class="highlight">data leakage</span>, and <span class="highlight">compliance audit failures</span>.</p>
            <p><strong>Current State:</strong> Only {len(baseline_roles)} security staff performing basic monitoring and reactive incident response.</p>
            <p><strong>Objective:</strong> Build a comprehensive security operations capability within <span class="highlight">${budget:,.0f}</span> budget to protect critical assets and meet regulatory requirements.</p>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card anim-fadeup">
                <h3>Budget Utilization</h3>
                <div class="value">{budget_used_pct:.1f}%</div>
                <div class="subtext">${result.total_cost:,.0f} / ${budget:,.0f}</div>
                <div class="budget-bar-wrap"><div class="budget-bar" style="--target-width:{min(budget_used_pct,100):.1f}%"></div></div>
            </div>
            <div class="metric-card anim-fadeup">
                <h3>Roles Optimized</h3>
                <div class="value">{len(result.selected_actions)}</div>
                <div class="subtext">{len(baseline_roles)} baseline → {len(after_roles)} total</div>
            </div>
            <div class="metric-card anim-fadeup">
                <h3>Capability Score</h3>
                <div class="value">{result.weighted_score:.0f}</div>
                <div class="subtext">Weighted by {focus.upper()} focus</div>
            </div>
            <div class="metric-card anim-fadeup">
                <h3>Avg Risk Coverage</h3>
                <div class="value">{sum(result.risk_reduction.values()) / len(result.risk_reduction):.0f}%</div>
                <div class="subtext">Across {len(result.risk_reduction)} threat scenarios</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📈 Before vs. After Analysis</h2>
            
            <div class="comparison-container">
                <div class="comparison-box before-box anim-left">
                    <h3>❌ BEFORE - Current State</h3>
                    <div class="stat">
                        <span class="label">Security Roles:</span>
                        <span class="value">{len(baseline_roles)}</span>
                    </div>
                    <div class="stat">
                        <span class="label">Tasks Coverage:</span>
                        <span class="value">{len(before_tasks)} tasks</span>
                    </div>
                    <div class="stat">
                        <span class="label">Skills Coverage:</span>
                        <span class="value">{len(before_skills)} skills</span>
                    </div>
                    <div class="stat">
                        <span class="label">Knowledge Areas:</span>
                        <span class="value">{len(before_knowledge)} areas</span>
                    </div>
                    <div class="stat">
                        <span class="label">Annual Cost:</span>
                        <span class="value">${before_cost:,.0f}</span>
                    </div>
                    <div class="stat">
                        <span class="label">Risk Posture:</span>
                        <span class="value" style="color: #dc3545;">❌ VULNERABLE</span>
                    </div>
                </div>
                
                <div class="comparison-box after-box anim-right">
                    <h3>✅ AFTER - Optimized State</h3>
                    <div class="stat">
                        <span class="label">Security Roles:</span>
                        <span class="value">{len(after_roles)} <span class="improvement">+{len(after_roles) - len(baseline_roles)}</span></span>
                    </div>
                    <div class="stat">
                        <span class="label">Tasks Coverage:</span>
                        <span class="value">{len(result.covered_tasks)} tasks <span class="improvement">+{len(result.covered_tasks) - len(before_tasks)}</span></span>
                    </div>
                    <div class="stat">
                        <span class="label">Skills Coverage:</span>
                        <span class="value">{len(result.covered_skills)} skills <span class="improvement">+{len(result.covered_skills) - len(before_skills)}</span></span>
                    </div>
                    <div class="stat">
                        <span class="label">Knowledge Areas:</span>
                        <span class="value">{len(result.covered_knowledge)} areas <span class="improvement">+{len(result.covered_knowledge) - len(before_knowledge)}</span></span>
                    </div>
                    <div class="stat">
                        <span class="label">Total Investment:</span>
                        <span class="value">${result.total_cost:,.0f}</span>
                    </div>
                    <div class="stat">
                        <span class="label">Risk Posture:</span>
                        <span class="value" style="color: #28a745;">✅ PROTECTED</span>
                    </div>
                </div>
            </div>
            
            <div class="chart-container anim-fadeup">
                <canvas id="coverageChart"></canvas>
            </div>
        </div>

        <div class="section">
            <h2>🎯 Risk Reduction &amp; Actions Breakdown</h2>
            <div class="charts-row">
                <div class="chart-container anim-left" style="height:380px; margin-bottom:0;">
                    <canvas id="riskChart"></canvas>
                </div>
                <div class="chart-container anim-right" style="height:380px; margin-bottom:0;">
                    <canvas id="donutChart"></canvas>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>📋 Recommended Actions</h2>
            <table class="actions-table">
                <thead>
                    <tr>
                        <th>Role ID</th>
                        <th>Action Type</th>
                        <th>Investment</th>
                        <th>Score Contribution</th>
                        <th>Capabilities Added</th>
                    </tr>
                </thead>
                <tbody>'''
    
    for action in result.selected_actions:
        badge_class = f"badge-{action.option}"
        capabilities = f"{len(action.covered_tasks)}T / {len(action.covered_skills)}S / {len(action.covered_knowledge)}K"
        html_template += f'''
                    <tr>
                        <td><strong>{action.role_id}</strong></td>
                        <td><span class="badge {badge_class}">{action.option}</span></td>
                        <td>${action.cost:,.0f}</td>
                        <td>{action.score_gain:.1f}</td>
                        <td>{capabilities}</td>
                    </tr>'''
    
    html_template += f'''
                </tbody>
            </table>
        </div>
        
        <div class="section">
            <h2>💡 Key Insights & Recommendations</h2>
            <div class="comparison-box" style="background: linear-gradient(135deg, #fff5e6 0%, #ffe0b2 100%);">
                <ul style="list-style: none; padding-left: 0;">
                    <li style="padding: 10px 0; border-bottom: 1px solid rgba(0,0,0,0.1);">
                        ✅ <strong>Coverage Improvement:</strong> Tasks increased by <span class="improvement">{((len(result.covered_tasks) - len(before_tasks)) / max(len(before_tasks), 1) * 100):.0f}%</span>, from {len(before_tasks)} to {len(result.covered_tasks)} tasks
                    </li>
                    <li style="padding: 10px 0; border-bottom: 1px solid rgba(0,0,0,0.1);">
                        ✅ <strong>Team Expansion:</strong> Adding {actions_by_type['hire']} new hires, upskilling {actions_by_type['upskill']} existing staff, outsourcing {actions_by_type['outsource']} roles
                    </li>
                    <li style="padding: 10px 0; border-bottom: 1px solid rgba(0,0,0,0.1);">
                        ✅ <strong>Risk Mitigation:</strong> Average threat coverage increased from 0% to {sum(result.risk_reduction.values()) / len(result.risk_reduction):.0f}%
                    </li>
                    <li style="padding: 10px 0;">
                        ✅ <strong>Budget Efficiency:</strong> Optimal allocation using {budget_used_pct:.1f}% of available budget with {focus.upper()}-focused strategy
                    </li>
                </ul>
            </div>
        </div>
        
        <div class="footer">
            <p>Generated by CISO DSS Optimizer (NICE Framework Aligned) | Focus: {focus.upper()}</p>
            <p>This analysis uses the NICE Cybersecurity Workforce Framework for role-to-task-knowledge-skill mapping</p>
        </div>
    </div>
    
    <script>
        /* ── Animación de entrada via IntersectionObserver ── */
        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(e => {{
                if (e.isIntersecting) {{
                    e.target.classList.add('visible');
                    // barra de presupuesto
                    const bar = e.target.querySelector('.budget-bar');
                    if (bar) bar.classList.add('animate');
                    observer.unobserve(e.target);
                }}
            }});
        }}, {{ threshold: 0.15 }});
        document.querySelectorAll('.anim-fadeup, .anim-left, .anim-right, .anim-scale').forEach(el => observer.observe(el));

        /* ── Opciones de animación reutilizables ── */
        const animOpts = {{
            animation: {{
                duration: 1200,
                easing: 'easeOutQuart',
                delay: (ctx) => ctx.dataIndex * 120
            }},
            transitions: {{
                active: {{ animation: {{ duration: 400 }} }}
            }}
        }};

        /* ── Coverage Comparison Chart (barras animadas) ── */
        const coverageCtx = document.getElementById('coverageChart').getContext('2d');
        new Chart(coverageCtx, {{
            type: 'bar',
            data: {{
                labels: ['Tasks', 'Skills', 'Knowledge Areas'],
                datasets: [
                    {{
                        label: 'Before (Current State)',
                        data: [{len(before_tasks)}, {len(before_skills)}, {len(before_knowledge)}],
                        backgroundColor: 'rgba(220, 53, 69, 0.75)',
                        borderColor: 'rgba(220, 53, 69, 1)',
                        borderWidth: 2,
                        borderRadius: 8,
                        borderSkipped: false
                    }},
                    {{
                        label: 'After (Optimized State)',
                        data: [{len(result.covered_tasks)}, {len(result.covered_skills)}, {len(result.covered_knowledge)}],
                        backgroundColor: 'rgba(40, 167, 69, 0.75)',
                        borderColor: 'rgba(40, 167, 69, 1)',
                        borderWidth: 2,
                        borderRadius: 8,
                        borderSkipped: false
                    }}
                ]
            }},
            options: {{
                ...animOpts,
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    title: {{
                        display: true,
                        text: 'Capability Coverage: Before vs. After',
                        font: {{ size: 18, weight: 'bold' }}
                    }},
                    legend: {{ position: 'top' }},
                    tooltip: {{
                        callbacks: {{
                            label: ctx => ` ${{ctx.dataset.label}}: ${{ctx.parsed.y}}`
                        }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        title: {{ display: true, text: 'Number of Capabilities' }},
                        grid: {{ color: 'rgba(0,0,0,0.05)' }}
                    }},
                    x: {{ grid: {{ display: false }} }}
                }}
            }}
        }});

        /* ── Risk Radar Chart (animado) ── */
        const riskCtx = document.getElementById('riskChart').getContext('2d');
        new Chart(riskCtx, {{
            type: 'radar',
            data: {{
                labels: {list(result.risk_reduction.keys())},
                datasets: [
                    {{
                        label: 'Before (0% Coverage)',
                        data: {[0]*len(result.risk_reduction)},
                        backgroundColor: 'rgba(220, 53, 69, 0.2)',
                        borderColor: 'rgba(220, 53, 69, 1)',
                        borderWidth: 2,
                        pointBackgroundColor: 'rgba(220, 53, 69, 1)'
                    }},
                    {{
                        label: 'After (Optimized Coverage)',
                        data: {list(result.risk_reduction.values())},
                        backgroundColor: 'rgba(40, 167, 69, 0.2)',
                        borderColor: 'rgba(40, 167, 69, 1)',
                        borderWidth: 2,
                        pointBackgroundColor: 'rgba(40, 167, 69, 1)'
                    }}
                ]
            }},
            options: {{
                animation: {{ duration: 1400, easing: 'easeOutElastic' }},
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    title: {{
                        display: true,
                        text: 'Threat Scenario Coverage (%)',
                        font: {{ size: 16, weight: 'bold' }}
                    }},
                    legend: {{ position: 'top' }}
                }},
                scales: {{
                    r: {{
                        beginAtZero: true, max: 100,
                        ticks: {{ stepSize: 20 }},
                        grid: {{ color: 'rgba(0,0,0,0.1)' }}
                    }}
                }}
            }}
        }});

        /* ── Donut Chart – Actions Breakdown ── */
        const donutCtx = document.getElementById('donutChart').getContext('2d');
        new Chart(donutCtx, {{
            type: 'doughnut',
            data: {{
                labels: ['Hire 🟢', 'Upskill 🟡', 'Outsource 🔵'],
                datasets: [{{
                    data: [{actions_by_type['hire']}, {actions_by_type['upskill']}, {actions_by_type['outsource']}],
                    backgroundColor: [
                        'rgba(40,  167,  69, 0.85)',
                        'rgba(255, 193,   7, 0.85)',
                        'rgba( 23, 162, 184, 0.85)'
                    ],
                    borderColor: ['#28a745','#ffc107','#17a2b8'],
                    borderWidth: 3,
                    hoverOffset: 18
                }}]
            }},
            options: {{
                animation: {{
                    animateRotate: true,
                    animateScale: true,
                    duration: 1500,
                    easing: 'easeOutBounce'
                }},
                responsive: true,
                maintainAspectRatio: false,
                cutout: '62%',
                plugins: {{
                    title: {{
                        display: true,
                        text: 'Actions Breakdown – Invest Distribution',
                        font: {{ size: 16, weight: 'bold' }}
                    }},
                    legend: {{ position: 'bottom' }},
                    tooltip: {{
                        callbacks: {{
                            label: ctx => ` ${{ctx.label}}: ${{ctx.parsed}} action(s)`
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>'''
    
    return html_template


def plan_to_dict(result: PlanResult) -> dict:
    """Convert PlanResult to dictionary for JSON serialization."""
    return {
        "total_cost": result.total_cost,
        "weighted_score": result.weighted_score,
        "selected_actions": [
            {
                "role_id": a.role_id,
                "option": a.option,
                "cost": round(a.cost, 2),
                "score_gain": round(a.score_gain, 2)
            }
            for a in result.selected_actions
        ],
        "coverage": {
            "tasks": sorted(result.covered_tasks),
            "skills": sorted(result.covered_skills),
            "knowledge": sorted(result.covered_knowledge),
        },
        "risk_reduction_percent": result.risk_reduction,
    }
