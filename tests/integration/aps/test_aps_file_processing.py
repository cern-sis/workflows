import base64
import json
import xml.etree.ElementTree as ET

import pytest
from airflow.models import DagBag
from aps.aps_api_client import APSApiClient
from aps.aps_process_file import enhance_aps, enrich_aps, replace_authors
from aps.parser import APSParser
from aps.xml_parser import APSParserXML
from pytest import fixture

DAG_NAME = "aps_process_file"


@pytest.fixture(scope="module")
def parser():
    return APSParser()


@pytest.fixture
def articles(shared_datadir):
    json_response = (shared_datadir / "json_response_content.json").read_text()
    return [article for article in json.loads(json_response)["data"]]


@pytest.fixture
def parsed_article(parser, articles):
    return parser._publisher_specific_parsing(articles[0])


@fixture(scope="module")
def xml_parser():
    return APSParserXML()


@fixture
def enhanced_article(parsed_article):
    return enhance_aps(parsed_article)


@fixture(scope="function")
def aps_api_client_fixture():
    yield APSApiClient()


@pytest.mark.vcr
@fixture
def populated_file(enhanced_article, aps_api_client_fixture):
    if "dois" not in enhanced_article:
        return enhanced_article

    doi = "10.1103/PhysRevLett.126.153601"

    pdf = aps_api_client_fixture.get_pdf_file(doi=doi)
    xml = aps_api_client_fixture.get_xml_file(doi=doi)

    downloaded_files = {
        "pdf": pdf,
        "xml": xml,
    }

    enhanced_article["files"] = downloaded_files
    return enhanced_article


@fixture
def enriched_article(populated_file):
    return enrich_aps(populated_file)


@fixture()
def parsed_article_xml(xml_parser, enriched_article):
    return xml_parser._publisher_specific_parsing(
        ET.fromstring(enriched_article["files"]["xml"])
    )


@fixture
def dag():
    dagbag = DagBag(dag_folder="dags/", include_examples=False)
    assert dagbag.import_errors.get(f"dags/{DAG_NAME}.py") is None
    return dagbag.get_dag(dag_id=DAG_NAME)


def test_dag_loaded(dag):
    assert dag is not None
    assert len(dag.tasks) == 8


def remove_ignored_fields(data, fields_to_ignore):
    if isinstance(data, dict):
        return {
            key: remove_ignored_fields(value, fields_to_ignore)
            for key, value in data.items()
            if key not in fields_to_ignore
        }
    elif isinstance(data, list):
        return [remove_ignored_fields(item, fields_to_ignore) for item in data]
    else:
        return data


def encode_binary(data):
    if isinstance(data, bytes):
        return base64.b64encode(data).decode("utf-8")
    if isinstance(data, dict):
        return {k: encode_binary(v) for k, v in data.items()}
    if isinstance(data, list):
        return [encode_binary(v) for v in data]
    return data


def test_process_file(enriched_article, parsed_article_xml, shared_datadir):
    complete_file = replace_authors(enriched_article, parsed_article_xml)

    complete_file_serializable = encode_binary(complete_file)

    serialized_output = json.dumps(complete_file_serializable, sort_keys=True)

    expected_output = json.loads(
        (shared_datadir / "expected_json_output.json").read_text()
    )

    fields_to_ignore = ["acquisition_source", "record_creation_date"]

    def remove_fields(data):
        return remove_ignored_fields(data, fields_to_ignore)

    actual_cleaned = remove_fields(json.loads(serialized_output))
    expected_cleaned = remove_fields(expected_output)

    assert actual_cleaned == expected_cleaned
