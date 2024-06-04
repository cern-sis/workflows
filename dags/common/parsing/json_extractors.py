from common.parsing.extractor import IExtractor
from inspire_utils.inspire_utils import get_value


class NestedValueExtractor(IExtractor):
    def __init__(
        self,
        destination,
        json_path,
        required=True,
        extra_function=lambda s: s,
    ) -> None:
        super().__init__(destination)
        self.destination = destination
        self.json_path = json_path
        self.required = required
        self.extra_function = extra_function

    def extract(self, article):
        return self.extra_function(get_value(article, self.json_path, default=""))


class CustomExtractor(IExtractor):
    def __init__(self, destination, extraction_function) -> None:
        super().__init__(destination)
        self.destination = destination
        self.extraction_function = extraction_function

    def extract(self, article):
        return self.extraction_function(article)
