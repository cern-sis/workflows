import os
import pathlib
from io import open

import pytest
from common.sftp_service import SFTPService


@pytest.fixture
def client_fixture():
    return SFTPService(dir="upload/springer")


def test_list_files(client_fixture: SFTPService):
    data_files = os.listdir(pathlib.Path().resolve().__str__() + "/data/springer")
    assert len(client_fixture.list_files()) == len(data_files)


def test_get_file(client_fixture: SFTPService):
    data_path = pathlib.Path().resolve().__str__() + "/data/springer"
    data_files = os.listdir(data_path)
    print(data_files)
    filename = data_files[0]
    with open(data_path + "/" + data_files[0], "rb") as file:
        assert file.read() == client_fixture.get_file(filename).read()
