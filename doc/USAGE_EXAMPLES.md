# 📚 Ejemplos de Uso - CISO DSS Optimizer

Este documento proporciona ejemplos prácticos de cómo usar el sistema DSS en diferentes escenarios.

---

## 🎯 Ejemplo 1: Optimización SOC (Caso FinTech Corp)

### Escenario

Empresa fintech con equipo mínimo de seguridad necesita mejorar capacidades SOC.

### Comando

```bash
python dss.py plan \
  --nice fixtures/nice_tks.json \
  --roles fixtures/roles_costs.csv \
  --risk fixtures/risk_scenarios.json \
  --baseline-workforce fixtures/baseline_workforce.json \
  --budget 250000 \
  --focus soc \
  --dashboard-file soc_dashboard.html \
  --output soc_plan.json
```

### Resultados Esperados

```json
{
  "total_cost": 208000.0,
  "weighted_score": 23.28,
  "selected_actions": [
    {
      "role_id": "PD-WRL-001",
      "option": "upskill",
      "cost": 24000.0,
      "score_gain": 5.86
    },
    {
      "role_id": "PD-WRL-003",
      "option": "upskill",
      "cost": 26000.0,
      "score_gain": 4.36
    },
    {
      "role_id": "IO-WRL-005",
      "option": "upskill",
      "cost": 18000.0,
      "score_gain": 3.92
    },
    {
      "role_id": "DD-WRL-002",
      "option": "outsource",
      "cost": 80000.0,
      "score_gain": 4.57
    },
    {
      "role_id": "PD-WRL-006",
      "option": "outsource",
      "cost": 60000.0,
      "score_gain": 4.58
    }
  ],
  "risk_reduction_percent": {
    "Ransomware": 66.67,
    "SupplyChainCompromise": 50.0,
    "DataLeaks": 60.0,
    "AuditFailures": 60.0
  }
}
```

### Interpretación

- ✅ **Presupuesto**: $208K de $250K (83% utilizado, $42K disponible para herramientas)
- ✅ **Acciones**: 3 upskills del personal existente + 2 outsourcing de funciones especializadas
- ✅ **Cobertura**: 60%+ de protección contra amenazas críticas
- ✅ **ROI**: Mejora de 190% en puntaje de capacidades

---

## 🎯 Ejemplo 2: Optimización GRC (Compliance-First)

### Escenario

Empresa necesita pasar auditoría SOC 2 y cumplir con GDPR/PCI DSS.

### Comando

```bash
python dss.py plan \
  --nice fixtures/nice_tks.json \
  --roles fixtures/roles_costs.csv \
  --risk fixtures/risk_scenarios.json \
  --baseline-workforce fixtures/baseline_workforce.json \
  --budget 300000 \
  --focus grc \
  --dashboard-file grc_dashboard.html \
  --output grc_plan.json
```

### Pesos Utilizados

- **Tasks**: 0.4 (menor prioridad a tareas operacionales)
- **Skills**: 0.8 (habilidades técnicas importantes)
- **Knowledge**: 1.0 (máxima prioridad a conocimiento de compliance)

### Resultado Esperado

El plan priorizará roles con fuerte componente de conocimiento en:

- Frameworks de compliance (ISO 27001, NIST CSF, PCI DSS)
- Gestión de riesgos
- Políticas y procedimientos
- Auditoría y reporting

---

## 🎯 Ejemplo 3: Optimización Custom (Balanceada)

### Escenario

Startup en crecimiento necesita balance entre operaciones y governance.

### Comando

```bash
python dss.py plan \
  --nice fixtures/nice_tks.json \
  --roles fixtures/roles_costs.csv \
  --risk fixtures/risk_scenarios.json \
  --baseline-workforce fixtures/baseline_workforce.json \
  --budget 180000 \
  --focus custom \
  --w-tasks 0.6 \
  --w-skills 0.5 \
  --w-knowledge 0.4 \
  --dashboard-file custom_dashboard.html \
  --output custom_plan.json
```

### Características

- Presupuesto más ajustado ($180K)
- Pesos balanceados entre T/K/S
- Enfoque pragmático en capacidades esenciales

---

## 🎯 Ejemplo 4: Gap Analysis - Planificación a Largo Plazo

### Escenario

CISO quiere entender la brecha entre equipo actual y objetivo ideal.

### Comando

```bash
python dss.py gap \
  --nice fixtures/nice_tks.json \
  --current "PD-WRL-001,PD-WRL-003,IO-WRL-005" \
  --target "PD-WRL-001,PD-WRL-002,PD-WRL-003,PD-WRL-004,PD-WRL-005,PD-WRL-006,DD-WRL-001,DD-WRL-002,IO-WRL-001,IO-WRL-005" \
  --top-n 15 \
  --output gap_report.json
```

### Resultado Esperado

```json
{
  "current_workforce": ["IO-WRL-005", "PD-WRL-001", "PD-WRL-003"],
  "target_workforce": [
    "DD-WRL-001", "DD-WRL-002", "IO-WRL-001", "IO-WRL-005",
    "PD-WRL-001", "PD-WRL-002", "PD-WRL-003", "PD-WRL-004",
    "PD-WRL-005", "PD-WRL-006"
  ],
  "missing_roles": [
    "DD-WRL-001", "DD-WRL-002", "IO-WRL-001",
    "PD-WRL-002", "PD-WRL-004", "PD-WRL-005", "PD-WRL-006"
  ],
  "task_coverage_current": 13,
  "task_coverage_target": 35,
  "delta_tasks": 22,
  "top_missing_tasks": [
    {
      "task": "T105",
      "enabled_by_roles": ["PD-WRL-002"]
    },
    ...
  ]
}
```

### Uso del Reporte

- Identificar roles críticos que faltan
- Priorizar contrataciones por tareas faltantes
- Planificar presupuesto multi-año
- Justificar inversión en seguridad ante C-suite

---

## 🎯 Ejemplo 5: Iteración y Refinamiento

### Escenario

Después de obtener un plan inicial, el CISO quiere probar diferentes escenarios.

### Paso 1: Plan Base (SOC)

```bash
python dss.py plan \
  --nice fixtures/nice_tks.json \
  --roles fixtures/roles_costs.csv \
  --risk fixtures/risk_scenarios.json \
  --baseline-workforce fixtures/baseline_workforce.json \
  --budget 250000 \
  --focus soc \
  --output plan_v1.json
```

### Paso 2: Plan Alternativo (Mayor Presupuesto)

```bash
python dss.py plan \
  --nice fixtures/nice_tks.json \
  --roles fixtures/roles_costs.csv \
  --risk fixtures/risk_scenarios.json \
  --baseline-workforce fixtures/baseline_workforce.json \
  --budget 350000 \
  --focus soc \
  --output plan_v2.json
```

### Paso 3: Comparación

```powershell
# Comparar resultados
python -c "
import json
v1 = json.load(open('plan_v1.json'))
v2 = json.load(open('plan_v2.json'))
print(f'V1: {len(v1[\"selected_actions\"])} acciones, score {v1[\"weighted_score\"]}')
print(f'V2: {len(v2[\"selected_actions\"])} acciones, score {v2[\"weighted_score\"]}')
print(f'Mejora incremental: +{v2[\"weighted_score\"] - v1[\"weighted_score\"]:.2f} score')
print(f'Costo adicional: +${v2[\"total_cost\"] - v1[\"total_cost\"]:,.0f}')
"
```

---

## 📊 Interpretando el Dashboard HTML

### Secciones Principales

#### 1. **Case Study**

Contexto narrativo del escenario de optimización.

#### 2. **Métricas Clave** (Cards Superiores)

- **Budget Utilization**: % de presupuesto usado
- **Roles Optimized**: Número de acciones seleccionadas
- **Capability Score**: Puntaje ponderado total
- **Avg Risk Coverage**: Cobertura promedio de amenazas

#### 3. **Before vs. After Analysis**

Comparación lado a lado de:

- Número de roles
- Cobertura de tareas/skills/knowledge
- Costo anual
- Postura de riesgo

#### 4. **Gráfico de Cobertura** (Barras)

Visualiza la mejora en:

- Tasks (tareas)
- Skills (habilidades)
- Knowledge (conocimientos)

#### 5. **Gráfico de Riesgos** (Radar)

Muestra cobertura % para cada escenario de amenaza:

- Ransomware
- Supply Chain Compromise
- Data Leaks
- Audit Failures

#### 6. **Tabla de Acciones**

Desglose detallado de cada acción recomendada con:

- Role ID
- Tipo de acción (hire/upskill/outsource)
- Costo individual
- Contribución al score
- Capacidades añadidas

#### 7. **Key Insights**

Resumen ejecutivo de:

- Mejora en cobertura
- Composición de acciones
- Mitigación de riesgos
- Eficiencia presupuestaria

---

## 🔧 Tips y Mejores Prácticas

### 1. Empezar con Focus Presets

Para primeras iteraciones, usar presets predefinidos:

- `--focus soc` si la prioridad es detección y respuesta
- `--focus grc` si la prioridad es compliance y governance

### 2. Guardar Múltiples Versiones

Mantener histórico de planes:

```bash
# Agregar timestamp a los archivos
python dss.py plan ... --output plan_$(date +%Y%m%d).json
```

### 3. Validar con Gap Analysis

Antes de implementar el plan:

```bash
# Comparar baseline vs. roles en el plan optimizado
python dss.py gap --nice fixtures/nice_tks.json \
  --current "PD-WRL-001,PD-WRL-003,IO-WRL-005" \
  --target "$(python extract_roles.py plan.json)"
```

### 4. Presentar a Stakeholders

El dashboard HTML es ideal para:

- Reuniones de leadership
- Board presentations
- Justificación de presupuesto
- Tracking de progreso trimestral

---

## 🚀 Casos de Uso Avanzados

### Escenario: Respuesta a Incidente Mayor

**Situación**: Después de un incidente de ransomware, necesitas justificar inversión urgente.

```bash
# Generar plan de respuesta rápida
python dss.py plan \
  --nice fixtures/nice_tks.json \
  --roles fixtures/roles_costs.csv \
  --risk fixtures/risk_scenarios.json \
  --baseline-workforce fixtures/baseline_workforce.json \
  --budget 500000 \
  --focus soc \
  --dashboard-file incident_response_plan.html
```

**Usar el dashboard para**:

- Mostrar la brecha de capacidades que permitió el incidente (Before)
- Presentar plan de remediación (After)
- Justificar presupuesto de emergencia
- Establecer métricas de éxito

---

### Escenario: Planificación Multi-Año

**Situación**: Necesitas roadmap de 3 años para madurez de seguridad.

```bash
# Año 1: Foundation (presupuesto limitado)
python dss.py plan --budget 150000 --focus soc --output year1_plan.json --dashboard-file year1_dashboard.html

# Año 2: Enhancement (presupuesto medio)
python dss.py plan --budget 250000 --focus soc --output year2_plan.json --dashboard-file year2_dashboard.html

# Año 3: Optimization (presupuesto completo)
python dss.py plan --budget 400000 --focus soc --output year3_plan.json --dashboard-file year3_dashboard.html
```

**Resultado**: 3 dashboards mostrando evolución incremental de capacidades.

---

## 📈 Métricas de Éxito

Al implementar el plan, trackear:

1. **Coverage Metrics**
   - % de tareas NICE cubiertas
   - Número de certificaciones obtenidas
   - Skills gap cerrado

2. **Risk Metrics**
   - Mean Time to Detect (MTTD)
   - Mean Time to Respond (MTTR)
   - # de incidentes prevenidos

3. **Business Metrics**
   - Compliance score (SOC 2, ISO 27001)
   - Audit findings reducidos
   - Insurance premium cambios

4. **Financial Metrics**
   - Actual spend vs. plan
   - ROI (breaches avoided $)
   - Cost avoidance

---

## ❓ Troubleshooting

### Problema: "No valid roles found"

**Causa**: Archivo nice_tks.json con formato incorrecto  
**Solución**: Verificar que tiene estructura `{"roles": [...]}`

### Problema: "Budget too low, no feasible solution"

**Causa**: Presupuesto insuficiente para cualquier acción válida  
**Solución**: Aumentar budget o revisar costos en roles_costs.csv

### Problema: "Dashboard no se genera"

**Causa**: Error en escritura de archivo  
**Solución**: Verificar permisos de escritura en directorio

---

_Para más ejemplos, ver [CASE_STUDY.md](CASE_STUDY.md)_
