import xml.etree.ElementTree as ET

from common.constants import WHITE_SPACES
from common.exceptions import RequiredFieldNotFoundExtractionError
from common.parsing.extractor import IExtractor
from common.utils import check_value
from structlog import get_logger


class TextExtractor(IExtractor):
    def __init__(
        self,
        destination,
        source,
        required=True,
        default_value=None,
        extra_function=lambda s: s,
        prefixes=None,
        all_content_between_tags=False,
    ):
        super().__init__(destination)

        self.destination = destination
        self.source = source
        self.prefixes = prefixes
        self.required = required
        self.default_value = default_value
        self.extra_function = extra_function
        self.all_content_between_tags = all_content_between_tags
        self.logger = get_logger().bind(class_name=type(self).__name__)

    def _get_text_value(self, raw_value):
        try:
            return raw_value.text
        except AttributeError:
            self.logger.error(f"{self.destination} is not found in XML")
            return

    def _get_content_as_text_value(self, node):
        try:
            values_in_regular_tags = [node.text or ""]
            values_math_expression_and_styling_tags = [
                ET.tostring(el).decode("ascii") for el in node
            ]
            extracted_value = " ".join(
                values_in_regular_tags + values_math_expression_and_styling_tags
            )
            return WHITE_SPACES.sub(" ", extracted_value).strip()
        except AttributeError:
            self.logger.error(f"{self.destination} is not found in XML")
            return

    def _process_text_with_extra_function(self, text):
        if text:
            try:
                return self.extra_function(text.replace('"', "'"))
            except Exception:
                self.logger.error("Error in extra function with value", text=text)

    def extract(self, article):
        if self.prefixes:
            node_with_prefix = self.extra_function(
                article.find(self.source, self.prefixes).text
            )
            return node_with_prefix
        node = article.find(self.source)
        if self.all_content_between_tags:
            value = self._get_content_as_text_value(node)
        else:
            value = self._get_text_value(node)
        processed_value = self._process_text_with_extra_function(value)

        if check_value(processed_value):
            return processed_value
        if self.required:
            raise RequiredFieldNotFoundExtractionError(self.destination)
        return self.default_value


class AttributeExtractor(IExtractor):
    def __init__(
        self,
        destination,
        source,
        attribute,
        default_value=None,
        required=False,
        extra_function=lambda x: x,
    ) :
        super().__init__(destination)
        self.destination = destination
        self.source = source
        self.attribute = attribute
        self.extra_function = extra_function
        self.default_value = default_value
        self.required = required
        self.logger = get_logger().bind(class_name=type(self).__name__)

    def _get_attribute_value(self, raw_value):
        try:
            return raw_value.get(self.attribute)
        except AttributeError:
            return None

    def _process_attribute_with_extra_function(self, attribute):
        if attribute:
            try:
                return self.extra_function(attribute)
            except Exception:
                self.logger.error(
                    "Error in extra function with value", attribute=attribute
                )

    def extract(self, article):
        node = article.find(self.source)
        value = self._get_attribute_value(node)
        processed_value = self._process_attribute_with_extra_function(value)

        if check_value(processed_value):
            return processed_value
        if self.required:
            raise RequiredFieldNotFoundExtractionError(self.destination)
        return self.default_value


class CustomExtractor(IExtractor):
    def __init__(
        self, destination, extraction_function, required=False, default_value=None
    ) :
        super().__init__(destination)
        self.destination = destination
        self.extraction_function = extraction_function
        self.default_value = default_value
        self.required = required

    def extract(self, article):
        value = self.extraction_function(article)
        if check_value(value):
            return value
        if self.required:
            raise RequiredFieldNotFoundExtractionError(self.destination)
        return self.default_value


class ConstantExtractor(IExtractor):
    def __init__(
        self,
        destination,
        value,
        required=False,
    ) :
        super().__init__(destination)
        self.destination = destination
        self.required = required
        self.value = value

    def extract(self, article):
        if not self.value and self.required:
            raise RequiredFieldNotFoundExtractionError(self.destination)
        return self.value
