import os

from common.sftp_service import SFTPService


class SpringerSFTPService(SFTPService):
    def __init__(self):
        super().__init__(
            host=os.getenv("SPRINGER_FTP_HOST", "localhost"),
            username=os.getenv("SPRINGER_FTP_USERNAME", "airflow"),
            password=os.getenv("SPRINGER_FTP_PASSWORD", "airflow"),
            port=int(os.getenv("SPRINGER_FTP_PORT", "2222")),
            dir=os.getenv("SPRINGER_FTP_DIR", "upload/springer"),
        )
