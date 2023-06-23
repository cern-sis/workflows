import pytest
from common.pull_ftp import migrate_from_ftp, trigger_file_processing
from oup.ftp_service import OUPFTPService
from oup.repository import OUPRepository
from structlog import get_logger


@pytest.fixture
def oup_empty_repo():
    repo = OUPRepository()
    repo.delete_all()
    yield repo


class TestOUPHarvestinDAGMethods:
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
