from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
from pyspark.sql import Row


def dict_to_spark_df(data: dict, spark):
    row = Row(**data)
    return spark.createDataFrame([row])


spark = SparkSession.builder.appName("marketing_prediction_service").getOrCreate()

# Calculate path to the model relative to project root
BASE_DIR = Path(__file__).resolve().parents[3]
MODEL_PATH = str(BASE_DIR / "ml" / "notebooks" / "models" / "bestModel")

loaded_model = PipelineModel.load(MODEL_PATH)


def predict(data: dict):

    df_input = dict_to_spark_df(data, spark)

    prediction = loaded_model.transform(df_input)

    prediction_value = prediction.select("prediction").collect()[0][0]

    probability = prediction.select("probability").collect()[0][0][1]

    return {
        "prediction": float(prediction_value),
        "probability": float(probability)
    }



# data = {
#     "Age": 35,
#     "Gender": "Male",
#     "Income": 60000,
#     "CampaignChannel": "Email",
#     "CampaignType": "Promotion",
#     "AdSpend": 200,
#     "ClickThroughRate": 0.15,
#     "WebsiteVisits": 8,
#     "PagesPerVisit": 5,
#     "TimeOnSite": 120,
#     "SocialShares": 1,
#     "EmailOpens": 3,
#     "EmailClicks": 1,
#     "PreviousPurchases": 2,
#     "LoyaltyPoints": 150,
#     "AdvertisingPlatform": "Google",
#     "AdvertisingTool": "AdsManager",
#     "SegmentID": 1
# }

# result = predict(data)

# print("Prediction:", result["prediction"])
# print("Probability:", result["probability"])