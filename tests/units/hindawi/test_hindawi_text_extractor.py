import xml.etree.ElementTree as ET

from common.parsing.xml_extractors import RequiredFieldNotFoundExtractionError
from hindawi.xml_extractors import HindawiTextExtractor
from pytest import fixture, raises


@fixture
def hindawi_doi_extractor():
    prefixes = {
        "marc": "http://www.loc.gov/MARC21/slim",
        "ns0": "http://www.openarchives.org/OAI/2.0/",
        "ns1": "http://www.loc.gov/MARC21/slim",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    }
    return HindawiTextExtractor(
        source="ns0:metadata/ns1:record/ns0:datafield/[@tag='024']/ns0:subfield/[@code='a']",
        destination="dois",
        prefixes=prefixes,
    )


@fixture
def articles(shared_datadir):
    articles = []
    files = ["example1.xml", "example2.xml"]

    for file in files:
        with open(shared_datadir / file) as file:
            articles.append(ET.fromstring(file.read()))
    return articles


def test_parsed_articles(hindawi_doi_extractor, articles):
    parsed_articles = [hindawi_doi_extractor.extract(article) for article in articles]
    assert parsed_articles == ["10.1155/2019/3465159", "10.1155/2022/5287693"]


@fixture
def hindawi_not_excitant_field_extractor():
    prefixes = {
        "marc": "http://www.loc.gov/MARC21/slim",
        "ns0": "http://www.openarchives.org/OAI/2.0/",
        "ns1": "http://www.loc.gov/MARC21/slim",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    }
    return HindawiTextExtractor(
        source="ns0:metadata/ns1:record/ns0:datafield/[@tag='024']/ns0:subfield/[@code='nothing']",
        destination="nothing",
        prefixes=prefixes,
    )


def test_parsed_articles_with_error(hindawi_not_excitant_field_extractor, articles):
    with raises(RequiredFieldNotFoundExtractionError):
        [hindawi_not_excitant_field_extractor.extract(article) for article in articles]
