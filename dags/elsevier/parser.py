import xml.etree.ElementTree as ET

from common.parsing.parser import IParser
from common.parsing.xml_extractors import (
    AttributeExtractor,
    CustomExtractor,
    TextExtractor,
)
from common.utils import extract_text
from structlog import get_logger


class ElsevierParser(IParser):
    def __init__(self) -> None:
        self.dois = None
        self.year = None
        self.journal_doctype = None
        self.collaborations = []
        self.logger = get_logger().bind(class_name=type(self).__name__)
        extractors = [
            CustomExtractor(
                destination="dois",
                extraction_function=self._get_dois,
                required=True,
            ),
            TextExtractor(
                destination="abstract",
                source="head/abstract/abstract-sec/simple-para",
                all_content_between_tags=True,
            ),
            TextExtractor(
                destination="title", source="head/title", all_content_between_tags=True
            ),
            CustomExtractor(
                destination="authors",
                extraction_function=self._get_authors,
                required=True,
            ),
            TextExtractor(
                destination="collaboration",
                source="author-group/collaboration/text/",
                required=False,
            ),
            TextExtractor(
                destination="copyright_holder",
                source="item-info/copyright",
            ),
            AttributeExtractor(
                destination="copyright_year",
                source="item-info/copyright",
                attribute="year",
            ),
            TextExtractor(
                destination="copyright_statement",
                source="item-info/copyright",
            ),
            TextExtractor(
                destination="journal_artid",
                source="item-info/aid",
            ),
        ]
        super().__init__(extractors)

    def _get_dois(self, article: ET.Element):
        node = article.find("item-info/doi")
        if node is None:
            return
        dois = node.text
        if dois:
            self.logger.msg("Parsing dois for article", dois=dois)
            self.dois = dois
            return [dois]
        return

    def _get_authors(self, article: ET.Element):
        """Get the authors."""
        authors = []
        author_group = article.find("head/author-group")
        author_collab_group = article.find(
            "head/author-group/collaboration/author-group"
        )
        for author_group_ in [author_group, author_collab_group]:
            if not author_group_:
                continue
            authors += self._get_authors_details(author_group_)
        return authors

    def _get_authors_details(self, author_group):
        authors = []
        for author in author_group.findall("author"):
            surname = extract_text(
                article=author, path="surname", field_name="surname", dois=self.dois
            )
            given_names = extract_text(
                article=author,
                path="given-name",
                field_name="given-name",
                dois=self.dois,
            )
            emails = extract_text(
                article=author, path="e-address", field_name="email", dois=self.dois
            )
            ref_ids = [cross.get("refid") for cross in author.findall("cross-ref")]
            affiliations = self._get_affiliations(ref_ids, author_group)

            auth_dict = {}
            if surname:
                auth_dict["surname"] = surname
            if given_names:
                auth_dict["given_names"] = given_names
            if affiliations:
                auth_dict["affiliations"] = affiliations
            if emails:
                auth_dict["email"] = emails
            authors.append(auth_dict)

        if not authors:
            self.logger.error("No authors found for article %s." % self.dois)
        return authors

    def _get_affiliations(self, ref_ids, author):
        affiliations = []
        for ref_id in ref_ids:
            affiliation_value = extract_text(
                article=author,
                path=f"affiliation/[@id='{ref_id}']/textfn",
                field_name="affiliation_value",
                dois=self.dois,
            )
            organization = extract_text(
                article=author,
                path=f"affiliation/[@id='{ref_id}']/affiliation/organization",
                field_name="organization",
                dois=self.dois,
            )
            country = extract_text(
                article=author,
                path=f"affiliation/[@id='{ref_id}']/affiliation/country",
                field_name="country",
                dois=self.dois,
            )
            affiliations.append(
                {
                    "value": affiliation_value,
                    "organization": organization,
                    "country": country,
                }
            )
        return affiliations
