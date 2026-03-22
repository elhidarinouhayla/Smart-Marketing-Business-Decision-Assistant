#  Smart Marketing Business Decision Assistant (Backend)

Welcome to the **Smart Marketing Assistant** backend! This system orchestrates a full Machine Learning pipeline—from data processing with Airflow and Spark to serving predictions via FastAPI and monitoring with Prometheus/Grafana.

---

##  Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10+)
- **Database**: [PostgreSQL 16](https://www.postgresql.org/)
- **Workflow Orchestration**: [Apache Airflow](https://airflow.apache.org/)
- **Data Processing**: [PySpark](https://spark.apache.org/docs/latest/api/python/index.html)
- **Model Tracking**: [MLflow](https://mlflow.org/)
- **Monitoring**: [Prometheus](https://prometheus.io/) & [Grafana](https://grafana.com/)
- **Containerization**: [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)

---

##  Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed.
- [Docker Compose](https://docs.docker.com/compose/install/) installed.

### Installation & Launch

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/elhidarinouhayla/Smart-Marketing-Business-Decision-Assistant.git
    cd Smart-Marketing-Business-Decision-Assistant
    ```

2.  **Spin up the services**:
    ```bash
    docker compose up -d
    ```
    *This will start the Database, Airflow, Backend API, MLflow, and Monitoring tools.*

3.  **Initialize the Database**:
    After the containers are up, populate the database with test data:
    ```bash
    docker exec backend python /app/populate_db.py
    ```

---

## 🔌API Services & Endpoints

| Service | Port (Host) | Description |
| :--- | :--- | :--- |
| **Backend API** | `8001` | Core FastAPI service serving the dashboard. |
| **Airflow Webserver** | `8081` | Pipeline orchestration and DAG management. |
| **MLflow UI** | `5001` | Experiment tracking and model registry. |
| **Prometheus** | `9090` | Metrics collection. |
| **Grafana** | `3001` | Visual monitoring dashboard. |

### API Documentation
Once the backend is running, you can access the interactive Swagger UI at:
👉 **[http://localhost:8001/docs](http://localhost:8001/docs)**

---

##  Project Structure

- `/backend`: FastAPI source code (Controllers, Models, Schemas).
- `/dags`: Airflow DAGs for ETL and Training.
- `/ml`: Machine Learning logic and data storage.
- `/monitoring`: Configuration for Prometheus and Grafana.
- `docker-compose.yml`: Main orchestration file.
- `populate_db.py`: Database seeding script.

---

##  Authentication

The backend uses **JWT (JSON Web Tokens)** for authentication. 
- All `/dashboard` and `/predictions` endpoints require a valid token in the headers.
- Default test user created by `populate_db.py`:
  - **Username**: `testuser`
  - **Password**: `testpassword123`

---

##  License
This project is licensed under the MIT License.
