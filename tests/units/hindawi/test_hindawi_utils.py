from datetime import date, datetime
from io import BytesIO

from common.utils import set_harvesting_interval
from hindawi.utils import save_file_in_s3, split_xmls

DAG_NAME = "hindawi_fetch_api"
TRIGGERED_DAG_NAME = "hindawi_file_processing"
hindawi_xml = "<wrapper><ListRecords><record>record</record></ListRecords></wrapper>"


class MockedRepo:
    def find_the_last_uploaded_file_date(self):
        today = date.today().strftime("%Y-%m-%d")
        return today

    def save(self, key, file):
        pass

    def find_by_id(self, id):
        return BytesIO(str.encode(hindawi_xml))

    def find_all(self):
        return len([])


class MockedHindawiApiClient:
    def get_articles_metadata(self, parameters):
        return hindawi_xml


def test_set_Hindawi_harvesting_interval(repo=MockedRepo()):
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
    expected_key = f'{today}/{ datetime.now().strftime("%Y-%m-%dT%H:%M")}.xml'
    data = str.encode(hindawi_xml)
    key = save_file_in_s3(data, repo)
    assert key == expected_key


def test_split_xml():
    records = split_xmls(repo=MockedRepo(), key="key/key")
    assert len(records) == 1
