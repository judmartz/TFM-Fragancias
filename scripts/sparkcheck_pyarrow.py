from pyspark.sql import SparkSession
import pyarrow

print("pyarrow version:", pyarrow.__version__)

spark = SparkSession.builder \
    .appName("CheckArrow") \
    .config("spark.master", "local[*]") \
    .getOrCreate()

arrow_enabled = spark.conf.get("spark.sql.execution.arrow.pyspark.enabled", "false")
print("Arrow enabled in Spark:", arrow_enabled)