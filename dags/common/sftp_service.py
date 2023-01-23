import os
from io import BytesIO

import pysftp


class SFTPService:
    def __init__(
        self,
        host="localhost",
        username="airflow",
        password="airflow",
        port=2222,
        dir="/upload",
    ):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.dir = dir

    def list_files(self):
        with self.__connect() as sftp:
            paths = [path for path in self.dir.split(",")]
            print(paths)
            files = []
            for path in paths:
                files = files + sftp.listdir(path)
            return files

    def get_file(self, file):
        with self.__connect() as sftp:
            with sftp.open(os.path.join(self.dir, file), "rb") as fl:
                return BytesIO(fl.read())

    def __connect(self):
        if self.host == "localhost":
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
        else:
            cnopts = pysftp.CnOpts(knownhosts="known_hosts")
        conn = pysftp.Connection(
            host=self.host,
            username=self.username,
            password=self.password,
            port=self.port,
            cnopts=cnopts,
        )
        paths = [path for path in self.dir.split(",")]
        for path in paths:
            if not conn.isdir(path):
                raise DirectoryNotFoundException(
                    "Remote directory doesn't exist. Abort connection."
                )
        return conn


class DirectoryNotFoundException(Exception):
    def __init__(self, *args):
        super().__init__(*args)
