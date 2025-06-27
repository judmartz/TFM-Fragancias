from pyspark.sql import SparkSession
from pyspark.sql.functions import split, explode, trim, col

# Crear sesión Spark con soporte Delta
spark = SparkSession.builder \
    .appName("ExplorarCategorías") \
    .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.1.0") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# Leer datos Delta (ruta relativa desde el proyecto)
df = spark.read.format("delta").load("data/trusted/beauty_products_delta")

# Mostrar categorías únicas ordenadas
df.select(explode(split("categories", ",")).alias("categoria")) \
  .select(trim(col("categoria")).alias("categoria")) \
  .distinct() \
  .orderBy("categoria") \
  .show(truncate=False, n=1000)

spark.stop()

