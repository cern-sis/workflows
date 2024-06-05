import os

import pytest
from common.request import Request
from aps.aps_params import APSParams

dates = {
    "from_date": "2022-02-05",
    "until_date": "2022-03-05",
}
parameters = APSParams(
    from_date=dates["from_date"], until_date=dates["until_date"]
).get_params()

exptected_params = {
    "base_url": os.getenv("APS_API_BASE_URL", "http://harvest.aps.org"),
    "parameters": parameters,
}


@pytest.fixture
def rest_api_fixture():
    return Request(
        base_url=os.getenv("APS_API_BASE_URL", "http://harvest.aps.org"),
        parameters=parameters,
    )


@pytest.fixture
def rest_api_with_params_fixture(rest_api_fixture):
    rest_api = rest_api_fixture
    assert exptected_params == rest_api.get_parameters()
    return rest_api


@pytest.mark.vcr
def test_get_response(rest_api_with_params_fixture):
    reponse = rest_api_with_params_fixture.get_response()
    assert reponse.status_code == 200
