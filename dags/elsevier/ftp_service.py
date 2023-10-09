import os

from common.ftp_service import FTPService


class ElsevierFTPService(FTPService):
    def __init__(self):
        super().__init__(
            host=os.getenv("ELSEVIER_FTP_HOST", "localhost"),
            username=os.getenv("ELSEVIER_FTP_USERNAME", "airflow"),
            password=os.getenv("ELSEVIER_FTP_PASSWORD", "airflow"),
            port=int(os.getenv("ELSEVIER_FTP_PORT", 21)),
            dir=os.getenv("ELSEVIER_FTP_DIR", "upload/elsevier"),
        )
