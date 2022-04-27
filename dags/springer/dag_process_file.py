import base64
import xml.etree.ElementTree as ET

import airflow
from airflow.decorators import dag, task
from springer.parser import SpringerParser


def springer_parse_file(**kwargs):
    if "params" in kwargs and "file" in kwargs["params"]:
        encoded_xml = kwargs["params"]["file"]
        xml_bytes = base64.b64decode(encoded_xml)
        xml = ET.fromstring(xml_bytes.decode("utf-8"))

        parser = SpringerParser()
        parsed = parser.parse(xml)

        return parsed
    raise Exception("There was no 'file' parameter. Exiting run.")


@dag(start_date=airflow.utils.dates.days_ago(0))
def springer_process_file():
    @task()
    def parse_file(**kwargs):
        return springer_parse_file(**kwargs)

    parse_file()


dag_taskflow = springer_process_file()
