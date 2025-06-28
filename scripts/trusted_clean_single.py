import os
import sys
from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip
from pyspark.sql.functions import col, lower

# 📌 Validar argumentos
if len(sys.argv) != 3:
    print("❌ Uso: python trusted_clean_single.py <dataset> <tabla>")
    sys.exit(1)

dataset = sys.argv[1]  # "sephora" o "ulta"
tabla = sys.argv[2]    # ej. reviews_250_500

input_path = f"data/landing/{dataset}/delta/{tabla}"
output_path = f"data/trusted/{dataset}_clean/{tabla}"

# 🚀 Iniciar Spark con soporte Delta
builder = SparkSession.builder \
    .appName(f"Cleaning {dataset}/{tabla}") \
    .master("local[*]") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .config("spark.sql.warehouse.dir", "file:///tmp/spark-warehouse") \
    .config("spark.hadoop.fs.defaultFS", "file:///")\
    .config("spark.driver.memory", "4g") \
    .config("spark.executor.memory", "4g") \

spark = configure_spark_with_delta_pip(builder).getOrCreate()

try:
    print(f"📥 Leyendo: {input_path}")
    df = spark.read.format("delta").load(input_path)

    print("🧼 Aplicando limpieza...")
    df_clean = df.dropna(how="all").dropDuplicates()

    if "review_text" in df_clean.columns:
        df_clean = df_clean.withColumn("review_text", lower(col("review_text")))

    print(f"💾 Guardando limpio en: {output_path}")
    df_clean.write.format("delta").mode("overwrite").save(output_path)

    print(f"✅ Limpieza completada para {tabla} ({df_clean.count()} filas).")

except Exception as e:
    print(f"❌ Error procesando {tabla}: {e}")

finally:
    spark.stop()
