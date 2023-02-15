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
        reprocess_specific_files = (
            "filenames_pull" in params
            and params["filenames_pull"]["enabled"]
            and params["filenames_pull"]["filenames"]
            and not params["filenames_pull"]["force_from_ftp"]
        )
        pull_force_all_files = (
            params["filenames_pull"]["enabled"]
            and params["filenames_pull"]["force_from_ftp"]
            and not params["filenames_pull"]["filenames"]
        )

        pull_force_specific_files = (
            params["filenames_pull"]["enabled"]
            and params["filenames_pull"]["force_from_ftp"]
            and params["filenames_pull"]["filenames"]
        )

        if reprocess_specific_files:
            specific_files_names = pull_ftp.reprocess_files(repo, logger, **kwargs)
            return specific_files_names

        if pull_force_specific_files:
            with sftp:
                specific_files_names_force = pull_ftp.pull_force_files_and_reprocess(
                    sftp, repo, logger, **kwargs
                )
                return specific_files_names_force

        if pull_force_all_files:
            root_dir = sftp.dir
            with sftp:
                base_folder_1 = os.getenv("SPRINGER_BASE_FOLDER_NAME_1", "EPJC")
                sftp.dir = os.path.join(root_dir, base_folder_1)
                all_files_names_1 = pull_ftp.pull_force_files_and_reprocess(
                    sftp, repo, logger, **kwargs
                )

                base_folder_2 = os.getenv("SPRINGER_BASE_FOLDER_NAME_2", "JHEP")
                sftp.dir = os.path.join(root_dir, base_folder_2)
                all_files_names_2 = pull_ftp.pull_force_files_and_reprocess(
                    sftp, repo, logger, **kwargs
                )
                return all_files_names_1 + all_files_names_2

        with sftp:
            root_dir = sftp.dir
            base_folder_1 = os.getenv("SPRINGER_BASE_FOLDER_NAME_1", "EPJC")
            sftp.dir = os.path.join(root_dir, base_folder_1)
            base_folder_1_files = pull_ftp.differential_pull(sftp, repo, logger)

            base_folder_2 = os.getenv("SPRINGER_BASE_FOLDER_NAME_2", "JHEP")
            sftp.dir = os.path.join(root_dir, base_folder_2)
            base_folder_2_files = pull_ftp.differential_pull(sftp, repo, logger)

            return base_folder_1_files + base_folder_2_files

    @task()
    def trigger_file_processing(repo=SpringerRepository(), filenames=None):
        return pull_ftp.trigger_file_processing(
            publisher="springer", repo=repo, logger=logger, filenames=filenames or []
        )

    filenames = migrate_from_ftp()
    trigger_file_processing(filenames=filenames)


dag_taskflow = springer_pull_ftp()
