import airflow
from airflow.decorators import dag, task


@dag(start_date=airflow.utils.dates.days_ago(0))
def iop_process_file():
    @task()
    def start():
        pass


dag_for_iop_files_processing = iop_process_file()
