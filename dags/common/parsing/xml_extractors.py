import xml.etree.ElementTree as ET

from common.parsing.extractor import IExtractor


class TextExtractor(IExtractor):
    def __init__(
        self,
        destination,
        source,
        required=True,
        default_value=None,
        extra_function=lambda s: s,
    ) -> None:
        super().__init__(destination)
        self.destination = destination
        self.source = source
        self.required = required
        self.default_value = default_value
        self.extra_function = extra_function

    def extract(self, article: ET.Element):
        node = article.find(self.source)
        if self.required and node is None:
            raise RequiredFieldNotFoundExtractionError(self.source)
        if node is None:
            return self.default_value
        return self.extra_function(article.find(self.source).text)


class AttributeExtractor(IExtractor):
    def __init__(
        self, destination, source, attribute, extra_function=lambda x: x
    ) -> None:
        super().__init__(destination)
        self.destination = destination
        self.source = source
        self.attribute = attribute
        self.extra_function = extra_function

    def extract(self, article: ET.Element):
        return self.extra_function(article.find(self.source).get(self.attribute))


class CustomExtractor(IExtractor):
    def __init__(self, destination, extraction_function) -> None:
        super().__init__(destination)
        self.destination = destination
        self.extraction_function = extraction_function

    def extract(self, article: ET.Element):
        return self.extraction_function(article)


class ConstantExtractor(IExtractor):
    def __init__(self, destination, constant) -> None:
        super().__init__(destination)
        self.constant = constant

    def extract(self, _: ET.Element):
        return self.constant


class RequiredFieldNotFoundExtractionError(RuntimeError):
    def __init__(self, error_field, *args: object) -> None:
        super().__init__(f"Required field not found in XML: {error_field}")
