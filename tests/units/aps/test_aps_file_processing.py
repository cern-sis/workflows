import json

import pytest
from aps.aps_process_file import aps_validate_record, enhance_aps, enrich_aps
from aps.parser import APSParser
from pytest import fixture


@fixture
def articles(shared_datadir):
    json_response = (shared_datadir / "json_response_content.json").read_text()
    return [article for article in json.loads(json_response)["data"]]


@fixture
def parser():
    return APSParser()


@fixture
def parsed_articles(articles, parser):
    return [parser._publisher_specific_parsing(article) for article in articles]


@fixture
def parsed_generic_articles(parsed_articles, parser):
    return [parser._generic_parsing(article) for article in parsed_articles]


@fixture
def enhance_articles(parsed_generic_articles):
    return [enhance_aps(article) for article in parsed_generic_articles]


@fixture
def enrich_article(enhance_articles):
    return [enrich_aps(article) for article in enhance_articles]


@pytest.mark.vcr
def test_aps_validated_record(enrich_article):
    [aps_validate_record(article) for article in enrich_article]
