import zipfile
from io import BytesIO
from typing import List
from unittest.mock import MagicMock, Mock, patch

import pytest
from common.pull_ftp import (
    differential_pull,
    pull_force_files_and_reprocess,
    reprocess_files,
    trigger_file_processing,
)
from common.repository import IRepository
from common.sftp_service import SFTPService
from structlog import get_logger

SFTP_LIST_FILES_RETURN_VALUE: List[str] = [
    "file1.zip",
    "file2.zip",
]

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
        mock_ziparchive.return_value.read.return_value = BytesIO().read()
        zip_patch.return_value.__enter__ = mock_ziparchive
        yield zip_patch


@pytest.fixture
def ftp_get_file_fixture():
    with patch.object(SFTPService, attribute="get_file") as patched:
        patched: MagicMock = patched
        mem_zip = BytesIO()
        with zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("test.data", b"test")
        patched.side_effect = lambda x: mem_zip if ".zip" in x else BytesIO()
        yield patched


@patch.object(
    SFTPService, attribute="list_files", return_value=SFTP_LIST_FILES_RETURN_VALUE
)
@patch.object(IRepository, attribute="is_meta")
@patch.object(IRepository, attribute="get_all_raw_filenames")
@patch.object(IRepository, attribute="save")
def test_migrate_from_ftp(
    repo_save: MagicMock,
    repo_get_all,
    repo_is_meta,
    sftp_list_files,
    ftp_get_file_fixture,
    zip_fixture,
):
    with SFTPService() as sftp:
        repo = IRepository()
        differential_pull(sftp, repo, get_logger().bind(class_name="test_logger"))
        assert repo_save.call_count == len(SFTP_LIST_FILES_RETURN_VALUE) + pow(
            len(SFTP_LIST_FILES_RETURN_VALUE), 2
        )


@patch.object(
    SFTPService, attribute="list_files", return_value=SFTP_LIST_FILES_RETURN_VALUE
)
@patch.object(IRepository, attribute="is_meta")
@patch.object(IRepository, attribute="get_all_raw_filenames")
@patch.object(IRepository, attribute="save")
def test_migrate_from_ftp_only_one_file(
    repo_save: MagicMock,
    repo_get_all: MagicMock,
    repo_is_meta,
    sftp_list_files,
    ftp_get_file_fixture,
    zip_fixture,
):
    repo_get_all.return_value = SFTP_LIST_FILES_RETURN_VALUE[0:-1]
    with SFTPService() as sftp:
        repo = IRepository()
        differential_pull(sftp, repo, get_logger().bind(class_name="test_logger"))
        assert repo_save.call_count == len(SFTP_LIST_FILES_RETURN_VALUE[0:-1]) + pow(
            2, len(SFTP_LIST_FILES_RETURN_VALUE[0:-1])
        )


@patch.object(
    SFTPService, attribute="list_files", return_value=SFTP_LIST_FILES_RETURN_VALUE
)
@patch.object(IRepository, attribute="is_meta")
@patch.object(IRepository, attribute="get_all_raw_filenames")
@patch.object(IRepository, attribute="save")
def test_migrate_from_ftp_force_flag(
    repo_save: MagicMock,
    repo_get_all: MagicMock,
    repo_is_meta,
    sftp_list_files,
    ftp_get_file_fixture,
    zip_fixture,
):
    repo_get_all.return_value = SFTP_LIST_FILES_RETURN_VALUE
    with SFTPService() as sftp:
        repo = IRepository()
        pull_force_files_and_reprocess(
            sftp,
            repo,
            get_logger().bind(class_name="test_logger"),
            **{
                "params": {
                    "filenames_pull": {
                        "enabled": True,
                        "filenames": [],
                        "force_from_ftp": True,
                    }
                }
            }
        )
        assert repo_save.call_count == len(SFTP_LIST_FILES_RETURN_VALUE) + pow(
            len(SFTP_LIST_FILES_RETURN_VALUE), 2
        )


@patch.object(
    SFTPService, attribute="list_files", return_value=SFTP_LIST_FILES_RETURN_VALUE
)
@patch.object(IRepository, attribute="is_meta")
@patch.object(IRepository, attribute="get_all_raw_filenames")
@patch.object(IRepository, attribute="save")
def test_migrate_from_ftp_specified_file_force_from_ftp(
    repo_save: MagicMock,
    repo_get_all: MagicMock,
    repo_is_meta,
    sftp_list_files,
    ftp_get_file_fixture,
    zip_fixture,
):
    repo_get_all.return_value = SFTP_LIST_FILES_RETURN_VALUE[0:-1]
    with SFTPService() as sftp:
        repo = IRepository()
        pull_force_files_and_reprocess(
            sftp,
            repo,
            get_logger().bind(class_name="test_logger"),
            **{
                "params": {
                    "filenames_pull": {
                        "enabled": True,
                        "filenames": ["file1.zip"],
                        "force_from_ftp": True,
                    }
                }
            }
        )
        assert repo_save.call_count == len(SFTP_LIST_FILES_RETURN_VALUE[0:-1]) + pow(
            2, len(SFTP_LIST_FILES_RETURN_VALUE[0:-1])
        )


@patch.object(SFTPService, attribute="__init__", return_value=None)
@patch.object(
    SFTPService, attribute="list_files", return_value=SFTP_LIST_FILES_RETURN_VALUE
)
@patch.object(IRepository, attribute="find_by_id")
@patch.object(IRepository, attribute="is_meta")
@patch.object(IRepository, attribute="get_all_raw_filenames")
@patch.object(IRepository, attribute="save")
def test_migrate_from_ftp_specified_file(
    repo_save: MagicMock,
    repo_get_all: MagicMock,
    repo_is_meta: MagicMock,
    repo_find_by_id: MagicMock,
    sftp_list_files,
    ftp_init,
    ftp_get_file_fixture,
    zip_fixture,
):
    repo_get_all.return_value = SFTP_LIST_FILES_RETURN_VALUE[0:-1]
    repo = IRepository()
    reprocess_files(
        repo,
        get_logger().bind(class_name="test_logger"),
        **{
            "params": {
                "filenames_pull": {
                    "enabled": True,
                    "filenames": ["file1.zip"],
                    "force_from_ftp": False,
                }
            }
        }
    )
    assert repo_save.call_count == 0
    assert repo_find_by_id.call_count == 1
    assert repo_is_meta.call_count == 2


@patch("common.pull_ftp.trigger_dag.trigger_dag")
@patch.object(IRepository, attribute="find_by_id", return_value=BytesIO())
@patch.object(
    IRepository, attribute="find_all", return_value=REPO_FIND_ALL_RETURN_VALUE
)
def test_trigger_file_processing(*args):
    repo = IRepository()
    files = trigger_file_processing(
        "test", repo, get_logger().bind(class_name="test_logger")
    )
    assert files == SFTP_LIST_FILES_RETURN_VALUE
