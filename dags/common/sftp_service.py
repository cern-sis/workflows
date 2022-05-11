from io import BytesIO
from typing import List

import pysftp


class SFTPService:
    def __init__(
        self,
        host: str = "localhost",
        username: str = "airflow",
        password: str = "airflow",
        port: int = 2222,
        dir: str = "/upload",
    ):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.dir = dir

    def list_files(self) -> List[str]:
        with self.__connect() as sftp:
            return sftp.listdir()

    def get_file(self, file) -> BytesIO:
        with self.__connect() as sftp:
            with sftp.open(file, "rb") as fl:
                return BytesIO(fl.read())

    def __connect(self) -> pysftp.Connection:
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        conn = pysftp.Connection(
            host=self.host,
            username=self.username,
            password=self.password,
            port=self.port,
            cnopts=cnopts,
        )
        if not conn.isdir(self.dir):
            raise DirectoryNotFoundException(
                "Remote directory doesn't exist. Abort connection."
            )
        conn.chdir(self.dir)
        return conn


class DirectoryNotFoundException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
