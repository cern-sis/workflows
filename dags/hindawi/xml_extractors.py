import re
import xml.etree.ElementTree as ET

from common.parsing.xml_extractors import (
    RequiredFieldNotFoundExtractionError,
    TextExtractor,
)


class HindawiTextExtractor(TextExtractor):
    def _get_none_value(self, value):
        if value:
            return value
        return ""

    def _get_extracted_value(self, node):
        if self.required and node is None:
            raise RequiredFieldNotFoundExtractionError(self.source)
        if node is None:
            return self.default_value
        pattern = re.compile(r"[\n\t]*")
        extracted_value = "".join(
            [pattern.sub("", node.text) or ""]
            + [pattern.sub("", ET.tostring(el).decode("ascii")) for el in node]
        )
        return self.extra_function(extracted_value)

    def extract(self, article: ET.Element):
        if self.prefixes:
            node = article.find(self.source, self.prefixes)
            return self._get_extracted_value(node)

        node = article.find(self.source)
        return self._get_extracted_value(node)


class HindawiTextsExtractor(TextExtractor):
    def _get_none_value(self, value):
        if value:
            return value
        return ""

    def extract(self, article: ET.Element):
        extracted_values = []
        pattern = re.compile(r"[\n\t]*")
        if self.prefixes:
            values = article.findall(self.source, self.prefixes)
            for value in values:
                extracted_values.append(
                    "".join(
                        [pattern.sub("", value.text)]
                        + [
                            pattern.sub("", ET.tostring(el).decode("UTF-8"))
                            for el in value
                        ]
                    )
                )
            print(extracted_values)
            return [
                self.extra_function(extracted_value)
                for extracted_value in extracted_values
            ]
        node = article.findall(self.source)
        if self.required and node is None:
            raise RequiredFieldNotFoundExtractionError(self.source)
        if node is None:
            return self.default_value
        return [
            self.extra_function(extracted_value)
            for extracted_value in article.findall(self.source)
        ]
