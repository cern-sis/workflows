import base64
import xml.etree.ElementTree as ET

import pendulum
import requests
from airflow.decorators import dag, task
from common.enhancer import Enhancer
from common.enricher import Enricher
from common.utils import create_or_update_article
from iop.parser import IOPParser
from jsonschema import validate


def iop_parse_file(**kwargs):
    if "params" not in kwargs or "file" not in kwargs["params"]:
        raise Exception("There was no 'file' parameter. Exiting run.")
    encoded_xml = kwargs["params"]["file"]
    xml_bytes = base64.b64decode(encoded_xml)
    xml = ET.fromstring(xml_bytes.decode("utf-8"))

    parser = IOPParser()
    parsed = parser.parse(xml)

    return parsed


def iop_enhance_file(parsed_file):
    return Enhancer()("IOP", parsed_file)


def iop_enrich_file(enhanced_file):
    return Enricher()(enhanced_file)


def iop_validate_record(enriched_file):
    schema = requests.get(enriched_file["$schema"]).json()
    validate(enriched_file, schema)


@dag(schedule=None, start_date=pendulum.today("UTC").add(days=-1))
def iop_process_file():
    @task()
    def parse_file(**kwargs):
        return iop_parse_file(**kwargs)

    @task()
    def enhance_file(parsed_file):
        return iop_enhance_file(parsed_file)

    @task()
    def enrich_file(enhanced_file):
        return iop_enrich_file(enhanced_file)

    @task()
    def validate_record(enriched_file):
        iop_validate_record(enriched_file)

    @task()
    def create_or_update(enriched_file):
        create_or_update_article(enriched_file)

    parsed_file = parse_file()
    enhanced_file = enhance_file(parsed_file)
    enriched_file = enrich_file(enhanced_file)
    validate_record(enriched_file)
    create_or_update(enriched_file)


dag_taskflow = iop_process_file()
