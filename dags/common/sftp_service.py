import os
import traceback
from io import BytesIO

import pysftp
from structlog import get_logger


class SFTPService:
    def __init__(
        self,
        host="localhost",
        username="airflow",
        password="airflow",
        port=2222,
        dir="/upload",
    ):
        self.connection = None
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.logger = get_logger().bind(class_name=type(self).__name__)
        self.dir = dir

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
        return conn

    def __enter__(self):
        self.connection = self.__connect()
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if self.connection:
            self.connection.close()
        if exc_type is not None:
            formed_exception = traceback.format_exception_only(exc_type, exc_value)
            self.logger.error(
                "An error occurred while exiting SFTPService",
                execption=formed_exception,
            )
        return True

    def list_files(self):
        try:
            return self.connection.listdir(self.dir)
        except AttributeError:
            raise NotConnectedException

    def get_file(self, file):
        try:
            file_ = self.connection.open(os.path.join(self.dir, file), "rb")
            return BytesIO(file_.read())
        except AttributeError:
            raise NotConnectedException


class DirectoryNotFoundException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class NotConnectedException(Exception):
    def __init__(self):
        super().__init__("SFTP connection not established")
