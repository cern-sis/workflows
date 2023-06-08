import os

from common.ftp_service import FTPService


class OUPFTPService(FTPService):
    def __init__(self):
        super().__init__()
        self.ftp_conn_id = "oup_ftp_service"
        self.dir = os.getenv("OUP_FTP_DIR", "/upload/oup")
