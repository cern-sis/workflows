import re

import requests
from common.parsing.json_extractors import CustomExtractor, NestedValueExtractor
from common.parsing.parser import IParser
from common.utils import construct_license
from structlog import get_logger

logger = get_logger()


class JagiellonianParser(IParser):
    def __init__(self) -> None:
        self.logger = get_logger().bind(class_name=type(self).__name__)
        self._ror_cache = {}
        article_type_mapping = {
            "journal-article": "article",
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
            NestedValueExtractor("dois", json_path="DOI", extra_function=lambda x: [x]),
            NestedValueExtractor(
                "journal_doctype",
                json_path="type",
                extra_function=lambda x: article_type_mapping.get(x, "other"),
            ),
            CustomExtractor(
                "page_nr", extraction_function=lambda x: self._calculate_page_nr(x)
            ),
            CustomExtractor(
                "arxiv_eprints",
                extraction_function=lambda x: self._get_arxiv_eprints(x),
            ),
            NestedValueExtractor(
                "abstract",
                json_path="abstract",
                extra_function=lambda x: self._clean_abstract(x),
            ),
            CustomExtractor("title", self._get_title),
            CustomExtractor("authors", self._form_authors),
            NestedValueExtractor("journal_title", json_path="container-title.0"),
            CustomExtractor("journal_title", self._get_journal_title),
            NestedValueExtractor("journal_issue", json_path="issue"),
            NestedValueExtractor("journal_volume", json_path="volume"),
            CustomExtractor(
                "journal_year",
                extraction_function=lambda x: self._get_journal_year(x),
            ),
            CustomExtractor(
                "date_published",
                extraction_function=lambda x: self._get_date_published(x),
            ),
            CustomExtractor(
                "acceptance_date",
                extraction_function=lambda x: self._get_acceptance_date(x),
            ),
            CustomExtractor(
                "reception_date",
                extraction_function=lambda x: self._get_reception_date(x),
            ),
            CustomExtractor(
                "copyright_holder",
                extraction_function=lambda x: self._get_copyright_holder(x),
            ),
            CustomExtractor(
                "copyright_year",
                extraction_function=lambda x: self._get_copyright_year(x),
            ),
            CustomExtractor(
                "copyright_statement",
                extraction_function=lambda x: self._get_copyright_statement(x),
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
            CustomExtractor(
                "files",
                extraction_function=lambda x: self._get_files(x),
            ),
        ]

        super().__init__(extractors)

    def _get_title(self, article):
        if "title" not in article:
            return ""

        title = article["title"]
        if title != []:
            return title[0]
        else:
            return ""

    def _clean_abstract(self, abstract_html):
        if not abstract_html:
            return ""

        abstract_text = re.sub(r"<[^>]+>", " ", abstract_html)
        abstract_text = re.sub(r"\s+", " ", abstract_text).strip()
        return abstract_text

    def _calculate_page_nr(self, article):
        if "page" in article:
            page_str = article.get("page", "")
            if "-" in page_str:
                start, end = page_str.split("-", 1)
                try:
                    return [int(end) - int(start) + 1]
                except (ValueError, TypeError):
                    return [1]
            else:
                return [1]
        elif "article-number" in article:
            return [1]
        return []

    def _get_arxiv_eprints(self, article):
        try:
            if "relation" in article and "has-preprint" in article["relation"]:
                for preprint in article["relation"]["has-preprint"]:
                    if preprint.get("id-type") == "arxiv":
                        return [{"value": preprint.get("id")}]
        except Exception:
            self.logger.error("Error extracting arXiv ID")
        return []

    def _get_journal_year(self, article):
        """Extract journal year from published date."""
        try:
            if "published" in article and "date-parts" in article["published"]:
                return int(article["published"]["date-parts"][0][0])
            elif "issued" in article and "date-parts" in article["issued"]:
                return int(article["issued"]["date-parts"][0][0])
        except (IndexError, TypeError, ValueError):
            self.logger.error("Error extracting journal year")
        return 0

    def _get_date_published(self, article):
        try:
            if "published" in article and "date-parts" in article["published"]:
                date_parts = article["published"]["date-parts"][0]
                if len(date_parts) >= 3:
                    return (
                        f"{date_parts[0]:04d}-{date_parts[1]:02d}-{date_parts[2]:02d}"
                    )
                elif len(date_parts) >= 2:
                    return f"{date_parts[0]:04d}-{date_parts[1]:02d}-01"
                elif len(date_parts) >= 1:
                    return f"{date_parts[0]:04d}-01-01"
            elif "issued" in article and "date-parts" in article["issued"]:
                date_parts = article["issued"]["date-parts"][0]
                if len(date_parts) >= 3:
                    return (
                        f"{date_parts[0]:04d}-{date_parts[1]:02d}-{date_parts[2]:02d}"
                    )
                elif len(date_parts) >= 2:
                    return f"{date_parts[0]:04d}-{date_parts[1]:02d}-01"
                elif len(date_parts) >= 1:
                    return f"{date_parts[0]:04d}-01-01"
        except (IndexError, TypeError):
            self.logger.error("Error extracting publication date")
        return ""

    def _get_acceptance_date(self, article):
        """Extract acceptance date from 'accepted' field."""
        try:
            if "accepted" in article and "date-parts" in article["accepted"]:
                date_parts = article["accepted"]["date-parts"][0]
                if len(date_parts) >= 3:
                    return (
                        f"{date_parts[0]:04d}-{date_parts[1]:02d}-{date_parts[2]:02d}"
                    )
                elif len(date_parts) >= 2:
                    return f"{date_parts[0]:04d}-{date_parts[1]:02d}-01"
                elif len(date_parts) >= 1:
                    return f"{date_parts[0]:04d}-01-01"
        except (IndexError, TypeError):
            self.logger.error("Error extracting acceptance date")
        return ""

    def _get_reception_date(self, article):
        """Extract reception date from assertion where name == 'date_received'."""
        try:
            if "assertion" in article:
                for assertion in article["assertion"]:
                    if assertion.get("name") == "date_received":
                        return assertion.get("value", "")
        except Exception:
            self.logger.error("Error extracting reception date")
        return ""

    def _form_authors(self, article):
        if "author" not in article:
            return []

        authors = []
        for author in article["author"]:
            full_name = f"{author.get('given', '')} {author.get('family', '')}".strip()
            author_data = {
                "full_name": full_name,
                "given_names": author.get("given", ""),
                "surname": author.get("family", ""),
                "orcid": re.sub(r"^https://orcid\.org/", "", author.get("ORCID", "")),
                "affiliations": self._get_affiliations(author),
            }

            authors.append(author_data)

        return authors

    def _get_journal_title(self, article):
        if "container-title" not in article:
            return ""

        journal_title = article["container-title"]
        if journal_title != []:
            return journal_title[0]
        else:
            return ""

    def extract_organization_and_ror(self, affiliation):
        org_name = affiliation.get("name", "")
        ror_id = None
        country = None

        for id_obj in affiliation.get("id", []):
            if id_obj.get("id-type") == "ROR":
                ror_id = id_obj.get("id")
                break

        if ror_id:
            if ror_id in self._ror_cache:
                country = self._ror_cache[ror_id]
            else:
                try:
                    resp = requests.get(
                        f"https://api.ror.org/v2/organizations/{ror_id}"
                    )
                    data = resp.json()
                    locs = data.get("locations", [])
                    if locs:
                        country = (
                            locs[0].get("geonames_details", {}).get("country_code")
                        )
                    self._ror_cache[ror_id] = country
                except Exception:
                    self.logger.error(f"Error fetching country for ROR {ror_id}")
        return org_name, ror_id, country

    def _get_affiliations(self, author):
        if "affiliation" not in author:
            return []
        parsed_affiliations = []
        for affiliation in author["affiliation"]:
            org_name, ror_id, country = self.extract_organization_and_ror(affiliation)
            aff_data = {"value": org_name, "organization": org_name}
            if ror_id:
                aff_data["ror"] = ror_id
            if country:
                aff_data["country"] = country
            parsed_affiliations.append(aff_data)
        return parsed_affiliations

    def _get_field_categories(self, article):
        categories = []

        if "subject" in article and article["subject"]:
            for subject in article["subject"]:
                categories.append(
                    {
                        "term": subject,
                        "scheme": "publisher",
                        "source": "",
                    }
                )

        if "assertion" in article:
            for assertion in article["assertion"]:
                if assertion.get("name") == "arxiv_main_category":
                    categories.append(
                        {
                            "term": assertion.get("value"),
                            "scheme": "arXiv",
                            "source": "",
                        }
                    )

        return categories

    def _get_copyright_holder(self, article):
        try:
            if "assertion" in article:
                for assertion in article["assertion"]:
                    if assertion.get("name") == "copyright_holder":
                        return assertion.get("value", "")
        except Exception:
            self.logger.error("Error extracting copyright holder")
        return ""

    def _get_copyright_year(self, article):
        try:
            if "assertion" in article:
                for assertion in article["assertion"]:
                    if assertion.get("name") == "copyright_year":
                        return int(assertion.get("value", 0))
        except (ValueError, TypeError):
            self.logger.error("Error extracting copyright year")
        return None

    def _get_copyright_statement(self, article):
        try:
            if "assertion" in article:
                for assertion in article["assertion"]:
                    if assertion.get("name") == "copyright_statement":
                        return assertion.get("value", "")
        except Exception:
            self.logger.error("Error extracting copyright statement")
        return ""

    def _get_licenses(self, article):
        try:
            if "license" in article and article["license"]:
                licenses = []
                for license_info in article["license"]:
                    if "URL" in license_info:
                        url = license_info["URL"]

                        if "creativecommons.org/licenses/" in url:
                            parts = url.split("/")

                            license_parts = []
                            version = None
                            for i, part in enumerate(parts):
                                if part == "licenses" and i + 1 < len(parts):
                                    license_parts = parts[i + 1].split("-")
                                if "." in part and part[0].isdigit():
                                    version = part

                            if license_parts:
                                license_type = (
                                    f"CC-{'-'.join(p.upper() for p in license_parts)}"
                                )
                                licenses.append(
                                    construct_license(
                                        url=url,
                                        license_type=license_type,
                                        version=version,
                                    )
                                )
                return licenses
        except Exception as e:
            self.logger.error(f"Error extracting license: {e}")
        return []

    def _get_files(self, article):
        files = {}

        try:
            if "assertion" in article:
                for assertion in article["assertion"]:
                    if assertion.get("name") == "full_text_link_pdf":
                        files["pdf"] = assertion.get("value", "")

                    elif assertion.get("name") == "full_text_link_pdfa":
                        files["pdfa"] = assertion.get("value", "")

            if "link" in article:
                for link in article["link"]:
                    content_type = link.get("content-type", "")
                    if content_type == "application/pdf" and "pdf" not in files:
                        files["pdf"] = link.get("URL", "")
                    elif (
                        content_type == "application/pdf+archive"
                        and "pdfa" not in files
                    ):
                        files["pdfa"] = link.get("URL", "")

            return files
        except Exception as e:
            self.logger.error(f"Error extracting file links: {e}")
            return {}
