from unittest import mock

from aps.aps_api_client import APSApiClient
from aps.aps_params import APSParams


def mocked_response(*args, **kwrgs):
    mocked_response = mock.Mock(autospec=True)
    mocked_response.status_code = 200
    mocked_response.url = args[0]
    mocked_response.content = '{"data":[{"abstract":{"value":"<p>We propose and theoretically analyze</p>"}}]}'
    mocked_response.json = mock.MagicMock(
        return_value={
            "data": [
                {"abstract": {"value": "<p>We propose and theoretically analyze</p>"}}
            ]
        }
    )
    return mocked_response


@mock.patch("common.request.requests.get", side_effect=mocked_response)
def test_get_articles_metadata(mocked_response):
    parameters = APSParams(
        from_date="2021-01-01",
        until_date="2021-01-02",
    ).get_params()
    aps_api_client = APSApiClient()
    metadata = aps_api_client.get_articles_metadata(parameters=parameters)
    assert metadata == {
        "data": [{"abstract": {"value": "<p>We propose and theoretically analyze</p>"}}]
    }


def mocked_empty_response(*args, **kwrgs):
    mocked_response = mock.Mock()
    mocked_response.status_code = 200
    mocked_response.url = args[0]
    mocked_response.content = '{"data":[]}'
    mocked_response.json = mock.MagicMock(return_value={"data": []})
    return mocked_response


@mock.patch("common.request.requests.get", side_effect=mocked_empty_response)
def test_get_articles_metadata_empty(mocked_response):
    parameters = APSParams(
        from_date="2021-01-01",
        until_date="2021-01-02",
    ).get_params()
    aps_api_client = APSApiClient()
    metadata = aps_api_client.get_articles_metadata(parameters=parameters)
    assert metadata is None
