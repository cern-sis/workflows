import pytest
from airflow import DAG
from airflow.models import DagBag
from common.pull_ftp import migrate_from_ftp, trigger_file_processing
from common.repository import IRepository
from oup.ftp_service import OUPFTPService
from oup.repository import OUPRepository
from structlog import get_logger

DAG_NAME = "oup_pull_ftp"


@pytest.fixture
def dag():
    dagbag = DagBag(dag_folder="dags/", include_examples=False)
    assert dagbag.import_errors.get(f"dags/{DAG_NAME}.py") is None
    return dagbag.get_dag(dag_id=DAG_NAME)


@pytest.fixture
def dag_was_paused(dag):
    return dag.get_is_paused()


@pytest.fixture
def oup_empty_repo():
    repo = OUPRepository()
    repo.delete_all()
    yield repo


class TestClassOUPFilesHarvesting:
    def test_dag_loaded(self, dag: DAG):
        assert dag is not None
        assert len(dag.tasks) == 2

    def test_dag_run(self, dag: DAG, dag_was_paused: bool, oup_empty_repo: IRepository):
        assert len(oup_empty_repo.find_all()) == 0
        dag.clean()
        dag.test()
        expected_files = [
            {
                "pdf": "extracted/2022-09-22_00:30:02_ptep_iss_2022_9_archival/ptac108.pdf",
                "xml": "extracted/2022-09-22_00:30:02_ptep_iss_2022_9.xml/ptac108.xml",
            },
            {
                "pdf": "extracted/2022-09-22_00:30:02_ptep_iss_2022_9_archival/ptac113.pdf",
                "xml": "extracted/2022-09-22_00:30:02_ptep_iss_2022_9.xml/ptac113.xml",
            },
            {
                "pdf": "extracted/2022-09-22_00:30:02_ptep_iss_2022_9_archival/ptac120.pdf",
                "xml": "extracted/2022-09-22_00:30:02_ptep_iss_2022_9.xml/ptac120.xml",
            },
        ]
        assert oup_empty_repo.find_all() == expected_files

    def test_dag_migrate_from_FTP(self, oup_empty_repo):
        assert len(oup_empty_repo.find_all()) == 0
        with OUPFTPService() as ftp:
            migrate_from_ftp(
                ftp,
                oup_empty_repo,
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
            assert oup_empty_repo.find_all() == [
                {
                    "pdf": "extracted/2022-09-22_00:30:02_ptep_iss_2022_9_archival/ptac108.pdf",
                    "xml": "extracted/2022-09-22_00:30:02_ptep_iss_2022_9.xml/ptac108.xml",
                },
                {
                    "pdf": "extracted/2022-09-22_00:30:02_ptep_iss_2022_9_archival/ptac113.pdf",
                    "xml": "extracted/2022-09-22_00:30:02_ptep_iss_2022_9.xml/ptac113.xml",
                },
                {
                    "pdf": "extracted/2022-09-22_00:30:02_ptep_iss_2022_9_archival/ptac120.pdf",
                    "xml": "extracted/2022-09-22_00:30:02_ptep_iss_2022_9.xml/ptac120.xml",
                },
            ]

    def test_dag_trigger_file_processing(self):
        repo = OUPRepository()
        assert [x["xml"] for x in repo.find_all()] == trigger_file_processing(
            "oup", repo, get_logger().bind(class_name="test_logger")
        )
