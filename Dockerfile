FROM registry.cern.ch/cern-sis/airflow-base:2.8.3

ENV AIRFLOW_HOME=/opt/airflow
WORKDIR /opt/airflow

ENV PYTHONBUFFERED=0
ENV AIRFLOW__LOGGING__LOGGING_LEVEL=INFO

COPY requirements.txt ./requirements.txt
COPY requirements-test.txt ./requirements-test.txt
COPY requirements-airflow.txt ./requirements-airflow.txt

COPY dags ./dags
COPY airflow.cfg ./airflow.cfg

RUN pip install --upgrade pip &&\
    pip install --no-cache-dir --upgrade setuptools==59.1.1 &&\
    pip install --no-cache-dir --upgrade wheel &&\
    pip install --no-cache-dir --user -r requirements-airflow.txt &&\
    pip install --no-cache-dir --user -r requirements.txt &&\
    pip install --no-cache-dir --user -r requirements-test.txt
