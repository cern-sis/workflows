import json
import logging
import os

import airflow
from airflow.decorators import dag, task
from aps.aps_api_client import APSApiClient
from aps.aps_params import APSParams
from aps.repository import APSRepository
from aps.utils import save_file_in_s3, set_APS_harvesting_interval, split_json
from aps.utils import trigger_file_processing as trigger_file_processing_
from common.repository import IRepository


@dag(start_date=airflow.utils.dates.days_ago(0))
def aps_fetch_api():
    @task()
    def set_fetching_intervals(repo: IRepository = APSRepository()):
        return set_APS_harvesting_interval(repo=repo)

    @task()
    def save_json_in_s3(dates: dict, repo: IRepository = APSRepository()):
        parameters = APSParams(
            from_date=dates["aps_fetching_from_date"],
            until_date=dates["aps_fetching_until_date"],
        ).get_params()
        rest_api = APSApiClient(
            base_url=os.getenv("APS_BASE_URL", "http://harvest.aps.org")
        )
        articles_metadata = str.encode(
            json.dumps(rest_api.get_articles_metadata(parameters))
        )
        return save_file_in_s3(data=articles_metadata, repo=repo)

    @task()
    def trigger_file_processing(key, repo: IRepository = APSRepository()):
        if key is None:
            logging.warning("No new files were downloaded to s3")
            return
        ids_and_articles = split_json(repo, key)
        trigger_file_processing_(ids_and_articles)

    intervals = set_fetching_intervals()
    key = save_json_in_s3(intervals)
    trigger_file_processing(key)


APS_download_files_dag = aps_fetch_api()
