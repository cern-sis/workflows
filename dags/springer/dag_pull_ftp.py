import airflow
import common.pull_ftp as pull_ftp
from airflow.decorators import dag, task
from common.repository import IRepository
from common.sftp_service import SFTPService
from springer.repository import SpringerRepository
from springer.sftp_service import SpringerSFTPService


@dag(start_date=airflow.utils.dates.days_ago(0))
def springer_pull_ftp():
    @task()
    def migrate_from_ftp(
        sftp: SFTPService = SpringerSFTPService(),
        repo: IRepository = SpringerRepository(),
    ):
        pull_ftp.migrate_from_ftp(sftp, repo)

    @task()
    def trigger_file_processing(repo: IRepository = SpringerRepository()):
        return pull_ftp.trigger_file_processing("springer", repo)

    migrate_from_ftp() >> trigger_file_processing()


dag_taskflow = springer_pull_ftp()
