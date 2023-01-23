import os

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
    def migrate_from_ftp(repo: IRepository = SpringerRepository(), **kwargs):
        base_folder_1 = os.getenv("SPRINGER_BASE_FOLDER_NAME_1", "EPJC")
        base_folder_2 = os.getenv("SPRINGER_BASE_FOLDER_NAME_2", "JHEP")
        sftp_1 = SpringerSFTPService(dir=f"upload/springer/{base_folder_1}")
        sftp_2 = SpringerSFTPService(dir=f"upload/springer/{base_folder_2}")
        files_from_folder_1 = pull_ftp.migrate_from_ftp(sftp_1, repo, logger, **kwargs)
        files_from_folder_2 = pull_ftp.migrate_from_ftp(sftp_2, repo, logger, **kwargs)
        return files_from_folder_1 + files_from_folder_2

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
