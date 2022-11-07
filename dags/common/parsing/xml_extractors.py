import xml.etree.ElementTree as ET

from common.parsing.extractor import IExtractor
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
    ) -> None:
        super().__init__(destination)
        self.destination = destination
        self.source = source
        self.prefixes = prefixes
        self.required = required
        self.default_value = default_value
        self.extra_function = extra_function
        self.logger = get_logger().bind(class_name=type(self).__name__)

    def extract(self, article: ET.Element):
        if self.prefixes:
            node_with_prefix = self.extra_function(
                article.find(self.source, self.prefixes).text
            )
            return node_with_prefix
        node = article.find(self.source)
        if self.required and node is None:
            raise RequiredFieldNotFoundExtractionError(self.source)
        if node is None:
            return self.default_value
        return self.extra_function(article.find(self.source).text)


class AttributeExtractor(IExtractor):
    def __init__(
        self,
        destination,
        source,
        attribute,
        default_value=None,
        required=False,
        extra_function=lambda x: x,
    ) -> None:
        super().__init__(destination)
        self.destination = destination
        self.source = source
        self.attribute = attribute
        self.extra_function = extra_function
        self.default_value = default_value
        self.required = required

    def extract(self, article: ET.Element):
        value = article.find(self.source)
        if value is not None:
            return self.extra_function(value.get(self.attribute))
        if self.required and value is None:
            raise RequiredFieldNotFoundExtractionError(self.source)
        return self.default_value


class CustomExtractor(IExtractor):
    def __init__(
        self, destination, extraction_function, required=False, default_value=None
    ) -> None:
        super().__init__(destination)
        self.destination = destination
        self.extraction_function = extraction_function
        self.default_value = default_value
        self.required = required

    def extract(self, article: ET.Element):
        value = self.extraction_function(article)
        if value is not None:
            return value
        if self.required and value is None:
            raise RequiredFieldNotFoundExtractionError(self.destination)
        return self.default_value


class ConstantExtractor(IExtractor):
    def __init__(self, destination, constant) -> None:
        super().__init__(destination)
        self.constant = constant

    def extract(self, _: ET.Element):
        return self.constant


class RequiredFieldNotFoundExtractionError(RuntimeError):
    def __init__(self, error_field, *args: object) -> None:
        super().__init__(f"Required field not found in XML: {error_field}")
