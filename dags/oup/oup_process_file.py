import airflow
from airflow.decorators import dag


@dag(schedule_interval=None, start_date=airflow.utils.dates.days_ago(0))
def oup_process_file():
    pass


dag_taskflow = oup_process_file()
