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
