import os
from datetime import datetime

from common.parsing.parser import IParser
from common.parsing.xml_extractors import CustomExtractor
from common.utils import extract_text, get_license_type_and_version_from_url
from structlog import get_logger


class ElsevierMetadataParser(IParser):
    def __init__(self, doi, file_path) -> None:
        self.dois = doi
        self.file_path = file_path
        self.year = None
        self.journal_doctype = None
        self.collaborations = []
        self.logger = get_logger().bind(class_name=type(self).__name__)
        self.extractors = [
            CustomExtractor(
                destination="journal_title",
                extraction_function=self._get_journal_title,
                required=True,
            ),
            CustomExtractor(
                destination="date_published",
                extraction_function=self._get_published_date,
                required=True,
            ),
            CustomExtractor(
                destination="journal_year",
                extraction_function=self._get_journal_year,
                required=True,
            ),
            CustomExtractor(
                destination="collections",
                extraction_function=self._get_collections,
            ),
            CustomExtractor(
                destination="license",
                extraction_function=self._get_license,
                required=True,
            ),
            # CustomExtractor(
            #     destination="local_files",
            #     extraction_function=self._get_local_files,
            #     # required=True,
            # ),
        ]

    def parse(self, article):
        extracted_value = {}
        journal_issues = article.findall("dataset-content/journal-item")
        for journal_issue in journal_issues:
            doi = journal_issue.find("journal-item-unique-ids/doi")
            if doi.text == self.dois:
                extracted_value = {
                    extractor.destination: value
                    for extractor in self.extractors
                    if (value := extractor.extract(journal_issue)) is not None
                }
                break
        return self._generic_parsing(extracted_value)

    def _get_published_date(self, article):
        date = extract_text(
            article=article,
            path="journal-item-properties/online-publication-date",
            field_name="published_date",
            dois=self.dois,
        )
        date = datetime.fromisoformat(date[:-1])
        self.published_date = date.strftime("%Y-%m-%d")
        self.year = date.strftime("%Y")
        return self.published_date

    def _get_journal_year(self, article):
        return self.year

    def _get_date_published(self, article):
        return self.published_date

    def _get_journal_title(self, article):
        journal_title = extract_text(
            article=article,
            path="journal-item-unique-ids/jid-aid/jid",
            field_name="collections",
            dois=self.dois,
        )
        self.journal_title = journal_title
        return journal_title

    def _get_collections(self, article):
        return [self.journal_title]

    def _get_license(self, article):
        url = "http://creativecommons.org/licenses/by/3.0/"
        return [get_license_type_and_version_from_url(url)]

    def _get_local_files(self, article):
        xml = article.find("files-info/ml/pathname").text
        pdf = {
            "filetype": "pdf",
            "path": os.path.join(
                self.file_path, article.find("files-info/web-pdf/pathname").text
            ),
        }
        xml = {
            "filetype": "xml",
            "path": os.path.join(
                self.file_path, article.find("files-info/ml/pathname").text
            ),
        }
        return [pdf, xml]
