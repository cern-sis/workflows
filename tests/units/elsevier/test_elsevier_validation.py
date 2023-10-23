import pytest
import requests
from common.enhancer import Enhancer
from common.enricher import Enricher
from common.utils import parse_without_names_spaces
from elsevier.metadata_parser import ElsevierMetadataParser
from elsevier.parser import ElsevierParser
from jsonschema import validate
from pytest import fixture


@fixture(scope="module")
def parser():
    return ElsevierParser()


@fixture(scope="module")
def metadata_parser():
    return ElsevierMetadataParser(
        doi="10.1016/j.physletb.2023.137730",
        file_path="extracted/CERNQ000000010669A/CERNQ000000010669",
    )


@fixture
def parsed_article(shared_datadir, parser, metadata_parser):
    with open(
        shared_datadir / "CERNQ000000010011" / "S0370269323000643" / "main.xml"
    ) as file:
        parsed_file = parser.parse(parse_without_names_spaces(file.read()))
    with open(shared_datadir / "CERNQ000000010011" / "dataset.xml") as file:
        parsed_file_with_metadata = metadata_parser.parse(
            parse_without_names_spaces(file.read())
        )
        full_parsed_file = {**parsed_file, **parsed_file_with_metadata}
        enhanced_file = Enhancer()("Elsevier", full_parsed_file)
        print(parsed_file)
        return Enricher()(enhanced_file)


@pytest.mark.vcr
def test_elsevier_validate_record(parsed_article):
    schema = requests.get(parsed_article["$schema"]).json()
    validate(parsed_article, schema)
