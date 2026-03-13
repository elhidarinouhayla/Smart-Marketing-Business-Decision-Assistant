import os
import sys
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import mlflow
import mlflow.spark
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import PipelineModel

# 1. configuration des chemins 
PROJECT_PATH = "/app"
sys.path.append(PROJECT_PATH)

from ml.models_training.train_conversion_model import (
    create_spark, split_data, Model_pipeline, evaluate_model, roc_curve_model
)

# dossier temporaire pour partager les donnees entre taches
DATA_DIR = "/tmp/ml_demo"
os.makedirs(DATA_DIR, exist_ok=True)

# les taches

def task_load_and_split():
    spark = create_spark()
    # creation de données simples pour la demo
    df = spark.createDataFrame([(1, 25, 0.8, "A"), (0, 30, 0.2, "B"), (1, 22, 0.9, "A"), (0, 45, 0.1, "C")], 
                               ["conversion", "age", "score", "segment"])
    
    train_df, test_df = split_data(df)
    
    # on sauvegarde sur le disque pour que la tâche suivante puisse les lire
    train_df.write.mode("overwrite").parquet(f"{DATA_DIR}/train.parquet")
    test_df.write.mode("overwrite").parquet(f"{DATA_DIR}/test.parquet")
    spark.stop()

def task_train_model():
    spark = create_spark()
    train_df = spark.read.parquet(f"{DATA_DIR}/train.parquet")
    
    # entraînement avec tes fonctions
    lr = LogisticRegression(labelCol="conversion", featuresCol="features")
    pipeline = Model_pipeline(num_columns=["age", "score"], cat_columns=["segment"], model=lr)
    model = pipeline.fit(train_df)
    
    # sauvegarde du modele
    model.write().overwrite().save(f"{DATA_DIR}/model")
    spark.stop()

def task_evaluate_log_mlflow():
    spark = create_spark()
    test_df = spark.read.parquet(f"{DATA_DIR}/test.parquet")
    model = PipelineModel.load(f"{DATA_DIR}/model")
    
    # calcul des metriques
    metrics = evaluate_model(model, test_df)
    _, _, roc_auc = roc_curve_model(model, test_df)
    
    # mlflow
    mlflow.set_experiment("Demo_Pipeline")
    with mlflow.start_run():
        mlflow.log_metric("accuracy", metrics["accuracy"])
        mlflow.log_metric("roc_auc", float(roc_auc))
        mlflow.spark.log_model(model, "model")
    
    print(" Terminé ! Métriques et Modèle envoyés à MLflow.")
    spark.stop()

# definition du dag

with DAG(
    'dag_simple_ml',
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False
) as dag:

    step1 = PythonOperator(task_id='prepare_data', python_callable=task_load_and_split)
    step2 = PythonOperator(task_id='train_model',  python_callable=task_train_model)
    step3 = PythonOperator(task_id='log_to_mlflow', python_callable=task_evaluate_log_mlflow)

    # L'ordre d'execution
    step1 >> step2 >> step3
