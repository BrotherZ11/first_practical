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

## Comando de optimización

```bash
python dss.py plan \
  --nice fixtures/nice_tks.json \
  --roles fixtures/roles_costs.csv \
  --risk fixtures/risk_scenarios.json \
  --budget 250000 \
  --focus soc \
  --dashboard
```

### Presets de enfoque
- `--focus soc`: prioriza cobertura operacional (Tasks>Skills>Knowledge).
- `--focus grc`: prioriza conocimiento de gobierno/riesgo/cumplimiento.
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
