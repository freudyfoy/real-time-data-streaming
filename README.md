# real-time-data-streaming
This project demonstrates each stage from data ingestion to processing and finally to storage, utilizing a robust tech stack that includes Apache Airflow, Python, Apache Kafka, Apache Zookeeper, Apache Spark, and Cassandra. Everything is containerized using Docker for ease of deployment and scalability.

## Tech Stack
- **Apache Airflow**
- **Apache Kafka**
- **Apache Zookeeper**
- **Apache Spark**
- **Cassandra**
- **PostgreSQL**
- **Docker**


## System Architecture
- **Data Source**
- **Apache Airflow**
- **Apache Kafka and Zookeeper**
- **Control Center and Schema Registry**: Helps in monitoring and schema management of our Kafka streams.
- **Apache Spark**
- **Cassandra**

<img width="3274" height="1221" alt="Data engineering architecture" src="images/Data engineering architecture.png" />


## Getting started

```bash
docker compose up
```

```python
python spark_stream.py
```

## Current state
- Project runs normally with python ```python spark_stream.py```
- **To do next**: Fixing bugs on ```spark-submit --master spark://localhost:7077 spark_stream.py```
