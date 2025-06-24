import pytest
from common.enricher import Enricher


@pytest.fixture
def enricher():
    return Enricher()


@pytest.fixture
def arxiv_output_content(datadir):
    return (datadir / "arxiv_output.xml").read_text()


def test_get_schema(enricher):
    assert "http://repo.qa.scoap3.org/schemas/hep.json" == enricher._get_schema()


def test_get_arxiv_categories_arxiv_id(
    enricher, arxiv_output_content, requests_mock, assertListEqual
):
    requests_mock.get(
        "http://export.arxiv.org/api/query?id_list=0000.00000",
        text=arxiv_output_content,
    )
    assertListEqual(
        ["hep-ph", "astro-ph.HE", "astro-ph.IM", "hep-ex"],
        enricher._get_arxiv_categories(arxiv_id="0000.00000"),
    )


def test_get_arxiv_categories_title(
    enricher, arxiv_output_content, requests_mock, assertListEqual
):
    requests_mock.get(
        'http://export.arxiv.org/api/query?search_query=ti:"test+title"',
        text=arxiv_output_content,
    )
    assertListEqual(
        ["hep-ph", "astro-ph.HE", "astro-ph.IM", "hep-ex"],
        enricher._get_arxiv_categories(title="test title"),
    )
