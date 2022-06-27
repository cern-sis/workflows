import json
from datetime import date, datetime
from io import BytesIO

from airflow.api.common import trigger_dag


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


def trigger_file_processing_DAG(ids_and_articles):
    for data in ids_and_articles:
        trigger_dag.trigger_dag(
            dag_id="aps_process_file",
            run_id=data["id"],
            conf={"article": json.dumps(data["article"])},
            replace_microseconds=False,
        )
    return data
