from pyspark.ml.feature import StringIndexer, VectorAssembler, StandardScaler
from pyspark.ml import Pipeline
from pyspark.sql import SparkSession
from sklearn.metrics import roc_curve, auc
from pyspark.ml.evaluation import MulticlassClassificationEvaluator


def create_spark():
    return (
        SparkSession.builder
        .appName("ConversionModel")
        .getOrCreate()
    )

def load_data(spark, path):
    return spark.read.parquet(path)






# split data
def split_data(df, test_size=0.2):

    train_df, test_df = df.randomSplit(
        [1-test_size, test_size],
        seed=42
    )

    return train_df, test_df



# pipeline 

def Model_pipeline(num_columns, cat_columns, model):

    #  categorical encoding 
    indexers = [
        StringIndexer(
            inputCol=c,
            outputCol=c+"_index",
            handleInvalid="keep"
        )
        for c in cat_columns
    ]


    #  feature Vector 
    assembler = VectorAssembler(
        inputCols=[c+"_index" for c in cat_columns] + num_columns,
        outputCol="raw_features"
    )


    #  normalisation 
    scaler = StandardScaler(
        inputCol="raw_features",
        outputCol="features"
    )

    #  pipeline 
    pipeline = Pipeline(
        stages=indexers + [assembler, scaler, model]
    )

    return pipeline



# metriques d'evaluation
def evaluate_model(model, test_df):

    predictions = model.transform(test_df)

    metrics = {}

    evaluator_acc = MulticlassClassificationEvaluator(
        labelCol="conversion",
        predictionCol="prediction",
        metricName="accuracy"
    )

    evaluator_precision = MulticlassClassificationEvaluator(
        labelCol="conversion",
        predictionCol="prediction",
        metricName="weightedPrecision"
    )

    evaluator_recall = MulticlassClassificationEvaluator(
        labelCol="conversion",
        predictionCol="prediction",
        metricName="weightedRecall"
    )

    evaluator_f1 = MulticlassClassificationEvaluator(
        labelCol="conversion",
        predictionCol="prediction",
        metricName="f1"
    )

    metrics["accuracy"] = evaluator_acc.evaluate(predictions)
    metrics["precision"] = evaluator_precision.evaluate(predictions)
    metrics["recall"] = evaluator_recall.evaluate(predictions)
    metrics["f1_score"] = evaluator_f1.evaluate(predictions)

    return metrics



# la courbe du roc
def roc_curve_model(model, test_df):

    predictions = model.transform(test_df)

    preds = predictions.select("probability", "conversion").collect()

    y_true = [row["conversion"] for row in preds]
    y_score = [float(row["probability"][1]) for row in preds]

    fpr, tpr, _ = roc_curve(y_true, y_score)
    roc_auc = auc(fpr, tpr)

    return fpr, tpr, roc_auc