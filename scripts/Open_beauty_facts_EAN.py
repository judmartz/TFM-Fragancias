import os
import requests
from pyspark.sql import SparkSession

# Detectar ruta raíz del proyecto
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# 📁 Rutas absolutas a partir del proyecto
landing_dir = os.path.join(project_root, "data", "landing", "Open_Beauty_facts_products")
parquet_path = os.path.join(landing_dir, "beauty.parquet")
delta_output = os.path.join(project_root, "data", "trusted", "beauty_products_delta")

# URL del dataset
parquet_url = "https://huggingface.co/datasets/openfoodfacts/product-database/resolve/main/beauty.parquet?download=true"

# 📥 Descargar Parquet si no existe
os.makedirs(landing_dir, exist_ok=True)
if not os.path.exists(parquet_path):
    print("⏬ Descargando beauty.parquet a", landing_dir)
    response = requests.get(parquet_url, stream=True)
    with open(parquet_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print("✅ Descarga completada.")
else:
    print("📦 Archivo ya existe, se usará directamente.")

# 🧠 SparkSession con soporte Delta
spark = SparkSession.builder \
    .appName("ConvertBeautyParquetToDelta") \
    .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.1.0") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# 📦 Leer el Parquet
df = spark.read.parquet(parquet_path)

# 💾 Guardar en formato Delta
df.write.format("delta").mode("overwrite").save(delta_output)

print("✅ Guardado como Delta en:", delta_output)

spark.stop()
