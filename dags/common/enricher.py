import xml.etree.ElementTree as ET
from logging import Logger
from typing import Dict

import backoff
import requests
from structlog import get_logger


class Enricher(object):
    def __init__(self) -> None:
        self.logger = get_logger().bind(class_name=type(self).__name__)

    def _get_schema(self):
        return "http://repo.scoap3.org/schemas/hep.json"

    @backoff.on_exception(
        backoff.expo, requests.exceptions.RequestException, max_time=60, max_tries=3
    )
    def _get_arxiv_categories(self, arxiv_id=None):
        if arxiv_id is None:
            raise ValueError("Arxiv is None.")

        def clean_arxiv(arxiv):
            if arxiv is None:
                return None

            return arxiv.split(":")[-1].split("v")[0].split(" ")[0].strip("\"'")

        def get_arxiv_categories_from_response_xml(xml: ET.Element):
            xml_namespaces = {
                "arxiv": "http://arxiv.org/schemas/atom",
                "w3": "http://www.w3.org/2005/Atom",
            }

            entries = xml.findall("./w3:entry", namespaces=xml_namespaces)
            if len(entries) != 1:
                return []
            entry = entries[0]

            primary_categories = [
                node.attrib["term"]
                for node in entry.findall(
                    "./arxiv:primary_category", namespaces=xml_namespaces
                )
            ]
            if not primary_categories:
                return []
            if len(primary_categories) > 1:
                Logger.error(
                    "Arxiv returned %d primary categories." % len(primary_categories)
                )
                return []
            primary_category = primary_categories[0]

            secondary_categories = [
                node.attrib["term"]
                for node in entry.findall("./w3:category", namespaces=xml_namespaces)
            ]
            if primary_category in secondary_categories:
                secondary_categories.remove(primary_category)

            return [primary_category] + secondary_categories

        arxiv_id = clean_arxiv(arxiv_id)

        query = f'id:"{arxiv_id}"'
        response = requests.get(
            f"http://export.arxiv.org/api/query?search_query={query}"
        )

        categories = []
        if response.status_code == 200:
            xml = ET.fromstring(response.content)
            categories = get_arxiv_categories_from_response_xml(xml)
            if not categories:
                self.logger.warning(
                    'Could not get arxiv categories for id="%s"' % (arxiv_id)
                )
        else:
            self.logger.error(
                f"Got status_code {response.status_code} from arXiv when looking for categires for id={arxiv_id}"
            )
        return categories

    def __call__(self, article: Dict):
        enriched_article = article.copy()
        enriched_article.update(
            {
                "$schema": self._get_schema(),
                "categories": self._get_arxiv_categories(
                    article.get("external_id", None)
                ),
            }
        )
