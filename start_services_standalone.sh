#!/bin/bash
# start_services_standalone.sh

export AIRFLOW_HOME=$(pwd)/airflow_home
export MLFLOW_TRACKING_URI=http://127.0.0.1:5000
mkdir -p $AIRFLOW_HOME/dags
mkdir -p mlflow_data

# Copier le DAG
cp dags/ml_conversion_pipeline.py $AIRFLOW_HOME/dags/

source venv/bin/activate

# Démarrer Airflow en mode standalone (automatisé)
echo "Démarrage d'Airflow Standalone..."
airflow standalone > airflow_standalone.log 2>&1 &

# Démarrer MLflow
echo "Démarrage de MLflow UI sur http://localhost:5000"
mlflow ui --host 127.0.0.1 --port 5000 > mlflow_ui.log 2>&1 &

echo "Airflow et MLflow sont en train de démarrer."
echo "Consultez airflow_standalone.log pour le mot de passe admin."
