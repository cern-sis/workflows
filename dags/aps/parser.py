import re

from common.parsing.json_extractors import CustomExtractor, NestedValueExtractor
from common.parsing.parser import IParser
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
            NestedValueExtractor("dois", json_path="identifiers.doi"),
            NestedValueExtractor(
                "journal_doctype",
                json_path="articleType",
                extra_function=lambda x: article_type_mapping[x],
            ),
            NestedValueExtractor("page_nr", json_path="numPages"),
            NestedValueExtractor(
                "arxiv_eprints",
                json_path="identifiers.arxiv",
                extra_function=lambda x: {
                    "value": re.sub("arxiv:", "", x, flags=re.IGNORECASE)
                },
            ),
            NestedValueExtractor("abstract", json_path="abstract.value"),
            NestedValueExtractor("title", json_path="title.value"),
            CustomExtractor("authors", self._form_authors),
            NestedValueExtractor("journal_title", json_path="journal.name"),
            NestedValueExtractor("journal_issue", json_path="issue.number"),
            NestedValueExtractor("journal_volume", json_path="volume.number"),
            NestedValueExtractor(
                "journal_year", json_path="date", extra_function=lambda x: int(x[:4])
            ),
            NestedValueExtractor("date_published", json_path="date"),
            NestedValueExtractor(
                "copyright_holder",
                json_path="rights.copyrightHolders",
                extra_function=lambda x: x[0]["name"],
            ),
            NestedValueExtractor("copyright_year", json_path="rights.copyrightYear"),
            NestedValueExtractor(
                "copyright_statement", json_path="rights.rightsStatement"
            ),
            NestedValueExtractor(
                "licenses",
                json_path="rights.licenses",
                extra_function=lambda x: x[0]["url"],
            ),
            NestedValueExtractor("collections", json_path="HEP.Citeable.Published"),
            CustomExtractor("field_categories", self._get_field_categories),
            CustomExtractor("extra_data", self._build_files_data),
        ]

        super().__init__(extractors)

    def _form_authors(self, article):
        authors = article["authors"]
        return {
            "authors": [
                {
                    "full_name": author["name"],
                    "given_names": author["firstname"],
                    "surname": author["surname"],
                    "affiliations": self._get_affiliations(
                        article, author["affiliationIds"]
                    ),
                }
                for author in authors
                if author["type"] == "Person"
            ]
        }

    def _get_affiliations(self, article, affiliationIds):
        parsed_affiliations = [
            {
                "value": affiliation["name"],
                "organization": (",").join(affiliation["name"].split(",")[:-1]),
                "country": affiliation["name"].split(", ")[-1:],
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
        return {
            "files": [
                {
                    "url": "http://harvest.aps.org/v2/journals/articles/{0}".format(
                        doi
                    ),
                    "headers": {"Accept": "application/pdf"},
                    "name": "{0}.pdf".format(doi),
                    "filetype": "pdf",
                },
                {
                    "url": "http://harvest.aps.org/v2/journals/articles/{0}".format(
                        doi
                    ),
                    "headers": {"Accept": "text/xml"},
                    "name": "{0}.xml".format(doi),
                    "filetype": "xml",
                },
            ]
        }
