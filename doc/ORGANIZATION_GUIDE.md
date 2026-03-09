# Guía de Organización del Repositorio

## 📁 Estructura Organizada

El repositorio ha sido completamente organizado para máxima claridad y mantenibilidad:

```
first_practical/
│
├── 📄 dss.py                    # Punto de entrada principal del sistema
├── 📄 generate_plans.py         # Script auxiliar para generar múltiples planes
├── 📄 README.md                 # Documentación principal del proyecto
├── 📄 .gitignore                # Configuración de archivos ignorados
│
├── 📦 dss_modules/              # MÓDULOS REFACTORIZADOS
│   ├── __init__.py              # Inicialización del paquete
│   ├── models.py                # Modelos de datos y constantes
│   ├── loaders.py               # Carga de datos desde archivos
│   ├── optimizer.py             # Algoritmo de optimización
│   ├── gap_analysis.py          # Análisis de brechas
│   ├── dashboard.py             # Generación de dashboards
│   └── cli.py                   # Interfaz de línea de comandos
│
├── 📂 fixtures/                 # DATOS DE ENTRADA
│   ├── nice_tks.json           # Mapeo NICE Framework
│   ├── roles_costs.csv         # Costos y criticidad de roles
│   ├── risk_scenarios.json     # Escenarios de riesgo
│   └── baseline_workforce.json # Fuerza de trabajo actual
│
├── 📂 output/                   # RESULTADOS GENERADOS (en .gitignore)
│   ├── README.md               # Documentación de la carpeta
│   ├── *.json                  # Planes en formato JSON
│   └── *.html                  # Dashboards HTML interactivos
│
├── 📚 doc/                      # DOCUMENTACIÓN COMPLETA
│   ├── README.md               # Guía de uso completa
│   ├── USAGE_EXAMPLES.md       # Ejemplos de uso prácticos
│   ├── DESIGN_DOCUMENT.md      # Diseño técnico
│   ├── CASE_STUDY.md           # Caso de estudio
│   ├── CISO_SLIDES.md          # Presentación ejecutiva
│   ├── DASHBOARD_SUMMARY.md    # Resumen de dashboards
│   ├── NICE_MASTER_MAPPING.md  # Mapeo NICE Framework
│   └── ARCHITECTURE.md         # Arquitectura del sistema
│
└── 🧪 tests/                    # TESTS UNITARIOS
    ├── test_dss.py             # Suite de tests
    └── __pycache__/            # Cache de Python
```

## 🎯 Principios de Organización

### 1. Separación por Función

Cada carpeta tiene un propósito específico:

- **dss_modules/**: Código fuente modular
- **fixtures/**: Datos estáticos de entrada
- **output/**: Archivos generados (ignorados en git)
- **doc/**: Toda la documentación
- **tests/**: Tests automatizados

### 2. Archivos Generados Separados

Los archivos de salida (JSON, HTML) están aislados en `output/`:

- ✅ No ensucian el directorio raíz
- ✅ Fáciles de limpiar/regenerar
- ✅ Ignorados en control de versiones
- ✅ Documentados internamente

### 3. Documentación Centralizada

Toda la documentación en una carpeta `doc/`:

- ✅ Fácil de navegar
- ✅ Clara jerarquía
- ✅ Mejor experiencia de lectura
- ✅ Separada del código

### 4. Código Modular

El código está dividido en módulos especializados:

- ✅ Alta cohesión interna
- ✅ Bajo acoplamiento entre módulos
- ✅ Fácil de mantener y testear
- ✅ Reutilizable en otros proyectos

## 📋 Convenciones

### Nomenclatura de Archivos

- **Código Python**: `snake_case.py`
- **Documentación**: `SCREAMING_SNAKE_CASE.md`
- **Resultados**: `descriptive_name_{type}.{ext}`

Ejemplos:

- `soc_plan.json` - Plan SOC
- `soc_dashboard.html` - Dashboard SOC
- `ARCHITECTURE.md` - Documento de arquitectura

### Estructura de Módulos

Cada módulo sigue el patrón:

1. Docstring explicativo
2. Imports
3. Constantes (si aplica)
4. Funciones/clases
5. Documentación inline

### Gestión de Dependencias

- **Producción**: Definidas en imports
- **Tests**: pytest
- **Datos**: fixtures/

## 🔄 Flujo de Trabajo

### Desarrollo

1. Modificar módulos en `dss_modules/`
2. Actualizar tests en `tests/`
3. Ejecutar tests: `pytest tests/`
4. Actualizar documentación en `doc/`

### Generación de Planes

1. Verificar datos en `fixtures/`
2. Ejecutar:
   - Automático: `python generate_plans.py`
   - Manual: `python dss.py plan [opciones]`
3. Revisar resultados en `output/`

### Documentación

1. Editar archivos en `doc/`
2. Mantener README.md raíz actualizado
3. Documentar cambios significativos

## 📊 Control de Versiones (.gitignore)

### Incluido en Git:

- ✅ Código fuente (`dss_modules/`)
- ✅ Tests (`tests/`)
- ✅ Fixtures (`fixtures/`)
- ✅ Documentación (`doc/`)
- ✅ `output/README.md` (documentación)

### Excluido de Git:

- ❌ `output /*` (excepto README.md)
- ❌ `__pycache__/`
- ❌ `.pytest_cache/`
- ❌ `.venv/`
- ❌ Archivos compilados (\*.pyc)

## 🚀 Quick Start

```bash
# Clonar y configurar
git clone <repo>
cd first_practical

# Generar planes de ejemplo
python generate_plans.py

# Ver resultados
cd output
# Abrir *.html en navegador

# Ejecutar tests
pytest tests/ -v

# Leer documentación
cd doc
# Revisar archivos .md
```

## 📝 Mantenimiento

### Limpieza de Resultados

```bash
# Eliminar todos los resultados generados
rm -rf output/*.json output/*.html

# O mantener solo README
rm output/*.{json,html}
```

### Regeneración Completa

```bash
# Regenerar todos los planes
python generate_plans.py

# O manualmente
python dss.py plan --focus soc --output output/soc_plan.json --dashboard-file output/soc_dashboard.html
python dss.py plan --focus grc --output output/grc_plan.json --dashboard-file output/grc_dashboard.html
```

## ✅ Checklist de Organización

- [x] Código modularizado en `dss_modules/`
- [x] Documentación en carpeta `doc/`
- [x] Resultados en carpeta `output/`
- [x] Fixtures organizados
- [x] Tests en carpeta dedicada
- [x] .gitignore configurado correctamente
- [x] README principal actualizado
- [x] Script de generación automática
- [x] Documentación de output/
- [x] Sin archivos sueltos en raíz

## 🎓 Mejores Prácticas

1. **Nunca edites archivos en `output/`** - Son generados automáticamente
2. **Documenta cambios significativos** en `doc/ARCHITECTURE.md`
3. **Mantén fixtures versionados** - Son datos de referencia
4. **Ejecuta tests antes de commit** - `pytest tests/`
5. **Actualiza README** cuando agregues funcionalidad

## 📧 Contacto

Para preguntas sobre la organización del repositorio, consulta:

- `doc/ARCHITECTURE.md` - Arquitectura técnica
- `doc/README.md` - Guía de uso
- `README.md` - Documentación general
