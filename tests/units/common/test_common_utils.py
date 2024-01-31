import os
from unittest import mock

import pytest
import requests
from common.utils import create_or_update_article


@pytest.mark.vcr
@mock.patch.dict(
    os.environ,
    {
        "BACKEND_URL": "https://backend.dev.scoap3.org/api/article-workflow-import/",
        "BACKEND_TOKEN": "CHANGE_ME",
    },
)
def test_create_article():
    data = {
        "_oai": {
            "updated": "2023-11-14T00:15:03Z",
            "id": "oai:repo.scoap3.org:81153",
            "sets": ["AHEP"],
        },
        "authors": [
            {
                "surname": "Mirza",
                "given_names": "M. Ibrahim",
                "raw_name": "Mirza, M. Ibrahim",
                "affiliations": [
                    {
                        "country": "USA",
                        "value": "Department of Physics and Astronomy, University of Tennessee, Knoxville, Tennessee 37916, USA",
                    }
                ],
                "full_name": "Mirza, M. Ibrahim",
                "orcid": "0009-0002-6581-5721",
            },
            {
                "surname": "Singh",
                "given_names": "Jyotsna",
                "raw_name": "Singh, Jyotsna",
                "affiliations": [
                    {
                        "country": "India",
                        "value": "Department of Physics, University of Lucknow, Lucknow, Uttar Pradesh, India",
                    }
                ],
                "full_name": "Singh, Jyotsna",
                "orcid": "0000-0003-3250-3326",
            },
        ],
        "titles": [
            {
                "source": "Hindawi",
                "title": "Theoretical and Experimental Challenges in the Measurement of Neutrino Mass",
            }
        ],
        "dois": [{"value": "10.1155/2023/8897375"}],
        "publication_info": [
            {
                "page_start": "8897375",
                "journal_title": "Advances in High Energy Physics",
                "year": 2023,
            }
        ],
        "$schema": "http://repo.scoap3.org/schemas/hep.json",
        "acquisition_source": {
            "date": "2023-11-14T00:15:01.612737",
            "source": "Hindawi",
            "method": "Hindawi",
            "submission_number": "d9b644cc828211eeb8f48e9c197d18e3",
        },
        "page_nr": [14],
        "license": [
            {
                "url": "http://creativecommons.org/licenses/by/3.0/",
                "license": "CC-BY-3.0",
            }
        ],
        "copyright": [
            {
                "statement": "Copyright \u00a9 2023 Jyotsna Singh and M. Ibrahim Mirza.",
                "year": "2023",
            }
        ],
        "control_number": "81153",
        "record_creation_date": "2023-10-27T12:15:05.910972",
        "collections": [{"primary": "Advances in High Energy Physics"}],
        "arxiv_eprints": [{"categories": ["hep-ex", "hep-ph"], "value": "2305.12654"}],
        "abstracts": [
            {
                "source": "Hindawi",
                "value": 'Neutrino masses are yet unknown. We discuss the present state of effective electron antineutrino mass from <math id="M1"><mi>\u03b2</mi></math> decay experiments; effective Majorana neutrino mass from neutrinoless double-beta decay experiments; neutrino mass squared differences from neutrino oscillation: solar, atmospheric, reactor, and accelerator-based experiments; sum of neutrino masses from cosmological observations. Current experimental challenges in the determination of neutrino masses are briefly discussed. The main focus is devoted to contemporary experiments.',
            }
        ],
        "imprints": [{"date": "2023-10-27", "publisher": "Hindawi"}],
    }
    article = create_or_update_article(data)
    assert (
        article["title"]
        == "Theoretical and Experimental Challenges in the Measurement of Neutrino Mass"
    )
    assert article["id"] == 81153


@pytest.mark.vcr
@mock.patch.dict(
    os.environ,
    {
        "BACKEND_URL": "https://backend.dev.scoap3.org/api/article-workflow-import/",
        "BACKEND_TOKEN": "CHANGE_ME",
    },
)
@pytest.fixture
def mock_response_create_fail():
    response = mock.Mock()
    response.raise_for_status.side_effect = requests.HTTPError("Create failed")
    response.json.return_value = {"message": "Create failed", "article_id": "81153"}
    return response


@pytest.fixture
def mock_response_update_success():
    """Mock response for successful update request."""
    response = mock.Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = {"title": "New title", "id": "81153"}
    return response


@mock.patch("requests.post")
@mock.patch("requests.put")
def test_update_article(
    mock_put, mock_post, mock_response_create_fail, mock_response_update_success
):
    mock_post.return_value = mock_response_create_fail
    mock_put.return_value = mock_response_update_success

    data = {
        "_oai": {
            "updated": "2023-11-14T00:15:03Z",
            "id": "oai:repo.scoap3.org:81153",
            "sets": ["AHEP"],
        },
        "authors": [
            {
                "surname": "Mirza",
                "given_names": "M. Ibrahim",
                "raw_name": "Mirza, M. Ibrahim",
                "affiliations": [
                    {
                        "country": "USA",
                        "value": "Department of Physics and Astronomy, University of Tennessee, Knoxville, Tennessee 37916, USA",
                    }
                ],
                "full_name": "Mirza, M. Ibrahim",
                "orcid": "0009-0002-6581-5721",
            },
            {
                "surname": "Singh",
                "given_names": "Jyotsna",
                "raw_name": "Singh, Jyotsna",
                "affiliations": [
                    {
                        "country": "India",
                        "value": "Department of Physics, University of Lucknow, Lucknow, Uttar Pradesh, India",
                    }
                ],
                "full_name": "Singh, Jyotsna",
                "orcid": "0000-0003-3250-3326",
            },
        ],
        "titles": [
            {
                "source": "Hindawi",
                "title": "Theoretical and Experimental Challenges in the Measurement of Neutrino Mass",
            }
        ],
        "dois": [{"value": "10.1155/2023/8897375"}],
        "publication_info": [
            {
                "page_start": "8897375",
                "journal_title": "Advances in High Energy Physics",
                "year": 2023,
            }
        ],
        "$schema": "http://repo.scoap3.org/schemas/hep.json",
        "acquisition_source": {
            "date": "2023-11-14T00:15:01.612737",
            "source": "Hindawi",
            "method": "Hindawi",
            "submission_number": "d9b644cc828211eeb8f48e9c197d18e3",
        },
        "page_nr": [14],
        "license": [
            {
                "url": "http://creativecommons.org/licenses/by/3.0/",
                "license": "CC-BY-3.0",
            }
        ],
        "copyright": [
            {
                "statement": "Copyright \u00a9 2023 Jyotsna Singh and M. Ibrahim Mirza.",
                "year": "2023",
            }
        ],
        "control_number": "81153",
        "record_creation_date": "2023-10-27T12:15:05.910972",
        "collections": [{"primary": "Advances in High Energy Physics"}],
        "arxiv_eprints": [{"categories": ["hep-ex", "hep-ph"], "value": "2305.12654"}],
        "abstracts": [
            {
                "source": "Hindawi",
                "value": 'Neutrino masses are yet unknown. We discuss the present state of effective electron antineutrino mass from <math id="M1"><mi>\u03b2</mi></math> decay experiments; effective Majorana neutrino mass from neutrinoless double-beta decay experiments; neutrino mass squared differences from neutrino oscillation: solar, atmospheric, reactor, and accelerator-based experiments; sum of neutrino masses from cosmological observations. Current experimental challenges in the determination of neutrino masses are briefly discussed. The main focus is devoted to contemporary experiments.',
            }
        ],
        "imprints": [{"date": "2023-10-27", "publisher": "Hindawi"}],
    }
    data["titles"][0]["title"] = "New title"
    article = create_or_update_article(data)

    assert article["title"] == "New title"
    assert article["id"] == "81153"

    mock_post.assert_called_once()
    mock_put.assert_called_once()


@pytest.mark.vcr
@mock.patch.dict(
    os.environ,
    {
        "BACKEND_URL": "https://backend.dev.scoap3.org/api/article-workflow-import/",
        "BACKEND_TOKEN": "CHANGE_ME",
    },
)
def test_create_or_update_article_with_error():
    with pytest.raises(requests.exceptions.HTTPError):
        create_or_update_article({})
