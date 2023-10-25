import os

from common.sftp_service import SFTPService


class ElsevierSFTPService(SFTPService):
    def __init__(self):
        super().__init__(
            host=os.getenv("ELSEVIER_FTP_HOST", "localhost"),
            username=os.getenv("ELSEVIER_FTP_USERNAME", "airflow"),
            password=os.getenv("ELSEVIER_FTP_PASSWORD", "airflow"),
            port=int(os.getenv("ELSEVIER_FTP_PORT", "2222")),
            dir=os.getenv("ELSEVIER_FTP_DIR", "upload/elsevier"),
        )
