FROM python:3.10-slim

WORKDIR /app

# Copier et installer les requirements backend
COPY backend/requirements.txt /requirements-backend.txt
RUN pip install --no-cache-dir -r /requirements-backend.txt

# Le code est monté via volume dans docker-compose