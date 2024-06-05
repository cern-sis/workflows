import pendulum
from airflow.decorators import dag, task
from common.pull_ftp import migrate_from_ftp as migrate_from_ftp_common
from common.pull_ftp import reprocess_files
from elsevier.repository import ElsevierRepository
from elsevier.sftp_service import ElsevierSFTPService
from elsevier.trigger_file_processing import trigger_file_processing_elsevier
from structlog import get_logger


@dag(
    start_date=pendulum.today("UTC").add(days=-1),
    schedule="30 */3 * * *",
    params={
        "excluded_directories": [],
        "force_pull": False,
        "filenames_pull": {"enabled": False, "filenames": [], "force_from_ftp": False},
    },
)
def elsevier_pull_sftp():
    logger = get_logger().bind(class_name="elsevier_pull_sftp")

    @task()
    def migrate_from_ftp(
        sftp=ElsevierSFTPService(), repo=ElsevierRepository(), **kwargs
    ):
        params = kwargs["params"]
        specific_files = (
            "filenames_pull" in params
            and params["filenames_pull"]["enabled"]
            and not params["filenames_pull"]["force_from_ftp"]
        )
        if specific_files:
            specific_files_names = reprocess_files(repo, logger, **kwargs)
            return specific_files_names

        with sftp:
            return migrate_from_ftp_common(
                sftp, repo, logger, publisher="elsevier", **kwargs
            )

    @task()
    def trigger_file_processing(
        repo=ElsevierRepository(),
        filenames=None,
    ):
        return trigger_file_processing_elsevier(
            publisher="elsevier", repo=repo, logger=logger, filenames=filenames or []
        )

    archive_names = migrate_from_ftp()
    trigger_file_processing(filenames=archive_names)


dag_taskflow = elsevier_pull_sftp()
