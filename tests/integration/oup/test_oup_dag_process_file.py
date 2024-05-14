from zipfile import ZipFile

import pytest
from airflow.models import DagBag
from common.utils import parse_without_names_spaces
from freezegun import freeze_time
from oup.oup_process_file import oup_enhance_file, oup_enrich_file
from oup.parser import OUPParser
from pytest import fixture

DAG_NAME = "oup_process_file"


@fixture
def dag():
    dagbag = DagBag(dag_folder="dags/", include_examples=False)
    assert dagbag.import_errors.get(f"dags/{DAG_NAME}.py") is None
    return dagbag.get_dag(dag_id=DAG_NAME)


@fixture
def parser():
    return OUPParser()


@fixture
def articles(parser):
    data_dir = "./data/oup/"
    test_file = "2022-09-22_00:30:02_ptep_iss_2022_9.xml.zip"

    def extract_zip_to_article(zip_filename):
        with ZipFile(zip_filename, "r") as zip_file:
            xmls = [
                file.filename for file in zip_file.filelist if ".xml" in file.filename
            ]
            xmls_content = [
                parse_without_names_spaces(zip_file.read(xml).decode("utf-8"))
                for xml in xmls
            ]
            return xmls_content

    articles = extract_zip_to_article(data_dir + test_file)

    return articles


@fixture
def article(parser):
    data_dir = "./data/oup/"
    test_file = "2022-09-22_00:30:02_ptep_iss_2022_9.xml.zip"

    def extract_zip_to_article(zip_filename):
        with ZipFile(zip_filename, "r") as zip_file:
            xmls = [
                file.filename for file in zip_file.filelist if ".xml" in file.filename
            ]
            xmls_content = [
                parse_without_names_spaces(zip_file.read(xml).decode("utf-8"))
                for xml in xmls
            ][0]
            return xmls_content

    article = extract_zip_to_article(data_dir + test_file)
    parsed_file = parser.parse(article)
    enhanced_file = oup_enhance_file(parsed_file)
    enriched_file = oup_enrich_file(enhanced_file)

    return enriched_file


def test_affiliation_countries_in_enriched(parser, articles):
    for article in articles:
        parsed_file = parser.parse(article)
        enhanced_file = oup_enhance_file(parsed_file)
        enriched_file = oup_enrich_file(enhanced_file)

        authors = enriched_file.get("authors", [])
        for author in authors:
            for aff in author.get("affiliations"):
                assert aff.get("country") is not None

def test_dag_loaded(dag):
    assert dag
    assert len(dag.tasks) == 6


publisher = "OUP"

generic_pseudo_parser_output = {
    "abstract": "this is abstracts",
    "copyright_holder": "copyright_holder",
    "copyright_year": "2020",
    "copyright_statement": "copyright_statement",
    "copyright_material": "copyright_material",
    "date_published": "2022-05-20",
    "title": "title",
    "subtitle": "subtitle",
}


expected_output = {
    "abstracts": [{"value": "this is abstracts", "source": publisher}],
    "acquisition_source": {
        "source": publisher,
        "method": publisher,
        "date": "2022-05-20T00:00:00",
    },
    "copyright": [
        {
            "holder": "copyright_holder",
            "year": "2020",
            "statement": "copyright_statement",
            "material": "copyright_material",
        }
    ],
    "imprints": [{"date": "2022-05-20", "publisher": publisher}],
    "record_creation_date": "2022-05-20T00:00:00",
    "titles": [{"title": "title", "subtitle": "subtitle", "source": publisher}],
}

empty_generic_pseudo_parser_output = {
    "abstract": "",
    "copyright_holder": "",
    "copyright_year": "",
    "copyright_statement": "",
    "copyright_material": "",
    "date_published": "",
    "title": "",
    "subtitle": "",
}


expected_output_from_empty_input = {
    "abstracts": [{"value": "", "source": publisher}],
    "acquisition_source": {
        "source": publisher,
        "method": publisher,
        "date": "2022-05-20T00:00:00",
    },
    "copyright": [{"holder": "", "year": "", "statement": "", "material": ""}],
    "imprints": [{"date": "", "publisher": publisher}],
    "record_creation_date": "2022-05-20T00:00:00",
    "titles": [{"title": "", "subtitle": "", "source": publisher}],
}


@pytest.mark.parametrize(
    "test_input, expected, publisher",
    [
        pytest.param(generic_pseudo_parser_output, expected_output, publisher),
        pytest.param(
            empty_generic_pseudo_parser_output,
            expected_output_from_empty_input,
            publisher,
        ),
    ],
)
@freeze_time("2022-05-20")
def test_dag_enhance_file(test_input, expected, publisher):
    assert expected == oup_enhance_file(test_input)


@pytest.mark.vcr
def test_dag_enrich_file(assertListEqual):
    input_article = {
        "arxiv_eprints": [{"value": "2112.01211"}],
        "curated": "Test Value",
        "citeable": "Test Value",
    }
    assertListEqual(
        {
            "arxiv_eprints": [
                {"value": "2112.01211", "categories": list(set(["hep-th", "hep-ph"]))}
            ],
        },
        oup_enrich_file(input_article),
    )
