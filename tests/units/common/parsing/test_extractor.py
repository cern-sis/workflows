import xml.etree.ElementTree as ET

from common.parsing.extractor import IExtractor
from common.parsing.parser import ObjectExtractor
from common.parsing.xml_extractors import (
    AttributeExtractor,
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
            <Empty nothing=""></Empty>
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

    def extract_empty_value(article):
        value = article.find("./FieldOne/Empty").text
        return value

    extractor = ObjectExtractor(
        None,
        [
            TextExtractor("text_value", "./FieldOne/FieldTwo"),
            TextExtractor("text_value2", "./FieldOne/UnexistantField", required=False),
            TextExtractor(
                "text_value3",
                "./FieldOne/UnexistantField",
                required=False,
                default_value="default value",
            ),
            AttributeExtractor("attribute_value", "./FieldOne", "TagOne"),
            AttributeExtractor(
                "attribute_value2",
                "./FieldWhichIsNotThere",
                "TagZero",
                default_value="default value",
            ),
            CustomExtractor("custom_value", extract_and_cast),
            CustomExtractor(
                "custom_value2", extract_empty_value, default_value="default value"
            ),
        ],
    )

    assert extractor.extract(xml_node) == {
        "text_value": "Value Field Two",
        "text_value3": "default value",
        "attribute_value": "TagOneValue",
        "attribute_value2": "default value",
        "custom_value": 5,
        "custom_value2": "default value",
    }


def test_not_existant_required_field_extraction(xml_node):
    def extract_empty_value(article):
        value = article.find("./FieldOne/Empty").text
        return value

    text_extractor_with_not_found_required_field = ObjectExtractor(
        None,
        [
            TextExtractor("text_value", "./FieldOne/UnexistantField"),
        ],
    )
    with raises(RequiredFieldNotFoundExtractionError):
        text_extractor_with_not_found_required_field.extract(xml_node)

    text_extractor_with_not_found_required_field_value = ObjectExtractor(
        None,
        [
            TextExtractor("text_value", "./FieldOne/Empty"),
        ],
    )
    with raises(RequiredFieldNotFoundExtractionError):
        text_extractor_with_not_found_required_field_value.extract(xml_node)

    attribute_extractor_with_not_found_required_field = ObjectExtractor(
        None,
        [
            AttributeExtractor(
                "attribute_value", "./FieldWhichIsNotThere", "TagZero", required=True
            ),
        ],
    )
    with raises(RequiredFieldNotFoundExtractionError):
        attribute_extractor_with_not_found_required_field.extract(xml_node)

    attribute_extractor_with_not_found_required_field_value = ObjectExtractor(
        None,
        [
            AttributeExtractor(
                "attribute_value", "./FieldOne/Empty", "nothing", required=True
            ),
        ],
    )
    with raises(RequiredFieldNotFoundExtractionError):
        attribute_extractor_with_not_found_required_field_value.extract(xml_node)

    custom_extractor_with_not_found_required_field = ObjectExtractor(
        None,
        [
            CustomExtractor("custom_value", extract_empty_value, required=True),
        ],
    )
    with raises(RequiredFieldNotFoundExtractionError):
        custom_extractor_with_not_found_required_field.extract(xml_node)


def test_custom_extractor_with_json_not_serializable_value(xml_node):
    def return_json_not_serializable_value(article):
        return article.find("./FieldOne/FieldInt")

    custom_extractor_with_json_not_serializable_value = ObjectExtractor(
        None,
        [
            CustomExtractor(
                "custom_value", return_json_not_serializable_value, required=True
            ),
        ],
    )
    with raises(RequiredFieldNotFoundExtractionError):
        custom_extractor_with_json_not_serializable_value.extract(xml_node)
