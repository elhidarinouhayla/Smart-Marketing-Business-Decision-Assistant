FROM apache/airflow:2.10.4-python3.10

USER root

# Install Java avec résilience réseau et version légère 
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    -o Acquire::Retries=3 \
    openjdk-17-jdk-headless && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

USER airflow

# Gestion propre des requirements 
COPY backend/requirements.txt /requirements-backend.txt
COPY ml/requirements.txt /requirements-ml.txt

RUN pip install --no-cache-dir --default-timeout=1000 \
    -r /requirements-backend.txt \
    -r /requirements-ml.txt