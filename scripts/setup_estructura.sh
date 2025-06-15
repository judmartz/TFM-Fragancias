#!/bin/bash

echo "📁 Creando estructura de carpetas del proyecto TFM-Fragancias..."

# Crear carpetas de datos
mkdir -p data/landing/sephora/delta
mkdir -p data/landing/ulta/delta

mkdir -p data/trusted/sephora_clean
mkdir -p data/trusted/ulta_clean
mkdir -p data/trusted/productos_unificados

mkdir -p data/exploitation/modelos_input
mkdir -p data/exploitation/analisis_final
mkdir -p data/exploitation/dashboards_data

# Crear carpetas adicionales del proyecto
mkdir -p scripts
mkdir -p notebooks
mkdir -p docs

# Crear archivos vacíos de ejemplo si no existen
touch README.md
touch requirements.txt
touch .gitignore

echo "✅ Estructura de carpetas creada con éxito."
