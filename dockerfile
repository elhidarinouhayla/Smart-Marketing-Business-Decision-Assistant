FROM python:3.10-slim

# installer java
RUN apt-get update && \
    apt-get install -y default-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH=$PATH:$JAVA_HOME/bin

WORKDIR /app

# copier et installer les requirements backend
COPY backend/requirements.txt /requirements.txt
RUN pip install --default-timeout=1000 --no-cache-dir -r /requirements.txt

