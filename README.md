Proyecto TFM-Fragancias

Este proyecto forma parte del Trabajo de Fin de Máster en Big Data. Consiste en una arquitectura de procesamiento y análisis de datos centrada en productos de belleza y cuidado personal, con especial énfasis en el análisis de reseñas de consumidores.

---

📁 Estructura del Proyecto

TFM-Fragancias/
│
├── data/
│   ├── landing/              # Datos brutos descargados
│   ├── trusted/              # Datos transformados en Delta Lake
│   └── exploitation/         # Datos listos para análisis y visualización
│
├── scripts/
│   ├── main.py                              # Orquesta la ejecución secuencial de todo el flujo
│   ├── Open_beauty_facts_EAN.py             # Descarga productos desde Open Beauty Facts por EAN
│   ├── exploration_openbeauty_products.py   # Muestra y explora categorías únicas
│   ├── exploration_openbeauty_products_cat+brand.py # Recuento de marcas por categoría
│   ├── explotation_skincare.py              # Análisis de reviews skincare en formato Delta
│   ├── trusted_clean_driver.py              # Limpieza y consolidación de datos Trusted
│   ├── trusted_clean_single.py              # Procesa tablas individuales de Trusted
│   ├── conversion_a_delta.py                # Conversión a formato Delta
│   └── analisis_skincare_reviews.py         # Análisis de reseñas de skincare
│
├── notebooks/
│   └── analisis_skincare_reviews.ipynb      # Notebook exploratorio para reseñas de skincare
│
├── Dockerfile                               # Entorno reproducible para ejecutar todo el proyecto
├── requirements.txt                         # Dependencias necesarias
├── .dockerignore                            # Archivos y carpetas excluidos del contexto Docker
└── README.md

---

OPCION 1
🐳 Ejecución desde Docker Hub

1️⃣ Descargar la imagen:

docker pull peterwithel/tfm-fragancias

2️⃣ Abrir un contenedor interactivo:

docker run -it peterwithel/tfm-fragancias /bin/bash

3️⃣ Ejecutar el flujo completo desde main.py:

python scripts/main.py

Esto ejecuta todos los pasos del proyecto en orden, incluyendo descarga, limpieza, conversión, y análisis.

OPCION 2 (menos robusta)

🐳 Ejecución desde Docker

1️⃣ Construir la imagen:

docker build -t tfm-fragancias .

2️⃣ Abrir un contenedor interactivo:

sudo docker run -it tfm-fragancias /bin/bash

3️⃣ Ejecutar el flujo completo desde main.py (recomendado):

python scripts/main.py
---

⚙️ Dependencias

Todas las dependencias de Python se instalan automáticamente en la construcción del contenedor Docker desde requirements.txt.

---

✨ Notas

- Este flujo está optimizado para ejecutarse desde Docker, con un entorno autocontenido y reproducible.
- Si necesitas trabajar en local sin Docker, instala las dependencias manualmente y ejecuta main.py desde tu entorno de Python.


