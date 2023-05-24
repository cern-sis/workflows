import datetime

import pytest
from airflow import DAG
from airflow.models import DagBag, DagModel
from airflow.utils.state import DagRunState
from busypie import SECOND, wait
from common.pull_ftp import migrate_from_ftp, trigger_file_processing
from common.repository import IRepository
from common.utils import check_dagrun_state
from iop.repository import IOPRepository
from iop.sftp_service import IOPSFTPService
from structlog import get_logger

DAG_NAME = "iop_pull_ftp"


@pytest.fixture
def dag():
    dagbag = DagBag(dag_folder="dags/", include_examples=False)
    assert dagbag.import_errors.get(f"dags/{DAG_NAME}.py") is None
    iop_dag = dagbag.get_dag(dag_id=DAG_NAME)
    return iop_dag


@pytest.fixture
def dag_was_paused(dag):
    return dag.get_is_paused()


@pytest.fixture
def iop_empty_repo():
    repo = IOPRepository()
    repo.delete_all()
    yield repo


class TestClassIOPFilesHarvesting:
    def test_dag_loaded(self, dag: DAG):
        assert dag is not None
        assert len(dag.tasks) == 2

    def test_dag_run(self, dag: DAG, dag_was_paused: bool, iop_empty_repo: IRepository):
        assert len(iop_empty_repo.find_all()) == 0
        dag_run_id = datetime.datetime.utcnow().strftime(
            "test_iop_dag_pull_ftp_%Y-%m-%dT%H:%M:%S.%f"
        )
        if dag.get_is_paused():
            DagModel.get_dagmodel(dag.dag_id).set_is_paused(is_paused=False)
        dagrun = dag.create_dagrun(DagRunState.QUEUED, run_id=dag_run_id)
        dagrun.update_state()
        wait().at_most(60, SECOND).until(
            lambda: check_dagrun_state(dagrun, not_allowed_states=["queued", "running"])
        )
        expected_files = [
            {
                "pdf": "extracted/2022-07-30T03_02_01_content/1674-1137/1674-1137_46/1674-1137_46_8/1674-1137_46_8_085001/cpc_46_8_085001.pdf",
                "xml": "extracted/2022-07-30T03_02_01_content/1674-1137/1674-1137_46/1674-1137_46_8/1674-1137_46_8_085001/cpc_46_8_085001.xml",
            },
            {
                "pdf": "extracted/2022-07-30T03_02_01_content/1674-1137/1674-1137_46/1674-1137_46_8/1674-1137_46_8_085104/cpc_46_8_085104.pdf",
                "xml": "extracted/2022-07-30T03_02_01_content/1674-1137/1674-1137_46/1674-1137_46_8/1674-1137_46_8_085104/cpc_46_8_085104.xml",
            },
            {
                "pdf": "extracted/2022-07-30T03_02_01_content/1674-1137/1674-1137_46/1674-1137_46_8/1674-1137_46_8_085106/cpc_46_8_085106.pdf",
                "xml": "extracted/2022-07-30T03_02_01_content/1674-1137/1674-1137_46/1674-1137_46_8/1674-1137_46_8_085106/cpc_46_8_085106.xml",
            },
            {
                "pdf": "extracted/2022-09-01T03_01_40_content/1674-1137/1674-1137_46/1674-1137_46_9/1674-1137_46_9_093111/cpc_46_9_093111.pdf",
                "xml": "extracted/2022-09-01T03_01_40_content/1674-1137/1674-1137_46/1674-1137_46_9/1674-1137_46_9_093111/cpc_46_9_093111.xml",
            },
            {
                "pdf": "extracted/2022-09-03T03_01_49_content/1674-1137/1674-1137_46/1674-1137_46_9/1674-1137_46_9_093110/cpc_46_9_093110.pdf",
                "xml": "extracted/2022-09-03T03_01_49_content/1674-1137/1674-1137_46/1674-1137_46_9/1674-1137_46_9_093110/cpc_46_9_093110.xml",
            },
            {
                "pdf": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103001/cpc_46_10_103001.pdf",
                "xml": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103001/cpc_46_10_103001.xml",
            },
            {
                "pdf": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103101/cpc_46_10_103101.pdf",
                "xml": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103101/cpc_46_10_103101.xml",
            },
            {
                "pdf": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103102/cpc_46_10_103102.pdf",
                "xml": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103102/cpc_46_10_103102.xml",
            },
            {
                "pdf": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103104/cpc_46_10_103104.pdf",
                "xml": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103104/cpc_46_10_103104.xml",
            },
            {
                "pdf": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103105/cpc_46_10_103105.pdf",
                "xml": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103105/cpc_46_10_103105.xml",
            },
            {
                "pdf": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103108/cpc_46_10_103108.pdf",
                "xml": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103108/cpc_46_10_103108.xml",
            },
            {"xml": "extracted/aca95c.xml/aca95c.xml"},
        ]

        assert iop_empty_repo.find_all() == expected_files
        if dag_was_paused:
            DagModel.get_dagmodel(dag.dag_id).set_is_paused(is_paused=True)

    def test_dag_migrate_from_FTP(self, iop_empty_repo):
        assert len(iop_empty_repo.find_all()) == 0
        with IOPSFTPService() as sftp:
            migrate_from_ftp(
                sftp,
                iop_empty_repo,
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
            assert iop_empty_repo.find_all() == [
                {
                    "pdf": "extracted/2022-07-30T03_02_01_content/1674-1137/1674-1137_46/1674-1137_46_8/1674-1137_46_8_085001/cpc_46_8_085001.pdf",
                    "xml": "extracted/2022-07-30T03_02_01_content/1674-1137/1674-1137_46/1674-1137_46_8/1674-1137_46_8_085001/cpc_46_8_085001.xml",
                },
                {
                    "pdf": "extracted/2022-07-30T03_02_01_content/1674-1137/1674-1137_46/1674-1137_46_8/1674-1137_46_8_085104/cpc_46_8_085104.pdf",
                    "xml": "extracted/2022-07-30T03_02_01_content/1674-1137/1674-1137_46/1674-1137_46_8/1674-1137_46_8_085104/cpc_46_8_085104.xml",
                },
                {
                    "pdf": "extracted/2022-07-30T03_02_01_content/1674-1137/1674-1137_46/1674-1137_46_8/1674-1137_46_8_085106/cpc_46_8_085106.pdf",
                    "xml": "extracted/2022-07-30T03_02_01_content/1674-1137/1674-1137_46/1674-1137_46_8/1674-1137_46_8_085106/cpc_46_8_085106.xml",
                },
                {
                    "pdf": "extracted/2022-09-01T03_01_40_content/1674-1137/1674-1137_46/1674-1137_46_9/1674-1137_46_9_093111/cpc_46_9_093111.pdf",
                    "xml": "extracted/2022-09-01T03_01_40_content/1674-1137/1674-1137_46/1674-1137_46_9/1674-1137_46_9_093111/cpc_46_9_093111.xml",
                },
                {
                    "pdf": "extracted/2022-09-03T03_01_49_content/1674-1137/1674-1137_46/1674-1137_46_9/1674-1137_46_9_093110/cpc_46_9_093110.pdf",
                    "xml": "extracted/2022-09-03T03_01_49_content/1674-1137/1674-1137_46/1674-1137_46_9/1674-1137_46_9_093110/cpc_46_9_093110.xml",
                },
                {
                    "pdf": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103001/cpc_46_10_103001.pdf",
                    "xml": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103001/cpc_46_10_103001.xml",
                },
                {
                    "pdf": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103101/cpc_46_10_103101.pdf",
                    "xml": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103101/cpc_46_10_103101.xml",
                },
                {
                    "pdf": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103102/cpc_46_10_103102.pdf",
                    "xml": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103102/cpc_46_10_103102.xml",
                },
                {
                    "pdf": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103104/cpc_46_10_103104.pdf",
                    "xml": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103104/cpc_46_10_103104.xml",
                },
                {
                    "pdf": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103105/cpc_46_10_103105.pdf",
                    "xml": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103105/cpc_46_10_103105.xml",
                },
                {
                    "pdf": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103108/cpc_46_10_103108.pdf",
                    "xml": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103108/cpc_46_10_103108.xml",
                },
                {"xml": "extracted/aca95c.xml/aca95c.xml"},
            ]

    def test_dag_trigger_file_processing(
        self,
    ):
        repo = IOPRepository()
        assert [x["xml"] for x in repo.find_all()] == trigger_file_processing(
            "iop", repo, get_logger().bind(class_name="test_logger")
        )
