import base64

import pendulum
import requests
from airflow.decorators import dag, task
from common.enhancer import Enhancer
from common.enricher import Enricher
from common.exceptions import EmptyOutputFromPreviousTask
from common.repository import IRepository
from common.utils import parse_without_names_spaces
from elsevier.metadata_parser import ElsevierMetadataParser
from elsevier.parser import ElsevierParser
from elsevier.repository import ElsevierRepository
from jsonschema import validate


def parse_elsevier(**kwargs):
    if "params" not in kwargs or "file" not in kwargs["params"]:
        raise KeyError("There was no 'file' parameter. Exiting run.")
    if "params" not in kwargs or "file_name" not in kwargs["params"]:
        raise KeyError("There was 'file_name' parameter. Exiting run.")
    encoded_xml = kwargs["params"]["file"]
    file_name = kwargs["params"]["file_name"]
    xml_bytes = base64.b64decode(encoded_xml)
    xml = parse_without_names_spaces(xml_bytes.decode("utf-8"))
    parser = ElsevierParser()
    parsed = parser.parse(xml)
    parsed["source_file_path"] = file_name
    return parsed


def enhance_elsevier(parsed_file):
    return Enhancer()("Elsevier", parsed_file)


def enrich_elsevier(enhanced_file):
    return Enricher()(enhanced_file)


def elsevier_parse_metadata(enriched_file, repo):
    file_path = enriched_file["source_file_path"]
    dataset_file_path = file_path.split("/")[:3]
    dataset_path_parts = dataset_file_path + ["dataset.xml"]
    full_path = "/".join((dataset_path_parts))
    file = repo.get_by_id(full_path)
    xml_bytes = base64.b64decode(base64.b64encode(file.getvalue()).decode())
    xml = parse_without_names_spaces(xml_bytes.decode("utf-8"))
    parser = ElsevierMetadataParser(
        file_path=file_path, doi=enriched_file["dois"][0]["value"]
    )
    metadata = parser.parse(xml)
    return {**enriched_file, **metadata}

def elsevier_validate_record(file_with_metadata):
    schema = requests.get(file_with_metadata["$schema"]).json()
    validate(file_with_metadata, schema)


@dag(schedule=None, start_date=pendulum.today("UTC").add(days=-1))
def elsevier_process_file():
    @task()
    def parse(**kwargs):
        return parse_elsevier(**kwargs)

    @task()
    def parse_metadata(parsed_file, repo: IRepository = ElsevierRepository()):
        if parsed_file:
            return elsevier_parse_metadata(parsed_file, repo)
        raise EmptyOutputFromPreviousTask("parsed_file")

    @task()
    def enhance(parsed_file_with_metadata):
        if parsed_file_with_metadata:
            return parsed_file and enhance_elsevier(parsed_file_with_metadata)
        raise EmptyOutputFromPreviousTask("parse_metadata")

    @task()
    def enrich(enhanced_file_with_metadata):
        if enhanced_file_with_metadata:
            return enrich_elsevier(enhanced_file_with_metadata)
        raise EmptyOutputFromPreviousTask("enhanced_file_with_metadata")

    @task()
    def validate_record(enriched_file_with_metadata):
        if enriched_file_with_metadata:
            return elsevier_validate_record(enriched_file_with_metadata)
        raise EmptyOutputFromPreviousTask("enriched_file_with_metadata")

    parsed_file = parse()
    parsed_file_with_metadata = parse_metadata(parsed_file)
    enhanced_file_with_metadata = enhance(parsed_file_with_metadata)
    enriched_file_with_metadata = enrich(enhanced_file_with_metadata)
    validate_record(enriched_file_with_metadata)


Elsevier_file_processing = elsevier_process_file()
