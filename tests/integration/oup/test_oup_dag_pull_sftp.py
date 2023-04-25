import datetime

import pytest
from airflow import DAG
from airflow.models import DagBag
from airflow.models.dagrun import DagRun
from airflow.utils.state import DagRunState
from busypie import SECOND, wait
from common.pull_ftp import migrate_from_ftp, trigger_file_processing
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
def oup_empty_repo():
    repo = OUPRepository()
    repo.delete_all()
    yield repo


def test_dag_loaded(dag: DAG):
    assert dag is not None
    assert len(dag.tasks) == 2


def test_dag_run(dag: DAG, oup_empty_repo):
    assert len(oup_empty_repo.find_all()) == 0
    id = datetime.datetime.utcnow().strftime(
        "test_oup_dag_pull_ftp_%Y-%m-%dT%H:%M:%S.%f"
    )
    dagrun = dag.create_dagrun(DagRunState.QUEUED, run_id=id)
    wait().at_most(60, SECOND).until(lambda: __test_dagrun_state(dagrun))
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


def test_dag_migrate_from_FTP(oup_empty_repo):
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


def test_dag_trigger_file_processing():
    repo = OUPRepository()
    assert [x["xml"] for x in repo.find_all()] == trigger_file_processing(
        "oup", repo, get_logger().bind(class_name="test_logger")
    )


def __test_dagrun_state(dagrun: DagRun):
    dagrun.update_state()
    return (
        not dagrun.get_state() == DagRunState.QUEUED
        and not dagrun.get_state() == DagRunState.RUNNING
    )
