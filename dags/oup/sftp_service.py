import os

from common.sftp_service import SFTPService


class OUPSFTPService(SFTPService):
    def __init__(self):
        super().__init__(
            host=os.getenv("OUP_FTP_HOST", "localhost"),
            username=os.getenv("OUP_FTP_USERNAME", "airflow"),
            password=os.getenv("OUP_FTP_PASSWORD", "airflow"),
            port=int(os.getenv("OUP_FTP_PORT", "2222")),
            dir=os.getenv("OUP_FTP_DIR", "upload/oup"),
        )
