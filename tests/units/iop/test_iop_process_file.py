import xml.etree.ElementTree as ET

from iop.iop_process_file import enhance_iop, enrich_iop, iop_validate_record
from iop.parser import IOPParser
from pytest import fixture


@fixture
def article(shared_datadir):
    file_content = (shared_datadir / "example1.xml").read_text()
    yield ET.fromstring(file_content)


@fixture
def parser():
    return IOPParser()


@fixture
def parsed_article(article, parser):
    return parser._publisher_specific_parsing(article)


@fixture
def parsed_generic_article(parsed_article, parser):
    return parser._generic_parsing(parsed_article)


@fixture
def enhance_article(parsed_generic_article):
    return enhance_iop(parsed_generic_article)


@fixture
def enrich_article(enhance_article):
    return enrich_iop(enhance_article)


def test_aps_validated_record(enrich_article):
    iop_validate_record(enrich_article)
