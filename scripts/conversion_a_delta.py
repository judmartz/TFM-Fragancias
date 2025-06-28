import os
from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

# 🚀 Inicializa Spark con soporte para Delta Lake
builder = SparkSession.builder \
    .appName("Trusted Zone Cleaning") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .config("spark.master", "local[*]") \
    .config("spark.sql.warehouse.dir", "file:///tmp/spark-warehouse") \
    .config("spark.hadoop.fs.defaultFS", "file:///")\
    .config("spark.driver.memory", "4g") \
    .config("spark.executor.memory", "4g") \

spark = configure_spark_with_delta_pip(builder).getOrCreate()

# 🗂️ Carpetas de entrada y salida
datasets = {
    "sephora": {
        "input_folder": "data/landing/sephora",
        "output_folder": "data/landing/sephora/delta"
    },
    "ulta": {
        "input_folder": "data/landing/ulta",
        "output_folder": "data/landing/ulta/delta"
    }
}

# 🔁 Procesar cada carpeta
for nombre, rutas in datasets.items():
    input_folder = rutas["input_folder"]
    output_base = rutas["output_folder"]

    print(f"\n📦 Procesando dataset: {nombre}")
    if not os.path.exists(input_folder):
        print(f"⚠️  Carpeta no encontrada: {input_folder}")
        continue

    for archivo in os.listdir(input_folder):
        if archivo.endswith(".csv"):
            ruta_csv = os.path.join(input_folder, archivo)
            nombre_base = os.path.splitext(archivo)[0]

            # 🧼 Reemplazar guiones por guiones bajos
            nombre_base_sanitizado = nombre_base.replace("-", "_")

            ruta_delta = os.path.join(output_base, nombre_base_sanitizado)

            # 🛠️ Crear carpeta si no existe
            os.makedirs(ruta_delta, exist_ok=True)

            print(f"🔄 Convirtiendo: {archivo} → Delta")

            df = spark.read.option("header", True).option("inferSchema", True).csv(ruta_csv)
            df = df.dropna(how="all")  # limpieza básica
            df.write.format("delta").mode("overwrite").save(ruta_delta)

            print(f"✅ Guardado en: {ruta_delta}")

# ✅ Finaliza
spark.stop()
