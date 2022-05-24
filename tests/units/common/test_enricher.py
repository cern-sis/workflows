import pytest
from common.enricher import Enricher


@pytest.fixture
def enricher():
    return Enricher()


@pytest.fixture
def arxiv_output_content(datadir):
    return (datadir / "arxiv_output.xml").read_text()


def test_get_schema(enricher):
    assert "http://repo.scoap3.org/schemas/hep.json" == enricher._get_schema()


def test_get_arxiv_categories_arxiv_id(enricher, arxiv_output_content, requests_mock):
    requests_mock.get(
        'http://export.arxiv.org/api/query?search_query=id:"test-id"',
        text=arxiv_output_content,
    )
    assert ["hep-th", "hep-ph"] == enricher._get_arxiv_categories(arxiv_id="test-id")
