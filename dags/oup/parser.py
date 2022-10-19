import xml.etree.ElementTree as ET

from common.parsing.parser import IParser
from common.parsing.xml_extractors import AttributeExtractor, CustomExtractor
from hindawi.xml_extractors import HindawiTextExtractor as TextExtractor
from structlog import get_logger


class OUPParser(IParser):
    prefixes = {
        "prefix": "http://specifications.silverchair.com/xsd/1/24/SCJATS-journalpublishing.xsd"
    }

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
            TextExtractor(
                destination="dois",
                source="prefix:front/prefix:article-meta/prefix:article-id/[@pub-id-type='doi']",
                extra_function=lambda x: [x],
                prefixes=self.prefixes,
                default_value=[],
            ),
            CustomExtractor(
                destination="journal_doctype",
                extraction_function=self._get_journal_doctype,
                default_value="",
            ),
            CustomExtractor(
                destination="related_article_doi",
                extraction_function=self._get_related_article_doi,
                default_value=[],
            ),
            CustomExtractor(
                destination="arxiv_eprints",
                extraction_function=self._get_arxiv_eprints,
                default_value=[],
            ),
            AttributeExtractor(
                destination="page_nr",
                source="prefix:front/prefix:article-meta/prefix:counts/prefix:page-count",
                attribute="count",
                extra_function=lambda x: int(x),
                prefixes=self.prefixes,
                default_value=[0],
            ),
            TextExtractor(
                destination="abstract",
                source="prefix:front/prefix:article-meta/prefix:abstract/prefix:p",
                extra_function=lambda x: x,
                prefixes=self.prefixes,
                default_value="",
            ),
            TextExtractor(
                destination="title",
                source="prefix:front/prefix:article-meta/prefix:title-group/prefix:article-title",
                extra_function=lambda x: x,
                prefixes=self.prefixes,
                default_value="",
            ),
            # Need an example with subtitle
            TextExtractor(
                destination="subtitle",
                source="prefix:front/prefix:article-meta/prefix:title-group/prefix:subtitle",
                extra_function=lambda x: x,
                required=False,
                prefixes=self.prefixes,
                default_value="",
            ),
            # Different from hepcawrl, need to double check
            CustomExtractor(
                destination="authors",
                extraction_function=self._get_authors,
                default_value=[],
            ),
        ]

        super().__init__(extractors)

    def _get_journal_doctype(self, article: ET.Element):
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

    def _get_related_article_doi(self, article: ET.Element):
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

    def _get_arxiv_eprints(self, article: ET.Element):
        arxivs_raw = article.find(
            "prefix:front/prefix:article-meta/prefix:article-id/[@pub-id-type='arxiv']",
            {
                "prefix": "http://specifications.silverchair.com/xsd/1/24/SCJATS-journalpublishing.xsd"
            },
        ).text
        arxiv_eprint = arxivs_raw.lower().replace("arxiv:", "")
        return {"value": arxiv_eprint}

    def _get_authors(self, article):
        contributions = article.findall(
            "prefix:front/prefix:article-meta/prefix:contrib-group/prefix:contrib[@contrib-type='author']",
            self.prefixes,
        )
        authors = []
        for contribution in contributions:
            surname = contribution.find(
                "prefix:name/prefix:surname", self.prefixes
            ).text
            given_names = contribution.find(
                "prefix:name/prefix:given-names", self.prefixes
            ).text
            email = (
                contribution.find("prefix:email", self.prefixes) is not None
                and contribution.find("prefix:email", self.prefixes).text
            )
            affiliations = contribution.findall("prefix:aff", self.prefixes)
            full_affiliation = [
                {
                    "institution": affiliation.find(
                        "prefix:institution", self.prefixes
                    ).text,
                    "country": affiliation.find("prefix:country", self.prefixes).text,
                }
                for affiliation in affiliations
            ]
            authors.append(
                {
                    "surname": surname,
                    "given_names": given_names,
                    "email": email,
                    "affiliations": full_affiliation,
                }
            )
        return authors
