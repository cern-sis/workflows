from iop.sftp_service import IOPSFTPService
from pytest import fixture


@fixture
def sftp_service():
    return IOPSFTPService()


def test_iop_sftp_path(sftp_service):
    assert sftp_service.list_files()
