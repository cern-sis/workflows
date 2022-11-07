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


def test_journal_doctype(parsed_happy_path_article):
    assert "article" == parsed_happy_path_article["journal_doctype"]


@fixture
def other_journal_doctype_article(shared_datadir):
    with open(shared_datadir / "other_in_journal_doctype.xml") as f:
        return ET.fromstring(f.read())


@fixture
def parsed_journal_doctype_with_value_other(iop_parser, other_journal_doctype_article):
    yield iop_parser._publisher_specific_parsing(other_journal_doctype_article)


def test_journal_doctype_other(parsed_journal_doctype_with_value_other):
    print(parsed_journal_doctype_with_value_other["journal_doctype"])
    assert "" == parsed_journal_doctype_with_value_other["journal_doctype"]


@fixture
def without_journal_doctype_article(shared_datadir):
    with open(shared_datadir / "without_journal_doctype.xml") as f:
        return ET.fromstring(f.read())


@fixture
def parsed_article_without_journal_doctype(iop_parser, without_journal_doctype_article):
    yield iop_parser._publisher_specific_parsing(without_journal_doctype_article)


def test_without_journal_doctype(parsed_article_without_journal_doctype):
    print(parsed_article_without_journal_doctype["journal_doctype"])
    assert "" == parsed_article_without_journal_doctype["journal_doctype"]


@fixture
def without_doi_article(shared_datadir):
    with open(shared_datadir / "without_doi.xml") as f:
        return ET.fromstring(f.read())


@fixture
def parsed_article_without_doi(iop_parser, without_doi_article):
    with raises(RequiredFieldNotFoundExtractionError):
        return iop_parser._publisher_specific_parsing(without_doi_article)
