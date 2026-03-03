# Mapeo de asignaturas oficiales del Máster al NICE Framework

## 1) Ciberinteligencia y Ciberdefensa

- **NICE categories / áreas**:
  - Protect & Defend (PD)
  - Analyze (AN)
  - Investigate (IN)
- **Alineación con TKS**:
  - **Tasks**: detección, análisis de amenazas, respuesta coordinada, priorización de incidentes.
  - **Skills**: threat hunting, correlación de indicadores, análisis táctico-operacional.
  - **Knowledge**: ciclo de inteligencia, TTPs adversarias, kill chain, modelos MITRE ATT&CK.
- **Impacto en el DSS**:
  - Se refleja principalmente en el preset **SOC**, que pondera fuertemente Tasks/Skills para capacidad operativa y defensiva en tiempo casi real.

## 2) Seguridad en Computación Cuántica

- **NICE categories / áreas**:
  - Securely Provision (SP)
  - Oversee & Govern (OV)
  - Protect & Defend (PD)
- **Alineación con TKS**:
  - **Tasks**: evaluación de riesgos criptográficos, planificación de transición a criptografía post-cuántica, gobierno de controles.
  - **Skills**: análisis de impacto de algoritmos cuánticos sobre PKI/firmas/intercambio de claves.
  - **Knowledge**: fundamentos de computación cuántica, amenazas a RSA/ECC, estándares PQC y cumplimiento.
- **Impacto en el DSS**:
  - Se refleja de forma natural en el preset **GRC**, priorizando Knowledge/Skills para resiliencia regulatoria y de arquitectura.

## Aplicación directa de presets oficiales en este proyecto

- `--focus soc`  → `tasks=1.0`, `skills=0.6`, `knowledge=0.3`
- `--focus grc`  → `tasks=0.4`, `skills=0.8`, `knowledge=1.0`

Estos pesos permiten simular decisiones con sesgo operativo (SOC) o de gobierno/cumplimiento y arquitectura de largo plazo (GRC).
