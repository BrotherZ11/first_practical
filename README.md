# CISO DSS Optimizer (NICE-aligned)

Sistema DSS para apoyar decisiones CISO con optimización multi-objetivo, análisis de brechas y salida ejecutiva.

## Entregables incluidos

- `dss.py`: CLI con comandos `plan` y `gap`.
- `DESIGN_DOCUMENT.md`: documento de diseño técnico.
- `CISO_SLIDES.md`: versión textual de slides ejecutivas.
- `NICE_MASTER_MAPPING.md`: mapeo de 2 asignaturas del Máster al NICE Framework.

## Datos de entrada

### `nice_tks.json`
Contiene roles NICE y su cobertura TKS.

### `roles_costs.csv`
Columnas obligatorias:
- `Role_ID`
- `Base_Salary`
- `Training_Cost`
- `Outsourcing_Cost`
- `Time_to_Hire`
- `Criticality_Score`
- `Risk_Impact`
- `Certification_Bonus_Cost`

### `risk_scenarios.json`
Escenarios mínimos requeridos:
- `Ransomware`
- `SupplyChainCompromise`
- `DataLeaks`
- `AuditFailures`

### `baseline_workforce.json`
Define los roles que actualmente existen en la empresa (Baseline Workforce).

Para este proyecto se incluyen:
- `PD-WRL-001`
- `PD-WRL-003`
- `IO-WRL-005`

## Criterio de optimización

El planificador usa una optimización tipo *multiple-choice knapsack* con workforce base: para cada rol selecciona como máximo una acción y busca la combinación que **maximiza el `weighted_score` total** sin superar el `budget`.

Regla de workforce:
- Si el rol está en `baseline_workforce`, sólo se permite `upskill` (ya existe en la empresa).
- Si el rol no está en `baseline_workforce`, se permite `hire` o `outsource` (cobertura externa cuando compensa por coste/velocidad).

Sensibilidad de pesos:
- Los pesos `tasks/skills/knowledge` son el componente principal del score.
- Criticidad, riesgo, prioridad de dominio y tiempo de contratación se aplican como ajustes moderados para evitar que anulen el efecto de los pesos de foco.

Esto evita sesgos por coste mínimo y asegura que, al añadir más filas/valores al CSV, se elija siempre la combinación con mejor score agregado dentro de presupuesto.

## Comando de optimización

```bash
python dss.py plan \
  --nice fixtures/nice_tks.json \
  --roles fixtures/roles_costs.csv \
  --risk fixtures/risk_scenarios.json \
  --baseline-workforce fixtures/baseline_workforce.json \
  --budget 250000 \
  --focus soc \
  --dashboard
```

### Presets de enfoque (valores oficiales)
- `--focus soc`: `tasks=1.0`, `skills=0.6`, `knowledge=0.3`.
- `--focus grc`: `tasks=0.4`, `skills=0.8`, `knowledge=1.0`.
- `--focus custom`: usa `--w-tasks --w-skills --w-knowledge`.

## Comando Gap Analysis

```bash
python dss.py gap \
  --nice fixtures/nice_tks.json \
  --current PD-WRL-001,DD-WRL-002 \
  --target PD-WRL-001,PD-WRL-003,PD-WRL-006,DD-WRL-002,IO-WRL-005
```

Salida: delta de cobertura entre Current Workforce y Target Workforce, incluyendo `top_missing_tasks`.

## Pruebas

```bash
pytest -q
```
