import datetime
import xml.etree.ElementTree as ET

from common.parsing.parser import IParser
from common.parsing.xml_extractors import (
    AttributeExtractor,
    ConstantExtractor,
    CustomExtractor,
    TextExtractor,
)
from common.utils import (
    clean_text,
    get_license_type_and_version_from_url,
    get_text_value,
)
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
        self.year = None

        extractors = [
            CustomExtractor(
                destination="dois", extraction_function=self._get_dois, required=True
            ),
            AttributeExtractor(
                destination="page_nr",
                source="front/article-meta/counts/page-count",
                attribute="count",
                extra_function=lambda x: int(x),
            ),
            CustomExtractor(
                destination="journal_doctype",
                extraction_function=self._get_journal_doctype,
            ),
            CustomExtractor(
                destination="arxiv_eprints",
                extraction_function=self._get_arxiv_eprints,
            ),
            CustomExtractor(
                destination="authors",
                extraction_function=self._get_authors,
                required=True,
            ),
            TextExtractor(
                destination="abstract",
                source="front/article-meta/abstract/p",
                all_content_between_tags=True,
            ),
            TextExtractor(
                destination="title",
                source="front/article-meta/title-group/article-title",
                all_content_between_tags=True,
            ),
            CustomExtractor(
                destination="date_published",
                extraction_function=self._get_published_date,
            ),
            TextExtractor(
                destination="journal_issue",
                source="front/article-meta/issue",
                required=False,
            ),
            CustomExtractor(
                destination="journal_volume",
                extraction_function=self._get_journal_volume,
            ),
            CustomExtractor(
                destination="journal_year",
                extraction_function=self._get_journal_year,
                required=True,
            ),
            TextExtractor(
                destination="journal_artid",
                source="front/article-meta/elocation-id",
                required=False,
            ),
            TextExtractor(
                destination="copyright_year",
                source="front/article-meta/permissions/copyright-year",
                extra_function=lambda x: int(x),
                required=False,
            ),
            TextExtractor(
                destination="copyright_statement",
                source="front/article-meta/permissions/copyright-statement",
                all_content_between_tags=True,
                required=False,
            ),
            CustomExtractor(
                destination="journal_title",
                extraction_function=self._get_journal_title,
                required=True,
            ),
            CustomExtractor(
                destination="license",
                extraction_function=self._get_license,
                required=True,
            ),
            ConstantExtractor(
                destination="collections",
                value=["Progress of Theoretical and Experimental Physics"],
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
        if "other" in journal_doctype:
            self.logger.warning(
                "There are unmapped article types for article",
                journal_doctype=journal_doctype,
            )
        return journal_doctype

    def _get_arxiv_eprints(self, article: ET.Element):
        arxivs_raw = get_text_value(
            article.find("front/article-meta/article-id/[@pub-id-type='arxiv']")
        )
        if not arxivs_raw:
            return
        arxiv_eprint = arxivs_raw.lower().replace("arxiv:", "")
        if not arxiv_eprint:
            return
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
            full_affiliation = []
            for affiliation in affiliations:
                country = get_text_value(
                    affiliation.find(
                        "country",
                    )
                )
                institution = get_text_value(
                    affiliation.find(
                        "institution",
                    )
                )
                if country:
                    country = country.capitalize()
                full_affiliation.append(
                    {"institution": institution, "country": country}
                )

            if not all([surname, given_names, email]) and not full_affiliation:
                pass
            else:
                authors.append(
                    {
                        "surname": surname,
                        "given_names": given_names,
                        "email": email,
                        "affiliations": full_affiliation,
                    }
                )
        return authors

    def _get_date(self, article):
        year = article.find("year").text
        month = article.find("month").text
        day = article.find("day").text
        if year and month and day:
            return datetime.date(
                day=int(day), month=int(month), year=int(year)
            ).isoformat()

    def _get_published_date(self, article: ET.Element):
        date = (
            article.find("front/article-meta/pub-date/[@pub-type='epub']")
            or article.find("front/article-meta/date/[@date-type='published']")
            or article.find("front/article-meta/pub-date/[@pub-type='ppub']")
        )
        if date is not None:
            return self._get_date(date)

    def _get_journal_volume(self, article):
        journal_volume = get_text_value(article.find("front/article-meta/volume"))
        self.year = journal_volume
        return journal_volume

    def _get_journal_year(self, article):
        return self.year

    def _get_journal_title(self, article: ET.Element):
        journal_title = get_text_value(
            article.find(
                "front/journal-meta/journal-title-group/journal-title",
            )
        )
        if journal_title:
            return clean_text(journal_title)
        journal_title_short_form = get_text_value(
            article.find(
                "front/journal-meta/journal-title-group/abbrev-journal-title/[@abbrev-type='pubmed']"
            )
        )
        if journal_title_short_form:
            return clean_text(journal_title_short_form)

        journal_publisher = get_text_value(
            article.find(
                "front/journal-meta/journal-title-group/abbrev-journal-title/[@abbrev-type='publisher']"
            )
        )
        if journal_publisher:
            return clean_text(journal_publisher)

    def _get_license(self, article: ET.Element):
        licenses = []
        licenses_nodes = article.findall(
            "front/article-meta/permissions/license/license-p/ext-link"
        )
        for license_node in licenses_nodes:
            try:
                url = get_text_value(license_node)
                type_and_version = get_license_type_and_version_from_url(url=url)
                if type_and_version:
                    licenses.append(type_and_version)
            except (KeyError, TypeError):
                self.logger.error("License is not found in XML.", dois=self.dois)
        return licenses
