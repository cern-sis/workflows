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
            with sftp:
                return pull_ftp.pull_force_files_and_reprocess(
                    sftp, repo, logger, **kwargs
                )

        with sftp:
            return pull_ftp.differential_pull(sftp, repo, logger)

    @task()
    def trigger_file_processing(repo=SpringerRepository(), filenames=None):
        return pull_ftp.trigger_file_processing(
            publisher="springer", repo=repo, logger=logger, filenames=filenames or []
        )

    filenames = migrate_from_ftp()
    trigger_file_processing(filenames=filenames)


dag_taskflow = springer_pull_ftp()
