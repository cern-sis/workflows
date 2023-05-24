import json
from datetime import datetime

import pytest
from airflow import DAG
from airflow.models import DagBag, DagModel
from airflow.utils.state import DagRunState
from aps.aps_api_client import APSApiClient
from aps.aps_params import APSParams
from aps.repository import APSRepository
from aps.utils import save_file_in_s3
from busypie import SECOND, wait
from common.utils import check_dagrun_state

DAG_NAME = "aps_fetch_api"
TRIGGERED_DAG_NAME = "aps_fetch_api"


@pytest.fixture
def dag_was_paused(dag):
    return dag.get_is_paused()


@pytest.fixture
def dag():
    dagbag = DagBag(dag_folder="dags/", include_examples=False)
    assert dagbag.import_errors.get(f"dags/{DAG_NAME}.py") is None
    return dagbag.get_dag(dag_id=DAG_NAME)


class TestClassAPSFilesHarvesting:
    def test_dag_loaded(self, dag: DAG):
        assert dag is not None
        assert len(dag.tasks) == 3

    @pytest.mark.vcr
    def test_aps_fetch_api(self, dag: DAG, dag_was_paused: bool):
        dates = {
            "start_date": "2022-02-05",
            "until_date": "2022-03-05",
        }
        repo = APSRepository()
        repo.delete_all()
        assert len(repo.find_all()) == 0
        parameters = APSParams(
            from_date=dates["start_date"],
            until_date=dates["until_date"],
        ).get_params()
        aps_api_client = APSApiClient()
        articles_metadata = str.encode(
            json.dumps(aps_api_client.get_articles_metadata(parameters))
        )
        save_file_in_s3(articles_metadata, repo)
        assert len(repo.find_all()) == 1

    def test_dag_run(self, dag: DAG, dag_was_paused: bool):
        repo = APSRepository()
        repo.delete_all()
        assert len(repo.find_all()) == 0
        dag_run_id = datetime.utcnow().strftime("test_dag_run_%Y-%m-%dT%H:%M:%S.%f")
        if dag.get_is_paused():
            DagModel.get_dagmodel(dag.dag_id).set_is_paused(is_paused=False)
        dagrun = dag.create_dagrun(
            DagRunState.QUEUED,
            run_id=dag_run_id,
            conf={"start_date": "2022-06-17", "until_date": "2022-06-21"},
        )
        wait().at_most(60, SECOND).until(
            lambda: check_dagrun_state(dagrun, not_allowed_states=["queued", "running"])
        )
        if dag_was_paused:
            DagModel.get_dagmodel(dag.dag_id).set_is_paused(is_paused=True)
        assert len(repo.find_all()) == 1
