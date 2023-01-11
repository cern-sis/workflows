import xml.etree.ElementTree as ET

from common.constants import ARXIV_EXTRACTION_PATTERN, NODE_ATTRIBUTE_NOT_FOUND_ERRORS
from common.parsing.parser import IParser
from common.parsing.xml_extractors import AttributeExtractor, CustomExtractor
from common.utils import extract_text, parse_to_int
from idutils import is_arxiv
from inspire_utils.date import PartialDate
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
        self.dois = None
        self.year = None
        self.journal_doctype = None
        self.logger = get_logger().bind(class_name=type(self).__name__)
        extractors = [
            CustomExtractor(
                destination="dois",
                extraction_function=self._get_dois,
                required=True,
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
                destination="arxiv_eprints",
                extraction_function=self._get_extracted_arxiv_eprint_value,
            ),
            AttributeExtractor(
                destination="page_nr",
                source="front/article-meta/counts/page-count",
                attribute="count",
                extra_function=lambda x: [parse_to_int(x)] if parse_to_int(x) else None,
            ),
            CustomExtractor(
                destination="authors",
                extraction_function=self._extract_authors,
                required=True,
            ),
            CustomExtractor(
                destination="date_published",
                extraction_function=self._get_date_published,
            ),
            CustomExtractor(
                destination="journal_year",
                extraction_function=self._get_journal_year,
                required=True,
            ),
            CustomExtractor(
                destination="copyright",
                extraction_function=self._get_copyright,
                required=True,
            ),
        ]
        super().__init__(extractors)

    def _get_dois(self, article: ET.Element):
        node = article.find("front/article-meta/article-id/[@pub-id-type='doi']")
        if node is None:
            return
        dois = node.text
        if dois:
            self.logger.msg("Parsing dois for article", dois=dois)
            self.dois = dois
            return [dois]
        return

    def _get_journal_doctype(self, article: ET.Element):
        node = article.find(".")
        value = node.get("article-type")
        if not value:
            self.logger.error("Article-type is not found in XML", dois=self.dois)
            return None
        try:
            self.journal_doctype = self.article_type_mapping[value]
            return self.journal_doctype
        except KeyError:
            self.logger.error(
                "Unmapped article type", dois=self.dois, article_type=value
            )
        except Exception:
            self.logger.error("Unknown error", dois=self.dois)

    def _get_related_article_doi(self, article):
        if self.journal_doctype not in ["corrigendum", "addendum"]:
            return
        node = article.find("front/article-meta/related-article[@ext-link-type='doi']")
        try:
            related_article_doi = node.get("href")
            if related_article_doi:
                self.logger.info("Adding related_article_doi.")
                return [related_article_doi]
        except AttributeError:
            self.logger.error("No related article dois found", dois=self.dois)
            return

    def _get_extracted_arxiv_eprint_value(self, article):
        arxivs_value = article.find(
            "front/article-meta/custom-meta-group/custom-meta/meta-value"
        )
        try:
            arxiv_value = ARXIV_EXTRACTION_PATTERN.sub("", arxivs_value.text.lower())
            if is_arxiv(arxiv_value):
                return [{"value": arxiv_value}]
            self.logger.error("The arXiv value is not valid.", dois=self.dois)
        except AttributeError:
            self.logger.error("No arXiv eprints found", dois=self.dois)

    def _get_date_element(self, article):
        date = (
            article.find("front/article-meta/history/date[@date-type='published']")
            or article.find("front/article-meta/history/date[@date-type='epub']")
            or article.find("front/article-meta/history/pub-date[@pub-type='ppub']")
            or article.find("front/article-meta/pub-date")
        )
        return date

    def _get_date_published(self, article):
        date_element = self._get_date_element(article)
        return self._get_date(date_element)

    def _get_date(self, date):
        try:
            year = int(date.find("year").text)
            self.year = year
        except NODE_ATTRIBUTE_NOT_FOUND_ERRORS:
            self.logger.error("Cannot find year of date_published in XML")
        try:
            month = int(date.find("month").text)
        # was discussed with Anne: if the day is not present, we return year and month
        # if the month value is not present - we return just year
        # if the year is not present - the parsing should crash, because according schema
        # the publication_year is required, which is take from date_published
        except NODE_ATTRIBUTE_NOT_FOUND_ERRORS:
            self.logger.error("Cannot find month of date_published in XML")
            month = None
        try:
            day = int(date.find("day").text)
        except NODE_ATTRIBUTE_NOT_FOUND_ERRORS:
            self.logger.error("Cannot find day of date_published in XML")
            day = None
        try:
            date = PartialDate(year=self.year, month=month, day=day)
            return PartialDate.dumps(date)
        except NODE_ATTRIBUTE_NOT_FOUND_ERRORS + (ValueError,):
            return str(self.year)

    def _get_journal_year(self, article):
        return self.year

    def _extract_authors(self, article):
        contrib_types = article.findall(
            "front/article-meta/contrib-group/contrib[@contrib-type='author']"
        )
        authors = []
        surname = ""
        given_names = ""

        for contrib_type in contrib_types:
            surname = self._extract_surname(contrib_type)
            given_names = self._extract_given_names(contrib_type)
            reffered_ids = contrib_type.findall("xref[@ref-type='aff']")
            affiliations = [
                self._get_affiliation_value(article, reffered_id)
                for reffered_id in reffered_ids
                if self._get_affiliation_value(article, reffered_id)
            ]
            author = {}
            if surname:
                author["surname"] = surname
            if given_names:
                author["given_names"] = given_names
            if affiliations:
                author["affiliations"] = affiliations
            if author:
                authors.append(author)
        return authors

    def _extract_surname(self, contrib_type):
        return extract_text(
            article=contrib_type,
            path="name/surname",
            field_name="surname",
            dois=self.dois,
        )

    def _extract_given_names(self, contrib_type):
        try:
            given_names = contrib_type.find("name/given-names").text
            # IOP puts the collaboration in authors as 'author' with the given_name,
            # which value actually is calloboration name
            if "collaboration" not in given_names.lower():
                return given_names
        except AttributeError:
            self.logger.error("Given_names is not found in XML", dois=self.dois)

    def _get_affiliation_value(self, article, reffered_id):
        try:
            institution_and_country = {}
            id = reffered_id.get("rid")
            institution = self._get_institution(article, id)
            country = self._get_country(article, id)
            if country:
                institution_and_country["country"] = country
            if institution and country:
                institution_and_country["institution"] = ", ".join(
                    [institution, country]
                )
            return institution_and_country
        except AttributeError:
            self.logger.error("Referred id is not found")

    def _get_institution(self, article, id):
        return extract_text(
            article=article,
            path=f"front/article-meta/contrib-group/aff[@id='{id}']/institution",
            field_name="institution",
            dois=self.dois,
        )

    def _get_country(self, article, id):
        return extract_text(
            article=article,
            path=f"front/article-meta/contrib-group/aff[@id='{id}']/country",
            field_name="country",
            dois=self.dois,
        )

    def _extract_copyright_year(self, article):
        return extract_text(
            article=article,
            path="front/article-meta/permissions/copyright-year",
            field_name="copyright_year",
            dois=self.dois,
        )

    def _extract_copyright_statement(self, article):
        return extract_text(
            article=article,
            path="front/article-meta/permissions/copyright-statement",
            field_name="copyright_statement",
            dois=self.dois,
        )

    def _get_copyright(self, article):
        copyright = {}
        extracted_year = self._extract_copyright_year(article)
        if extracted_year:
            copyright["year"] = extracted_year
        extracted_statement = self._extract_copyright_statement(article)
        if extracted_statement:
            copyright["copyright_statement"] = extracted_statement
        return [copyright]
