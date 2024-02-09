import pytest
from common.enricher import Enricher


@pytest.fixture
def enricher():
    return Enricher()


@pytest.mark.vcr
def test_get_arxiv_categories_arxiv_id(enricher, assertListEqual):
    assertListEqual(
        ["hep-th", "hep-ph"], enricher._get_arxiv_categories(arxiv_id="2112.01211")
    )


@pytest.mark.vcr
def test_get_arxiv_categories_title(enricher, assertListEqual):
    assertListEqual(
        ["hep-ex"],
        enricher._get_arxiv_categories(
            title="A strategy for a general search for new phenomena using data-derived signal regions and its application within the ATLAS experiment"
        ),
    )


@pytest.mark.vcr
def test_enricher(enricher, assertListEqual):
    input_article = {
        "arxiv_eprints": [{"value": "2112.01211"}],
        "curated": "Test Value",
        "citeable": "Test Value",
        "files": "Test Value",
    }
    assertListEqual(
        {
            "arxiv_eprints": [
                {"value": "2112.01211", "categories": list(set(["hep-th", "hep-ph"]))}
            ],
            "$schema": "http://repo.qa.scoap3.org/schemas/hep.json",
        },
        enricher(input_article),
    )
