from pyspark.ml.feature import VectorAssembler, StandardScaler, StringIndexer
from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator
from pyspark.ml import Pipeline
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when


# Colonnes numeriques 
numeric_cols = [
    "Age", "Income", "AdSpend",
    "ClickThroughRate", "LoyaltyPoints",
    "WebsiteVisits", "PagesPerVisit", "TimeOnSite",
    "SocialShares", "EmailOpens", "EmailClicks",
    "PreviousPurchases"
]

# Colonnes categorielles 
categorical_cols = ["Gender", "CampaignChannel", "CampaignType"]

# toutes les features 
kmeans_featres = numeric_cols + [c + "_index" for c in categorical_cols]


def create_spark():
    return SparkSession.builder.appName("customerSegmentation").getOrCreate()


def load_data(spark, path):
    return spark.read.parquet(path)


def cast_numeric_columns(df):
    for column in numeric_cols:
        df = df.withColumn(column, col(column).cast("double"))
    return df



# encoder les categorielles + assembler + scaler 
def prepare_for_elbow(df):
    indexers  = [StringIndexer(inputCol=c, outputCol=c + "_index") for c in categorical_cols]
    assembler = VectorAssembler(inputCols=kmeans_featres, outputCol="features")
    scaler    = StandardScaler(inputCol="features", outputCol="scaled_features", withMean=True, withStd=True)
    pipeline  = Pipeline(stages=indexers + [assembler, scaler])
    return pipeline.fit(df).transform(df)


def compute_elbow_costs(df_scaled, k_min=2, k_max=8):
    costs = []
    for k in range(k_min, k_max + 1):
        model = KMeans(k=k, seed=42, featuresCol="scaled_features", predictionCol="SegmentID").fit(df_scaled)
        costs.append((k, model.summary.trainingCost))
        print(f"  K={k} → Cost={model.summary.trainingCost:,.0f}")
    return costs


def train_model(df, k):
    indexers  = [StringIndexer(inputCol=c, outputCol=c + "_index") for c in categorical_cols]
    assembler = VectorAssembler(inputCols=kmeans_featres, outputCol="features")
    scaler    = StandardScaler(inputCol="features", outputCol="scaled_features", withMean=True, withStd=True)
    kmeans    = KMeans(k=k, seed=42, featuresCol="scaled_features", predictionCol="SegmentID")
    pipeline  = Pipeline(stages=indexers + [assembler, scaler, kmeans])
    return pipeline.fit(df)


def evaluate_model(model, df):
    predictions = model.transform(df)
    score = ClusteringEvaluator(featuresCol="scaled_features", predictionCol="SegmentID").evaluate(predictions)
    return score


def get_cluster_centers(model):
    centers = model.stages[-1].clusterCenters()
    return {i: dict(zip(kmeans_featres, [round(v, 2) for v in c])) for i, c in enumerate(centers)}


def add_segment_names(df, segment_names):
    mapping = when(col("SegmentID") == list(segment_names.keys())[0], list(segment_names.values())[0])
    for seg_id, name in list(segment_names.items())[1:]:
        mapping = mapping.when(col("SegmentID") == seg_id, name)
    return df.withColumn("SegmentName", mapping.otherwise("Unknown"))


def save_data(model, df, segment_names, output_path):
    df_result = model.transform(df)
    df_result = add_segment_names(df_result, segment_names)
    cols_to_drop = ["features", "scaled_features"] + [c + "_index" for c in categorical_cols]
    df_result.drop(*cols_to_drop).write.mode("overwrite").parquet(output_path)


def save_model(model, path):
    model.write().overwrite().save(path)