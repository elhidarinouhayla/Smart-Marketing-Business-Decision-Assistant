from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator
from pyspark.sql import SparkSession
from pyspark.sql.functions import col



def create_spark():
    return (
        SparkSession.builder
        .appName("customerSegmentation")
        .getOrCreate()
    )


# load data
def load_data(spark, path):
    return spark.read.parquet(path)



def cast_numeric_columns(df):

    numeric_columns = [
        "Age",
        "Income",
        "LoyaltyPoints",
        "PreviousPurchases"
    ]

    for column in numeric_columns:
        df = df.withColumn(column, col(column).cast("double"))

    return df



def assemble_features(df):

    assembler = VectorAssembler(
        inputCols=["Age", "Income", "LoyaltyPoints", "PreviousPurchases"],
        outputCol="features"
    )

    return assembler.transform(df)



def scale_features(df):

    scaler = StandardScaler(
        inputCol="features",
        outputCol="scaled_features",
        withMean=True,
        withStd=True
    )

    scaler_model = scaler.fit(df)

    return scaler_model.transform(df)


# train model
def train_kmeans(df, k):

    model = KMeans(
        k=k,
        seed=42,
        featuresCol="scaled_features",
        predictionCol="SegmentID"
    ).fit(df)

    return model



# evaluate model
def evaluate_model(model, df):

    evaluator = ClusteringEvaluator(
        featuresCol="scaled_features",
        predictionCol="SegmentID"
    )

    return evaluator.evaluate(model.transform(df))


def save_segmented_data(model, df, path):

    # appliquer le modèle
    segmented_df = model.transform(df)

    # supprimer les colonnes techniques
    final_df = segmented_df.drop("features", "scaled_features")

    # sauvegarder toutes les colonnes + SegmentID
    final_df.write.mode("overwrite").parquet(path)


# save model
def save_model(model, path):
    model.write().overwrite().save(path)

 