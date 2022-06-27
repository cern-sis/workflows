import base64
import xml.etree.ElementTree as ET

import airflow
import requests
from airflow.decorators import dag, task
from common.enhancer import Enhancer
from common.enricher import Enricher
from jsonschema import validate
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


def springer_enhance_file(parsed_file):
    return Enhancer()("Springer", parsed_file)


def springer_enrich_file(enhanced_file):
    return Enricher()(enhanced_file)


def springer_validate_record(enriched_file):
    schema = requests.get(enriched_file["$schema"]).json()
    validate(enriched_file, schema)


@dag(start_date=airflow.utils.dates.days_ago(0))
def springer_process_file():
    @task()
    def parse_file(**kwargs):
        return springer_parse_file(**kwargs)

    @task()
    def enhance_file(parsed_file):
        return springer_enhance_file(parsed_file)

    @task()
    def enrich_file(enhanced_file):
        return springer_enrich_file(enhanced_file)

    @task()
    def validate_record(enriched_file):
        springer_validate_record(enriched_file)

    parsed_file = parse_file()
    enhanced_file = enhance_file(parsed_file)
    enriched_file = enrich_file(enhanced_file)
    validate_record(enriched_file)


dag_taskflow = springer_process_file()
