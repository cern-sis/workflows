import os

from common.sftp_service import SFTPService


class IOPSFTPService(SFTPService):
    def __init__(self):
        super().__init__(
            host=os.getenv("IOP_FTP_HOST", "localhost"),
            username=os.getenv("IOP_FTP_USERNAME", "airflow"),
            password=os.getenv("IOP_FTP_PASSWORD", "airflow"),
            port=int(os.getenv("IOP_FTP_PORT", "2222")),
            dir=os.getenv("IOP_FTP_DIR", "upload/iop"),
        )
