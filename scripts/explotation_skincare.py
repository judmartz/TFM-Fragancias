import os
from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip
from pyspark.sql.functions import col

# 🚀 Iniciar Spark
builder = SparkSession.builder \
    .appName("Explotation - Skincare Reviews") \
    .master("local[*]") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .config("spark.sql.warehouse.dir", "file:///tmp/spark-warehouse") \
    .config("spark.hadoop.fs.defaultFS", "file:///")\
    .config("spark.driver.memory", "4g") \
    .config("spark.executor.memory", "4g") \

spark = configure_spark_with_delta_pip(builder).getOrCreate()

# 📥 Leer datos trusted
ruta_reviews = "data/trusted/sephora_clean/reviews_0-250" #typo _ per -
ruta_productos = "data/trusted/sephora_clean/product_info"

df_reviews = spark.read.format("delta").load(ruta_reviews)
df_productos = spark.read.format("delta").load(ruta_productos)

# 🧽 Filtrar productos Skincare
df_skincare = df_productos.filter(col("primary_category") == "Skincare").select("product_id").distinct()

# 🔗 Unir con reviews
df_resultado = df_reviews.join(df_skincare, on="product_id", how="inner").select("product_id", "review_text")

# 📊 Mostrar métricas
print(f"🧾 Total de reviews Skincare: {df_resultado.count()}")
print(f"📦 Total de productos Skincare: {df_resultado.select('product_id').distinct().count()}")

# 💾 Guardar en zona exploitation
output_path = "data/exploitation/products/skincare_reviews"
os.makedirs(output_path, exist_ok=True)  # crea si no existe

df_resultado.write.format("delta").mode("overwrite").save(output_path)

print(f"✅ Dataset guardado en: {output_path}")

spark.stop()
