import xml.etree.ElementTree as ET

from iop.parser import IOPParser
from pytest import fixture


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


def test_happy_path_article(parsed_happy_path_article):
    assert [9] == parsed_happy_path_article["page_nr"]


@fixture
def without_page_nr_article(shared_datadir):
    with open(shared_datadir / "just_with_required_fields.xml") as f:
        return ET.fromstring(f.read())


@fixture
def parsed_without_page_nr_article(iop_parser, without_page_nr_article):
    yield iop_parser._publisher_specific_parsing(without_page_nr_article)


def test_without_page_nr(parsed_without_page_nr_article):
    assert [0] == parsed_without_page_nr_article["page_nr"]


@fixture
def with_str_page_nr_article(shared_datadir):
    with open(shared_datadir / "string_page_nr.xml") as f:
        return ET.fromstring(f.read())


@fixture
def parsed_with_str_page_nr_article(iop_parser, with_str_page_nr_article):
    yield iop_parser._publisher_specific_parsing(with_str_page_nr_article)


def test_parsed_with_str_page_nr_article(parsed_with_str_page_nr_article):
    assert [0] == parsed_with_str_page_nr_article["page_nr"]
