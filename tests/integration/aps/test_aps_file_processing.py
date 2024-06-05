import pytest
from airflow.models import DagBag

DAG_NAME = "scoap3_aps_process_file"


@pytest.fixture
def dag():
    dagbag = DagBag(dag_folder="dags/", include_examples=False)
    assert dagbag.import_errors.get(f"dags/{DAG_NAME}.py") is None
    return dagbag.get_dag(dag_id=DAG_NAME)


def test_dag_loaded(dag):
    assert dag is not None
    assert len(dag.tasks) == 6
