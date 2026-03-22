#!/bin/bash
# start_services.sh

export AIRFLOW_HOME=$(pwd)/airflow_home
export MLFLOW_TRACKING_URI=http://127.0.0.1:5000
mkdir -p $AIRFLOW_HOME/dags
mkdir -p mlflow_data

# Copier le DAG dans le dossier airflow_home
cp dags/ml_conversion_pipeline.py $AIRFLOW_HOME/dags/

source venv/bin/activate

# Initialiser Airflow
airflow db init
airflow users create \
    --username admin \
    --password admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com

# Démarrer les services en arrière-plan
echo "Démarrage d'Airflow Webserver sur http://localhost:8080"
airflow webserver --port 8080 > airflow_webserver.log 2>&1 &

echo "Démarrage d'Airflow Scheduler"
airflow scheduler > airflow_scheduler.log 2>&1 &

echo "Démarrage de MLflow UI sur http://localhost:5000"
mlflow ui --host 127.0.0.1 --port 5000 > mlflow_ui.log 2>&1 &

echo "Services démarrés !"
