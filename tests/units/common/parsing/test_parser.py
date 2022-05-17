import json
import xml.etree.ElementTree as ET

from common.parsing.parser import IParser
from common.parsing.xml_extractors import (
    AttributeExtractor,
    ConstantExtractor,
    CustomExtractor,
    TextExtractor,
)
from pytest import fixture

TEST_XML_STRING = """
    <Root>
        <FieldOne TagOne="TagOneValue">
            <FieldTwo>Value Field Two</FieldTwo>
            <FieldThree>Value Field Three</FieldThree>
            <FieldFour>Value Field Four</FieldFour>
            <FieldInt>5</FieldInt>
        </FieldOne>
    </Root>
"""

publisher_parsed_article = {
    "journal_doctype": "article",
    "dois": ["Test dois"],
    "arxiv_eprints": [{"value": "Test Eprint"}],
    "page_nr": [45],
    "abstract": "Test abstract",
    "title": "Test title",
    "classification_numbers": ["Test classification 1", "Test classification 2"],
    "authors": [
        {
            "surname": "Test Surname",
            "given_names": "Test names",
            "email": "test@email.com",
            "affiliations": [
                {
                    "value": "Test affiliation",
                    "organization": "Test org",
                    "country": "Test country",
                }
            ],
            "full_name": "Test, Name",
        }
    ],
    "collaborations": ["Test collaboration"],
    "journal_title": "Test title",
    "journal_issue": "2",
    "journal_volume": "79",
    "journal_artid": "Test art-id",
    "journal_fpage": "1",
    "journal_lpage": "45",
    "journal_year": 2019,
    "date_published": "2019-02-06",
    "related_article_doi": ["Test related article doi"],
    "copyright_holder": "Test Copyright",
    "copyright_year": "2019",
    "license": [
        {"license": "CC-BY-4.0", "url": "https://creativecommons.org/licenses//by/4.0"}
    ],
    "collections": ["Test Collection"],
    "control_field": ["Test control field"],
    "free_keywords": ["Test free 1", "Test free 2"],
    "thesis_supervisor": [
        {
            "surname": "Test Surname",
            "given_names": "Test names",
            "email": "test@email.com",
            "affiliations": [
                {
                    "value": "Test affiliation",
                    "organization": "Test org",
                    "country": "Test country",
                }
            ],
            "full_name": "Test, Name",
        }
    ],
    "thesis": ["Test thesis", "Test other thesis"],
    "urls": ["test.com"],
    "local_files": ["Test local file"],
}

expected_generic_parsing_output = {
    "abstract": "Test abstract",
    "arxiv_eprints": [{"value": "Test Eprint"}],
    "authors": [
        {
            "affiliations": [
                {
                    "country": "Test country",
                    "organization": "Test org",
                    "value": "Test affiliation",
                }
            ],
            "email": "test@email.com",
            "full_name": "Test Surname, Test names",
            "given_names": "Test names",
            "surname": "Test Surname",
        }
    ],
    "classification_numbers": [
        {"classification_number": "Test classification 1", "standard": "PACS"},
        {"classification_number": "Test classification 2", "standard": "PACS"},
    ],
    "collaborations": [{"value": "Test collaboration"}],
    "collections": [{"primary": "Test Collection"}],
    "control_field": "Test control field",
    "copyright_holder": "Test Copyright",
    "copyright_year": "2019",
    "date_published": "2019-02-06",
    "dois": [{"value": "Test dois"}, {"value": "Test related article doi"}],
    "free_keywords": [
        {"source": "author", "value": "Test free 1"},
        {"source": "author", "value": "Test free 2"},
    ],
    "license": [
        {"license": "CC-BY-4.0", "url": "https://creativecommons.org/licenses//by/4.0"}
    ],
    "local_files": [{"value": "Test local file"}],
    "page_nr": [45],
    "publication_info": [
        {
            "artid": "Test art-id",
            "journal_issue": "2",
            "journal_title": "Test title",
            "journal_volume": "79",
            "material": "article",
            "page_end": "45",
            "page_start": "1",
            "year": 2019,
        }
    ],
    "thesis": "Test thesis",
    "thesis_supervisor": [
        {
            "affiliations": [
                {
                    "country": "Test country",
                    "organization": "Test org",
                    "value": "Test affiliation",
                }
            ],
            "full_name": "Test Surname, Test names",
        }
    ],
    "title": "Test title",
    "urls": [{"value": "test.com"}],
}


@fixture
def publisher_parsed_article(datadir):
    return json.loads((datadir / "input.json").read_text())


@fixture
def expected_generic_parsing_output(datadir):
    return json.loads((datadir / "expected.json").read_text())


@fixture
def xml_node():
    return ET.fromstring(TEST_XML_STRING)


def test_publisher_parsing(xml_node: ET.Element):
    def extract_and_cast(article: ET.Element):
        value = article.find("./FieldOne/FieldInt").text
        return int(value)

    parser = IParser(
        [
            TextExtractor("text_value", "./FieldOne/FieldTwo"),
            TextExtractor("text_value", "./FieldOne/UnexistantField", required=False),
            AttributeExtractor("attribute_value", "./FieldOne", "TagOne"),
            CustomExtractor("custom_value", extract_and_cast),
            ConstantExtractor("constant_value", "Constant"),
        ]
    )
    assert parser._publisher_specific_parsing(xml_node) == {
        "text_value": "Value Field Two",
        "attribute_value": "TagOneValue",
        "custom_value": 5,
        "constant_value": "Constant",
    }


def test_generic_parsing(publisher_parsed_article, expected_generic_parsing_output):
    parser = IParser([])
    assert expected_generic_parsing_output == parser._generic_parsing(
        publisher_parsed_article
    )
