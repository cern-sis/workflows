import base64
import xml.etree.ElementTree as ET

import pendulum
import requests
from airflow.decorators import dag, task
from common.enhancer import Enhancer
from common.enricher import Enricher
from common.utils import create_or_update_article
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
    return enriched_file


@dag(schedule=None, start_date=pendulum.today("UTC").add(days=-1))
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
        return enriched_file and springer_validate_record(enriched_file)

    @task()
    def create_or_update(enriched_file):
        create_or_update_article(enriched_file)

    parsed_file = parse_file()
    enhanced_file = enhance_file(parsed_file)
    enriched_file = enrich_file(enhanced_file)
    validated_record = validate_record(enriched_file)
    create_or_update(validated_record)


dag_taskflow = springer_process_file()
