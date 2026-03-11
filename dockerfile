FROM python:3.10-slim

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    openjdk-21-jre-headless \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Définir JAVA_HOME pour PySpark
ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
ENV AIRFLOW_HOME=/opt/airflow

# Copier et installer les requirements racine
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /requirements.txt

# Le code est monté via volume dans docker-compose