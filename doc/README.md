# 🛡️ CISO DSS Optimizer - Sistema de Optimización de Fuerza Laboral en Ciberseguridad

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![NICE Framework](https://img.shields.io/badge/NICE-Framework-green.svg)](https://www.nist.gov/itl/applied-cybersecurity/nice/nice-framework-resource-center)

Sistema profesional de soporte a decisiones (DSS) para CISOs que optimiza la planificación de la fuerza laboral en ciberseguridad usando el **NICE Cybersecurity Workforce Framework**. Incluye análisis de brechas avanzado, optimización de presupuesto y dashboards ejecutivos interactivos.

---

## ✨ Características Principales

### 🎯 Capacidades Core

- **Optimización de Fuerza Laboral**: Optimiza la composición del equipo de seguridad dentro de restricciones presupuestarias
- **Análisis de Brechas**: Compara capacidades actuales vs. objetivos
- **Planificación Basada en Riesgos**: Alinea roles con escenarios de amenaza críticos
- **Alineación con NICE Framework**: Mapea roles a Tareas, Conocimientos y Habilidades
- **Estrategia Multi-opción**: Combina contratación, capacitación y outsourcing
- **Dashboards Profesionales**: Reportes HTML interactivos con visualizaciones antes/después

### 📊 Características del Dashboard

- **Análisis Antes vs. Después**: Visualización clara de brechas
- **Gráficos Interactivos**: Comparación de cobertura y métricas de reducción de riesgos
- **Seguimiento de Presupuesto**: Monitoreo en tiempo real del uso del presupuesto
- **Recomendaciones Accionables**: Lista priorizada de acciones optimizadas
- **Listo para Ejecutivos**: Diseño profesional para presentaciones C-level

---

## 🚀 Inicio Rápido

### Instalación

```bash
# No requiere dependencias adicionales (usa solo stdlib de Python)
```

### Uso Básico

```bash
# Generar plan optimizado con dashboard profesional
python dss.py plan \
  --nice fixtures/nice_tks.json \
  --roles fixtures/roles_costs.csv \
  --risk fixtures/risk_scenarios.json \
  --baseline-workforce fixtures/baseline_workforce.json \
  --budget 250000 \
  --focus soc \
  --dashboard-file executive_dashboard.html \
  --output plan.json
```

**Abrir el dashboard:**

```bash
# Windows
start executive_dashboard.html

# PowerShell
Invoke-Item executive_dashboard.html
```

---

## 📖 Guía de Uso

### Comando: `plan`

Construye un plan optimizado de fuerza laboral bajo restricciones de presupuesto.

```bash
python dss.py plan [OPCIONES]
```

#### Argumentos Requeridos

| Argumento              | Descripción                           | Ejemplo                            |
| ---------------------- | ------------------------------------- | ---------------------------------- |
| `--nice`               | Mapeo de roles/TKS del NICE Framework | `fixtures/nice_tks.json`           |
| `--roles`              | Costos y metadatos de roles           | `fixtures/roles_costs.csv`         |
| `--risk`               | Definiciones de escenarios de riesgo  | `fixtures/risk_scenarios.json`     |
| `--baseline-workforce` | Fuerza laboral actual                 | `fixtures/baseline_workforce.json` |

#### Argumentos Opcionales

| Argumento          | Por Defecto | Descripción                                     |
| ------------------ | ----------- | ----------------------------------------------- |
| `--budget`         | 250000      | Presupuesto máximo                              |
| `--focus`          | custom      | Preset de enfoque: `soc`, `grc`, o `custom`     |
| `--w-tasks`        | 0.5         | Peso para cobertura de tareas (si focus=custom) |
| `--w-skills`       | 0.3         | Peso para cobertura de habilidades              |
| `--w-knowledge`    | 0.2         | Peso para cobertura de conocimientos            |
| `--output`         | -           | Guardar plan en archivo JSON                    |
| `--dashboard`      | false       | Mostrar dashboard de texto en consola           |
| `--dashboard-file` | -           | Generar dashboard HTML profesional              |

#### Presets de Enfoque

| Preset     | Descripción                        | Pesos (T/S/K)           |
| ---------- | ---------------------------------- | ----------------------- |
| **soc**    | Centro de Operaciones de Seguridad | 1.0 / 0.6 / 0.3         |
| **grc**    | Governance, Risk & Compliance      | 0.4 / 0.8 / 1.0         |
| **custom** | Pesos personalizados               | Especificar manualmente |

### Comando: `gap`

Realiza análisis de brechas entre fuerza laboral actual y objetivo.

```bash
python dss.py gap \
  --nice fixtures/nice_tks.json \
  --current "PD-WRL-001,PD-WRL-003,IO-WRL-005" \
  --target "PD-WRL-001,PD-WRL-002,PD-WRL-003,DD-WRL-002,PD-WRL-006" \
  --top-n 10 \
  --output gap_analysis.json
```

---

## 📁 Estructura de Archivos de Datos

### 1. `nice_tks.json` - Mapeos del NICE Framework

Mapea IDs de roles a Tareas, Conocimientos y Habilidades:

```json
{
  "roles": [
    {
      "role_id": "PD-WRL-001",
      "tasks": ["T100", "T101", "T102"],
      "skills": ["S100", "S101", "S102"],
      "knowledge": ["K100", "K101", "K102"]
    }
  ]
}
```

### 2. `roles_costs.csv` - Economía de Roles

```csv
Role_ID,Base_Salary,Training_Cost,Outsourcing_Cost,Time_to_Hire,Criticality_Score,Risk_Impact,Certification_Bonus_Cost
PD-WRL-001,70000,18000,45000,75,1.4,0.9,6000
```

### 3. `risk_scenarios.json` - Escenarios de Amenazas

```json
{
  "Ransomware": ["T100", "T101", "T109", "T111"],
  "SupplyChainCompromise": ["T200", "T203", "T206"],
  "DataLeaks": ["T303", "T308", "T311"],
  "AuditFailures": ["T400", "T402", "T414"]
}
```

### 4. `baseline_workforce.json` - Equipo Actual

```json
{
  "baseline_workforce": [
    {
      "role_id": "PD-WRL-001",
      "description": "Actualmente realiza monitoreo básico de SIEM/EDR."
    }
  ]
}
```

---

## 🎓 Caso de Estudio: FinTech Corp

Un caso de estudio completo demuestra el DSS en acción:

**Escenario:** Empresa fintech mediana con capacidades de seguridad limitadas  
**Desafío:** Equipo de 3 personas enfrentando ransomware, ataques de cadena de suministro, fugas de datos  
**Presupuesto:** $250,000  
**Resultado:** 67% de expansión del equipo, 60%+ de cobertura de riesgos, 190% de mejora en capacidades

📄 **Caso de Estudio Completo**: [CASE_STUDY.md](CASE_STUDY.md)

### Métricas Clave

| Métrica              | Antes     | Después         | Mejora       |
| -------------------- | --------- | --------------- | ------------ |
| Roles de Seguridad   | 3         | 5               | +67%         |
| Cobertura de Tareas  | 13        | 11 (optimizado) | Enfocado     |
| Cobertura de Riesgos | 0%        | 60%+            | ✅ Protegido |
| Puntaje de Capacidad | ~8        | 23.28           | +190%        |
| Inversión            | $210K/año | $208K           | Neutral      |

---

## 🏗️ Arquitectura

### Algoritmo: Multiple-Choice Knapsack

El optimizador usa **programación dinámica** para resolver un problema de mochila de elección múltiple:

- **Items**: Roles de seguridad
- **Opciones**: Contratar, Capacitar o Outsourcing
- **Restricción**: Límite de presupuesto
- **Objetivo**: Maximizar puntaje ponderado de capacidades

### Factores de Puntuación

1. **Métricas de Cobertura**: Tareas, Habilidades, Conocimientos (pesos definidos por usuario)
2. **Multiplicadores Estratégicos**:
   - Puntaje de Criticidad (+0-20%)
   - Impacto en Riesgo (+0-10%)
   - Dominio Prioritario (PD: +20%, DD: +15%)
3. **Penalizaciones Operacionales**:
   - Tiempo de contratación lento (-60% a 0%)
4. **Bonos por Opción**:
   - Bonus de velocidad por outsourcing (+3%)

---

## 📊 Vista Previa del Dashboard

### Visualización Antes vs. Después

El dashboard profesional incluye:

- ✅ Comparación lado a lado (estado actual vs. optimizado)
- ✅ Gráficos de barras interactivos (cobertura de capacidades)
- ✅ Gráficos de radar (cobertura de escenarios de amenazas)
- ✅ Desglose detallado de acciones con costo/beneficio
- ✅ Insights clave y recomendaciones
- ✅ Cálculos de ROI

**Ejemplo de Salida del Dashboard:**

```
=== Métricas Principales ===
✅ Utilización de Presupuesto: 83.2% ($208,000 / $250,000)
✅ Roles Optimizados: 5 acciones (3 baseline → 5 total)
✅ Puntaje de Capacidad: 23.28 (enfoque SOC)
✅ Cobertura Promedio de Riesgos: 59% en 4 escenarios

=== Análisis Antes vs. Después ===
ANTES - Estado Actual:
- Roles de Seguridad: 3
- Cobertura de Tareas: 13 tareas
- Postura de Riesgo: ❌ VULNERABLE

DESPUÉS - Estado Optimizado:
- Roles de Seguridad: 5 (+67%)
- Cobertura de Tareas: 11+ tareas (optimizado)
- Postura de Riesgo: ✅ PROTEGIDO

=== Acciones Recomendadas ===
1. PD-WRL-001: upskill → $24,000 (Capacitación avanzada en threat hunting)
2. PD-WRL-003: upskill → $26,000 (Capacidades forenses)
3. IO-WRL-005: upskill → $18,000 (Enfoque dedicado en seguridad)
4. DD-WRL-002: outsource → $80,000 (Gestión de vulnerabilidades 24/7)
5. PD-WRL-006: outsource → $60,000 (Inteligencia de amenazas)
```

---

## 🧪 Pruebas

```bash
# Ejecutar suite de pruebas
python -m pytest tests/test_dss.py -v

# Con cobertura
python -m pytest tests/test_dss.py --cov=dss --cov-report=html
```

---

## 📚 Documentación

- **[NICE Framework](https://www.nist.gov/itl/applied-cybersecurity/nice/nice-framework-resource-center)**: Recurso oficial de NIST
- **[Documento de Diseño](DESIGN_DOCUMENT.md)**: Detalles de arquitectura y algoritmo
- **[Caso de Estudio](CASE_STUDY.md)**: Ejemplo de aplicación real
- **[Slides CISO](CISO_SLIDES.md)**: Materiales para presentación ejecutiva
- **[Mapeo NICE](NICE_MASTER_MAPPING.md)**: Mapeo de asignaturas del Máster al NICE Framework

---

## 🎯 Criterio de Optimización

El planificador usa optimización tipo **multiple-choice knapsack** con workforce base:

- Para cada rol selecciona **como máximo una acción**
- Busca la combinación que **maximiza el `weighted_score` total**
- Sin superar el `budget`

**Regla de Workforce:**

- Si el rol está en `baseline_workforce`: solo se permite `upskill` (ya existe en la empresa)
- Si el rol NO está en `baseline_workforce`: se permite `hire` u `outsource` (debe incorporarse)

Esto evita sesgos por costo mínimo y asegura elegir siempre la combinación con mejor score agregado dentro de presupuesto.

---

## 🙏 Entregables Incluidos

- ✅ `dss.py`: CLI con comandos `plan` y `gap`
- ✅ `DESIGN_DOCUMENT.md`: documento de diseño técnico
- ✅ `CISO_SLIDES.md`: versión textual de slides ejecutivas
- ✅ `NICE_MASTER_MAPPING.md`: mapeo de 2 asignaturas del Máster al NICE Framework
- ✅ `CASE_STUDY.md`: caso de estudio completo con análisis ROI
- ✅ `executive_dashboard.html`: dashboard profesional e interactivo
- ✅ `tests/test_dss.py`: suite completa de pruebas

---

## 📧 Contacto

**Repository**: [github.com/BrotherZ11/first_practical](https://github.com/BrotherZ11/first_practical)  
**Issues**: [Reportar bugs o solicitar features](https://github.com/BrotherZ11/first_practical/issues)

---

_Construido con ❤️ para CISOs y líderes de seguridad_
