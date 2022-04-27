import xml.etree.ElementTree as ET

from common.parsing.extractor import IExtractor
from common.parsing.parser import ObjectExtractor
from common.parsing.xml_extractors import (
    AttributeExtractor,
    ConstantExtractor,
    CustomExtractor,
    TextExtractor,
)
from pytest import fixture, raises

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
def xml_node():
    return ET.fromstring(TEST_XML_STRING)


def test_extractor_extract_raises_error():
    extractor = IExtractor([])
    raises(NotImplementedError, extractor.extract, root=ET.Element("root"))


def test_object_extractor(xml_node):
    def extract_and_cast(article: ET.Element):
        value = article.find("./FieldOne/FieldInt").text
        return int(value)

    extractor = ObjectExtractor(
        None,
        [
            TextExtractor("text_value", "./FieldOne/FieldTwo"),
            TextExtractor("text_value", "./FieldOne/UnexistantField", required=False),
            AttributeExtractor("attribute_value", "./FieldOne", "TagOne"),
            CustomExtractor("custom_value", extract_and_cast),
            ConstantExtractor("constant_value", "Constant"),
        ],
    )

    assert extractor.extract(xml_node) == {
        "text_value": "Value Field Two",
        "attribute_value": "TagOneValue",
        "custom_value": 5,
        "constant_value": "Constant",
    }
