from oup.sftp_service import OUPSFTPService
from pytest import fixture


@fixture
def sftp_service():
    return OUPSFTPService()


def test_iop_sftp_path(sftp_service):
    assert sftp_service.list_files()
