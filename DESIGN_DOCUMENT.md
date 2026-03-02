# Design Document — CISO DSS (NICE)

## 1. Objetivo
Construir un DSS que recomiende acciones de plantilla (hire/upskill/outsource) para maximizar cobertura TKS NICE bajo presupuesto y con reducción de riesgo medible.

## 2. Arquitectura
- **Ingesta**: JSON NICE + CSV costos + JSON escenarios.
- **Motor**: scoring multi-objetivo con constraints de presupuesto.
- **Salida**: JSON estructurado + dashboard ejecutivo textual.

## 3. Modelo de decisión
Score por acción:
- Base: `w_tasks*T + w_skills*S + w_knowledge*K`
- Ajustes: `criticality_score`, `risk_impact`, multiplicadores PD/DD.
- Penalización de contratación: `hiring_speed_multiplier(time_to_hire)`.

## 4. Reglas de negocio clave
- Horizonte de 2 años para `hire` y `outsource`.
- `upskill` suma `Certification_Bonus_Cost` al costo.
- Escenarios de riesgo obligatorios: Ransomware, SupplyChainCompromise, DataLeaks, AuditFailures.

## 5. Gap Analysis
Comando `gap`:
- Entrada: workforce actual y objetivo.
- Salida: missing roles, delta de tasks y top missing tasks con roles habilitadores.

## 6. Limitaciones
- Solver greedy (no MILP exacto).
- Cobertura parcial para upskill/outsource simplificada por ratio fijo.
