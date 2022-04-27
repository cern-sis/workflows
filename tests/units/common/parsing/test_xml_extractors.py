import xml.etree.ElementTree as ET

from common.parsing.xml_extractors import (
    AttributeExtractor,
    ConstantExtractor,
    CustomExtractor,
    RequiredFieldNotFoundExtractionError,
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


def test_text_extractor(xml_node: ET.Element):
    extractor = TextExtractor(None, "./FieldOne/FieldTwo")
    assert extractor.extract(xml_node) == "Value Field Two"


def test_text_extractor_crash_on_required(xml_node: ET.Element):
    extractor = TextExtractor(None, "./FieldOne/UnexistantField")
    raises(RequiredFieldNotFoundExtractionError, extractor.extract, article=xml_node)


def test_text_extractor_returns_default_if_not_found(xml_node: ET.Element):
    extractor = TextExtractor(
        None,
        "./FieldOne/UnexistantField",
        required=False,
        default_value="Default Value",
    )
    assert extractor.extract(xml_node) == "Default Value"


def test_text_extractor_extra_function(xml_node: ET.Element):
    extractor = TextExtractor(
        None, "./FieldOne/FieldTwo", extra_function=lambda x: x.lstrip("Value ")
    )
    assert extractor.extract(xml_node) == "Field Two"


def test_attribute_extractor(xml_node: ET.Element):
    extractor = AttributeExtractor(None, "./FieldOne", "TagOne")
    assert extractor.extract(xml_node) == "TagOneValue"


def test_custom_extractor(xml_node: ET.Element):
    def extract_and_cast(article: ET.Element):
        value = article.find("./FieldOne/FieldInt").text
        return int(value)

    extractor = CustomExtractor(None, extract_and_cast)
    assert extractor.extract(xml_node) == 5


def test_constant_extractor(xml_node: ET.Element):
    extractor = ConstantExtractor(None, "Constant")
    assert extractor.extract(xml_node) == "Constant"
