import os
from datetime import datetime, timezone

from airflow.models import DagBag
from freezegun import freeze_time
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


@freeze_time("2023-09-20")
@fixture
def old_temp_dir(tmpdir, tmp_path):
    logs_date = datetime.utcnow().astimezone(timezone.utc)
    log_path = tmpdir.join(
        f'logs/dag_id=test/run_id=test__{logs_date.strftime("%Y-%m-%dT%H:%M:%S.%f%z")}/task_id=test_task/attempt=1.log'
    )
    log_path.dirpath().ensure_dir()
    yield log_path


@freeze_time("2023-09-20")
def test_clean_up_command(dag, old_temp_dir, monkeypatch):
    monkeypatch.setenv("AIRFLOW_HOME", old_temp_dir)
    dag.clear()
    dag.test()
    assert not os.path.exists(old_temp_dir)
