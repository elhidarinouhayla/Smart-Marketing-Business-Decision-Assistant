from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.sql.functions import col



def create_spark():
    return (
        SparkSession.builder
        .appName("ConversionModel")
        .getOrCreate()
    )

def load_data(spark, path):
    return spark.read.parquet(path)



def cast_numeric_columns(df):

    numeric_columns = [
        "Age",
        "Income",
        "LoyaltyPoints",
        "PreviousPurchases",
        "AdSpend",
        "ClickThroughRate",
        "WebsiteVisits",
        "SegmentID",
        "Conversion"
    ]

    for column in numeric_columns:
        df = df.withColumn(column, col(column).cast("double"))

    return df



def encode_gender(df):

    indexer = StringIndexer(
        inputCol="Gender",
        outputCol="Gender_index"
    )

    df = indexer.fit(df).transform(df)

    encoder = OneHotEncoder(
        inputCols=["Gender_index"],
        outputCols=["Gender_encoded"]
    )

    df = encoder.fit(df).transform(df)

    return df


def encode_campaign_channel(df):

    indexer = StringIndexer(
        inputCol="CampaignChannel",
        outputCol="Channel_index"
    )

    df = indexer.fit(df).transform(df)

    encoder = OneHotEncoder(
        inputCols=["Channel_index"],
        outputCols=["Channel_encoded"]
    )

    df = encoder.fit(df).transform(df)

    return df





def assemble_features(df):

    if "features" in df.columns:
        df = df.drop("features")
        
    assembler = VectorAssembler(
        inputCols=[
            "Age",
            "Income",
            "LoyaltyPoints",
            "PreviousPurchases",
            "AdSpend",
            "ClickThroughRate",
            "WebsiteVisits",
            "Gender_encoded",
            "Channel_encoded",
            "SegmentID"
        ],
        outputCol="features"
    )

    df = assembler.transform(df)

    return df



def split_data(df):
    return df.randomSplit([0.8, 0.2], seed=42)



def train_model(train_df):

    rf = RandomForestClassifier(
        labelCol="Conversion",
        featuresCol="features",
        numTrees=100
    )

    model = rf.fit(train_df)

    return model




def evaluate_model(model, test_df):

    predictions = model.transform(test_df)

    evaluator = BinaryClassificationEvaluator(
        labelCol="Conversion",
        metricName="areaUnderROC"
    )

    auc = evaluator.evaluate(predictions)

    print("AUC:", auc)

    return auc



def save_model(model, path):
    model.write().overwrite().save(path)