import logging
import os

import airflow
from airflow.decorators import dag, task
from common.repository import IRepository
from common.utils import set_harvesting_interval
from hindawi.hindawi_api_client import HindawiApiClient
from hindawi.hindawi_params import HindawiParams
from hindawi.repository import HindawiRepository
from hindawi.utils import save_file_in_s3, split_xmls, trigger_file_processing_DAG


@dag(start_date=airflow.utils.dates.days_ago(0))
def hindawi_fetch_api():
    @task()
    def set_fetching_intervals(repo: IRepository = HindawiRepository(), **kwargs):
        return set_harvesting_interval(repo=repo, **kwargs)

    @task()
    def save_xml_in_s3(dates: dict, repo: IRepository = HindawiRepository()):
        parameters = HindawiParams(
            from_date=dates["start_date"],
            until_date=dates["until_date"],
        ).get_params()
        rest_api = HindawiApiClient(
            base_url=os.getenv("HINDAWI_API_BASE_URL", "https://www.hindawi.com")
        )
        articles_metadata = rest_api.get_articles_metadata(parameters)
        if not articles_metadata:
            logging.warning("No new data is uploaded to s3")
            return
        return save_file_in_s3(data=articles_metadata, repo=repo)

    @task()
    def trigger_files_processing(key, repo: IRepository = HindawiRepository()):
        if not key:
            logging.warning("No new files were downloaded to s3")
            return
        records = split_xmls(repo, key)
        return trigger_file_processing_DAG(records)

    intervals = set_fetching_intervals()
    key = save_xml_in_s3(intervals)
    trigger_files_processing(key)


hindawi_download_files_dag = hindawi_fetch_api()