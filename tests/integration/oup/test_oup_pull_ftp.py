import datetime

import pytest
from airflow import DAG
from airflow.models import DagBag
from airflow.models.dagrun import DagRun
from airflow.utils.state import DagRunState
from busypie import SECOND, wait
from common.pull_ftp import migrate_from_ftp
from oup.ftp_service import OUPFTPService
from oup.repository import OUPRepository
from structlog import get_logger

DAG_NAME = "oup_pull_ftp"


@pytest.fixture
def dag():
    dagbag = DagBag(dag_folder="dags/", include_examples=False)
    assert dagbag.import_errors.get(f"dags/{DAG_NAME}.py") is None
    yield dagbag.get_dag(dag_id=DAG_NAME)


def test_dag_loaded(dag: DAG):
    assert dag is not None
    assert len(dag.tasks) == 2


def test_dag_run(dag: DAG):
    repo = OUPRepository()
    repo.delete_all()
    assert len(repo.find_all()) == 0
    id = datetime.datetime.utcnow().strftime("test_oup_pull_ftp_%Y-%m-%dT%H:%M:%S.%f")
    dagrun = dag.create_dagrun(DagRunState.QUEUED, run_id=id)
    wait().at_most(90, SECOND).until(lambda: get_dagrun_state(dagrun))
    assert len(repo.find_all()) == 3


def test_dag_migrate_from_FTP():
    repo = OUPRepository()
    repo.delete_all()
    assert len(repo.find_all()) == 0
    with OUPFTPService() as ftp:
        migrate_from_ftp(
            ftp,
            repo,
            get_logger().bind(class_name="test_logger"),
            **{
                "params": {
                    "excluded_directories": [],
                    "force_pull": False,
                    "filenames_pull": {
                        "enabled": False,
                        "filenames": [],
                        "force_from_ftp": False,
                    },
                }
            },
        )
        assert len(repo.find_all()) == 3


def get_dagrun_state(dagrun: DagRun):
    dagrun.update_state()
    return (
        not dagrun.get_state() == DagRunState.QUEUED
        and not dagrun.get_state() == DagRunState.RUNNING
    )
