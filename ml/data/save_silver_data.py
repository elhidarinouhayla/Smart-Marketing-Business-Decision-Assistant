from pyspark.sql import SparkSession


# chemins locaux bases sur ta structure 
parquet_path = "/opt/airflow/ml/data/silver/silver_data"
jar_path = "/opt/airflow/ml/spark_libs/postgresql-42.6.0.jar"
jdbc_URL     = "jdbc:postgresql://postgres:5432/airflow?sslmode=disable"

#  connexion PostgreSQL 
table_name = "silver_data"

db_proprerities = {
    "user"    : "postgres",
    "password": "postgres",
    "driver"  : "org.postgresql.Driver",
    "ssl"      : "false",        
    "sslmode"  : "disable" 
}


def create_spark():
    return (
        SparkSession.builder
        .appName("SaveSilverDataToPostgres")
        .config("spark.jars", jar_path)
        .config("spark.driver.memory", "4g")
        .config("spark.executor.memory", "4g")
        .getOrCreate()
    )


def load_parquet(spark, path):
    df = spark.read.parquet(path)
    print(f"Données chargées : {df.count()} lignes")
    df.show(5)
    return df


def save_to_postgres(df, jdbc_URL, table_name, properties):
    df.write \
        .mode("overwrite") \
        .option("batchsize", "50000") \
        .option("numPartitions", "10") \
        .jdbc(url=jdbc_URL, table=table_name, properties=properties)
    print(f" data sauvegardees dans la table '{table_name}'")


def verify_postgres(spark, jdbc_URL, table_name, properties):
    df = spark.read.jdbc(url=jdbc_URL, table=table_name, properties=properties)
    print(f" verification — {df.count()} lignes dans PostgreSQL")
    df.show(5)


# if __name__ == "__main__":
#     # Vérifier que le jar existe avant de démarrer Spark
#     if not os.path.exists(jar_path):
#         print(f" Jar introuvable : {jar_path}")
#         print(" Lance cette commande pour le télécharger :")
#         print(f"   wget https://jdbc.postgresql.org/download/postgresql-42.6.0.jar -O {jar_path}")
#         exit(1)

#     spark = create_spark()

#     df = load_parquet(spark, parquet_path)
#     save_to_postgres(df, jdbc_URL, table_name, db_proprerities)
#     verify_postgres(spark, jdbc_URL, table_name, db_proprerities)

#     spark.stop()
#     print(" termine !")