from io import BytesIO
from unittest.mock import patch

import pytest
from springer.repository import SpringerRepository


class S3BucketResultObj:
    def __init__(self, key) -> None:
        self.key = key


S3_RETURNED_VALUES = [
    "file1.txt",
    "file1.scoap",
    "file1.pdf",
    "file2.txt",
    "file2.Meta",
    "file2.pdf",
]
FIND_ALL_EXPECTED_VALUES = [
    {"xml": "file1.scoap", "pdf": "file1.pdf"},
    {"xml": "file2.Meta", "pdf": "file2.pdf"},
]
FIND_ALL_EXTRACTED_FILES_EXPECTED_VALUES = [
    "file1.scoap",
    "file1.pdf",
    "file2.Meta",
    "file2.pdf",
]


@pytest.fixture
def boto3_fixture():
    with patch("scoap3.common.s3_service.boto3", autospec=True) as boto3_mock:
        boto3_mock.resource.return_value.Bucket.return_value.objects.filter.return_value.all.return_value = [
            S3BucketResultObj(file) for file in S3_RETURNED_VALUES
        ]
        yield boto3_mock


def test_find_all(boto3_fixture):
    repo = SpringerRepository()
    assert repo.find_all() == FIND_ALL_EXPECTED_VALUES


def test_find_all_extracted_files(boto3_fixture):
    repo = SpringerRepository()
    assert (
        repo._SpringerRepository__find_all_extracted_files()
        == FIND_ALL_EXTRACTED_FILES_EXPECTED_VALUES
    )


def test_save_zip_file(boto3_fixture):
    upload_mock = boto3_fixture.resource.return_value.Bucket.return_value.upload_fileobj
    file = BytesIO()
    filename = "test.zip"
    repo = SpringerRepository()
    repo.save(filename, file)
    upload_mock.assert_called_with(file, "raw/" + filename)


def test_save_file(boto3_fixture):
    upload_mock = boto3_fixture.resource.return_value.Bucket.return_value.upload_fileobj
    file = BytesIO()
    filename = "test.pdf"
    repo = SpringerRepository()
    repo.save(filename, file)
    upload_mock.assert_called_with(file, "extracted/" + filename)


def test_file_is_meta():
    repo = SpringerRepository()
    assert repo.is_meta("test.scoap")
    assert repo.is_meta("test.Meta")
    assert not repo.is_meta("test.test")
