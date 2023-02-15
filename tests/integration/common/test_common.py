from common.pull_ftp import pull_force_files_and_reprocess, reprocess_files
from springer.repository import SpringerRepository
from springer.sftp_service import SpringerSFTPService
from structlog import get_logger


def test_force_pull_from_sftp():
    repo = SpringerRepository()
    repo.delete_all()
    with SpringerSFTPService() as sftp:
        pull_force_files_and_reprocess(
            sftp,
            repo,
            get_logger().bind(class_name="test_logger"),
            **{
                "params": {
                    "filenames_pull": {
                        "enabled": True,
                        "filenames": ["JHEP/ftp_PUB_19-01-29_20-02-10_JHEP.zip"],
                        "force_from_ftp": True,
                    }
                }
            }
        )
        assert len(repo.find_all()) == 1


def test_pull_from_sftp_and_reprocess():
    repo = SpringerRepository()
    repo.delete_all()
    with SpringerSFTPService() as sftp:
        pull_force_files_and_reprocess(
            sftp,
            repo,
            get_logger().bind(class_name="test_logger"),
            **{
                "params": {
                    "filenames_pull": {
                        "enabled": True,
                        "filenames": ["JHEP/ftp_PUB_19-01-29_20-02-10_JHEP.zip"],
                        "force_from_ftp": True,
                    }
                }
            }
        )
        assert len(repo.find_all()) == 1
        reprocess_files(
            repo,
            get_logger().bind(class_name="test_logger"),
            **{
                "params": {
                    "filenames_pull": {
                        "enabled": True,
                        "filenames": ["JHEP/ftp_PUB_19-01-29_20-02-10_JHEP.zip"],
                        "force_from_ftp": False,
                    }
                }
            }
        )
        assert len(repo.find_all()) == 1
