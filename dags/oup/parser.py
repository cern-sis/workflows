import datetime
import xml.etree.ElementTree as ET

from common.parsing.parser import IParser
from common.parsing.xml_extractors import (
    AttributeExtractor,
    ConstantExtractor,
    CustomExtractor,
)
from common.utils import construct_license
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
                source="prefix:front/prefix:article-meta/prefix:issue",
                extra_function=lambda x: x,
                required=False,
                prefixes=self.prefixes,
                default_value="",
            ),
            TextExtractor(
                destination="journal_volume",
                source="prefix:front/prefix:article-meta/prefix:volume",
                extra_function=lambda x: x,
                required=False,
                prefixes=self.prefixes,
                default_value="",
            ),
            TextExtractor(
                destination="journal_artid",
                source="prefix:front/prefix:article-meta/prefix:elocation-id",
                extra_function=lambda x: x,
                required=False,
                prefixes=self.prefixes,
                default_value="",
            ),
            # Different from hepcrawl, there looks like can be more than one volume, can it be (journal_year and volume are the same)?
            TextExtractor(
                destination="journal_year",
                source="prefix:front/prefix:article-meta/prefix:volume",
                extra_function=lambda x: x,
                required=False,
                prefixes=self.prefixes,
                default_value="",
            ),
            TextExtractor(
                destination="copyright_statement",
                source="prefix:front/prefix:article-meta/prefix:permissions/prefix:copyright-statement",
                extra_function=lambda x: x,
                required=False,
                prefixes=self.prefixes,
                default_value="",
            ),
            # I cannot find holder, maybe there is none?
            TextExtractor(
                destination="copyright_holder",
                source="prefix:front/prefix:article-meta/prefix:permissions/prefix:copyright-holder",
                extra_function=lambda x: x,
                required=False,
                prefixes=self.prefixes,
                default_value="",
            ),
            TextExtractor(
                destination="copyright_year",
                source="prefix:front/prefix:article-meta/prefix:permissions/prefix:copyright-year",
                extra_function=lambda x: int(x),
                required=False,
                prefixes=self.prefixes,
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

    def _get_authors(self, article: ET.Element):
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

    def _get_date(self, date):
        return datetime.date(
            day=int(date.find("prefix:day", self.prefixes).text),
            month=int(date.find("prefix:month", self.prefixes).text),
            year=int(date.find("prefix:year", self.prefixes).text),
        ).isoformat()

    def _get_published_date(self, article: ET.Element):
        print(
            article.find(
                "prefix:front/prefix:article-meta/prefix:pub-date/[@pub-type='epub']",
                self.prefixes,
            )
        )
        date = (
            article.find(
                "prefix:front/prefix:article-meta/prefix:pub-date/[@pub-type='epub']",
                self.prefixes,
            )
            or article.find(
                "prefix:front/prefix:article-meta/prefix:date/[@date-type='published']",
                self.prefixes,
            )
            or article.find(
                "prefix:front/prefix:article-meta/prefix:pub-date/[@pub-type='ppub']",
                self.prefixes,
            )
            or article.find(
                "prefix:front/prefix:article-meta/prefix:pub-date/[@pub-type='ppub']",
                self.prefixes,
            )
        )
        if date is not None:
            return self._get_date(date)
        else:
            # In the worst case we return today
            return datetime.date.today().isoformat()

        # A little bit different from hepcrawl

    def _get_journal_title(self, article: ET.Element):
        journal_title = article.find(
            "prefix:front/prefix:journal-meta/prefix:journal-title-group/prefix:journal-title",
            self.prefixes,
        )
        if journal_title is not None:
            return journal_title.text
        journal_publisher = article.find(
            "prefix:front/prefix:journal-meta/prefix:journal-title-group/prefix:abbrev-journal-title",
            self.prefixes,
        )
        if journal_publisher is not None:
            return journal_publisher.text

    def _get_license(self, article):
        licenses = []
        try:
            licenses_url_obj = article.findall(
                "prefix:front/prefix:article-meta/prefix:permissions/prefix:license/prefix:license-p/prefix:ext-link",
                self.prefixes,
            )
            print(licenses_url_obj, "KSDJKJSDK ")
            for license_url_obj in licenses_url_obj:
                url = license_url_obj.text
                clean_url_parts = list(filter(bool, url.split("/")))
                version = clean_url_parts[-1]
                license_type = clean_url_parts[-2]
                print(url, license_type, version)
                licenses.append(
                    construct_license(
                        url=url, license_type=license_type.upper(), version=version
                    )
                )
        except Exception:
            self.logger.error("Error was raised while parsing licenses")
        return licenses
