# Output Directory

Esta carpeta contiene los resultados generados por el CISO DSS Optimizer.

## 📁 Contenido

### Archivos JSON

Planes de optimización en formato JSON estructurado:

- `plan.json` - Plan personalizado con pesos custom
- `soc_plan.json` - Plan optimizado para SOC (Security Operations Center)
- `grc_plan.json` - Plan optimizado para GRC (Governance, Risk & Compliance)

**Estructura JSON:**

```json
{
  "total_cost": 123456.78,
  "weighted_score": 456.78,
  "selected_actions": [
    {
      "role_id": "PR-CDA-001",
      "option": "hire",
      "cost": 120000.0,
      "score_gain": 45.6
    }
  ],
  "coverage": {
    "tasks": ["T0001", "T0002"],
    "skills": ["S0001", "S0002"],
    "knowledge": ["K0001", "K0002"]
  },
  "risk_reduction_percent": {
    "Ransomware": 85.5,
    "SupplyChainCompromise": 72.3,
    "DataLeaks": 90.1,
    "AuditFailures": 95.0
  }
}
```

### Archivos HTML

Dashboards ejecutivos interactivos con visualizaciones:

- `executive_dashboard.html` - Dashboard ejecutivo general
- `soc_dashboard.html` - Dashboard para estrategia SOC
- `grc_dashboard.html` - Dashboard para estrategia GRC

**Características de los dashboards:**

- 📊 Gráficos interactivos con Chart.js
- 📈 Análisis Before/After
- 🎯 Visualización de reducción de riesgo
- 💰 Métricas de presupuesto y ROI
- 📱 Diseño responsive

## 🔄 Regeneración

Los archivos en esta carpeta son generados automáticamente y **no deben** ser editados manualmente. Para regenerar:

```bash
# Plan SOC
python dss.py plan \
  --nice fixtures/nice_tks.json \
  --roles fixtures/roles_costs.csv \
  --risk fixtures/risk_scenarios.json \
  --baseline-workforce fixtures/baseline_workforce.json \
  --focus soc \
  --budget 250000 \
  --output output/soc_plan.json \
  --dashboard-file output/soc_dashboard.html

# Plan GRC
python dss.py plan \
  --nice fixtures/nice_tks.json \
  --roles fixtures/roles_costs.csv \
  --risk fixtures/risk_scenarios.json \
  --baseline-workforce fixtures/baseline_workforce.json \
  --focus grc \
  --budget 250000 \
  --output output/grc_plan.json \
  --dashboard-file output/grc_dashboard.html
```

## 📝 Notas

- Esta carpeta está incluida en `.gitignore` para evitar subir archivos generados al repositorio
- Los archivos se sobrescriben en cada ejecución
- Abre los archivos HTML directamente en tu navegador preferido
- Los JSON pueden ser procesados por otras herramientas o scripts

## 🎯 Uso de los Resultados

### Para Ejecutivos (CISO, CIO)

👉 Abre el archivo HTML correspondiente en tu navegador para ver:

- Resumen ejecutivo con métricas clave
- Visualizaciones de reducción de riesgo
- Comparación antes/después
- Lista de acciones recomendadas con inversiones

### Para Analistas Técnicos

👉 Usa los archivos JSON para:

- Integración con otras herramientas
- Análisis programático
- Generación de reportes personalizados
- Automatización de procesos

### Para Auditoría

👉 Los archivos proporcionan trazabilidad completa de:

- Decisiones de inversión
- Justificación basada en riesgo
- Cobertura de capacidades NICE Framework
- Alineamiento con objetivos de seguridad
