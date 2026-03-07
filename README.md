# CISO DSS Optimizer - NICE Framework Aligned

Optimizador de fuerza de trabajo de ciberseguridad alineado con el marco NICE Framework.

## 📁 Estructura del Proyecto

```
first_practical/
├── dss.py                     # Punto de entrada principal
├── dss_modules/               # Módulos refactorizados
│   ├── __init__.py
│   ├── models.py              # Modelos de datos y constantes
│   ├── loaders.py             # Cargadores de datos
│   ├── optimizer.py           # Algoritmo de optimización
│   ├── gap_analysis.py        # Análisis de brechas
│   ├── dashboard.py           # Generación de dashboards
│   └── cli.py                 # Interfaz de línea de comandos
├── fixtures/                  # Datos de entrada
│   ├── nice_tks.json         # Mapeo NICE Framework
│   ├── roles_costs.csv       # Costos de roles
│   ├── risk_scenarios.json   # Escenarios de riesgo
│   └── baseline_workforce.json
├── output/                    # Resultados de ejecución (generados)
│   ├── *.json                # Planes en formato JSON
│   └── *.html                # Dashboards HTML interactivos
├── tests/                     # Tests unitarios
│   └── test_dss.py
└── doc/                       # Documentación
    ├── README.md              # Documentación principal
    ├── USAGE_EXAMPLES.md      # Ejemplos de uso
    ├── DESIGN_DOCUMENT.md     # Documento de diseño
    ├── CASE_STUDY.md          # Caso de estudio
    ├── CISO_SLIDES.md         # Presentación ejecutiva
    ├── DASHBOARD_SUMMARY.md   # Resumen del dashboard
    ├── NICE_MASTER_MAPPING.md # Mapeo NICE Framework
    └── ARCHITECTURE.md        # Arquitectura del sistema

```

## 🚀 Uso Rápido

### Opción 1: Script de Generación Automática

Genera múltiples planes de una vez:

```bash
python generate_plans.py
```

Este script genera automáticamente:

- Plan SOC (Security Operations Center)
- Plan GRC (Governance, Risk & Compliance)
- Plan SOC con mayor presupuesto

### Opción 2: Generación Manual

#### Generar Plan Optimizado

```bash
python dss.py plan \
  --nice fixtures/nice_tks.json \
  --roles fixtures/roles_costs.csv \
  --risk fixtures/risk_scenarios.json \
  --baseline-workforce fixtures/baseline_workforce.json \
  --focus soc \
  --budget 250000 \
  --output output/plan.json \
  --dashboard-file output/soc_dashboard.html
```

### Análisis de Brechas

```bash
python dss.py gap \
  --nice fixtures/nice_tks.json \
  --current "PR-CDA-001,AN-TWA-001,OM-ANA-001" \
  --target "PR-CDA-001,AN-TWA-001,OM-ANA-001,SP-RSK-001,OV-MGT-001"
```

## 📚 Módulos

### models.py

Define los modelos de datos principales:

- `RoleCost`: Información de costos de roles
- `RoleTKS`: Tareas, conocimientos y habilidades
- `PlanAction`: Acciones del plan
- `PlanResult`: Resultado de optimización

### loaders.py

Funciones para cargar datos desde archivos:

- `load_nice_tks()`: Carga mapeo NICE
- `load_role_costs()`: Carga costos de roles
- `load_risk_scenarios()`: Carga escenarios de riesgo
- `load_baseline_workforce()`: Carga fuerza de trabajo actual

### optimizer.py

Algoritmo de optimización multiple-choice knapsack:

- `optimize_plan()`: Optimiza selección de roles bajo presupuesto
- `build_action()`: Construye acción con cálculo de score

### gap_analysis.py

Análisis de brechas de capacidades:

- `gap_analysis()`: Compara fuerza de trabajo actual vs objetivo

### dashboard.py

Generación de visualizaciones:

- `dashboard_text()`: Dashboard texto simple
- `generate_html_dashboard()`: Dashboard HTML profesional
- `plan_to_dict()`: Serialización a JSON

### cli.py

Interfaz de línea de comandos:

- `parse_args()`: Parse argumentos CLI
- `run_plan_command()`: Ejecuta optimización
- `run_gap_command()`: Ejecuta análisis de brechas

## 🧪 Tests

Ejecuta los tests con pytest:

```bash
pytest tests/test_dss.py -v
```

## 📖 Documentación Completa

Consulta la carpeta `doc/` para documentación detallada:

- **README.md**: Documentación principal
- **USAGE_EXAMPLES.md**: Ejemplos prácticos de uso
- **DESIGN_DOCUMENT.md**: Diseño técnico del sistema
- **CASE_STUDY.md**: Estudio de caso completo
- **ARCHITECTURE.md**: Arquitectura del sistema refactorizado

## 📂 Resultados de Ejecución

Los archivos generados se guardan automáticamente en la carpeta `output/`:

- **JSON files**: Planes de optimización en formato estructurado
- **HTML files**: Dashboards ejecutivos interactivos con visualizaciones

```bash
output/
├── plan.json                  # Plan personalizado
├── soc_plan.json             # Plan optimizado SOC
├── executive_dashboard.html  # Dashboard ejecutivo
└── soc_dashboard.html        # Dashboard SOC
```

💡 **Tip**: Abre los archivos HTML directamente en tu navegador para ver los dashboards interactivos.

## 🎯 Características

- ✅ Optimización basada en algoritmo multiple-choice knapsack
- ✅ Alineamiento con NICE Cybersecurity Workforce Framework
- ✅ Soporte para múltiples estrategias (SOC, GRC, Custom)
- ✅ Dashboards HTML interactivos con gráficos
- ✅ Análisis de reducción de riesgo por escenario
- ✅ Análisis de brechas de capacidades

## 📄 Licencia

MIT License - Ver archivo LICENSE para detalles.
