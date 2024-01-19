import xml.etree.ElementTree as ET

from common.parsing.parser import IParser
from common.parsing.xml_extractors import (
    AttributeExtractor,
    CustomExtractor,
    TextExtractor,
)
from common.utils import extract_text, parse_country_from_value
from structlog import get_logger


class ElsevierParser(IParser):
    def __init__(self) -> None:
        self.dois = None
        self.year = None
        self.logger = get_logger().bind(class_name=type(self).__name__)
        self.article_type_mapping = {
            "article": "article",
            "sco": "article",
            "fla": "article",
            "abs": "article",
            "rev": "article",
            "add": "addendum",
            "edb": "editorial",
            "edi": "editorial",
            "err": "erratum",
            "ret": "retraction",
            "rem": "retraction",
            "adv": "other",
            "ann": "other",
            "brv": "other",
            "cal": "other",
            "chp": "other",
            "cnf": "other",
            "con": "other",
            "cop": "other",
            "cor": "other",
            "crp": "other",
            "dis": "other",
            "dup": "other",
            "exm": "other",
            "ind": "other",
            "lit": "other",
            "mis": "other",
            "nws": "other",
            "ocn": "other",
            "pgl": "other",
            "pnt": "other",
            "prp": "other",
            "prv": "other",
            "pub": "other",
            "req": "other",
            "ssu": "other",
        }
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
            CustomExtractor(
                destination="journal_doctype",
                extraction_function=self._get_journal_doctype,
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
            self._get_affiliation(
                article=author, ref_id=ref_id, affiliations=affiliations
            )
        if not affiliations:
            for affiliation in author.findall("affiliation"):
                self._get_affiliation(article=affiliation, affiliations=affiliations)
        return affiliations

    def _get_affiliation(self, article, ref_id="", affiliations=[]):
        ref_id_value = f"affiliation/[@id='{ref_id}']/" if ref_id else ""
        affiliation_value = extract_text(
            article=article,
            path=f"{ref_id_value}textfn",
            field_name="affiliation_value",
            dois=self.dois,
        )
        organization = extract_text(
            article=article,
            path=f"{ref_id_value}affiliation/organization",
            field_name="organization",
            dois=self.dois,
        )
        country = extract_text(
            article=article,
            path=f"{ref_id_value}affiliation/country",
            field_name="country",
            dois=self.dois,
        )
        country = country and parse_country_from_value(country)
        if affiliation_value and organization and country:
            affiliations.append(
                {
                    "value": affiliation_value,
                    "organization": organization,
                    "country": country,
                }
            )
        else:
            affiliation_value = extract_text(
                article=article,
                path=f"{ref_id_value}affiliation/address-line",
                field_name="affiliation_value",
                dois=self.dois,
            )
            if affiliation_value:
                affiliations.append(
                    {
                        "value": affiliation_value,
                    }
                )

    def _get_journal_doctype(self, article):
        node = article.find(".")
        value = node.get("docsubtype")
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
