import pytest
from airflow import DAG
from airflow.models import DagBag
from common.pull_ftp import migrate_from_ftp, trigger_file_processing
from common.repository import IRepository
from elsevier.sftp_service import ElsevierSFTPService
from elsevier.repository import ElsevierRepository
from structlog import get_logger

DAG_NAME = "elsevier_pull_ftp"


@pytest.fixture
def dag():
    dagbag = DagBag(dag_folder="dags/", include_examples=False)
    assert dagbag.import_errors.get(f"dags/{DAG_NAME}.py") is None
    return dagbag.get_dag(dag_id=DAG_NAME)


@pytest.fixture
def dag_was_paused(dag):
    return dag.get_is_paused()


@pytest.fixture
def elsevier_empty_repo():
    repo = ElsevierRepository()
    repo.delete_all()
    yield repo


def test_dag_loaded(dag: DAG):
    assert dag is not None
    assert len(dag.tasks) == 2


def test_dag_run(dag: DAG, dag_was_paused: bool, elsevier_empty_repo: IRepository):
    assert len(elsevier_empty_repo.find_all()) == 0
    dag.clear()
    dag.test()
    expected_files = [
        {
            "pdf": "extracted/CERNQ000000010669A/CERNQ000000010669/S0370269323005105/main.pdf",
            "xml": "extracted/CERNQ000000010669A/CERNQ000000010669/S0370269323005105/main.xml",
        },
        {"xml": "extracted/CERNQ000000010669A/CERNQ000000010669/dataset.xml"},
    ]
    assert elsevier_empty_repo.find_all() == expected_files


def test_dag_migrate_from_FTP(elsevier_empty_repo):
    assert len(elsevier_empty_repo.find_all()) == 0
    with ElsevierSFTPService() as ftp:
        migrate_from_ftp(
            ftp,
            elsevier_empty_repo,
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
        assert elsevier_empty_repo.find_all() == [
            {
                "pdf": "extracted/CERNQ000000010669A/CERNQ000000010669/S0370269323005105/main.pdf",
                "xml": "extracted/CERNQ000000010669A/CERNQ000000010669/S0370269323005105/main.xml",
            },
            {"xml": "extracted/CERNQ000000010669A/CERNQ000000010669/dataset.xml"},
        ]


def test_dag_trigger_file_processing():
    repo = ElsevierRepository()
    assert [x["xml"] for x in repo.find_all()] == trigger_file_processing(
        "oup", repo, get_logger().bind(class_name="test_logger")
    )
