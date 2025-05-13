import datetime
import os

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
    def __init__(self, file_path=None):
        self.file_path = file_path
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
                extra_function=lambda x: [int(x)],
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
            CustomExtractor(
                destination="files",
                extraction_function=self._get_local_files,
            ),
        ]
        super().__init__(extractors)

    def _get_dois(self, article):
        source = "front/article-meta/article-id/[@pub-id-type='doi']"
        doi_element = article.find(source)
        doi = get_text_value(doi_element)
        if not doi:
            return []
        self.logger.msg("Parsing dois for article", dois=doi)
        self.dois = doi
        return [doi]

    def _get_journal_doctype(self, article):
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

    def _get_arxiv_eprints(self, article):
        arxiv_eprints = []
        arxivs_raw = article.findall(
            "front/article-meta/article-id/[@pub-id-type='arxiv']"
        )
        for arxiv in arxivs_raw:
            arxiv_text = get_text_value(arxiv)
            arxiv_eprint = arxiv_text.lower().replace("arxiv:", "")
            if arxiv_eprint:
                arxiv_eprints.append({"value": arxiv_eprint})
        return arxiv_eprints

    def _get_authors(self, article):
        contributions = article.findall(
            "front/article-meta/contrib-group/contrib[@contrib-type='author']"
        )
        authors = []
        for contribution in contributions:
            orcid = get_text_value(
                contribution.find("contrib-id[@contrib-id-type='orcid']")
            )
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
                _aff = {"organization": institution}
                if country:
                    country = country.capitalize()
                    _aff["country"] = country
                full_affiliation.append(_aff)

            if not all([surname, given_names, email]) and not full_affiliation:
                pass
            else:
                author = {
                    "surname": surname,
                    "given_names": given_names,
                    "email": email,
                    "affiliations": full_affiliation,
                }
                if orcid:
                    author.update({"orcid": orcid})
                authors.append(author)
        return authors

    def _get_date(self, article):
        year = article.find("year").text
        month = article.find("month").text
        day = article.find("day").text
        if year and month and day:
            return datetime.date(
                day=int(day), month=int(month), year=int(year)
            ).isoformat()

    def _get_published_date(self, article):
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

    def _get_journal_title(self, article):
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

    def _get_license(self, article):
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

    def _get_local_files(self, article):
        if not self.file_path:
            self.logger.error("No file path provided")
            return
        self.logger.msg("Parsing local files", file=self.file_path)

        dir_path = os.path.dirname(self.file_path)
        file_name = os.path.basename(self.file_path).split(".")[0]
        pdf_dir_path = dir_path.replace("xml", "pdf")
        pdfa_dir_path = dir_path.replace(".xml", ".archival")
        pdf_path = os.path.join(pdf_dir_path, f"{file_name}.pdf")
        pdfa_path = os.path.join(pdfa_dir_path, f"{file_name}.pdf")

        files = {
            "xml": self.file_path,
            "pdf": pdf_path,
            "pdfa": pdfa_path,
        }
        self.logger.msg("Local files parsed", files=files)
        return files
