import io
from typing import List
from unittest.mock import MagicMock, Mock, patch

import pytest
from common.pull_ftp import migrate_from_ftp, trigger_file_processing
from common.repository import IRepository
from common.sftp_service import SFTPService

SFTP_LIST_FILES_RETURN_VALUE: List[str] = ["file1", "file2"]
REPO_FIND_ALL_RETURN_VALUE: List[dict] = [
    {"xml": f, "pdf": f} for f in SFTP_LIST_FILES_RETURN_VALUE
]


@pytest.fixture
def zip_fixture():
    with patch("zipfile.ZipFile", autospec=True) as zip_patch:
        mock_ziparchive = Mock()
        mock_ziparchive.return_value.namelist.return_value = (
            SFTP_LIST_FILES_RETURN_VALUE
        )
        mock_ziparchive.return_value.read.return_value = io.BytesIO().read()
        zip_patch.return_value.__enter__ = mock_ziparchive
        yield zip_patch


@patch.object(SFTPService, attribute="__init__", return_value=None)
@patch.object(SFTPService, attribute="get_file", return_value=io.BytesIO())
@patch.object(
    SFTPService, attribute="list_files", return_value=SFTP_LIST_FILES_RETURN_VALUE
)
@patch.object(IRepository, attribute="save")
def test_migrate_from_ftp(
    repo_save: MagicMock, sftp_list_files, sftp_get_file, sftp_init, zip_fixture
):
    sftp = SFTPService()
    repo = IRepository()
    migrate_from_ftp(sftp, repo)
    assert repo_save.call_count == len(SFTP_LIST_FILES_RETURN_VALUE) + pow(
        len(SFTP_LIST_FILES_RETURN_VALUE), 2
    )


@patch("common.pull_ftp.trigger_dag.trigger_dag")
@patch.object(IRepository, attribute="find_by_id", return_value=io.BytesIO())
@patch.object(
    IRepository, attribute="find_all", return_value=REPO_FIND_ALL_RETURN_VALUE
)
def test_trigger_file_processing(*args):
    repo = IRepository()
    files = trigger_file_processing("test", repo)
    assert files == REPO_FIND_ALL_RETURN_VALUE
