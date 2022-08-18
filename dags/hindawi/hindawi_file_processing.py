import airflow
from airflow.decorators import dag, task


@dag(start_date=airflow.utils.dates.days_ago(0))
def hindawi_file_processing():
    @task()
    def parse(**kwargs):
        return kwargs.get("params")


Hindawi_file_processing = hindawi_file_processing()
