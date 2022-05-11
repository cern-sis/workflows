from datetime import date, datetime
from io import BytesIO

import pytest
from airflow.models import DagBag
from aps.utils import save_file_in_s3, set_APS_harvesting_interval, split_json

DAG_NAME = "aps_fetch_api"
TRIGGERED_DAG_NAME = "aps_process_file"


@pytest.fixture
def dag():
    dagbag = DagBag(dag_folder="dags/", include_examples=False)
    assert dagbag.import_errors.get(f"dags/{DAG_NAME}.py") is None
    return dagbag.get_dag(dag_id=DAG_NAME)


class MockedRepo:
    def find_the_last_uploaded_file_date(self):
        today = date.today()
        return today

    def save(self, key, file):
        pass

    def find_by_id(self, id):
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
    today = date.today()
    expected_days = {
        "aps_fetching_from_date": today.strftime("%Y-%m-%d"),
        "aps_fetching_until_date": today.strftime("%Y-%m-%d"),
    }
    dates = set_APS_harvesting_interval(repo)
    assert dates == expected_days


def test_save_file_in_s3():
    today = date.today()
    repo = MockedRepo()
    exptected_key = f'{today.strftime("%Y-%m-%d")}/{ datetime.now().strftime("%Y-%m-%dT%H:%M")}.json'
    data = str.encode('{"data": ["abstracts": "abstract value"]}')
    key = save_file_in_s3(data, repo)
    assert key == exptected_key


def test_split_json():
    doi = "10.1103/PhysRevLett.126.153601"
    today = datetime.now().strftime("%Y-%m-%dT%H:%M")
    ids_and_articles = split_json(repo=MockedRepo(), key="key/key")
    expected_id = f"APS_{doi}_{today}"
    assert ids_and_articles[0]["id"] == expected_id
    assert len(ids_and_articles) == 1
