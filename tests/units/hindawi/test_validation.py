import xml.etree.ElementTree as ET

import requests
from common.enhancer import Enhancer
from common.enricher import Enricher
from common.parsing.xml_extractors import RequiredFieldNotFoundExtractionError
from hindawi.parser import HindawiParser
from jsonschema import validate
from pytest import fixture, raises


@fixture(scope="module")
def parser():
    return HindawiParser()


@fixture
def parsed_article(shared_datadir, parser):
    with open(shared_datadir / "example1.xml") as file:
        parsed_file = parser.parse(ET.fromstring(file.read()))
        enhanced_file = Enhancer()("Hindawi", parsed_file)
        return Enricher()(enhanced_file)


def test_hindawi_validate_record(parsed_article):
    schema = requests.get(parsed_article["$schema"]).json()
    validate(parsed_article, schema)


def test_hindawi_validate_record_without_doi(parser, shared_datadir):
    with open(shared_datadir / "example3.xml") as file:
        with raises(RequiredFieldNotFoundExtractionError):
            parsed_file = parser.parse(ET.fromstring(file.read()))
            enhanced_file = Enhancer()("Hindawi", parsed_file)
            parsed_article_without_doi = Enricher()(enhanced_file)
            schema = requests.get(parsed_article_without_doi["$schema"]).json()
            validate(parsed_article, schema)
