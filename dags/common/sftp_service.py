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
            return sftp.listdir()

    def get_file(self, file):
        with self.__connect() as sftp:
            with sftp.open(file, "rb") as fl:
                return BytesIO(fl.read())

    def __connect(self):
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
    def __init__(self, *args):
        super().__init__(*args)
