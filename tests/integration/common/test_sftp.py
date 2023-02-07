import os
import pathlib
from io import open

from common.sftp_service import SFTPService


def test_list_files():
    with SFTPService(dir="upload/springer/JHEP") as sftp:
        data_files = os.listdir(
            pathlib.Path().resolve().__str__() + "/data/springer/JHEP"
        )
        assert len(sftp.list_files()) == len(data_files)


def test_get_file():
    data_path = pathlib.Path().resolve().__str__() + "/data/springer/JHEP"
    data_files = os.listdir(data_path)
    filename = data_files[0]
    with open(data_path + "/" + data_files[0], "rb") as file:
        with SFTPService(dir="upload/springer/JHEP") as sftp:
            assert file.read() == sftp.get_file(filename).read()
