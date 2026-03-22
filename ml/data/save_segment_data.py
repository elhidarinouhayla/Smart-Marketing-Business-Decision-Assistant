from pyspark.sql import SparkSession
import os

base_path    = "/opt/airflow/ml"
parquet_path = f"{base_path}/data/silver/segment_data"
jar_path = "/opt/airflow/ml/spark_libs/postgresql-42.6.0.jar"
jdbc_URL     = "jdbc:postgresql://postgres:5432/airflow?sslmode=disable"
table_name   = "segment_data"

db_properties = {
    "user"    : "postgres",
    "password": "postgres",
    "driver"  : "org.postgresql.Driver",
    "ssl"     : "false",
    "sslmode" : "disable"
}

def create_spark():
    return (
        SparkSession.builder
        .appName("SaveSegmentDataToPostgres")
        .config("spark.jars", jar_path)
        .config("spark.driver.memory", "4g")
        .getOrCreate()
    )

# if __name__ == "__main__":
#     spark = create_spark()

#     df = spark.read.parquet(parquet_path)
#     print(f" segment_data charge : {df.count()} lignes")
#     print(f" Colonnes : {df.columns}")

#     df.write \
#         .mode("overwrite") \
#         .option("batchsize", "50000") \
#         .jdbc(url=jdbc_URL, table=table_name, properties=db_properties)

#     print(f" segment_data sauvegarde dans PostgreSQL")
#     spark.stop()