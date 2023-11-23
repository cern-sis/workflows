import base64

import pendulum
import requests
from airflow.decorators import dag, task
from common.enhancer import Enhancer
from common.enricher import Enricher
from common.exceptions import EmptyOutputFromPreviousTask
from common.utils import parse_without_names_spaces
from elsevier.parser import ElsevierParser
from jsonschema import validate


def parse_elsevier(**kwargs):
    try:
        encoded_xml = kwargs["params"]["file_content"]
    except KeyError:
        raise Exception("There was no 'file_content' parameter. Exiting run.")
    xml_bytes = base64.b64decode(encoded_xml)
    xml = parse_without_names_spaces(xml_bytes.decode("utf-8"))
    parser = ElsevierParser()
    parsed = parser.parse(xml)
    try:
        metadata = kwargs["params"]["metadata"]
    except KeyError:
        raise Exception("Record is missing metadata. Exiting run.")
    return {**parsed, **metadata}


def enhance_elsevier(parsed_file):
    return Enhancer()("Elsevier", parsed_file)


def enrich_elsevier(enhanced_file):
    return Enricher()(enhanced_file)


def elsevier_validate_record(file_with_metadata):
    schema = requests.get(file_with_metadata["$schema"]).json()
    validate(file_with_metadata, schema)


@dag(schedule=None, start_date=pendulum.today("UTC").add(days=-1))
def elsevier_process_file():
    @task()
    def parse(**kwargs):
        return parse_elsevier(**kwargs)

    @task()
    def enhance(parsed_file):
        if parsed_file:
            return parsed_file and enhance_elsevier(parsed_file)
        raise EmptyOutputFromPreviousTask("parse_metadata")

    @task()
    def enrich(enhanced_file):
        if enhanced_file:
            return enrich_elsevier(enhanced_file)
        raise EmptyOutputFromPreviousTask("enhanced_file_with_metadata")

    @task()
    def validate_record(enriched_file):
        if enriched_file:
            return elsevier_validate_record(enriched_file)
        raise EmptyOutputFromPreviousTask("enriched_file_with_metadata")

    parsed_file = parse()
    enhanced_file = enhance(parsed_file)
    enriched_file = enrich(enhanced_file)
    validate_record(enriched_file)


Elsevier_file_processing = elsevier_process_file()
