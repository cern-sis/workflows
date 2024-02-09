import common.pull_ftp as pull_ftp
import pendulum
from airflow.decorators import dag, task
from common.ftp_service import FTPService
from common.repository import IRepository
from oup.ftp_service import OUPFTPService
from oup.repository import OUPRepository
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
def oup_pull_ftp():
    logger = get_logger().bind(class_name="oup_pull_ftp")

    @task()
    def migrate_from_ftp(
        ftp: FTPService = OUPFTPService(), repo: IRepository = OUPRepository(), **kwargs
    ):
        params = kwargs["params"]
        specific_files = (
            "filenames_pull" in params
            and params["filenames_pull"]["enabled"]
            and not params["filenames_pull"]["force_from_ftp"]
        )
        if specific_files:
            specific_files_names = pull_ftp.reprocess_files(repo, logger, **kwargs)
            return specific_files_names

        with ftp:
            return pull_ftp.migrate_from_ftp(ftp, repo, logger, **kwargs)

    @task()
    def trigger_file_processing(
        repo: IRepository = OUPRepository(),
        filenames=None,
    ):
        return pull_ftp.trigger_file_processing(
            publisher="oup", repo=repo, logger=logger, filenames=filenames or []
        )

    filenames = migrate_from_ftp()
    trigger_file_processing(filenames=filenames)


dag_taskflow = oup_pull_ftp()
