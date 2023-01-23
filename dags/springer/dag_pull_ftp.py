import airflow
import common.pull_ftp as pull_ftp
from airflow.decorators import dag, task
from common.repository import IRepository
from springer.repository import SpringerRepository
from springer.sftp_service import SpringerSFTPService
from structlog import get_logger


@dag(
    start_date=airflow.utils.dates.days_ago(0),
    schedule_interval="@hourly",
    params={
        "force_pull": False,
        "filenames_pull": {"enabled": False, "filenames": [], "force_from_ftp": False},
    },
)
def springer_pull_ftp():
    logger = get_logger().bind(class_name="springer_pull_ftp")

    @task()
    def migrate_from_ftp(
        repo: IRepository = SpringerRepository(), sftp=SpringerSFTPService(), **kwargs
    ):
        return pull_ftp.migrate_from_ftp(sftp, repo, logger, **kwargs)

    @task()
    def trigger_file_processing(
        filenames=None, repo: IRepository = SpringerRepository()
    ):
        return pull_ftp.trigger_file_processing(
            "springer", repo, logger, filenames or []
        )

    filenames = migrate_from_ftp()
    trigger_file_processing(filenames)


dag_taskflow = springer_pull_ftp()
