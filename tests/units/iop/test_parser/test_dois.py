import xml.etree.ElementTree as ET

from common.parsing.xml_extractors import RequiredFieldNotFoundExtractionError
from iop.parser import IOPParser
from pytest import fixture, raises


@fixture(scope="module")
def iop_parser():
    yield IOPParser()


@fixture
def happy_path_article(shared_datadir):
    with open(shared_datadir / "example1.xml") as f:
        return ET.fromstring(f.read())


@fixture
def parsed_happy_path_article(iop_parser, happy_path_article):
    yield iop_parser._publisher_specific_parsing(happy_path_article)


def test_parsed_happy_path_article(parsed_happy_path_article):
    assert ["10.1088/1674-1137/ac66cc"] == parsed_happy_path_article["dois"]


@fixture
def without_doi_article(shared_datadir):
    with open(shared_datadir / "without_doi.xml") as f:
        return ET.fromstring(f.read())


def test_parse_without_doi_article(iop_parser, without_doi_article):
    with raises(RequiredFieldNotFoundExtractionError):
        assert iop_parser._publisher_specific_parsing(without_doi_article)
