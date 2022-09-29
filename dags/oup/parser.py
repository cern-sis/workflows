from common.parsing.json_extractors import NestedValueExtractor
from common.parsing.parser import IParser
from structlog import get_logger


class APSParser(IParser):
    def __init__(self) -> None:
        self.logger = get_logger().bind(class_name=type(self).__name__)
        # article_type_mapping = {
        #     "research-article": "article",
        #     "corrected-article": "article",
        #     "original-article": "article",
        #     "correction": "corrigendum",
        #     "addendum": "addendum",
        #     "editorial": "editorial",
        # }

        extractors = [
            NestedValueExtractor(
                "dois", json_path="identifiers.doi", extra_function=lambda x: [x]
            ),
        ]

        super().__init__(extractors)

    def _form_authors(self, article):
        pass
