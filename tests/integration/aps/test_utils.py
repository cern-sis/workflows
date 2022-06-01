import json
from datetime import datetime

import pytest
from airflow import DAG
from airflow.models import DagBag
from airflow.models.dagrun import DagRun
from airflow.utils.state import DagRunState
from aps.aps_api_client import APSApiClient
from aps.aps_params import APSParams
from aps.repository import APSRepository
from aps.utils import save_file_in_s3
from busypie import SECOND, wait

DAG_NAME = "aps_fetch_api"
TRIGGERED_DAG_NAME = "aps_process_file"


@pytest.fixture
def dag():
    dagbag = DagBag(dag_folder="dags/", include_examples=False)
    assert dagbag.import_errors.get(f"dags/{DAG_NAME}.py") is None
    return dagbag.get_dag(dag_id=DAG_NAME)


def test_dag_loaded(dag: DAG):
    assert dag is not None
    assert len(dag.tasks) == 3


@pytest.mark.vcr
def test_aps_fetch_api():
    dates = {
        "aps_fetching_from_date": "2022-02-05",
        "aps_fetching_until_date": "2022-03-05",
    }
    repo = APSRepository()
    repo.delete_all()
    assert len(repo.find_all()) == 0
    parameters = APSParams(
        from_date=dates["aps_fetching_from_date"],
        until_date=dates["aps_fetching_until_date"],
    ).get_params()
    aps_api_client = APSApiClient()
    articles_metadata = str.encode(
        json.dumps(aps_api_client.get_articles_metadata(parameters))
    )
    save_file_in_s3(articles_metadata, repo)
    assert len(repo.find_all()) == 1


@pytest.mark.vcr
def test_dag_run(dag: DAG):
    repo = APSRepository()
    repo.delete_all()
    assert len(repo.find_all()) == 0
    id = datetime.utcnow().strftime("test_aps_fetch_api_%Y-%m-%dT%H:%M:%S.%f")
    dagrun = dag.create_dagrun(DagRunState.QUEUED, run_id=id)
    wait().at_most(60, SECOND).until(lambda: __test_dagrun_state(dagrun))
    assert len(repo.find_all()) == 1


def __test_dagrun_state(dagrun: DagRun):
    dagrun.update_state()
    return (
        not dagrun.get_state() == DagRunState.QUEUED
        and not dagrun.get_state() == DagRunState.RUNNING
    )
