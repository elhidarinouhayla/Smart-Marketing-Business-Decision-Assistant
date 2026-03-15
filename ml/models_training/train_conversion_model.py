from pyspark.ml.feature import StringIndexer, VectorAssembler, StandardScaler
from pyspark.ml import Pipeline
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.evaluation import MulticlassClassificationEvaluator, BinaryClassificationEvaluator
from sklearn.metrics import roc_curve, auc


# colonnes numeriques 
nimeric_cols = [
    "Age", "Income", "AdSpend",
    "ClickThroughRate", "LoyaltyPoints",
    "WebsiteVisits", "PagesPerVisit", "TimeOnSite",
    "SocialShares", "EmailOpens", "EmailClicks",
    "PreviousPurchases"
]

# colonnes categorielles 
categorical_cols = [
    "Gender", "CampaignChannel", "CampaignType",
    "SegmentName" 
]

# colonne cible
target = "conversion"


def create_spark():
    return SparkSession.builder.appName("ConversionModel").getOrCreate()


def load_data(spark, path):
    return spark.read.parquet(path)


def cast_numeric_columns(df):
    for column in nimeric_cols:
        df = df.withColumn(column, col(column).cast("double"))
    return df


def split_data(df, test_size=0.2):
    train_df, test_df = df.randomSplit([1 - test_size, test_size], seed=42)
    return train_df, test_df


def model_pipeline(num_columns, cat_columns, model):
    
    indexers = [
        StringIndexer(inputCol=c, outputCol=c + "_index", handleInvalid="keep")
        for c in cat_columns      
    ]

    assembler = VectorAssembler(
        inputCols=[c + "_index" for c in cat_columns] + num_columns,  
        outputCol="raw_features"
    )

    scaler = StandardScaler(
        inputCol="raw_features",
        outputCol="features"
    )

    pipeline = Pipeline(stages=indexers + [assembler, scaler, model])
    return pipeline

def evaluate_model(model, test_df):
    predictions = model.transform(test_df)

    def get_metric(name):
        return MulticlassClassificationEvaluator(
            labelCol=target, predictionCol="prediction", metricName=name
        ).evaluate(predictions)

    auc_score = BinaryClassificationEvaluator(
        labelCol=target, rawPredictionCol="rawPrediction", metricName="areaUnderROC"
    ).evaluate(predictions)

    metrics = {
        "accuracy"  : get_metric("accuracy"),
        "precision" : get_metric("weightedPrecision"),
        "recall"    : get_metric("weightedRecall"),
        "f1_score"  : get_metric("f1"),
        "auc"       : auc_score      
    }

    return metrics


def roc_curve_model(model, test_df):
    predictions = model.transform(test_df)
    preds = predictions.select("probability", target).collect()

    y_true  = [row[target] for row in preds]
    y_score = [float(row["probability"][1]) for row in preds]

    fpr, tpr, _ = roc_curve(y_true, y_score)
    roc_auc = auc(fpr, tpr)

    return fpr, tpr, roc_auc


def save_model(model, path):
    model.write().overwrite().save(path)