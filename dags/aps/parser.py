import re

from common.parsing.json_extractors import CustomExtractor, NestedValueExtractor
from common.parsing.parser import IParser
from common.utils import construct_license
from inspire_utils.record import get_value
from structlog import get_logger


class APSParser(IParser):
    def __init__(self) -> None:
        self.logger = get_logger().bind(class_name=type(self).__name__)
        article_type_mapping = {
            "article": "article",
            "erratum": "erratum",
            "editorial": "editorial",
            "retraction": "retraction",
            "essay": "other",
            "comment": "other",
            "letter-to-editor": "other",
            "rapid": "other",
            "brief": "other",
            "reply": "other",
            "announcement": "other",
            "nobel": "other",
        }

        extractors = [
            NestedValueExtractor(
                "dois", json_path="identifiers.doi", extra_function=lambda x: [x]
            ),
            NestedValueExtractor(
                "journal_doctype",
                json_path="articleType",
                extra_function=lambda x: article_type_mapping.get(x, "other"),
            ),
            NestedValueExtractor(
                "page_nr", json_path="numPages", extra_function=lambda x: [x]
            ),
            NestedValueExtractor(
                "arxiv_eprints",
                json_path="identifiers.arxiv",
                extra_function=lambda x: [
                    {"value": re.sub("arxiv:", "", x, flags=re.IGNORECASE)}
                ],
            ),
            NestedValueExtractor("abstract", json_path="abstract.value"),
            NestedValueExtractor("title", json_path="title.value"),
            CustomExtractor("authors", self._form_authors),
            NestedValueExtractor("journal_title", json_path="journal.name"),
            NestedValueExtractor("journal_issue", json_path="issue.number"),
            NestedValueExtractor("journal_volume", json_path="volume.number"),
            NestedValueExtractor(
                "journal_year",
                json_path="date",
                extra_function=lambda x: int(x[:4] if (len(x) >= 4) else 0000),
            ),
            NestedValueExtractor("date_published", json_path="date"),
            NestedValueExtractor(
                "copyright_holder",
                json_path="rights.copyrightHolders",
                extra_function=lambda x: x[0]["name"] if len(x) >= 1 else "",
            ),
            NestedValueExtractor("copyright_year", json_path="rights.copyrightYear"),
            NestedValueExtractor(
                "copyright_statement", json_path="rights.rightsStatement"
            ),
            CustomExtractor(
                "license",
                extraction_function=lambda x: self._get_licenses(x),
            ),
            CustomExtractor(
                "collections",
                extraction_function=lambda x: ["HEP", "Citeable", "Published"],
            ),
            CustomExtractor("field_categories", self._get_field_categories),
            CustomExtractor("files", self._build_files_data),
        ]

        super().__init__(extractors)

    def _form_authors(self, article):
        authors = article["authors"]
        return [
            {
                "full_name": author["name"],
                "given_names": author["firstname"],
                "surname": author["surname"],
                "affiliations": self._get_affiliations(
                    article, author["affiliationIds"]
                )
                if "affiliationIds" in author
                else [],
            }
            for author in authors
            if author["type"] == "Person"
        ]

    def _get_affiliations(self, article, affiliationIds):
        parsed_affiliations = [
            {
                "value": affiliation["name"],
                "organization": (",").join(affiliation["name"].split(",")[:-1]),
                "country": affiliation["name"].split(", ")[-1:][0],
            }
            for affiliation in article["affiliations"]
            if affiliation["id"] in affiliationIds
        ]
        return parsed_affiliations

    def _get_field_categories(self, article):
        return [
            {
                "term": term.get("label"),
                "scheme": "APS",
                "source": "",
            }
            for term in get_value(
                article, "classificationSchemes.subjectAreas", default=""
            )
        ]

    def _build_files_data(self, article):
        doi = get_value(article, "identifiers.doi")
        return [
            {
                "url": "http://harvest.aps.org/v2/journals/articles/{0}".format(doi),
                "headers": {"Accept": "application/pdf"},
                "name": "{0}.pdf".format(doi),
                "filetype": "pdf",
            },
            {
                "url": "http://harvest.aps.org/v2/journals/articles/{0}".format(doi),
                "headers": {"Accept": "text/xml"},
                "name": "{0}.xml".format(doi),
                "filetype": "xml",
            },
        ]

    def _get_licenses(self, x):
        try:
            rights = x["rights"]["licenses"]
            licenses = []
            for right in rights:
                url = right["url"]
                clean_url_parts = list(filter(bool, url.split("/")))
                version = clean_url_parts[-1]
                license_type = clean_url_parts[-2]
                licenses.append(
                    construct_license(
                        url=url, license_type=license_type.upper(), version=version
                    )
                )
            return licenses
        except Exception:
            self.logger.error("Error was raised while parsing licenses.")
