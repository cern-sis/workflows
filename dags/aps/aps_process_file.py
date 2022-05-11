import airflow
from airflow.decorators import dag, task


@dag(start_date=airflow.utils.dates.days_ago(0))
def aps_process_file():
    @task()
    def start():
        return None

    @task()
    def done():
        return None

    start() >> done()


aps_process_file_ = aps_process_file()
