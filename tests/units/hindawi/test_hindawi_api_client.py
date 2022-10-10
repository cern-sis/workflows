from hindawi.hindawi_api_client import HindawiApiClient
from hindawi.hindawi_params import HindawiParams
from pytest import fixture, mark, raises


@fixture
def pdf_file(shared_datadir):
    with open(shared_datadir / "3902819.pdf", "rb") as file:
        return file.read()


@mark.vcr
def test_hindawi_api_client_get_metadata():
    rest_api = HindawiApiClient(base_url="https://www.hindawi.com")
    parameters = HindawiParams(
        from_date="2022-01-01",
        until_date="2022-01-10",
    ).get_params()
    articles_metadata = rest_api.get_articles_metadata(parameters)
    assert articles_metadata is not None


@mark.vcr
def test_hindawi_api_client_get_not_existent_metadata():
    rest_api = HindawiApiClient(base_url="https://www.hindawi.com")
    parameters = HindawiParams(
        from_date="2022-01-01",
        until_date="2022-01-01",
    ).get_params()
    articles_metadata = rest_api.get_articles_metadata(parameters)
    assert articles_metadata is None


def test_hindawi_api_client_get_metadata_without_dates():
    rest_api = HindawiApiClient(base_url="https://www.hindawi.com")
    with raises(AttributeError, match=r"until date is required"):
        parameters = HindawiParams(
            from_date="",
            until_date="",
        ).get_params()
        rest_api.get_articles_metadata(parameters)


@mark.vcr
def test_hindawi_api_client_get_metadata_without_from_date():
    rest_api = HindawiApiClient(base_url="https://www.hindawi.com")
    parameters = HindawiParams(
        from_date="",
        until_date="2022-10-04",
    ).get_params()
    articles_metadata = rest_api.get_articles_metadata(parameters)
    assert articles_metadata is not None


@mark.vcr
def test_hindawi_api_client_get_metadata_with_wrong_dates():
    rest_api = HindawiApiClient(base_url="https://www.hindawi.com")
    parameters = HindawiParams(
        from_date="2022-10-02",
        until_date="2022-01-01",
    ).get_params()
    articles_metadata = rest_api.get_articles_metadata(parameters)
    assert articles_metadata is None


@mark.vcr
def test_hindawi_get_file(pdf_file):
    rest_api = HindawiApiClient(base_url="https://www.hindawi.com")
    parameters = HindawiParams(
        from_date="2022-01-01",
        until_date="2022-01-10",
    ).get_params()
    file = rest_api.get_file(parameters, "pdf", doi="10.1155/2019/3902819")
    assert file == pdf_file


@mark.vcr
def test_hindawi_get_file_with_wrong_DOI(pdf_file):
    rest_api = HindawiApiClient(base_url="https://www.hindawi.com")
    parameters = HindawiParams(
        from_date="2022-01-01",
        until_date="2022-01-10",
    ).get_params()
    file = rest_api.get_file(parameters, "pdf", doi="10.1155/2019/0000000")
    assert file is None


def test_hindawi_get_file_without_extension():
    rest_api = HindawiApiClient(base_url="https://www.hindawi.com")
    parameters = HindawiParams(
        from_date="2022-01-01",
        until_date="2022-01-10",
    ).get_params()
    with raises(AttributeError, match=r"The extension has to be pdf, pdfa or xml"):
        rest_api.get_file(
            parameters, "not_existent_extension", doi="10.1155/2019/3902819"
        )
