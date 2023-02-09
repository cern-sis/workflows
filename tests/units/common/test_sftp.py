from unittest.mock import MagicMock, patch

from common.sftp_service import DirectoryNotFoundException, SFTPService
from pysftp import Connection
from pytest import raises


def test_connect():
    def initiate_sftp_service():
        with SFTPService() as sftp:
            return sftp

    assert initiate_sftp_service() is not None


@patch.object(Connection, attribute="isdir", return_value=False)
def test_connect_should_crash(connection_mock: MagicMock, *args):
    def initiate_sftp_service():
        with SFTPService():
            pass

    raises(DirectoryNotFoundException, initiate_sftp_service)


def test_error_raise():
    with raises(Exception):
        with SFTPService():
            raise Exception
