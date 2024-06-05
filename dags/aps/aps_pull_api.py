import json
import logging
import os

import pendulum
from airflow.decorators import dag, task
from aps.aps_api_client import APSApiClient
from aps.aps_params import APSParams
from aps.repository import APSRepository
from aps.utils import save_file_in_s3, split_json, trigger_file_processing_DAG
from common.utils import set_harvesting_interval


@dag(
    start_date=pendulum.today("UTC").add(days=-1),
    schedule="30 */2 * * *",
    params={"from_date": None, "until_date": None, "per_page": None},
)
def scoap3_aps_pull_api():
    @task()
    def set_fetching_intervals(repo=APSRepository(), **kwargs):
        return set_harvesting_interval(repo=repo, **kwargs)

    @task()
    def save_json_in_s3(dates: dict, repo=APSRepository(), **kwargs):
        parameters = APSParams(
            from_date=dates["from_date"],
            until_date=dates["until_date"],
            per_page=kwargs.get("per_page", None),
        ).get_params()
        rest_api = APSApiClient(
            base_url=os.getenv("APS_API_BASE_URL", "http://harvest.aps.org")
        )
        articles_metadata = rest_api.get_articles_metadata(parameters)
        if articles_metadata is not None:
            articles_metadata = json.dumps(
                rest_api.get_articles_metadata(parameters)
            ).encode()
            return save_file_in_s3(data=articles_metadata, repo=repo)
        return None

    @task()
    def trigger_files_processing(key, repo=APSRepository()):
        if key is None:
            logging.warning("No new files were downloaded to s3")
            return
        ids_and_articles = split_json(repo, key)
        return trigger_file_processing_DAG(ids_and_articles)

    intervals = set_fetching_intervals()
    key = save_json_in_s3(intervals)
    trigger_files_processing(key)


APS_download_files_dag = scoap3_aps_pull_api()
