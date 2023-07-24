FROM python:3.10

WORKDIR /opt/airflow/
ENV AIRFLOW_HOME=/opt/airflow/

ENV PYTHONBUFFERED=0
ENV AIRFLOW_UID=501

COPY pyproject.toml ./pyproject.toml
COPY poetry.lock ./poetry.lock

COPY dags ./dags
RUN pip install --upgrade pip &&\
    pip install --no-cache-dir --upgrade setuptools==59.1.1 &&\
    pip install --no-cache-dir --upgrade wheel &&\
    pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false --local

RUN poetry install
