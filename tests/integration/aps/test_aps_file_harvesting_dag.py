import pytest
from airflow import DAG
from airflow.models import DagBag
from aps.repository import APSRepository

DAG_NAME = "aps_fetch_api"


@pytest.fixture
def dag():
    dagbag = DagBag(dag_folder="dags/", include_examples=False)
    assert dagbag.import_errors.get(f"dags/{DAG_NAME}.py") is None
    return dagbag.get_dag(dag_id=DAG_NAME)


@pytest.fixture
def aps_empty_repo():
    repo = APSRepository()
    repo.delete_all()
    yield repo


class TestClassAPSFilesHarvestingDAG:
    def test_dag_loaded(self, dag: DAG):
        assert dag is not None
        assert len(dag.tasks) == 3

    def test_aps_harvesting_dag(self, dag: DAG, aps_empty_repo: APSRepository):
        assert len(aps_empty_repo.find_all()) == 0
        dag.test(run_conf={"start_date": "2022-02-05", "until_date": "2022-03-05"})
        assert len(aps_empty_repo.find_all()) == 1
