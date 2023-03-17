import xml.etree.ElementTree as ET

from common.parsing.parser import IParser
from common.parsing.xml_extractors import CustomExtractor
from common.utils import get_text_value
from structlog import get_logger


class OUPParser(IParser):
    def __init__(self) -> None:
        self.logger = get_logger().bind(class_name=type(self).__name__)
        self.article_type_mapping = {
            "research-article": "article",
            "corrected-article": "article",
            "original-article": "article",
            "correction": "corrigendum",
            "addendum": "addendum",
            "editorial": "editorial",
        }

        extractors = [
            CustomExtractor(
                destination="dois", extraction_function=self._get_dois, required=True
            ),
            CustomExtractor(
                destination="journal_doctype",
                extraction_function=self._get_journal_doctype,
            ),
        ]
        super().__init__(extractors)

    def _get_dois(self, article: ET.Element):
        source = ".front/article-meta/article-id/[@pub-id-type='doi']"
        doi_element = article.find(source)
        doi = get_text_value(doi_element)
        if not doi:
            return []
        self.logger.msg("Parsing dois for article", dois=doi)
        self.dois = doi
        return [doi]

    def _get_journal_doctype(self, article: ET.Element):
        self.logger.msg("Parsing journal doctype for article", dois=self.dois)
        journal_doctype_raw = article.find("front/..").get("article-type")
        if not journal_doctype_raw:
            return
        try:
            journal_doctype = self.article_type_mapping[journal_doctype_raw]
        except KeyError:
            journal_doctype = "other"
            self.logger.warning(
                "There are unmapped article types for article",
                journal_doctype=journal_doctype,
            )
        return journal_doctype
