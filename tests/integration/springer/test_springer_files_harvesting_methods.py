import pytest
from common.pull_ftp import migrate_from_ftp, reprocess_files, trigger_file_processing
from springer.repository import SpringerRepository
from springer.sftp_service import SpringerSFTPService
from structlog import get_logger

DAG_NAME = "springer_pull_ftp"


@pytest.fixture
def springer_empty_repo():
    repo = SpringerRepository()
    repo.delete_all()
    yield repo


class TestSpringerFilesHarvestingMethods:
    def test_dag_trigger_file_processing(self):
        repo = SpringerRepository()
        assert [x["xml"] for x in repo.find_all()] == trigger_file_processing(
            "springer", repo, get_logger().bind(class_name="test_logger")
        )

    def test_force_pull_from_sftp(self, springer_empty_repo):
        with SpringerSFTPService() as sftp:
            migrate_from_ftp(
                sftp,
                springer_empty_repo,
                get_logger().bind(class_name="test_logger"),
                **{
                    "params": {
                        "force_pull": False,
                        "excluded_directories": [],
                        "filenames_pull": {
                            "enabled": True,
                            "filenames": [
                                "JHEP/ftp_PUB_19-01-29_20-02-10_JHEP.zip",
                                "EPJC/ftp_PUB_19-02-06_16-01-13_EPJC_stripped.zip",
                            ],
                            "force_from_ftp": True,
                        },
                    }
                },
            )
            expected_files = [
                {
                    "xml": "extracted/EPJC/ftp_PUB_19-02-06_16-01-13_EPJC_stripped/JOU=10052/VOL=2019.79/ISU=2/ART=6540/10052_2019_Article_6540.xml.Meta",
                    "pdf": "extracted/EPJC/ftp_PUB_19-02-06_16-01-13_EPJC_stripped/JOU=10052/VOL=2019.79/ISU=2/ART=6540/BodyRef/PDF/10052_2019_Article_6540.pdf",
                },
                {
                    "xml": "extracted/JHEP/ftp_PUB_19-01-29_20-02-10_JHEP/JOU=13130/VOL=2019.2019/ISU=1/ART=9848/13130_2019_Article_9848.xml.scoap",
                    "pdf": "extracted/JHEP/ftp_PUB_19-01-29_20-02-10_JHEP/JOU=13130/VOL=2019.2019/ISU=1/ART=9848/BodyRef/PDF/13130_2019_Article_9848.pdf",
                },
            ]
            assert sorted(
                springer_empty_repo.find_all(),
                key=lambda x: (x["xml"], x["pdf"]),
                reverse=True,
            ) == sorted(
                expected_files, key=lambda x: (x["xml"], x["pdf"]), reverse=True
            )

    def test_force_pull_from_sftp_with_excluded_folder(self, springer_empty_repo):
        with SpringerSFTPService() as sftp:
            migrate_from_ftp(
                sftp,
                springer_empty_repo,
                get_logger().bind(class_name="test_logger"),
                **{
                    "params": {
                        "force_pull": True,
                        "excluded_directories": ["EPJC"],
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
                    "xml": "extracted/JHEP/ftp_PUB_19-01-29_20-02-10_JHEP/JOU=13130/VOL=2019.2019/ISU=1/ART=9848/13130_2019_Article_9848.xml.scoap",
                    "pdf": "extracted/JHEP/ftp_PUB_19-01-29_20-02-10_JHEP/JOU=13130/VOL=2019.2019/ISU=1/ART=9848/BodyRef/PDF/13130_2019_Article_9848.pdf",
                }
            ]
            assert sorted(
                springer_empty_repo.find_all(),
                key=lambda x: (x["xml"], x["pdf"]),
                reverse=True,
            ) == sorted(
                expected_files, key=lambda x: (x["xml"], x["pdf"]), reverse=True
            )

    def test_pull_from_sftp_and_reprocess(self, springer_empty_repo):
        with SpringerSFTPService() as sftp:
            migrate_from_ftp(
                sftp,
                springer_empty_repo,
                get_logger().bind(class_name="test_logger"),
                **{
                    "params": {
                        "force_pull": False,
                        "excluded_directories": [],
                        "filenames_pull": {
                            "enabled": True,
                            "filenames": ["JHEP/ftp_PUB_19-01-29_20-02-10_JHEP.zip"],
                            "force_from_ftp": True,
                        },
                    }
                },
            )
            excepted_files = [
                {
                    "xml": "extracted/JHEP/ftp_PUB_19-01-29_20-02-10_JHEP/JOU=13130/VOL=2019.2019/ISU=1/ART=9848/13130_2019_Article_9848.xml.scoap",
                    "pdf": "extracted/JHEP/ftp_PUB_19-01-29_20-02-10_JHEP/JOU=13130/VOL=2019.2019/ISU=1/ART=9848/BodyRef/PDF/13130_2019_Article_9848.pdf",
                }
            ]
            assert springer_empty_repo.find_all() == excepted_files

            reprocess_files(
                springer_empty_repo,
                get_logger().bind(class_name="test_logger"),
                **{
                    "params": {
                        "force_pull": False,
                        "excluded_directories": [],
                        "filenames_pull": {
                            "enabled": True,
                            "filenames": ["JHEP/ftp_PUB_19-01-29_20-02-10_JHEP.zip"],
                            "force_from_ftp": False,
                        },
                    }
                },
            )
            excepted_files = [
                {
                    "xml": "extracted/JHEP/ftp_PUB_19-01-29_20-02-10_JHEP/JOU=13130/VOL=2019.2019/ISU=1/ART=9848/13130_2019_Article_9848.xml.scoap",
                    "pdf": "extracted/JHEP/ftp_PUB_19-01-29_20-02-10_JHEP/JOU=13130/VOL=2019.2019/ISU=1/ART=9848/BodyRef/PDF/13130_2019_Article_9848.pdf",
                }
            ]
            assert springer_empty_repo.find_all() == excepted_files
