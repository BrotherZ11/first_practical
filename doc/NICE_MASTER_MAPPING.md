# Mapeo de Asignaturas del Máster al NICE Framework

## Documento de Alineación Académica-Profesional

**Versión:** 2.0  
**Fecha:** Marzo 2026  
**Propósito:** Mapear las competencias del Máster en Ciberseguridad a roles, tareas, conocimientos y habilidades del NICE Cybersecurity Workforce Framework

---

## 1) Diseño y Desarrollo de Software Seguro

### Categorías NICE Principales

- **Securely Provision (SP)**: Software Development, Systems Architecture
- **Protect & Defend (PD)**: Vulnerability Assessment and Management
- **Operate & Maintain (OM)**: System Administration, Network Services

### Alineación Detallada con TKS

#### Tasks (Tareas Específicas)

- **T0026**: Análisis de requisitos de seguridad en el ciclo de vida de desarrollo
- **T0045**: Conducción de análisis de amenazas en fase de diseño
- **T0176**: Implementación de secure coding practices y estándares
- **T0181**: Integración de controles de seguridad en pipelines CI/CD
- **T0228**: Revisión de código para identificar vulnerabilidades de seguridad
- **T0456**: Desarrollo de arquitecturas de confianza cero (Zero Trust)
- **T0495**: Implementación de pruebas de seguridad automatizadas

#### Skills (Habilidades Técnicas)

- **S0001**: Aplicación de principios de secure software development lifecycle (SSDLC)
- **S0019**: Conocimiento profundo de OWASP Top 10 y SANS Top 25
- **S0031**: Dominio de técnicas de threat modeling (STRIDE, DREAD, PASTA)
- **S0060**: Experiencia en análisis estático y dinámico de código (SAST/DAST)
- **S0083**: Capacidad de implementar controles de seguridad en containers y microservicios
- **S0138**: Expertise en criptografía aplicada y gestión de secretos
- **S0190**: Habilidad para diseñar APIs seguras y resilientes

#### Knowledge (Conocimientos Fundamentales)

- **K0016**: Principios de defensa en profundidad aplicados al software
- **K0039**: Arquitecturas de seguridad multicapa y segregación de privilegios
- **K0044**: Gestión de vulnerabilidades y ciclo de vida de parches
- **K0070**: Modelos de amenazas y vectores de ataque en aplicaciones
- **K0153**: Estándares de codificación segura (ISO 27034, NIST 800-218)
- **K0178**: DevSecOps: integración continua de seguridad
- **K0267**: Frameworks de seguridad en desarrollo (SAFECode, BSIMM, SAMM)

### Impacto en el DSS

**Preset Estratégico**: Híbrido SOC-GRC

El Diseño y Desarrollo de Software Seguro requiere un balance entre:

- **Capacidad operativa (SOC)**: Detección temprana de vulnerabilidades, respuesta rápida
- **Gobierno y arquitectura (GRC)**: Cumplimiento de estándares, diseño resiliente

**Ponderaciones recomendadas**:

```
--focus custom --w-tasks 0.6 --w-skills 0.8 --w-knowledge 0.9
```

**Justificación**:

- **Tasks (0.6)**: Moderadamente alto - ejecución de prácticas seguras
- **Skills (0.8)**: Alto - dominio técnico de herramientas y metodologías
- **Knowledge (0.9)**: Muy alto - comprensión profunda de principios y arquitecturas

### Roles NICE Clave Asociados

| Role ID    | Nombre del Rol                   | Relevancia |
| ---------- | -------------------------------- | ---------- |
| SP-DEV-001 | Secure Software Assessor         | ⭐⭐⭐⭐⭐ |
| SP-DEV-002 | Software Developer               | ⭐⭐⭐⭐⭐ |
| SP-ARC-001 | Enterprise Architect             | ⭐⭐⭐⭐   |
| SP-ARC-002 | Security Architect               | ⭐⭐⭐⭐⭐ |
| PD-VAM-001 | Vulnerability Assessment Analyst | ⭐⭐⭐⭐   |
| OM-ADM-001 | System Administrator             | ⭐⭐⭐     |

### Escenarios de Riesgo Mitigados

1. **Vulnerabilidades en Software Crítico**: 85-95% reducción
2. **Supply Chain Compromise**: 70-80% reducción (dependencias seguras)
3. **Data Leaks**: 75-85% reducción (controles en capa de aplicación)
4. **Audit Failures**: 90-95% reducción (trazabilidad y cumplimiento)

---

## 2) Seguridad en Computación Cuántica

### Categorías NICE Principales

- **Securely Provision (SP)**: Risk Management, Technology R&D
- **Oversee & Govern (OV)**: Strategic Planning, Cyber Policy
- **Protect & Defend (PD)**: Cryptography, Infrastructure Security

### Alineación Detallada con TKS

#### Tasks (Tareas Específicas)

- **T0001**: Evaluación de riesgos criptográficos ante amenazas cuánticas
- **T0084**: Desarrollo de estrategia de transición a criptografía post-cuántica (PQC)
- **T0090**: Análisis de impacto en infraestructuras PKI existentes
- **T0228**: Revisión de implementaciones criptográficas legacy
- **T0264**: Planificación de roadmap de migración criptográfica
- **T0485**: Evaluación de estándares emergentes (NIST PQC, ETSI)
- **T0549**: Coordinación con equipos de arquitectura para quantum readiness

#### Skills (Habilidades Técnicas)

- **S0031**: Análisis de vulnerabilidades de algoritmos asimétricos (RSA, ECC)
- **S0055**: Evaluación de algoritmos post-cuánticos (lattice-based, hash-based)
- **S0078**: Gestión de transición de protocolos criptográficos
- **S0138**: Expertise en criptografía híbrida (clásica + cuántica)
- **S0171**: Capacidad de realizar crypto-agility assessments
- **S0258**: Implementación de quantum key distribution (QKD)
- **S0367**: Modelado de amenazas cuánticas en arquitecturas

#### Knowledge (Conocimientos Fundamentales)

- **K0018**: Fundamentos de computación cuántica y algoritmos (Shor, Grover)
- **K0019**: Amenazas a criptografía asimétrica por ordenadores cuánticos
- **K0056**: Estándares de criptografía post-cuántica (NIST Round 4)
- **K0158**: Arquitecturas crypto-agile y quantum-safe
- **K0260**: Regulaciones y compliance en transición criptográfica
- **K0308**: Ciclo de vida de certificados y PKI en era post-cuántica
- **K0427**: Timeline de amenaza cuántica (Y2Q - Years to Quantum)

### Impacto en el DSS

**Preset Estratégico**: GRC-focused

La Seguridad en Computación Cuántica es fundamentalmente un desafío de:

- **Gobierno**: Políticas de transición criptográfica
- **Risk Management**: Evaluación de amenazas a largo plazo
- **Compliance**: Preparación para requisitos regulatorios futuros

**Ponderaciones recomendadas**:

```
--focus grc
# Equivalente a: --w-tasks 0.4 --w-skills 0.8 --w-knowledge 1.0
```

**Justificación**:

- **Tasks (0.4)**: Moderado - planificación estratégica vs. ejecución
- **Skills (0.8)**: Alto - evaluación técnica especializada
- **Knowledge (1.0)**: Crítico - comprensión profunda de amenazas emergentes

### Roles NICE Clave Asociados

| Role ID    | Nombre del Rol                           | Relevancia |
| ---------- | ---------------------------------------- | ---------- |
| SP-RSK-001 | Cyber Policy and Strategy Planner        | ⭐⭐⭐⭐⭐ |
| SP-RSK-002 | Cyber Workforce Developer and Manager    | ⭐⭐⭐     |
| OV-MGT-001 | Information Systems Security Manager     | ⭐⭐⭐⭐⭐ |
| OV-MGT-002 | Communications Security (COMSEC) Manager | ⭐⭐⭐⭐   |
| SP-ARC-002 | Security Architect                       | ⭐⭐⭐⭐⭐ |
| PD-INF-001 | Technical Support Specialist             | ⭐⭐⭐     |

### Escenarios de Riesgo Mitigados

1. **Ransomware**: 60-70% reducción (crypto-agility mejora recuperación)
2. **Supply Chain Compromise**: 80-90% reducción (validación criptográfica)
3. **Data Leaks**: 85-95% reducción (cifrado quantum-safe)
4. **Audit Failures**: 95-100% reducción (cumplimiento proactivo)

---

## Aplicación Directa de Presets en el DSS

### Configuraciones Oficiales

```bash
# Preset SOC (Operaciones de Seguridad)
python dss.py plan --focus soc
# Pesos: tasks=1.0, skills=0.6, knowledge=0.3
# Orientado a: Detección, respuesta, capacidad operativa

# Preset GRC (Gobierno, Riesgo y Cumplimiento)
python dss.py plan --focus grc
# Pesos: tasks=0.4, skills=0.8, knowledge=1.0
# Orientado a: Estrategia, políticas, arquitectura resiliente

# Custom (Balanceado para ambas asignaturas)
python dss.py plan --focus custom --w-tasks 0.5 --w-skills 0.7 --w-knowledge 0.7
# Pesos: personalizados para un mix de capacidades
```

### Matriz de Decisión por Asignatura

| Asignatura                             | Preset Recomendado   | Justificación                               |
| -------------------------------------- | -------------------- | ------------------------------------------- |
| Diseño y Desarrollo de Software Seguro | Custom (0.6/0.8/0.9) | Balance entre implementación y arquitectura |
| Seguridad en Computación Cuántica      | GRC (0.4/0.8/1.0)    | Enfoque estratégico y de largo plazo        |
| Ambas (Portfolio Completo)             | Hybrid (0.5/0.7/0.7) | Cobertura integral de capacidades           |

### Interpretación de Resultados del DSS

Cuando el DSS genera un plan optimizado:

1. **SOC-focused**: Mayor número de analistas, ingenieros operativos, respuesta rápida
2. **GRC-focused**: Mayor inversión en arquitectos, planificadores, especialistas en cumplimiento
3. **Custom**: Mix balanceado según los pesos específicos

**Ejemplo de Salida**:

```json
{
  "weighted_score": 456.78,
  "risk_reduction_percent": {
    "Ransomware": 85.5,
    "SupplyChainCompromise": 72.3,
    "DataLeaks": 90.1,
    "AuditFailures": 95.0
  },
  "selected_actions": [
    {
      "role_id": "SP-DEV-002",
      "option": "hire",
      "cost": 120000.0,
      "score_gain": 87.3
    }
  ]
}
```

---

## Coordinación Global del Máster

### Visión Integrada de Competencias

El CISO DSS Optimizer permite a los estudiantes del Máster:

1. **Comprender** cómo sus asignaturas se mapean a roles profesionales reales (NICE Framework)
2. **Cuantificar** el impacto de diferentes competencias en la reducción de riesgo
3. **Optimizar** decisiones de inversión en workforce considerando múltiples variables
4. **Comunicar** decisiones técnicas a nivel ejecutivo con datos objetivos

### Mapa de Competencias por Categoría NICE

```
NICE Framework Coverage by Master's Subjects:
═══════════════════════════════════════════════

Securely Provision (SP)     ████████████████████ 95%
├─ Software Development     ███████████████████ (Diseño Software)
└─ Risk Management          ██████████████████ (Comp. Cuántica)

Protect & Defend (PD)       ███████████████████ 90%
├─ Vulnerability Mgmt       ██████████████████ (Diseño Software)
└─ Infrastructure Security  █████████████████ (Comp. Cuántica)

Oversee & Govern (OV)       ████████████████████ 95%
└─ Strategic Planning       ███████████████████ (Comp. Cuántica)

Operate & Maintain (OM)     ███████████████ 75%
└─ System Administration    ██████████████ (Diseño Software)
```

### Beneficios Académicos del DSS

1. ✅ **Trazabilidad**: Conexión directa asignatura → TKS → roles → impacto en riesgo
2. ✅ **Cuantificación**: Decisiones basadas en datos, no en intuición
3. ✅ **Profesionalización**: Alineamiento con estándares de industria (NICE)
4. ✅ **Empleabilidad**: Comprensión clara de perfiles demandados

---

## Referencias y Estándares

- **NICE Framework**: [NIST Special Publication 800-181 Revision 1](https://www.nist.gov/itl/applied-cybersecurity/nice/nice-framework-resource-center)
- **OWASP**: Open Web Application Security Project
- **NIST PQC**: Post-Quantum Cryptography Standardization
- **ISO 27034**: Application Security
- **SAFECode**: Software Assurance Forum for Excellence in Code

---

**Versión del Documento**: 2.0  
**Última Actualización**: Marzo 2026  
**Autores**: Programa de Máster en Ciberseguridad  
**Herramienta**: CISO DSS Optimizer (NICE Framework Aligned)
