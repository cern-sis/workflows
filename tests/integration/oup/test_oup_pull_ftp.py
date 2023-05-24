import datetime

import pytest
from airflow import DAG
from airflow.models import DagBag, DagModel
from airflow.utils.state import DagRunState
from busypie import SECOND, wait
from common.pull_ftp import migrate_from_ftp
from common.utils import check_dagrun_state
from oup.ftp_service import OUPFTPService
from oup.repository import OUPRepository
from structlog import get_logger

DAG_NAME = "oup_pull_ftp"


@pytest.fixture
def dag():
    dagbag = DagBag(dag_folder="dags/", include_examples=False)
    assert dagbag.import_errors.get(f"dags/{DAG_NAME}.py") is None
    yield dagbag.get_dag(dag_id=DAG_NAME)


@pytest.fixture
def dag_was_paused(dag):
    return dag.get_is_paused()


class TestClassOUPPullFilesFromFTP:
    def test_dag_loaded(self, dag: DAG):
        assert dag is not None
        assert len(dag.tasks) == 2

    def test_dag_run(
        self,
        dag: DAG,
        dag_was_paused: bool,
    ):
        repo = OUPRepository()
        repo.delete_all()
        assert len(repo.find_all()) == 0
        dag_run_id = datetime.datetime.utcnow().strftime(
            "test_oup_pull_ftp_%Y-%m-%dT%H:%M:%S.%f"
        )
        if dag.get_is_paused:
            DagModel.get_dagmodel(dag.dag_id).set_is_paused(is_paused=False)
        dagrun = dag.create_dagrun(DagRunState.QUEUED, run_id=dag_run_id)
        wait().at_most(90, SECOND).until(
            lambda: check_dagrun_state(dagrun, not_allowed_states=["queued", "running"])
        )
        assert len(repo.find_all()) == 3
        if dag_was_paused:
            DagModel.get_dagmodel(dag.dag_id).set_is_paused(is_paused=True)

    def test_dag_migrate_from_FTP(self):
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
