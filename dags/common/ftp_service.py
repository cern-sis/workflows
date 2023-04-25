import ftplib
import io
import os
import re
import traceback

from common.exceptions import DirectoryNotFoundException, NotConnectedException
from common.utils import append_file_if_not_in_excluded_directory, walk_ftp
from structlog import get_logger


class FTPService:
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
        ftp = ftplib.FTP(self.host)
        ftp.login(self.username, self.password)
        try:
            ftp.dir(self.dir)
        except FileNotFoundError:
            raise DirectoryNotFoundException(
                "Remote directory doesn't exist. Abort connection."
            )
        return ftp

    def __enter__(self):
        self.connection = self.__connect()
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if self.connection:
            self.connection.close()
        if exc_type is not None:
            formed_exception = traceback.format_exception_only(exc_type, exc_value)
            self.logger.error(
                "An error occurred while exiting FTPService",
                execption=formed_exception,
            )
            return False
        return True

    def list_files(self, excluded_directories=None):
        try:
            file_names = []
            filtered_files = []
            walk_ftp(ftp=self.connection, remotedir=self.dir, paths=file_names)
            for file_name in file_names:
                append_file_if_not_in_excluded_directory(
                    re.sub(self.dir + "/", "", file_name),
                    excluded_directories,
                    filtered_files,
                )
            return filtered_files
        except AttributeError:
            raise NotConnectedException

    def get_file(self, file):
        try:
            file_contents = io.BytesIO()
            self.connection.retrbinary(
                f"RETR {os.path.join(self.dir, file)}", file_contents.write
            )
            return file_contents
        except AttributeError:
            raise NotConnectedException
