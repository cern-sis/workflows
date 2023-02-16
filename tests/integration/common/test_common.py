from common.pull_ftp import pull_force_files_and_reprocess, reprocess_files
from pytest import fixture
from springer.repository import SpringerRepository
from springer.sftp_service import SpringerSFTPService
from structlog import get_logger


@fixture
def springer_empty_repo():
    repo = SpringerRepository()
    repo.delete_all()
    yield repo


def test_force_pull_from_sftp(springer_empty_repo):
    with SpringerSFTPService() as sftp:
        pull_force_files_and_reprocess(
            sftp,
            springer_empty_repo,
            get_logger().bind(class_name="test_logger"),
            **{
                "params": {
                    "excluded_dirs": [],
                    "filenames_pull": {
                        "enabled": True,
                        "filenames": [
                            "JHEP/ftp_PUB_19-01-29_20-02-10_JHEP.zip",
                            "EPJC/ftp_PUB_19-02-06_16-01-13_EPJC_stripped.zip",
                        ],
                        "force_from_ftp": True,
                    },
                }
            }
        )
        assert len(springer_empty_repo.find_all()) == 2


def test_force_pull_from_sftp_with_excluded_folder(springer_empty_repo):
    with SpringerSFTPService() as sftp:
        pull_force_files_and_reprocess(
            sftp,
            springer_empty_repo,
            get_logger().bind(class_name="test_logger"),
            **{
                "params": {
                    "excluded_dirs": ["EPJC"],
                    "filenames_pull": {
                        "enabled": True,
                        "filenames": [
                            "JHEP/ftp_PUB_19-01-29_20-02-10_JHEP.zip",
                            "EPJC/ftp_PUB_19-02-06_16-01-13_EPJC_stripped.zip",
                        ],
                        "force_from_ftp": True,
                    },
                }
            }
        )
        assert len(springer_empty_repo.find_all()) == 1


def test_pull_from_sftp_and_reprocess(springer_empty_repo):
    with SpringerSFTPService() as sftp:
        pull_force_files_and_reprocess(
            sftp,
            springer_empty_repo,
            get_logger().bind(class_name="test_logger"),
            **{
                "params": {
                    "excluded_dirs": [],
                    "filenames_pull": {
                        "enabled": True,
                        "filenames": ["JHEP/ftp_PUB_19-01-29_20-02-10_JHEP.zip"],
                        "force_from_ftp": True,
                    },
                }
            }
        )
        assert len(springer_empty_repo.find_all()) == 1
        reprocess_files(
            springer_empty_repo,
            get_logger().bind(class_name="test_logger"),
            **{
                "params": {
                    "excluded_dirs": [],
                    "filenames_pull": {
                        "enabled": True,
                        "filenames": ["JHEP/ftp_PUB_19-01-29_20-02-10_JHEP.zip"],
                        "force_from_ftp": False,
                    },
                }
            }
        )
        assert len(springer_empty_repo.find_all()) == 1
