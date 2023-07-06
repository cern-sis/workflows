import pytest
from airflow import DAG
from airflow.models import DagBag
from common.pull_ftp import migrate_from_ftp
from oup.ftp_service import OUPFTPService
from oup.repository import OUPRepository
from structlog import get_logger

DAG_NAME = "oup_pull_ftp"
## eee

@pytest.fixture
def dag():
    dagbag = DagBag(dag_folder="dags/", include_examples=False)
    assert dagbag.import_errors.get(f"dags/{DAG_NAME}.py") is None
    yield dagbag.get_dag(dag_id=DAG_NAME)


@pytest.fixture
def dag_was_paused(dag):
    return dag.get_is_paused()


def test_dag_loaded(dag: DAG):
    assert dag is not None
    assert len(dag.tasks) == 2


def test_dag_run(
    dag: DAG,
    dag_was_paused: bool,
):
    repo = OUPRepository()
    repo.delete_all()
    assert len(repo.find_all()) == 0
    dag.clear()
    dag.test()
    assert len(repo.find_all()) == 3


@pytest.mark.skip("Already tested in test_dag_run")
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
