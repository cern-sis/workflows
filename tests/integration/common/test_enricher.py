import pytest
from common.enricher import Enricher


@pytest.fixture
def enricher():
    return Enricher()


@pytest.mark.vcr
def test_get_arxiv_categories_arxiv_id(enricher):
    assert ["hep-th", "hep-ph"] == enricher._get_arxiv_categories(arxiv_id="2112.01211")
