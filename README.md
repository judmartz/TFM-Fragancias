EJECUTABLES DESDE DOCKER:
    abrir docker: BASH: sudo docker run -it tfm-fragancias /bin/bash
SCRIPTS:

    python scripts/exploration_openbeauty_products.py
    python scripts/exploration_openbeauty_products_cat+brand.py
    python scripts/analisis_skincare_reviews.py


Este proyecto forma parte del Trabajo de Fin de Máster en Big Data. Consiste en una arquitectura de procesamiento y análisis de datos centrado en productos de belleza y cuidado personal, con especial énfasis en el análisis de reseñas de consumidores.

---

## 📁 Estructura del Proyecto

TFM-Fragancias/
│
├── data/
│ ├── landing/ # Datos brutos descargados
│ ├── trusted/ # Datos transformados en Delta Lake
│ └── exploitation/ # Datos listos para análisis y visualización
│
├── scripts/
│ ├── Open_beauty_facts_EAN.py # Descarga productos desde Open Beauty Facts por EAN
│ ├── exploration_openbeauty_products.py # Muestra y explora categorías únicas
│ ├── exploration_openbeauty_products_cat+brand.py # Recuento de marcas por categoría
│ └── explotation_skincare.py # Análisis de reviews skincare en formato Delta
│
├── notebooks/
│ └── analisis_skincare_reviews.ipynb # Notebook exploratorio para reseñas de skincare
│
├── Dockerfile # Entorno reproducible para ejecutar todo el proyecto
├── requirements.txt # Dependencias necesarias
└── README.md

