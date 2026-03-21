#!/bin/bash
# init_airflow.sh

set -e

echo "Initialisation de la base de données Airflow..."
airflow db init

echo "Création de l'utilisateur Admin..."
airflow users create \
    --username admin \
    --password admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com

echo "Airflow initialisé avec succès !"