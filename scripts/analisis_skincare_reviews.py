#!/usr/bin/env python
# coding: utf-8

# # 🧴 Análisis de Reseñas - Skincare (Text Analytics)
# Este notebook realiza una limpieza básica de texto y detecta reseñas con lenguaje positivo sobre productos de cuidado de la piel (Skincare).
# 


import os
from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

# Inicializar Spark con Delta
builder = SparkSession.builder \
    .appName("Skincare Reviews Analytics") \
    .master("local[*]") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()

# Cargar dataset Delta limpio

ruta = os.path.expanduser("~/MASTER_BIGDATA/TFM/TFM-Fragancias/data/exploitation/products/skincare_reviews")
df = spark.read.format("delta").load(ruta)
df_pd = df.toPandas()

# Vista previa
df_pd.head()


import string

# Palabras positivas básicas
positive_words = {"love", "like", "amazing", "great", "perfect", "awesome", "wonderful", "excellent"}

def clean_and_detect(text):
    if not isinstance(text, str):
        return False
    # Eliminar puntuación y pasar a minúsculas
    text_clean = text.translate(str.maketrans("", "", string.punctuation)).lower()
    return any(word in text_clean for word in positive_words)

# Aplicar detección
df_pd["is_positive"] = df_pd["review_text"].apply(clean_and_detect)

# Ver primeras filas
df_pd[["product_id", "review_text", "is_positive"]].head()


print("📝 Total de reseñas:", len(df_pd))
print("👍 Reseñas positivas detectadas:", df_pd['is_positive'].sum())


# Si hay menos de 5 positivas, mostrar todas
positivas = df_pd[df_pd["is_positive"]]
sample_size = min(5, len(positivas))

positivas[["product_id", "review_text"]].sample(sample_size, random_state=42)

