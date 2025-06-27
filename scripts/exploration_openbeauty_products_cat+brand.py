from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, trim, col, count, desc, collect_list, size, row_number
from pyspark.sql.window import Window

# 🚀 Crear sesión Spark con soporte Delta
spark = SparkSession.builder \
    .appName("ResumenCategorias") \
    .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.1.0") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# 📥 Leer datos desde Delta Lake
df = spark.read.format("delta").load("data/trusted/beauty_products_delta")

# 🎯 Explode de categorías y marcas
exploded_df = df.select(
    explode(split("categories", ",")).alias("categoria"),
    trim(col("brands")).alias("brand")
).select(
    trim(col("categoria")).alias("categoria"),
    col("brand")
).filter(col("categoria").isNotNull() & col("brand").isNotNull() & (col("brand") != ""))

# 🧮 Recuento de marcas por categoría
categoria_marca_counts = exploded_df.groupBy("categoria", "brand").count()

# 🏆 Obtener las 10 marcas con más productos por categoría
window = Window.partitionBy("categoria").orderBy(desc("count"))
top_marcas_por_categoria = categoria_marca_counts \
    .withColumn("rank", row_number().over(window)) \
    .filter(col("rank") <= 10) \
    .groupBy("categoria") \
    .agg(
        count("brand").alias("num_marcas"),
        collect_list("brand").alias("top_10_marcas")
    )

# 💄 Formatear como string separado por coma
from pyspark.sql.functions import concat_ws
resultado = top_marcas_por_categoria.withColumn("top_10_marcas", concat_ws(", ", col("top_10_marcas"))) \
    .orderBy(desc("num_marcas"))

# 📊 Mostrar resultado
resultado.show(truncate=False, n=100)

# 🧹 Parar Spark
spark.stop()