import os
from datetime import datetime

from common.parsing.parser import IParser
from common.parsing.xml_extractors import CustomExtractor
from common.utils import extract_text, get_license_type_and_version_from_url
from structlog import get_logger


class ElsevierMetadataParser(IParser):
    def __init__(self, file_path):
        self.file_path = file_path
        self.year = None
        self.logger = get_logger().bind(class_name=type(self).__name__)
        self.extractors = [
            CustomExtractor(
                destination="dois",
                extraction_function=self._get_dois,
                required=True,
            ),
            CustomExtractor(
                destination="journal_title",
                extraction_function=self._get_journal_title,
                required=True,
            ),
            CustomExtractor(
                destination="journal_artid",
                extraction_function=self._get_journal_aid,
                required=True,
            ),
            CustomExtractor(
                destination="date_published",
                extraction_function=self._get_published_date,
            ),
            CustomExtractor(
                destination="journal_year",
                extraction_function=self._get_journal_year,
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
            CustomExtractor(
                destination="files",
                extraction_function=self._get_local_files,
                required=True,
            ),
        ]

    def parse(self, article):
        extracted_value = {}
        journal_issues = article.findall("dataset-content/journal-item")
        parsed_articles = []
        for journal_issue in journal_issues:
            extracted_value = {
                extractor.destination: value
                for extractor in self.extractors
                if (value := extractor.extract(journal_issue)) is not None
            }
            extracted_value["journal_volume"] = self._get_journal_volume(
                article.find("dataset-content")
            )
            parsed_articles.append(self._generic_parsing(extracted_value))
        return parsed_articles

    def _get_dois(self, article):
        node = article.find("journal-item-unique-ids/doi")
        if node is None:
            return
        dois = node.text
        if dois:
            self.logger.msg("Parsing dois for article", dois=dois)
            self.dois = dois
            return [dois]
        return

    def _get_published_date(self, article):
        date = extract_text(
            article=article,
            path="journal-item-properties/online-publication-date",
            field_name="published_date",
            dois=self.dois,
        )
        if date:
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
            field_name="journal_title",
            dois=self.dois,
        )
        self.journal_title = journal_title
        return journal_title

    def _get_journal_aid(self, article):
        journal_aid = extract_text(
            article=article,
            path="journal-item-unique-ids/jid-aid/aid",
            field_name="journal_aid",
            dois=self.dois,
        )
        return journal_aid

    def _get_journal_volume(self, article):
        vol_first = extract_text(
            article=article,
            path="journal-issue/journal-issue-properties/volume-issue-number/vol-first",
            field_name="volume_vol_first",
            dois=None,
        )
        suppl = extract_text(
            article=article,
            path="journal-issue/journal-issue-properties/volume-issue-number/suppl",
            field_name="volume_suppl",
            dois=None,
        )

        return f"{vol_first} {suppl}"

    def _get_collections(self, article):
        return [self.journal_title]

    def _get_license(self, article):
        url = "http://creativecommons.org/licenses/by/3.0/"
        return [get_license_type_and_version_from_url(url)]

    def _get_local_files(self, article):
        if self.file_path.endswith("A.tar"):
            self.file_path = self.file_path.replace("A.tar", "")
        if self.file_path.endswith(".zip"):
            self.file_path = self.file_path.replace(".zip", "")
        if self.file_path.startswith("raw"):
            self.file_path = self.file_path.replace("raw/", "")

        files_dir_base = os.path.dirname(self.file_path)

        pdf_file_path = os.path.join(
            files_dir_base,
            article.find("files-info/web-pdf/pathname").text,
        )
        return {
            "pdf": pdf_file_path,
            "pdfa": os.path.join(os.path.split(pdf_file_path)[0], "main_a-2b.pdf"),
            "xml": os.path.join(
                files_dir_base, article.find("files-info/ml/pathname").text
            ),
        }
