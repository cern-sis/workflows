import json
from datetime import date, datetime
from io import BytesIO

from airflow.api.common import trigger_dag
from airflow.models import Variable


def set_APS_harvesting_interval(repo):
    today = date.today()
    aps_fetching_from_date = repo.find_the_last_uploaded_file_date()
    aps_fetching_until_date = today.strftime("%Y-%m-%d")
    Variable.set(
        "aps_fetching_from_date", aps_fetching_from_date or aps_fetching_until_date
    )
    Variable.set("aps_fetching_until_date", aps_fetching_until_date)
    return {
        "aps_fetching_from_date": Variable.get("aps_fetching_from_date"),
        "aps_fetching_until_date": Variable.get("aps_fetching_until_date"),
    }


def save_file_in_s3(data, repo):
    if bool(data):
        date_today = date.today().strftime("%Y-%m-%d")
        prefix = datetime.now().strftime("%Y-%m-%dT%H:%M")

        byte_file = BytesIO(data)
        key = f"{date_today}/{prefix}.json"
        repo.save(key, byte_file)
        return key


def split_json(repo, key):
    file = repo.find_by_id(key)
    data = json.loads(file.getvalue().decode("utf-8"))["data"]
    ids_and_articles = []
    for article in data:
        doi = article["identifiers"]["doi"]
        today = datetime.now().strftime("%Y-%m-%dT%H:%M")
        id = f"APS_{doi}_{today}"
        ids_and_articles.append({"id": id, "article": article})
    return ids_and_articles


def trigger_file_processing(ids_and_articles):
    for data in ids_and_articles:
        trigger_dag.trigger_dag(
            dag_id="aps_process_file",
            run_id=data["id"],
            conf=json.dumps(data["article"]),
            replace_microseconds=False,
        )
    return ids_and_articles
