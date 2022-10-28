import re
import xml.etree.ElementTree as ET

from common.parsing.parser import IParser
from common.parsing.xml_extractors import CustomExtractor
from hindawi.xml_extractors import HindawiTextExtractor as TextExtractor
from structlog import get_logger


class HindawiParser(IParser):
    prefixes = {
        "marc": "http://www.loc.gov/MARC21/slim",
        "ns0": "http://www.openarchives.org/OAI/2.0/",
        "ns1": "http://www.loc.gov/MARC21/slim",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    }

    def __init__(self) -> None:
        self.logger = get_logger().bind(class_name=type(self).__name__)
        extractors = [
            TextExtractor(
                destination="dois",
                source="ns0:metadata/ns1:record/ns0:datafield/[@tag='024']/ns0:subfield/[@code='a']",
                prefixes=self.prefixes,
                extra_function=lambda x: [x],
                default_value=[],
            ),
            CustomExtractor(
                destination="authors",
                extraction_function=self._get_authors,
                default_value=[],
            ),
            TextExtractor(
                destination="abstract",
                source="ns0:metadata/ns1:record/ns0:datafield/[@tag='520']/ns0:subfield/[@code='a']",
                prefixes=self.prefixes,
                extra_function=lambda x: " ".join(x.split()),
                default_value="",
            ),
            TextExtractor(
                destination="title",
                source="ns0:metadata/ns1:record/ns0:datafield/[@tag='245']/ns0:subfield/[@code='a']",
                prefixes=self.prefixes,
                extra_function=lambda x: x,
                default_value="",
            ),
            TextExtractor(
                destination="date_published",
                required=False,
                source="ns0:metadata/ns1:record/ns0:datafield/[@tag='260']/ns0:subfield/[@code='c']",
                prefixes=self.prefixes,
                extra_function=lambda x: x,
                default_value="2000-00-00",
            ),
            TextExtractor(
                destination="page_nr",
                source="ns0:metadata/ns1:record/ns0:datafield/[@tag='300']/ns0:subfield/[@code='a']",
                required=False,
                prefixes=self.prefixes,
                extra_function=lambda x: [int(x)],
                default_value=[0],
            ),
            CustomExtractor(
                destination="publication_info",
                extraction_function=self._get_publication_info,
                default_value=[],
            ),
            CustomExtractor(
                destination="arxiv_eprints",
                extraction_function=self._get_arxiv,
                default_value=[],
            ),
            CustomExtractor(
                destination="copyright_statement",
                extraction_function=self._get_copyright_statement,
                default_value="",
            ),
            CustomExtractor(
                destination="copyright_year",
                extraction_function=self._get_copyright_year,
                default_value=0,
            ),
            CustomExtractor(
                destination="license",
                extraction_function=self._get_license,
                default_value=[],
            ),
        ]
        super().__init__(extractors)

    def _get_authors(self, article: ET.Element):
        authors_all = article.findall(
            "ns0:metadata/ns1:record/ns0:datafield/[@tag='100']", self.prefixes
        ) + article.findall(
            "ns0:metadata/ns1:record/ns0:datafield/[@tag='700']", self.prefixes
        )

        authors = []
        for author in authors_all:
            raw_name = author.find("ns0:subfield[@code='a']", self.prefixes).text
            if not raw_name:
                continue
            author_ = {
                "raw_name": raw_name,
                "affiliations": self._get_affiliations(author),
            }
            orcid = author.find("ns0:subfield[@code='j']", self.prefixes)
            if orcid.text:
                author_["orcid"] = orcid.text
            authors.append(author_)

        return authors

    def _get_affiliations(self, author):
        affiliations = author.findall("ns0:subfield[@code='u']", self.prefixes)
        parsed_affiliations = [
            {
                "value": affiliation.text,
                "organization": re.sub(r",\s[A-Z]?[a-z]*$", "", affiliation.text),
                "country": re.search(r"[A-Z]?[a-z]*$", affiliation.text).group(0),
            }
            for affiliation in affiliations
        ]
        return parsed_affiliations

    def _get_arxiv(self, article: ET.Element):
        arxivs = article.findall(
            "ns0:metadata/ns1:record/ns0:datafield/[@tag='037']/ns0:subfield/[@code='9']",
            self.prefixes,
        )
        if not arxivs:
            self.logger.error("No arxiv id_get_copyright_statement found.")
            return None

        return [
            {"value": re.sub("arxiv:", "", arxiv_value, flags=re.IGNORECASE).strip()}
            for arxiv in arxivs
            if (
                arxiv_value := arxiv.text.lower() == "arxiv"
                and article.find(
                    "ns0:metadata/ns1:record/ns0:datafield/[@tag='037']/ns0:subfield/[@code='a']",
                    self.prefixes,
                ).text.lower()
            )
            is not None
        ]

    def _get_journal_pages(self, article: ET.Element):
        journal_pages = article.find(
            "ns0:metadata/ns1:record/ns0:datafield/[@tag='773']/ns0:subfield/[@code='c']",
            self.prefixes,
        ).text
        if "-" in journal_pages:
            return journal_pages.split("-", 1)
        return journal_pages, ""

    def _construct_license(self, url, license_type, version):
        if url and license_type and version:
            return {
                "url": url,
                "license": f"CC-{license_type}-{version}",
            }

    def _get_license(self, article: ET.Element):
        licenses = []
        license_urls = article.findall(
            "ns0:metadata/ns1:record/ns0:datafield/[@tag='540']/ns0:subfield/[@code='u']",
            self.prefixes,
        )
        license_texts = article.findall(
            "ns0:metadata/ns1:record/ns0:datafield/[@tag='540']/ns0:subfield/[@code='a']",
            self.prefixes,
        )
        for license_url, license_text in zip(license_urls, license_texts):
            if license_url.text:
                clean_url_parts = list(filter(bool, license_url.text.split("/")))
                version = clean_url_parts.pop()
                license_type = clean_url_parts.pop()
                licenses.append(
                    self._construct_license(
                        license_url.text, license_type.upper(), version
                    )
                )
            elif license_text.text:
                licenses.append(license_text.text)
        return licenses

    def _get_copyright_statement(self, article):
        copyright_statement = article.find(
            "ns0:metadata/ns1:record/ns0:datafield/[@tag='542']/ns0:subfield/[@code='f']",
            self.prefixes,
        ).text
        return copyright_statement

    def _get_copyright_year(self, article):
        copyright_year = re.search(
            r"[0-9]{4}", self._get_copyright_statement(article)
        ).group(0)
        return copyright_year

    def _get_publication_info(self, article):
        journals = article.findall(
            "ns0:metadata/ns1:record/ns0:datafield/[@tag='773']", self.prefixes
        )
        return [
            {
                "journal_title": journal.find(
                    "./ns0:subfield/[@code='p']", self.prefixes
                ).text,
                "journal_volume": journal.find(
                    "./ns0:subfield/[@code='v']", self.prefixes
                ).text,
                "journal_year": journal.find(
                    "./ns0:subfield/[@code='y']", self.prefixes
                ).text,
            }
            for journal in journals
        ]
