FROM apache/airflow:2.5.3-python3.10

ENV PYTHONBUFFERED=0
ENV AIRFLOW_UID=501
ENV PYTHONASYNCIODEBUG=1
ENV AIRFLOW__LOGGING__LOGGING_LEVEL=DEBUG
ENV AIRFLOW__WEBSERVER__SESSION_BACKEND=securecookie

COPY requirements.txt ./requirements.txt
COPY requirements-test.txt ./requirements-test.txt
COPY dags ./dags
USER airflow
RUN pip install --upgrade pip &&\
    pip install --no-cache-dir --upgrade setuptools==59.1.1 &&\
    pip install --no-cache-dir --upgrade wheel &&\
    pip install --no-cache-dir --user -r requirements.txt -r requirements-test.txt
