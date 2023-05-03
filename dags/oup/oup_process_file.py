import base64

import pendulum
import requests
from airflow.decorators import dag, task
from common.enhancer import Enhancer
from common.enricher import Enricher
from common.utils import parse_without_names_spaces
from jsonschema import validate
from oup.parser import OUPParser


def oup_parse_file(**kwargs):
    if "params" not in kwargs or "file" not in kwargs["params"]:
        raise KeyError("There was no 'file' parameter. Exiting run.")
    encoded_xml = kwargs["params"]["file"]
    xml_bytes = base64.b64decode(encoded_xml)
    xml = parse_without_names_spaces(xml_bytes.decode("utf-8"))

    parser = OUPParser()
    parsed = parser.parse(xml)

    return parsed


def oup_enhance_file(parsed_file):
    return Enhancer()("OUP", parsed_file)


def oup_enrich_file(enhanced_file):
    return Enricher()(enhanced_file)


def oup_validate_record(enriched_file):
    schema = requests.get(enriched_file["$schema"]).json()
    validate(enriched_file, schema)


@dag(schedule=None, start_date=pendulum.today("UTC").add(days=-1))
def oup_process_file():
    @task()
    def parse_file(**kwargs):
        return oup_parse_file(**kwargs)

    @task()
    def enhance_file(parsed_file):
        return oup_enhance_file(parsed_file)

    @task()
    def enrich_file(enhanced_file):
        return oup_enrich_file(enhanced_file)

    @task()
    def validate_record(enriched_file):
        oup_validate_record(enriched_file)

    parsed_file = parse_file()
    enhanced_file = enhance_file(parsed_file)
    enriched_file = enrich_file(enhanced_file)
    validate_record(enriched_file)


dag_taskflow = oup_process_file()
