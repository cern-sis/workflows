from os import getenv
from xml.etree import ElementTree

from common.request import Request
from requests.exceptions import RequestException
from structlog import get_logger


class HindawiApiClient:
    def __init__(
        self,
        base_url=None,
        files_url=None,
    ):
        self.base_url = base_url or getenv(
            "HINDAWI_API_BASE_URL", "https://www.hindawi.com"
        )
        self.files_url = files_url or getenv(
            "HINDAWI_API_FILES_URL", "http://downloads.hindawi.com"
        )
        self.logger = get_logger().bind(class_name=type(self).__name__)

    def get_articles_metadata(self, parameters, doi=None):
        path_segments = ["oai-pmh", "oai.aspx"]
        empty_xml = True
        if doi:
            path_segments.append(doi)
        request = Request(
            base_url=self.base_url,
            path_segments=path_segments,
            parameters=parameters,
        )
        if "until" not in parameters:
            raise AttributeError("until date is required")
        response_content = request.get_response_xml()

        for tag in ElementTree.fromstring(response_content):
            if "ListRecords" in tag.tag:
                empty_xml = False
                break
        if not empty_xml:
            return response_content
        return None

    def get_file(self, parameters, extension, doi):
        if extension not in ("pdf", "pdfa", "xml"):
            raise AttributeError("The extension has to be pdf, pdfa or xml")
        path_segments_for_files = ["journals", "ahep"]
        try:
            doi_part = doi.replace("10.1155/", "") + f".{extension}"
            request = Request(
                base_url=self.files_url,
                path_segments=path_segments_for_files + [doi_part],
                parameters=parameters,
            )
            return request.get_response_bytes()
        except RequestException:
            self.logger.error("Request failed with exception.")

    def __repr__(self) -> str:
        return f"<HindawiApiClient base_url={self.base_url}, \
                    parameters={self.parameters}>"
