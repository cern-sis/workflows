from datetime import date, datetime
from io import BytesIO

from aps.utils import save_file_in_s3, split_json
from common.utils import set_harvesting_interval

DAG_NAME = "aps_fetch_api"
TRIGGERED_DAG_NAME = "aps_process_file"


class MockedRepo:
    def find_the_last_uploaded_file_date(self):
        today = date.today().strftime("%Y-%m-%d")
        return today

    def save(self, key, file):
        pass

    def get_by_id(self, id):
        return BytesIO(
            str.encode(
                '{"data":[{"abstract":\
                    {"value":"<p>We propose and theoretically analyze</p>"},\
                    "identifiers":{"doi":"10.1103/PhysRevLett.126.153601"}}]}'
            )
        )

    def find_all(self):
        return len([])


class MockedAPSApiClient:
    def get_articles_metadata(self, parameters):
        return {
            "data": [
                {"abstract": {"value": "<p>We propose and theoretically analyze</p>"}}
            ]
        }


def test_set_APS_harvesting_interval(repo=MockedRepo()):
    today = date.today().strftime("%Y-%m-%d")
    expected_days = {
        "start_date": today,
        "until_date": today,
    }
    dates = set_harvesting_interval(repo)
    assert dates == expected_days


def test_save_file_in_s3():
    today = date.today()
    repo = MockedRepo()
    expected_key = f'{today}/{ datetime.now().strftime("%Y-%m-%dT%H:%M")}.json'
    data = str.encode('{"data": ["abstracts": "abstract value"]}')
    key = save_file_in_s3(data, repo)
    assert key == expected_key


def test_split_json():
    doi = "10.1103/PhysRevLett.126.153601"
    today = datetime.now().strftime("%Y-%m-%dT%H:%M")
    ids_and_articles = split_json(repo=MockedRepo(), key="key/key")
    expected_id = f"APS_{doi}_{today}"
    assert ids_and_articles[0]["id"] == expected_id
    assert len(ids_and_articles) == 1
