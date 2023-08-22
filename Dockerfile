FROM apache/airflow:2.6.0-python3.10

ENV AIRFLOW_HOME=/opt/airflow
WORKDIR /opt/airflow

ENV PYTHONBUFFERED=0
ENV AIRFLOW_UID=501
ENV AIRFLOW__LOGGING__LOGGING_LEVEL=DEBUG

COPY requirements.txt ./requirements.txt
COPY requirements-test.txt ./requirements-test.txt
COPY dags ./dags
COPY airflow.cfg ./airflow.cfg

USER airflow
RUN pip install --upgrade pip &&\
    pip install --no-cache-dir --upgrade setuptools==59.1.1 &&\
    pip install --no-cache-dir --upgrade wheel &&\
    pip install --no-cache-dir --user -r requirements.txt -r requirements-test.txt
