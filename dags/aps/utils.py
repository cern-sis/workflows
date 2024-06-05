import json
from datetime import date, datetime
from io import BytesIO

from airflow.api.common import trigger_dag
from common.pull_ftp import _generate_id


def save_file_in_s3(data, repo):
    if not bool(data):
        return
    date_today = date.today().strftime("%Y-%m-%d")
    prefix = datetime.now().strftime("%Y-%m-%dT%H:%M")

    byte_file = BytesIO(data)
    key = f"{date_today}/{prefix}.json"
    repo.save(key, byte_file)
    return key


def split_json(repo, key):
    _file = repo.get_by_id(key)
    data = json.loads(_file.getvalue().decode("utf-8"))["data"]
    ids_and_articles = []
    for article in data:
        _id = _generate_id("APS")
        ids_and_articles.append({"id": _id, "article": article})
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
