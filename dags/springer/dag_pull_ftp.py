import os

import airflow
import common.pull_ftp as pull_ftp
from airflow.decorators import dag, task
from springer.repository import SpringerRepository
from springer.sftp_service import SpringerSFTPService
from structlog import get_logger


@dag(
    start_date=airflow.utils.dates.days_ago(0),
    schedule_interval="30 */3 * * *",
    params={
        "force_pull": False,
        "filenames_pull": {"enabled": False, "filenames": [], "force_from_ftp": False},
    },
)
def springer_pull_ftp():
    logger = get_logger().bind(class_name="springer_pull_ftp")

    @task()
    def migrate_from_ftp(
        repo=SpringerRepository(), sftp=SpringerSFTPService(), **kwargs
    ):
        params = kwargs["params"]
        specific_files = (
            "filenames_pull" in params
            and params["filenames_pull"]["enabled"]
            and not params["filenames_pull"]["force_from_ftp"]
        )
        if specific_files:
            root_dir = sftp.dir
            specific_files_names = pull_ftp.reprocess_files(repo, logger, **kwargs)
            return specific_files_names

        with sftp:
            root_dir = sftp.dir
            base_folder_1 = os.getenv("SPRINGER_BASE_FOLDER_NAME_1", "EPJC")
            sftp.dir = os.path.join(root_dir, base_folder_1)
            base_folder_1_files = pull_ftp.migrate_from_ftp(
                sftp, repo, logger, **kwargs
            )

            base_folder_2 = os.getenv("SPRINGER_BASE_FOLDER_NAME_2", "JHEP")
            sftp.dir = os.path.join(root_dir, base_folder_2)
            base_folder_2_files = pull_ftp.migrate_from_ftp(
                sftp, repo, logger, **kwargs
            )

            return base_folder_1_files + base_folder_2_files

    @task()
    def trigger_file_processing(repo=SpringerRepository(), filenames=None):
        return pull_ftp.trigger_file_processing(
            publisher="springer", repo=repo, logger=logger, filenames=filenames or []
        )

    filenames = migrate_from_ftp()
    trigger_file_processing(filenames=filenames)


dag_taskflow = springer_pull_ftp()
