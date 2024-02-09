import datetime
import re

from common.exceptions import UnknownLicense
from common.parsing.parser import IParser, ObjectExtractor
from common.parsing.xml_extractors import (
    AttributeExtractor,
    CustomExtractor,
    TextExtractor,
)
from common.utils import construct_license
from structlog import get_logger


class SpringerParser(IParser):
    def __init__(self):
        self.logger = get_logger().bind(class_name=type(self).__name__)
        self.dois = None
        article_type_mapping = {
            "OriginalPaper": "article",
            "ReviewPaper": "review",
            "BriefCommunication": "article",
            "EditorialNotes": "editorial",
            "BookReview": "review",
            "ContinuingEducation": "other",
            "Interview": "other",
            "Letter": "other",
            "Erratum": "erratum",
            "Legacy": "other",
            "Abstract": "other",
            "Report": "other",
            "Announcement": "other",
            "News": "other",
            "Events": "other",
            "Acknowledgments": "other",
            "MediaReport": "other",
            "BibliographicalNote": "other",
            "ProductNotes": "other",
            "Unknown": "other",
        }

        extractors = [
            CustomExtractor(
                destination="dois", extraction_function=self.get_dois, required=True
            ),
            AttributeExtractor(
                "journal_doctype",
                "./Journal/Volume/Issue/Article/ArticleInfo",
                "ArticleType",
                extra_function=lambda x: article_type_mapping[x],
            ),
            CustomExtractor("arxiv_eprints", self._get_arxiv_eprints),
            CustomExtractor("page_nr", self._get_page_nrs),
            CustomExtractor("abstract", self._get_abstract),
            TextExtractor(
                "title",
                "./Journal/Volume/Issue/Article/ArticleInfo/ArticleTitle",
            ),
            CustomExtractor("authors", self._get_authors),
            TextExtractor(
                destination="collaborations",
                source="./Journal/Volume/Issue/Article/ArticleHeader/AuthorGroup/InstitutionalAuthor/InstitutionalAuthorName",
                required=False,
                extra_function=lambda x: [x],
            ),
            TextExtractor(
                destination="journal_title",
                source="./Journal/JournalInfo/JournalTitle",
                extra_function=lambda s: s.lstrip("The "),
            ),
            TextExtractor(
                destination="journal_issue",
                source="./Journal/Volume/Issue/IssueInfo/IssueIDStart",
            ),
            TextExtractor(
                destination="journal_volume",
                source="./Journal/Volume/VolumeInfo/VolumeIDStart",
            ),
            AttributeExtractor("journal_artid", "./Journal/Volume/Issue/Article", "ID"),
            TextExtractor(
                destination="journal_fpage",
                source="./Journal/Volume/Issue/Article/ArticleInfo/ArticleFirstPage",
            ),
            TextExtractor(
                destination="journal_lpage",
                source="./Journal/Volume/Issue/Article/ArticleInfo/ArticleLastPage",
            ),
            TextExtractor(
                destination="journal_year",
                source="./Journal/Volume/Issue/Article/ArticleInfo/*/OnlineDate/Year",
                extra_function=lambda x: int(x),
            ),
            CustomExtractor("date_published", self._get_published_date),
            TextExtractor(
                destination="copyright_holder",
                source="./Journal/Volume/Issue/Article/ArticleInfo/ArticleCopyright/CopyrightHolderName",
            ),
            TextExtractor(
                destination="copyright_year",
                source="./Journal/Volume/Issue/Article/ArticleInfo/ArticleCopyright/CopyrightYear",
                extra_function=lambda x: int(x),
            ),
            TextExtractor(
                destination="copyright_statement",
                source="./Journal/Volume/Issue/Article/ArticleInfo/ArticleCopyright/copyright-statement",
                required=False,
            ),
            CustomExtractor("license", self._get_license),
            TextExtractor(
                destination="collections",
                source="./Journal/JournalInfo/JournalTitle",
                extra_function=lambda x: [x.lstrip("The ")],
            ),
        ]
        super().__init__(extractors)

    def get_dois(self, article):
        source = "./Journal/Volume/Issue/Article/ArticleInfo/ArticleDOI"
        doi_element = article.find(source)
        if doi_element is None:
            return []
        dois = doi_element.text
        self.logger.msg("Parsing dois for article", dois=dois)
        self.dois = dois
        return [dois]

    def _get_abstract(self, article):
        def is_latex_node(node):
            return node.tag == "EquationSource" and node.attrib["Format"] == "TEX"

        paragraph = article.find(
            "./Journal/Volume/Issue/Article/ArticleHeader/Abstract/Para"
        )

        text_to_skip_flatten = [
            child_node.text
            for child in paragraph
            for child_node in child.iter()
            if not is_latex_node(child_node)
        ]

        abstract = " ".join(
            [text for text in paragraph.itertext() if text not in text_to_skip_flatten]
        )
        return re.sub("\\s+", " ", abstract)

    def _get_arxiv_eprints(self, article):
        arxiv_eprints = []
        for arxiv in article.findall(
            "./Journal/Volume/Issue/Article/ArticleInfo/ArticleExternalID[@Type='arXiv']"
        ):
            arxiv_eprints.append({"value": arxiv.text})
        return arxiv_eprints

    def _clean_aff(self, article):
        org_div_node = article.find("./OrgDivision")
        org_name_node = article.find("./OrgName")
        street_node = article.find("./OrgAddress/Street")
        city_node = article.find("./OrgAddress/City")
        state_node = article.find("./OrgAddress/State")
        postcode_node = article.find("./OrgAddress/Postcode")
        country_node = article.find("./OrgAddress/Country")

        result = [
            node.text
            for node in [
                org_div_node,
                org_name_node,
                street_node,
                city_node,
                state_node,
                postcode_node,
                country_node,
            ]
            if node is not None
        ]

        return ", ".join(result), org_name_node.text, country_node.text

    def _get_published_date(self, article):
        year = article.find(
            "./Journal/Volume/Issue/Article/ArticleInfo/*/OnlineDate/Year"
        ).text
        month = article.find(
            "./Journal/Volume/Issue/Article/ArticleInfo/*/OnlineDate/Month"
        ).text
        day = article.find(
            "./Journal/Volume/Issue/Article/ArticleInfo/*/OnlineDate/Day"
        ).text
        return datetime.date(day=int(day), month=int(month), year=int(year)).isoformat()

    def _get_affiliations(self, author_group, contrib):
        affiliations = []
        referred_id = contrib.get("AffiliationIDS")

        if not referred_id:
            self.logger.msg("No referred id linked to this article.")
            return affiliations

        for ref in referred_id.split():
            cleaned_aff = self._clean_aff(
                author_group.find(f"./Affiliation[@ID='{ref}']")
            )
            if cleaned_aff not in affiliations:
                affiliations.append(cleaned_aff)

        mapped_affiliations = [
            {"value": aff, "organization": org, "country": country}
            for aff, org, country, in affiliations
        ]

        return mapped_affiliations

    def _get_authors(self, article):
        authors = []
        for contrib in article.findall(
            "./Journal/Volume/Issue/Article/ArticleHeader/AuthorGroup/Author"
        ):
            author = ObjectExtractor(
                None,
                [
                    AttributeExtractor("orcid", ".", "ORCID"),
                    TextExtractor(
                        destination="surname", source="./AuthorName/FamilyName"
                    ),
                    TextExtractor(
                        destination="given_names", source="./AuthorName/GivenName"
                    ),
                    TextExtractor(
                        destination="email", source="./Contact/Email", required=False
                    ),
                ],
            ).extract(contrib)
            author["affiliations"] = self._get_affiliations(
                article.find(
                    "./Journal/Volume/Issue/Article/ArticleHeader/AuthorGroup"
                ),
                contrib,
            )

            authors.append(author)

        return authors

    def _get_page_nrs(self, article):
        first_page_node = article.find(
            "./Journal/Volume/Issue/Article/ArticleInfo/ArticleFirstPage"
        )
        last_page_node = article.find(
            "./Journal/Volume/Issue/Article/ArticleInfo/ArticleLastPage"
        )

        if first_page_node is not None and last_page_node is not None:
            return [int(last_page_node.text) - int(first_page_node.text) + 1]

        self.logger.warning("No first/last page found. Returning empty page_nrs.")
        return []

    def _get_license(self, article):
        license_node = article.find(
            "./Journal/Volume/Issue/Article/ArticleInfo/ArticleCopyright/License"
        )
        version_node = article.find(
            "./Journal/Volume/Issue/Article/ArticleInfo/ArticleCopyright/License"
        )
        base_url = "https://creativecommons.org/licenses"

        if license_node is not None:
            license_type_parts = license_node.get("SubType").split(" ")
            license_type = "-".join(license_type_parts)
            version = version_node.get("Version")
            try:
                url = f"{base_url}/{license_type_parts[1].lower()}/{version}"
            except IndexError:
                raise UnknownLicense(" ".join(license_type_parts))
            return [
                construct_license(
                    url=url, license_type=license_type.upper(), version=version
                )
            ]

        self.logger.warning("License not found, returning default license.")
        return [
            {
                "license": "CC-BY-3.0",
                "url": "https://creativecommons.org/licenses/by/3.0",
            }
        ]
