from common.parsing.parser import IParser
from common.parsing.xml_extractors import CustomExtractor, TextExtractor
from structlog import get_logger


class OUPParser(IParser):
    def __init__(self) -> None:
        self.logger = get_logger().bind(class_name=type(self).__name__)
        self.prefixes = {
            "prefix": "http://specifications.silverchair.com/xsd/1/24/SCJATS-journalpublishing.xsd"
        }
        self.article_type_mapping = {
            "research-article": "article",
            "corrected-article": "article",
            "original-article": "article",
            "correction": "corrigendum",
            "addendum": "addendum",
            "editorial": "editorial",
        }

        extractors = [
            TextExtractor(
                destination="dois",
                source="prefix:front/prefix:article-meta/prefix:article-id/[@pub-id-type='doi']",
                extra_function=lambda x: [x],
                prefixes=self.prefixes,
            ),
            CustomExtractor(
                destination="journal_doctype",
                extraction_function=self._get_journal_doctype,
            ),
            CustomExtractor(
                destination="related_article_doi",
                extraction_function=self._get_related_article_doi,
            ),
            CustomExtractor(
                destination="arxiv_eprints", extraction_function=self._get_arxiv_eprints
            ),
        ]

        super().__init__(extractors)

    def _form_authors(self, article):
        pass

    def _get_journal_doctype(self, article):
        journal_doctype_raw = article.find(
            "prefix:front/..",
            {
                "prefix": "http://specifications.silverchair.com/xsd/1/24/SCJATS-journalpublishing.xsd"
            },
        ).get("article-type")
        journal_doctype = self.article_type_mapping[journal_doctype_raw]
        if "other" in journal_doctype:
            self.logger.warning(
                f"There are unmapped article types for article with this type {journal_doctype}"
            )
        return journal_doctype

    def _get_related_article_doi(self, article):
        journal_doctype_raw = article.find(
            "prefix:front/..",
            {
                "prefix": "http://specifications.silverchair.com/xsd/1/24/SCJATS-journalpublishing.xsd"
            },
        ).get("article-type")
        if journal_doctype_raw in ["correction", "addendum"]:
            self.logger.info("Adding related_article_doi.")
            return article.find(
                "prefix:front/prefix:article-meta/prefix:related-article[@ext-link-type='doi']",
                {
                    "prefix": "http://specifications.silverchair.com/xsd/1/24/SCJATS-journalpublishing.xsd"
                },
            ).get("href")

    def _get_arxiv_eprints(self, article):
        arxiv_eprints = []
        arxivs_raw = article.find(
            "prefix:front/prefix:article-meta/prefix:article-id/[@pub-id-type='arxiv']",
            {
                "prefix": "http://specifications.silverchair.com/xsd/1/24/SCJATS-journalpublishing.xsd"
            },
        ).get("article-type")
        for arxiv in arxivs_raw:
            ar = arxiv.extract().replace("arXiv:", "")
            if ar:
                arxiv_eprints.append({"value": ar})
        return arxiv_eprints
