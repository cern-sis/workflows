import xml.etree.ElementTree as ET

from common.parsing.parser import IParser
from common.parsing.xml_extractors import CustomExtractor
from structlog import get_logger


class IOPParser(IParser):
    article_type_mapping = {
        "research-article": "article",
        "corrected-article": "article",
        "original-article": "article",
        "correction": "corrigendum",
        "addendum": "addendum",
        "editorial": "editorial",
    }

    def __init__(self) -> None:
        self.logger = get_logger().bind(class_name=type(self).__name__)
        extractors = [
            CustomExtractor(
                destination="dois",
                extraction_function=self._get_dois,
                required=True,
            ),
        ]
        super().__init__(extractors)

    def _get_dois(self, article: ET.Element):
        node = article.find("front/article-meta/article-id/[@pub-id-type='doi']")
        if node is None:
            return None
        dois = node.text
        if dois:
            self.logger.msg("Parsing dois for article", dois=dois)
            return [dois]
        return None
