import io
import os
import re

from airflow.contrib.hooks.ftp_hook import FTPHook
from common.exceptions import NotConnectedException
from common.utils import append_not_excluded_files, walk_ftp
from structlog import get_logger


class FTPService(FTPHook):
    def __init__(self):
        super().__init__()
        self.logger = get_logger().bind(class_name=type(self).__name__)

    def get_file(self, _file):
        file_contents = io.BytesIO()
        file_path = os.path.join(self.dir, _file)
        self.retrieve_file(
            remote_full_path=file_path, local_full_path_or_buffer=file_contents
        )
        return file_contents

    def list_files(self, excluded_directories=[]):
        try:
            file_names = []
            filtered_files = []
            walk_ftp(self, remotedir=self.dir, paths=file_names)
            for file_name in file_names:
                append_not_excluded_files(
                    re.sub(self.dir + "/", "", file_name),
                    excluded_directories,
                    filtered_files,
                )
            return filtered_files
        except AttributeError:
            raise NotConnectedException
