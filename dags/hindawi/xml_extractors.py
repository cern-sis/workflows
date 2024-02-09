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
        pattern = re.compile(r"[\n\t]{0,}" + r"\s{2,}")
        extracted_value = "".join(
            [node.text or ""] + [ET.tostring(el).decode("ascii") for el in node]
        )
        final_value = self.extra_function(pattern.sub("", extracted_value))
        self.logger.info("Extracted value", field=self.destination, value=final_value)
        return final_value

    def extract(self, article):
        if self.prefixes:
            node = article.find(self.source, self.prefixes)
            return self._get_extracted_value(node)

        node = article.find(self.source)
        return self._get_extracted_value(node)
