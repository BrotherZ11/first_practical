# CISO DSS Optimizer (NICE-aligned)

Script en Python para construir un plan de 2 años que optimiza cobertura de **Tasks, Skills, Knowledge (TKS)** del framework NICE bajo un presupuesto fijo.

## Características

- Ingesta de datos NICE desde JSON (roles + TKS).
- Carga de costos organizacionales desde `roles_costs.csv`.
- Optimización multi-objetivo con pesos configurables:
  - `Score = w_tasks * Tasks + w_skills * Skills + w_knowledge * Knowledge`.
- Restricción de presupuesto total (default: **$250,000**).
- Tres estrategias por rol:
  - `hire`
  - `upskill`
  - `outsource`
- Priorización proactiva de dominios:
  - `PD` (Protection & Defense)
  - `DD` (Design & Development)
- Cálculo de reducción de riesgo por amenaza usando tareas NICE cubiertas.

## Estructura esperada de archivos

### `nice_tks.json`

```json
{
  "roles": [
    {
      "role_id": "PD-WRL-001",
      "tasks": ["T1", "T2"],
      "skills": ["S1"],
      "knowledge": ["K1"]
    }
  ]
}
```

### `roles_costs.csv`

Columnas obligatorias:

- `Role_ID`
- `Base_Salary`
- `Training_Cost`
- `Outsourcing_Cost`
- `Time_to_Hire`
- `Criticality_Score`

### `risk_scenarios.json`

```json
{
  "Ransomware": ["T1", "T2"],
  "SupplyChainCompromise": ["T5"]
}
```

## Uso

```bash
python dss.py \
  --nice fixtures/nice_tks.json \
  --roles fixtures/roles_costs.csv \
  --risk fixtures/risk_scenarios.json \
  --budget 250000 \
  --w-tasks 0.5 \
  --w-skills 0.3 \
  --w-knowledge 0.2
```

Opcionalmente:

- `--output plan.json` para guardar salida en archivo JSON.

## Pruebas

```bash
pytest -q
```
