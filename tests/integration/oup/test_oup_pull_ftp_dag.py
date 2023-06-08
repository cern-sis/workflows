import pytest
from airflow.models import DagBag
from oup.repository import OUPRepository

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


class TestOUPPullFTPDAG:
    def test_OUP_dag_migrate_from_FTP(self, dag, oup_empty_repo):
        assert len(oup_empty_repo.find_all()) == 0
        dag.test()
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
