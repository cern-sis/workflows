import xml.etree.ElementTree as ET
from typing import List

from common.parsing.extractor import IExtractor


class IParser:
    extractors: List[IExtractor]

    def __init__(self, extractors) -> None:
        self.extractors = extractors

    def parse(self, article: ET.Element):
        return {
            extractor.destination: value
            for extractor in self.extractors
            if (value := extractor.extract(article)) is not None
        }


class ObjectExtractor(IParser, IExtractor):
    def __init__(self, destination, extractors, extra_function=lambda x: x) -> None:
        super().__init__(destination)
        self.destination = destination
        self.extractors = extractors
        self.extra_function = extra_function

    def extract(self, article: ET.Element):
        return self.extra_function(super().parse(article))
