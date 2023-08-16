import json
import os

import pytest
from aps.aps_api_client import APSApiClient
from aps.aps_params import APSParams


@pytest.fixture(scope="function")
def aps_api_client_fixture():
    yield APSApiClient()


# @pytest.mark.vcr
def test_get_articles_metadata(aps_api_client_fixture, shared_datadir):
    parameters = APSParams(
        from_date="2021-04-10", until_date="2022-04-10", per_page=1
    ).get_params()
    metadata_value = aps_api_client_fixture.get_articles_metadata(parameters=parameters)
    file_path = os.path.join(shared_datadir, "test_json.json")
    with open(file_path, "rb") as json_file:
        content = json_file.read()
        json_content = json.loads(content)
        assert json_content == metadata_value
        assert len(metadata_value["data"]) == 1


@pytest.mark.vcr
def test_get_pdf_file(aps_api_client_fixture, shared_datadir):
    doi = "10.1103/PhysRevLett.126.153601"
    pdf = aps_api_client_fixture.get_pdf_file(doi=doi)
    file_path = os.path.join(shared_datadir, "test_pdf.pdf")
    with open(file_path, "rb") as pdf_file:
        assert pdf_file.read() == pdf


@pytest.mark.vcr
def test_get_xml(aps_api_client_fixture, shared_datadir):
    doi = "10.1103/PhysRevLett.126.153601"
    xml = aps_api_client_fixture.get_xml_file(doi=doi)
    file_path = os.path.join(shared_datadir, "test_xml.xml")
    with open(file_path, "rb") as xml_file:
        assert xml_file.read() == xml
