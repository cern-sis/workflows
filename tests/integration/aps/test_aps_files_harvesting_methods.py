import json

import pytest
from airflow import DAG
from airflow.models import DagBag
from aps.aps_api_client import APSApiClient
from aps.aps_params import APSParams
from aps.repository import APSRepository
from aps.utils import save_file_in_s3

DAG_NAME = "aps_fetch_api"
TRIGGERED_DAG_NAME = "aps_fetch_api"


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
    def test_aps_fetch_api(self, dag: DAG):
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
