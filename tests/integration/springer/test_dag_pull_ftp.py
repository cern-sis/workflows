import datetime

import pytest
from airflow import DAG
from airflow.models import DagBag
from airflow.models.dagrun import DagRun
from airflow.utils.state import DagRunState
from busypie import SECOND, wait
from common.pull_ftp import migrate_from_ftp, trigger_file_processing
from springer.repository import SpringerRepository
from springer.sftp_service import SpringerSFTPService
from structlog import get_logger

DAG_NAME = "springer_pull_ftp"


@pytest.fixture
def dag():
    dagbag = DagBag(dag_folder="dags/", include_examples=False)
    assert dagbag.import_errors.get(f"dags/{DAG_NAME}.py") is None
    return dagbag.get_dag(dag_id=DAG_NAME)


def test_dag_loaded(dag: DAG):
    assert dag is not None
    assert len(dag.tasks) == 2


def test_dag_run(dag: DAG):
    repo = SpringerRepository()
    repo.delete_all()
    assert len(repo.find_all()) == 0
    id = datetime.datetime.utcnow().strftime(
        "test_springer_dag_pull_ftp_%Y-%m-%dT%H:%M:%S.%f"
    )
    dagrun = dag.create_dagrun(DagRunState.QUEUED, run_id=id)
    wait().at_most(60, SECOND).until(lambda: __test_dagrun_state(dagrun))
    expected_files = [
        {
            "xml": "extracted/EPJC/ftp_PUB_19-01-29_20-02-10_EPJC/JOU=10052/VOL=2019.79/ISU=1/ART=6572/10052_2019_Article_6572.xml.Meta",
            "pdf": "extracted/EPJC/ftp_PUB_19-01-29_20-02-10_EPJC/JOU=10052/VOL=2019.79/ISU=1/ART=6572/BodyRef/PDF/10052_2019_Article_6572.pdf",
        },
        {
            "xml": "extracted/EPJC/ftp_PUB_19-02-06_16-01-13_EPJC_stripped/JOU=10052/VOL=2019.79/ISU=2/ART=6540/10052_2019_Article_6540.xml.Meta",
            "pdf": "extracted/EPJC/ftp_PUB_19-02-06_16-01-13_EPJC_stripped/JOU=10052/VOL=2019.79/ISU=2/ART=6540/BodyRef/PDF/10052_2019_Article_6540.pdf",
        },
        {
            "xml": "extracted/JHEP/ftp_PUB_19-01-29_20-02-10_JHEP/JOU=13130/VOL=2019.2019/ISU=1/ART=9848/13130_2019_Article_9848.xml.scoap",
            "pdf": "extracted/JHEP/ftp_PUB_19-01-29_20-02-10_JHEP/JOU=13130/VOL=2019.2019/ISU=1/ART=9848/BodyRef/PDF/13130_2019_Article_9848.pdf",
        },
    ]
    assert repo.find_all() == expected_files


def test_dag_migrate_from_FTP():
    repo = SpringerRepository()
    repo.delete_all()
    assert len(repo.find_all()) == 0
    with SpringerSFTPService(dir="upload/springer/EPJC") as sftp:
        migrate_from_ftp(
            sftp,
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
        expected_files = [
            {
                "xml": "extracted/ftp_PUB_19-01-29_20-02-10_EPJC/JOU=10052/VOL=2019.79/ISU=1/ART=6572/10052_2019_Article_6572.xml.Meta",
                "pdf": "extracted/ftp_PUB_19-01-29_20-02-10_EPJC/JOU=10052/VOL=2019.79/ISU=1/ART=6572/BodyRef/PDF/10052_2019_Article_6572.pdf",
            },
            {
                "xml": "extracted/ftp_PUB_19-02-06_16-01-13_EPJC_stripped/JOU=10052/VOL=2019.79/ISU=2/ART=6540/10052_2019_Article_6540.xml.Meta",
                "pdf": "extracted/ftp_PUB_19-02-06_16-01-13_EPJC_stripped/JOU=10052/VOL=2019.79/ISU=2/ART=6540/BodyRef/PDF/10052_2019_Article_6540.pdf",
            },
        ]
        assert repo.find_all() == expected_files


def test_dag_trigger_file_processing():
    repo = SpringerRepository()
    assert list(map(lambda x: x["xml"], repo.find_all())) == trigger_file_processing(
        "springer", repo, get_logger().bind(class_name="test_logger")
    )


def __test_dagrun_state(dagrun: DagRun):
    dagrun.update_state()
    return (
        not dagrun.get_state() == DagRunState.QUEUED
        and not dagrun.get_state() == DagRunState.RUNNING
    )
