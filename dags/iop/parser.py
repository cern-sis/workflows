import xml.etree.ElementTree as ET

from common.constants import ARXIV_EXTRACTION_PATTERN
from common.parsing.parser import IParser
from common.parsing.xml_extractors import AttributeExtractor, CustomExtractor
from common.utils import parse_to_int
from idutils import is_arxiv
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
        try:
            return contrib_type.find("name/surname").text
        except AttributeError:
            self.logger.error("Surname is not found in XML", dois=self.dois)

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
        institution_and_country = {}
        try:
            id = reffered_id.get("rid")
        except AttributeError:
            self.logger.error("Referred id is not found")
        institution = self._get_institution(article, id)
        country = self._get_country(article, id)
        if country:
            institution_and_country["country"] = country
        if institution and country:
            institution_and_country["institution"] = ", ".join([institution, country])
        return institution_and_country

    def _get_institution(self, article, id):
        try:
            institution = article.find(
                f"front/article-meta/contrib-group/aff[@id='{id}']/institution"
            ).text
            return institution
        except AttributeError:
            self.logger.error("Institution is not found in XML")
            return

    def _get_country(self, article, id):
        try:
            country = article.find(
                f"front/article-meta/contrib-group/aff[@id='{id}']/country"
            ).text
            return country
        except AttributeError:
            self.logger.error("Country is not found in XML")
            return
