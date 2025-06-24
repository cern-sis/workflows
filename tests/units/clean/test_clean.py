from airflow.models import DagBag
from pytest import fixture


@fixture
def dag():
    dagbag = DagBag(dag_folder="dags/", include_examples=False)
    assert dagbag.import_errors.get("dags/cleanup_logs.py") is None
    clean_dag = dagbag.get_dag(dag_id="cleanup_logs")
    return clean_dag


def test_dag_loaded(dag):
    assert dag is not None
    assert len(dag.tasks) == 1
