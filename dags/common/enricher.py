import os
import re
import xml.etree.ElementTree as ET
from typing import Dict

import backoff
import requests
from common.cleanup import remove_unnecessary_fields
from common.parsing.generic_parsing import remove_empty_values
from structlog import get_logger


class Enricher(object):
    def __init__(self) -> None:
        self.logger = get_logger().bind(class_name=type(self).__name__)

    def _get_schema(self):
        return os.getenv("REPO_URL", "http://repo.qa.scoap3.org/schemas/hep.json")

    def _clean_arxiv(self, arxiv):
        if arxiv is None:
            return None
        try:
            return re.search(r"\d{4}\.\d{4,5}", arxiv).group()
        except AttributeError:
            return None

    def _get_arxiv_categories_from_response_xml(self, xml: ET.Element):
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
            self.logger.error(
                "Arxiv returned multiple primary categories.",
                categories=primary_categories,
            )
            return []
        primary_category = primary_categories[0]

        secondary_categories = [
            node.attrib["term"]
            for node in entry.findall("./w3:category", namespaces=xml_namespaces)
        ]
        for (index, secondary_category) in enumerate(secondary_categories):
            if secondary_category == primary_category:
                secondary_categories.pop(index)

        return list([primary_category] + secondary_categories)

    @backoff.on_exception(
        backoff.expo, requests.exceptions.RequestException, max_time=60, max_tries=5
    )
    def _get_arxiv_categories(self, arxiv_id=None, title=None, doi=None):
        if arxiv_id is None and title is None and doi is None:
            raise ValueError(
                "One of the arxiv_id, title and doi parameters has to be different then None."
            )

        arxiv_id = self._clean_arxiv(arxiv_id)

        params = {}
        if arxiv_id:
            params["id_list"] = arxiv_id
        if title:
            params["search_query"] = f'ti:"{title.replace("-", "?")}"'
        response = requests.get("http://export.arxiv.org/api/query", params)

        categories = []
        if response.status_code == 200:
            xml = ET.fromstring(response.content)
            categories = self._get_arxiv_categories_from_response_xml(xml)
            if not categories:
                self.logger.warning(
                    "Could not get arxiv categories.",
                    id=arxiv_id,
                    title=title,
                    doi=doi,
                )
        else:
            self.logger.error(
                "Got arxiv response error.",
                status_code=response.status_code,
                id=arxiv_id,
                title=title,
                doi=doi,
            )
            response.raise_for_status()
        return categories

    def _set_categories(self, eprint: Dict):
        if eprint["value"]:
            eprint["categories"] = self._get_arxiv_categories(eprint["value"])
            eprint["value"] = self._clean_arxiv(eprint["value"])
        return eprint

    def __call__(self, article: Dict):
        enriched_article = article.copy()
        enriched_article.update(
            {
                "$schema": self._get_schema(),
                "arxiv_eprints": [
                    self._set_categories(eprint)
                    for eprint in enriched_article.get("arxiv_eprints", [])
                ],
            }
        )
        enriched_article = remove_empty_values(enriched_article)
        enriched_article = remove_unnecessary_fields(enriched_article)
        return enriched_article
