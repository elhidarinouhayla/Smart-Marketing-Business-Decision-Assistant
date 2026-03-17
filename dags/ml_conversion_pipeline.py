import os
from datetime import datetime
from airflow.decorators import dag, task

# chemins 
DATA_PATH  = "/opt/airflow/ml/data/silver/segment_data"
TEMP_PATH  = "/opt/airflow/ml/data/temp"
MODEL_PATH = "/opt/airflow/ml/models/conversion_model"

mlflow_experiment = "Conversion_Model"
mlflow_tracking_uri = "http://mlflow:5000" 


@dag(
    dag_id="conversion_model_training",
    start_date=datetime(2026, 3, 15),
    schedule_interval="@daily",
    catchup=False,
)
def conversion_model_dag():

    # load data
    @task()
    def load():
        import sys
        sys.path.append("/opt/airflow") 
        from ml.models_training.train_conversion_model import create_spark, load_data, cast_numeric_columns
 
        os.makedirs(TEMP_PATH, exist_ok=True)
 
        spark = create_spark()
        df    = load_data(spark, DATA_PATH)
        df    = cast_numeric_columns(df)
 
        temp_path = f"{TEMP_PATH}/loaded_data"
        df.write.mode("overwrite").parquet(temp_path)
        return temp_path


    # split data
    @task()
    def split(df_path):
        import sys
        sys.path.append("/opt/airflow")
        from ml.models_training.train_conversion_model  import create_spark, load_data, split_data
 
        spark             = create_spark()
        df                = load_data(spark, df_path)
        train_df, test_df = split_data(df, test_size=0.2)
 
        train_path = f"{TEMP_PATH}/train_data"
        test_path  = f"{TEMP_PATH}/test_data"
 
        train_df.write.mode("overwrite").parquet(train_path)
        test_df.write.mode("overwrite").parquet(test_path)
 
        return {"train_path": train_path, "test_path": test_path}
 



    # train model
    @task()
    def training(split_result):
        import sys
        import mlflow
        import mlflow.spark
        sys.path.append("/opt/airflow")
        from ml.models_training.train_conversion_model import (
            create_spark, load_data, model_pipeline,
            numeric_cols, categorical_cols, target
        )
        from pyspark.ml.classification import LogisticRegression
 
        spark    = create_spark()
        train_df = load_data(spark, split_result["train_path"])
 
        lr       = LogisticRegression(featuresCol="features", labelCol=target)
        pipeline = model_pipeline(numeric_cols, categorical_cols, lr)
 

        mlflow.set_tracking_uri(mlflow_tracking_uri)
        mlflow.set_experiment(mlflow_experiment)
        with mlflow.start_run() as run:
            model = pipeline.fit(train_df)
    
            mlflow.log_param("model_type",   "LogisticRegression")
            mlflow.log_param("num_features", len(numeric_cols))
            mlflow.log_param("cat_features", len(categorical_cols))
            mlflow.log_param("test_size",    0.2)
    
            run_id = run.info.run_id 
    
            temp_model_path = f"{TEMP_PATH}/temp_model"
            model.write().overwrite().save(temp_model_path)
    
        return {
                "model_path": temp_model_path,
                "test_path" : split_result["test_path"],
                "run_id"    : run_id
            }

    # metrics
    @task()
    def metrics(training_result):
        import sys
        import mlflow
        sys.path.append("/opt/airflow")
        from ml.models_training.train_conversion_model import create_spark, load_data, evaluate_model  
        from pyspark.ml import PipelineModel
 
        spark   = create_spark()
        model   = PipelineModel.load(training_result["model_path"])
        test_df = load_data(spark, training_result["test_path"])
 
        result  = evaluate_model(model, test_df)
 
        print(f"Accuracy  : {result['accuracy']:.4f}")
        print(f"Precision : {result['precision']:.4f}")
        print(f"Recall    : {result['recall']:.4f}")
        print(f"F1 Score  : {result['f1_score']:.4f}")
        print(f"AUC       : {result['auc']:.4f}")
 

        mlflow.set_tracking_uri(mlflow_tracking_uri)
        mlflow.set_experiment(mlflow_experiment)
        with mlflow.start_run(run_id=training_result["run_id"]):
            mlflow.log_metric("accuracy",  result["accuracy"])
            mlflow.log_metric("precision", result["precision"])
            mlflow.log_metric("recall",    result["recall"])
            mlflow.log_metric("f1_score",  result["f1_score"])
            mlflow.log_metric("auc",       result["auc"])




    # save model
    @task()
    def save(metrics_result):
        import sys
        import mlflow
        import mlflow.spark
        sys.path.append("/opt/airflow")
        from ml.models_training.train_conversion_model import save_model
        from pyspark.ml import PipelineModel
 
        model = PipelineModel.load(metrics_result["model_path"])
        save_model(model, MODEL_PATH)
 

        mlflow.set_tracking_uri(mlflow_tracking_uri)
        mlflow.set_experiment(mlflow_experiment)
        with mlflow.start_run(run_id=metrics_result["run_id"]):
            mlflow.spark.log_model(model, "conversion_model")
 
        print(f" Modèle sauvegardé → {MODEL_PATH}")
        print(f"   AUC      : {metrics_result['auc']:.4f}")
        print(f"   Accuracy : {metrics_result['accuracy']:.4f}")
        print(f"   F1 Score : {metrics_result['f1_score']:.4f}")
 
        return {"model_saved": True, "path": MODEL_PATH}
 


    df_path         = load()
    split_result    = split(df_path)
    training_result = training(split_result)
    metrics_result  = metrics(training_result)
    save(metrics_result)
 
 
conversion_model_dag()