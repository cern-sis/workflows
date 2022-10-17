import airflow
import common.pull_ftp as pull_ftp
from airflow.decorators import dag, task
from common.repository import IRepository
from common.sftp_service import SFTPService
from iop.repository import IOPRepository
from iop.sftp_service import IOPSFTPService
from structlog import get_logger


@dag(
    start_date=airflow.utils.dates.days_ago(0),
    params={
        "force_pull": False,
        "filenames_pull": {"enabled": False, "filenames": [], "force_from_ftp": False},
    },
)
def iop_pull_ftp():
    logger = get_logger().bind(class_name="iop_pull_ftp")

    @task()
    def migrate_from_ftp(
        sftp: SFTPService = IOPSFTPService(),
        repo: IRepository = IOPRepository(),
        **kwargs
    ):
        return pull_ftp.migrate_from_ftp(sftp, repo, logger, **kwargs)

    @task()
    def trigger_file_processing(filenames=None, repo: IRepository = IOPRepository()):
        return pull_ftp.trigger_file_processing("iop", repo, logger, filenames or [])

    filenames = migrate_from_ftp()
    trigger_file_processing(filenames)


dag_taskflow = iop_pull_ftp()
