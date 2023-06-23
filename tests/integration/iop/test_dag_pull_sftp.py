from airflow import DAG
from airflow.models import DagBag
from common.repository import IRepository
from iop.repository import IOPRepository
from pytest import fixture

DAG_NAME = "iop_pull_ftp"


@fixture
def dag():
    dagbag = DagBag(dag_folder="dags/", include_examples=False)
    assert dagbag.import_errors.get(f"dags/{DAG_NAME}.py") is None
    iop_dag = dagbag.get_dag(dag_id=DAG_NAME)
    return iop_dag


@fixture
def iop_empty_repo():
    repo = IOPRepository()
    repo.delete_all()
    yield repo


class TestClassIOPFilesHarvesting:
    def test_dag_loaded(self, dag: DAG):
        assert dag is not None
        assert len(dag.tasks) == 2

    def test_dag_run(self, dag: DAG, iop_empty_repo: IRepository):
        assert len(iop_empty_repo.find_all()) == 0
        dag.test()
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

        assert sorted(
            iop_empty_repo.find_all(), key=lambda x: x["xml"], reverse=True
        ) == sorted(expected_files, key=lambda x: x["xml"], reverse=True)
