FROM apache/airflow:3.0.2-python3.11

COPY requirements.txt /requirements.txt
COPY requirements-test.txt /requirements-test.txt
COPY requirements-airflow.txt /requirements-airflow.txt

# Install apt packages for 'leveldb'
USER root
RUN apt-get update && apt-get install -y \
    build-essential \
    libleveldb-dev \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
USER airflow

RUN pip install --no-cache-dir \
    "apache-airflow[celery,postgres,redis,cncf.kubernetes,sentry,amazon,opensearch]==${AIRFLOW_VERSION}" \
    -r /requirements.txt \
    -r /requirements-test.txt \
    --constraint https://raw.githubusercontent.com/apache/airflow/constraints-3.0.2/constraints-3.11.txt

RUN pip install apache-airflow-providers-elasticsearch==6.3.0

COPY dags /opt/airflow/dags
COPY plugins /opt/airflow/plugins
COPY airflow.cfg /opt/airflow/airflow.cfg
