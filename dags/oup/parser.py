import datetime
import xml.etree.ElementTree as ET

from common.parsing.parser import IParser
from common.parsing.xml_extractors import (
    AttributeExtractor,
    ConstantExtractor,
    CustomExtractor,
)
from common.utils import construct_license, get_text_value
from hindawi.xml_extractors import HindawiTextExtractor as TextExtractor
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
            TextExtractor(
                destination="dois",
                source="front/article-meta/article-id/[@pub-id-type='doi']",
                extra_function=lambda x: [x],
                default_value=[],
            ),
            TextExtractor(
                destination="dois",
                source="front/article-meta/article-id/[@pub-id-type='doi']",
                extra_function=lambda x: [x],
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
                source="front/article-meta/counts/page-count",
                attribute="count",
                extra_function=lambda x: int(x),
                default_value=[0],
            ),
            TextExtractor(
                destination="abstract",
                source="front/article-meta/abstract/p",
                extra_function=lambda x: x,
                default_value="",
            ),
            TextExtractor(
                destination="title",
                source="front/article-meta/title-group/article-title",
                extra_function=lambda x: x,
                default_value="",
            ),
            # Need an example with subtitle
            TextExtractor(
                destination="subtitle",
                source="front/article-meta/title-group/subtitle",
                extra_function=lambda x: x,
                required=False,
                default_value="",
            ),
            # Different from hepcawrl, need to double check
            CustomExtractor(
                destination="authors",
                extraction_function=self._get_authors,
                default_value=[],
            ),
            # IMPORTANT: IDK HOW WITH COLLAB
            CustomExtractor(
                destination="date_published",
                extraction_function=self._get_published_date,
                default_value="2000-00-00",
            ),
            CustomExtractor(
                destination="journal_title",
                extraction_function=self._get_journal_title,
                default_value="Progress of Theoretical and Experimental Physics",
            ),
            TextExtractor(
                destination="journal_issue",
                source="front/article-meta/issue",
                extra_function=lambda x: x,
                required=False,
                default_value="",
            ),
            TextExtractor(
                destination="journal_volume",
                source="front/article-meta/volume",
                extra_function=lambda x: x,
                required=False,
                default_value="",
            ),
            TextExtractor(
                destination="journal_artid",
                source="front/article-meta/elocation-id",
                extra_function=lambda x: x,
                required=False,
                default_value="",
            ),
            TextExtractor(
                destination="journal_year",
                source="front/article-meta/volume",
                extra_function=lambda x: x,
                required=False,
                default_value="",
            ),
            TextExtractor(
                destination="copyright_statement",
                source="front/article-meta/permissions/copyright-statement",
                extra_function=lambda x: x,
                required=False,
                default_value="",
            ),
            TextExtractor(
                destination="copyright_year",
                source="front/article-meta/permissions/copyright-year",
                extra_function=lambda x: int(x),
                required=False,
                default_value=2000,
            ),
            CustomExtractor(
                destination="license",
                extraction_function=self._get_license,
                default_value=[],
            ),
            ConstantExtractor(
                destination="collections",
                constant=["Progress of Theoretical and Experimental Physics"],
            ),
        ]

        super().__init__(extractors)

    def _get_journal_doctype(self, article: ET.Element):
        journal_doctype_raw = article.find("front/..").get("article-type")
        journal_doctype = self.article_type_mapping[journal_doctype_raw]
        if "other" in journal_doctype:
            self.logger.warning(
                f"There are unmapped article types for article with this type {journal_doctype}"
            )
        return journal_doctype

    def _get_related_article_doi(self, article: ET.Element):
        journal_doctype_raw = article.find("front/..").get("article-type")
        if journal_doctype_raw in ["correction", "addendum"]:
            self.logger.info("Adding related_article_doi.")
            raw_related_doi = article.find(
                "front/article-meta/related-article[@ext-link-type='doi']"
            )
            return raw_related_doi is not None and raw_related_doi.get("href")

    def _get_arxiv_eprints(self, article: ET.Element):
        arxivs_raw = get_text_value(
            article.find("front/article-meta/article-id/[@pub-id-type='arxiv']")
        )
        arxiv_eprint = arxivs_raw.lower().replace("arxiv:", "")
        return {"value": arxiv_eprint}

    def _get_authors(self, article: ET.Element):
        contributions = article.findall(
            "front/article-meta/contrib-group/contrib[@contrib-type='author']"
        )
        authors = []
        for contribution in contributions:
            surname = get_text_value(contribution.find("name/surname"))
            given_names = get_text_value(contribution.find("name/given-names"))
            email = get_text_value(contribution.find("email"))
            affiliations = contribution.findall("aff")

            full_affiliation = [
                {
                    "institution": get_text_value(
                        affiliation.find(
                            "institution",
                        )
                    ),
                    "country": get_text_value(
                        affiliation.find(
                            "country",
                        )
                    ),
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

    def _get_date(self, date):
        return datetime.date(
            day=int(get_text_value(date.find("day"))),
            month=int(get_text_value(date.find("month"))),
            year=int(get_text_value(date.find("year"))),
        ).isoformat()

    def _get_published_date(self, article: ET.Element):
        date = (
            article.find(
                "front/article-meta/pub-date/[@pub-type='epub']",
            )
            or article.find(
                "front/article-meta/date/[@date-type='published']",
            )
            or article.find(
                "front/article-meta/pub-date/[@pub-type='ppub']",
            )
            or article.find(
                "front/article-meta/pub-date/[@pub-type='ppub']",
            )
        )
        if date is not None:
            return self._get_date(date)
        else:
            return datetime.date.today().isoformat()

        # A little bit different from hepcrawl

    def _get_journal_title(self, article: ET.Element):
        journal_title = get_text_value(
            article.find(
                "front/journal-meta/journal-title-group/journal-title",
            )
        )
        if journal_title is not None:
            return journal_title
        journal_publisher = get_text_value(
            article.find(
                "front/journal-meta/journal-title-group/abbrev-journal-title",
            )
        )
        if journal_publisher is not None:
            return journal_publisher

    def _get_license(self, article):
        licenses = []
        try:
            licenses_url_obj = article.findall(
                "front/article-meta/permissions/license/license-p/ext-link",
            )
            for license_url_obj in licenses_url_obj:
                url = get_text_value(license_url_obj)
                clean_url_parts = list(filter(bool, url.split("/")))
                version = clean_url_parts[-1]
                license_type = clean_url_parts[-2]
                licenses.append(
                    construct_license(
                        url=url, license_type=license_type.upper(), version=version
                    )
                )
        except Exception:
            self.logger.error("Error was raised while parsing licenses")
        return licenses
