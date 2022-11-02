import base64
import xml.etree.ElementTree as ET

import airflow
import requests
from airflow.decorators import dag, task
from common.enhancer import Enhancer
from common.enricher import Enricher
from inspire_utils.record import get_value
from iop.parser import IOPParser
from jsonschema import validate


def iop_parse_file(**kwargs):
    encoded_xml = get_value(kwargs, "params.file", default={})
    xml_bytes = base64.b64decode(encoded_xml)
    xml = ET.fromstring(xml_bytes.decode("utf-8"))

    parser = IOPParser()
    parsed = parser.parse(xml)
    if encoded_xml:
        return parsed
    raise Exception("There was no 'file' parameter. Exiting run.")


def enhance_iop(parsed_file):
    return Enhancer()("IOP", parsed_file)


def enrich_iop(enhanced_file):
    return Enricher()(enhanced_file)


def iop_validate_record(enriched_file):
    schema = requests.get(enriched_file["$schema"]).json()
    validate(enriched_file, schema)


@dag(start_date=airflow.utils.dates.days_ago(0))
def iop_process_file():
    @task()
    def parse_file(**kwargs):
        return iop_parse_file(**kwargs)

    @task()
    def enchance(parsed_file):
        return parsed_file and enhance_iop(parsed_file)

    @task()
    def enrich(enhanced_file):
        return enhanced_file and enrich_iop(enhanced_file)

    @task()
    def validate_record(enriched_file):
        return enriched_file and iop_validate_record(enriched_file)

    parsed_file = parse_file()
    enhanced_file = enchance(parsed_file)
    enriched_file = enrich(enhanced_file)
    validate_record(enriched_file)


dag_taskflow = iop_process_file()
