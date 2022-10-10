import xml.etree.ElementTree as ET
from typing import Dict, List

from common.cleanup import (
    clean_collaboration,
    clean_whitespace_characters,
    remove_orcid_prefix,
)
from common.parsing.extractor import IExtractor
from common.parsing.generic_parsing import (
    classification_numbers,
    clear_unnecessary_fields,
    fix_publication_date,
    free_keywords,
    list_to_value_dict,
    merge_dois,
    parse_author,
    parse_thesis_supervisors,
    publication_info,
    remove_empty_values,
    take_first,
)


def pipe_functions(functions, value):
    if len(functions) > 0:
        return pipe_functions(functions[1:], functions[0](value))
    return value


class IParser:
    extractors: List[IExtractor]

    def __init__(self, extractors) -> None:
        self.extractors = extractors

    def _publisher_specific_parsing(self, article: ET.Element):
        extracted_value = {
            extractor.destination: value
            for extractor in self.extractors
            if (value := extractor.extract(article)) is not None
        }
        return extracted_value

    def _generic_parsing(self, publisher_parsed_article: Dict):
        def get(field, default=[]):
            return publisher_parsed_article.get(field, default)

        parsed_article = publisher_parsed_article.copy()

        parsed_article.update(
            {
                "authors": list(map(parse_author, get("authors", []))),
                "abstract": clean_whitespace_characters(get("abstract")),
                "collaborations": pipe_functions(
                    [lambda x: map(clean_collaboration, x), list_to_value_dict],
                    get("collaborations"),
                ),
                "collections": list_to_value_dict(get("collections"), "primary"),
                "title": clean_whitespace_characters(get("title")),
                "subtitle": pipe_functions(
                    [lambda x: map(clean_whitespace_characters, x), take_first],
                    get("subtitle"),
                ),
                "journal_year": get("journal_year"),
                "preprint_date": take_first(get("preprint_date")),
                "date_published": fix_publication_date(get("date_published")),
                "related_article_doi": list_to_value_dict(get("related_article_doi")),
                "free_keywords": pipe_functions(
                    [lambda x: map(clean_whitespace_characters, x), free_keywords],
                    get("free_keywords"),
                ),
                "classification_numbers": classification_numbers(
                    get("classification_numbers")
                ),
                "dois": list_to_value_dict(get("dois")),
                "thesis_supervisor": list(
                    map(parse_thesis_supervisors, get("thesis_supervisor"))
                ),
                "thesis": take_first(get("thesis")),
                "urls": list_to_value_dict(get("urls")),
                "local_files": list_to_value_dict(get("local_files")),
                "record_creation_date": take_first(get("record_creation_date")),
                "control_field": take_first(get("control_field")),
                "publication_info": publication_info(publisher_parsed_article),
            }
        )

        parsed_article["dois"] = merge_dois(parsed_article)
        parsed_article = pipe_functions(
            [clear_unnecessary_fields, remove_empty_values, remove_orcid_prefix],
            parsed_article,
        )

        return parsed_article

    def parse(self, article: ET.Element):
        publisher_parsed_article = self._publisher_specific_parsing(article)
        return self._generic_parsing(publisher_parsed_article)


class ObjectExtractor(IParser, IExtractor):
    def __init__(self, destination, extractors, extra_function=lambda x: x) -> None:
        super().__init__(destination)
        self.destination = destination
        self.extractors = extractors
        self.extra_function = extra_function

    def extract(self, article: ET.Element):
        return self.extra_function(super()._publisher_specific_parsing(article))
