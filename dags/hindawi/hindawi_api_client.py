from os import getenv
from xml.etree import ElementTree

from common.request import Request


class HindawiApiClient:
    def __init__(
        self,
        base_url=None,
        path_segments=None,
    ):
        self.base_url = base_url or getenv(
            "HINDAWI_API_BASE_URL", "https://www.hindawi.com"
        )
        self.path_segments = path_segments or ["oai-pmh", "oai.aspx"]

    def get_articles_metadata(self, parameters, doi=None):
        if doi:
            self.path_segments.append(doi)
        request = Request(
            base_url=self.base_url,
            path_segments=self.path_segments,
            parameters=parameters,
        )
        response_content = request.get_response_xml()
        for tag in ElementTree.fromstring(response_content):
            if "ListRecords" in tag.tag:
                break
            return response_content

    # TODO: don't forget to download pdf when it will be needed
    def __repr__(self) -> str:
        return f"<HindawiApiClient base_url={self.base_url}, \
                    path_segments={self.path_segments}, \
                    parameters={self.parameters}>"
