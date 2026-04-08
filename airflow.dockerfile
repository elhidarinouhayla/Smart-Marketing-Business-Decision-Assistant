FROM apache/airflow:2.8.1-python3.10

USER root

# installer Java 
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-jdk \
    procps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# definir JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH=$PATH:$JAVA_HOME/bin

USER airflow

RUN pip install --no-cache-dir --default-timeout=1000 pyspark==3.5.0
RUN pip install --no-cache-dir --default-timeout=1000 mlflow==2.17.2 pandas==2.1.4 scikit-learn==1.3.2
RUN pip install --no-cache-dir --default-timeout=1000 fastapi==0.108.0 uvicorn[standard]==0.25.0
RUN pip install --no-cache-dir --default-timeout=1000 pydantic==2.5.3 pydantic-settings==2.1.0
RUN pip install --no-cache-dir --default-timeout=1000 "sqlalchemy>=1.4.28,<2.0" psycopg2-binary==2.9.9
RUN pip install --no-cache-dir --default-timeout=1000 python-dotenv==1.0.0 python-multipart==0.0.6
RUN pip install --no-cache-dir --default-timeout=1000 python-jose[cryptography]==3.3.0 passlib[bcrypt]==1.7.4
RUN pip install --no-cache-dir --default-timeout=1000 "universal-pathlib<0.2.0" "flask-session<0.6.0" joblib==1.3.2