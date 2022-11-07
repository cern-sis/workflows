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
    assert [{"value": "2108.04010"}] == parsed_happy_path_article["arxiv_eprints"]


@fixture
def without_arxiv_article(shared_datadir):
    with open(shared_datadir / "without_arxiv.xml") as f:
        return ET.fromstring(f.read())


@fixture
def parsed_without_arxiv_article(iop_parser, without_arxiv_article):
    yield iop_parser._publisher_specific_parsing(without_arxiv_article)


def test_without_arxiv(parsed_without_arxiv_article):
    assert [] == parsed_without_arxiv_article["arxiv_eprints"]


@fixture
def with_version_arxiv_article(shared_datadir):
    with open(shared_datadir / "with_version_arxiv_article.xml") as f:
        return ET.fromstring(f.read())


@fixture
def parsed_with_version_arxiv_article(iop_parser, with_version_arxiv_article):
    yield iop_parser._publisher_specific_parsing(with_version_arxiv_article)


def test_with_version_arxiv(parsed_with_version_arxiv_article):
    assert [{"value": "2108.04010"}] == parsed_with_version_arxiv_article[
        "arxiv_eprints"
    ]
