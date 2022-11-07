import xml.etree.ElementTree as ET

from iop.parser import IOPParser
from pytest import fixture


@fixture(scope="module")
def iop_parser():
    yield IOPParser()


@fixture
def no_related_dois_article(shared_datadir):
    with open(shared_datadir / "journal_type_cerrection.xml") as f:
        return ET.fromstring(f.read())


@fixture
def parsed_no_related_dois_article(iop_parser, no_related_dois_article):
    yield iop_parser._publisher_specific_parsing(no_related_dois_article)


def test_related_dois_article(parsed_no_related_dois_article):
    assert [] == parsed_no_related_dois_article["related_article_doi"]


@fixture
def without_journal_doctype_article(shared_datadir):
    with open(shared_datadir / "without_journal_doctype.xml") as f:
        return ET.fromstring(f.read())


@fixture
def parsed_without_journal_doctype(iop_parser, without_journal_doctype_article):
    yield iop_parser._publisher_specific_parsing(without_journal_doctype_article)


def test_related_dois_article_without_journal_doctype(parsed_without_journal_doctype):
    assert [] == parsed_without_journal_doctype["related_article_doi"]


@fixture
def with_journal_doctype_article(shared_datadir):
    with open(shared_datadir / "example1.xml") as f:
        return ET.fromstring(f.read())


@fixture
def parsed_with_journal_doctype(iop_parser, with_journal_doctype_article):
    yield iop_parser._publisher_specific_parsing(with_journal_doctype_article)


def test_related_dois_article_with_journal_doctype(parsed_with_journal_doctype):
    assert [] == parsed_with_journal_doctype["related_article_doi"]
