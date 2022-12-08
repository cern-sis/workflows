import xml.etree.ElementTree as ET

from common.parsing.xml_extractors import RequiredFieldNotFoundExtractionError
from iop.parser import IOPParser
from pytest import fixture, raises
from structlog.testing import capture_logs


@fixture
def parser():
    return IOPParser()


def test_doi(shared_datadir, parser):
    content = (shared_datadir / "just_required_fields.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert parsed_article["dois"] == ["10.1088/1674-1137/ac66cc"]


def test_no_doi(shared_datadir, parser):
    content = (shared_datadir / "no_data.xml").read_text()
    article = ET.fromstring(content)
    with raises(RequiredFieldNotFoundExtractionError):
        parser._publisher_specific_parsing(article)


def test_no_doi_in_text(shared_datadir, parser):
    content = (shared_datadir / "just_fields_no_text_data.xml").read_text()
    article = ET.fromstring(content)
    with raises(RequiredFieldNotFoundExtractionError):
        parser._publisher_specific_parsing(article)


def test_journal_doctype(shared_datadir, parser):
    content = (shared_datadir / "just_required_fields.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert parsed_article["journal_doctype"] == "article"


def test_no_journal_doctype(shared_datadir, parser):
    content = (shared_datadir / "without_journal_doc_type.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert "journal_doctype" not in parsed_article


def test_no_journal_doctype_in_attribute(shared_datadir, parser):
    content = (
        shared_datadir / "without_journal_doc_type_attribute_value.xml"
    ).read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert "journal_doctype" not in parsed_article


def test_journal_doctype_with_wrong_value(shared_datadir, parser):
    content = (shared_datadir / "all_fields_wrong_values.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert "journal_doctype" not in parsed_article


def test_journal_doctype_log_error_with_wrong_value(shared_datadir):
    with capture_logs() as cap_logs:
        content = (shared_datadir / "all_fields_wrong_values.xml").read_text()
        article = ET.fromstring(content)
        parser = IOPParser()
        parser._publisher_specific_parsing(article)
        assert cap_logs == [
            {
                "class_name": "IOPParser",
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "Parsing dois for article",
                "log_level": "info",
            },
            {
                "class_name": "IOPParser",
                "doi": "10.1088/1674-1137/ac66cc",
                "article_type": "no-data",
                "event": "Unmapped article type",
                "log_level": "error",
            },
        ]


def test_journal_doctype_log_error_without_value(shared_datadir, parser):
    with capture_logs() as cap_logs:
        parser = IOPParser()
        content = (shared_datadir / "without_journal_doc_type.xml").read_text()
        article = ET.fromstring(content)
        parser._publisher_specific_parsing(article)
        assert cap_logs == [
            {
                "class_name": "IOPParser",
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "Parsing dois for article",
                "log_level": "info",
            },
            {
                "class_name": "IOPParser",
                "doi": "10.1088/1674-1137/ac66cc",
                "event": "Article-type is not found in XML",
                "log_level": "error",
            },
        ]
