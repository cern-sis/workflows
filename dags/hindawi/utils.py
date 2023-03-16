from datetime import date, datetime
from io import BytesIO
from xml.etree import ElementTree

from airflow.api.common import trigger_dag


def save_file_in_s3(data, repo):
    if not data:
        return None
    date_today = date.today().strftime("%Y-%m-%d")
    prefix = datetime.now().strftime("%Y-%m-%dT%H:%M")
    key = f"{date_today}/{prefix}.xml"
    byte_file = BytesIO(data)
    repo.save(key, byte_file)
    return key


def split_xmls(repo, key):
    ids_and_records = []
    file = repo.get_by_id(key)
    xml_string = file.getvalue().decode("utf-8")
    for tag in ElementTree.fromstring(xml_string):
        if "ListRecords" in tag.tag or "GetRecord" in tag.tag:
            for record in tag:
                if "record" not in record.tag:
                    continue
                ids_and_records.append(
                    ElementTree.tostring(record).decode("utf-8"),
                )

    return ids_and_records


def trigger_file_processing_DAG(records):
    if not records:
        return
    for record in records:
        trigger_dag.trigger_dag(
            dag_id="hindawi_file_processing",
            conf={"record": record},
            replace_microseconds=False,
        )
    return records
