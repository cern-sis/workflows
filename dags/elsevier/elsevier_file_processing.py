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
    if "params" not in kwargs or "file" or "file_name" not in kwargs["params"]:
        raise KeyError("There was no 'file' or 'file_name' parameter. Exiting run.")
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
    dataset_file_path = file_path.split("/")[:-2]
    dataset_path_parts = dataset_file_path + ["dataset.xml"]
    file = repo.get_by_id("/".join(*dataset_path_parts))
    xml_bytes = base64.b64decode(file)
    xml = parse_without_names_spaces(xml_bytes.decode("utf-8"))
    parser = ElsevierMetadataParser()
    metadata = parser.parse(xml, file_path)
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
    def enchance(parsed_file):
        if parsed_file:
            return parsed_file and enhance_elsevier(parsed_file)
        raise EmptyOutputFromPreviousTask("parsed_file")

    @task()
    def enrich(enhanced_file):
        if enhanced_file:
            return enrich_elsevier(enhanced_file)
        raise EmptyOutputFromPreviousTask("enhanced_file")

    @task()
    def parse_metadata(enriched_file, repo: IRepository = ElsevierRepository()):
        if enriched_file:
            return elsevier_parse_metadata(enriched_file, repo)
        raise EmptyOutputFromPreviousTask("enriched_file")

    @task()
    def validate_record(enriched_file_with_metadata):
        if enriched_file_with_metadata:
            return elsevier_validate_record(enriched_file)
        raise EmptyOutputFromPreviousTask("enriched_file_with_metadata")

    parsed_file = parse()
    enhanced_file = enchance(parsed_file)
    enriched_file = enrich(enhanced_file)
    enriched_file_with_metadata = parse_metadata(enriched_file)
    validate_record(enriched_file_with_metadata)


Elsevier_file_processing = elsevier_process_file()
