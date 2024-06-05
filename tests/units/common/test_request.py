from unittest import mock

from common.request import Request


def mocked_get_response(*args, **kwrgs):
    mocked_response = mock.Mock()
    mocked_response.status_code = 200
    mocked_response.url = args[0]
    mocked_response.content = '{"content": "content"}'
    mocked_response.json = mock.MagicMock(return_value={"content": "content"})
    return mocked_response


@mock.patch("scoap3.common.request.requests.get", side_effect=mocked_get_response)
def test_get_url_forming(mocked_requests):
    base_url = "https://www.test.com"
    path_segments = ["a", "b", "c"]
    parameters = {"parameter1": 1, "parameter2": 2}
    expected_url = "https://www.test.com/a/b/c?parameter1=1&parameter2=2"
    response = Request(
        base_url=base_url, path_segments=path_segments, parameters=parameters
    ).get_response()
    assert response.url == expected_url


@mock.patch("scoap3.common.request.requests.get", side_effect=mocked_get_response)
def test_get_response_content(mocked_response):
    base_url = "https://www.test.com"
    path_segments = ["a", "b", "c"]
    parameters = {"parameter1": 1, "parameter2": 2}
    response_content = Request(
        base_url=base_url, path_segments=path_segments, parameters=parameters
    ).get_response_bytes()
    assert response_content == '{"content": "content"}'
    response_content_json = Request(
        base_url=base_url, path_segments=path_segments, parameters=parameters
    ).get_response_json()
    assert response_content_json == {"content": "content"}
