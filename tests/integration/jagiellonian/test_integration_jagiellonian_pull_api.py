import json
import os
from datetime import datetime, timezone
from unittest import mock
from unittest.mock import MagicMock
from urllib.parse import urlparse

import boto3
import pytest
from airflow.models import Connection, DagBag
from airflow.utils.session import create_session
from botocore.config import Config

endpoint = os.getenv("S3_ENDPOINT", "s3")
parsed = urlparse(endpoint if "://" in endpoint else f"http://{endpoint}")
MINIO_HOST = parsed.hostname or "s3"


@pytest.fixture(scope="class")
def dagbag():
    return DagBag(dag_folder="dags/", include_examples=False)


@pytest.mark.usefixtures("dagbag")
class TestIntegrationJagiellonianPullApi:
    def setup_method(self):
        with create_session() as session:
            session.query(Connection).filter(
                Connection.conn_id == "aws_s3_minio_test"
            ).delete()
            conn = Connection(
                conn_id="aws_s3_minio_test",
                conn_type="aws",
                host=MINIO_HOST,
                port=9000,
                login="airflow",
                password="Airflow01",
                extra=json.dumps(
                    {
                        "endpoint_url": f"http://{MINIO_HOST}:9000",
                        "region_name": "us-east-1",
                        "verify": False,
                    }
                ),
            )
            session.add(conn)

            session.query(Connection).filter(
                Connection.conn_id == "crossref_api_test"
            ).delete()
            conn = Connection(
                conn_id="crossref_api_test",
                conn_type="http",
                host="https://api.production.crossref.org",
            )
            session.add(conn)

            session.commit()

        self.dag_id = "jagiellonian_pull_api"
        self.execution_date = datetime.now(timezone.utc)

        self.dag = DagBag(dag_folder="dags/", include_examples=False).get_dag(
            self.dag_id
        )
        assert self.dag is not None, f"DAG {self.dag_id} failed to load"

        s3 = boto3.client(
            "s3",
            endpoint_url=f"http://{MINIO_HOST}:9000",
            aws_access_key_id="airflow",
            aws_secret_access_key="Airflow01",
            region_name="us-east-1",
            config=Config(signature_version="s3v4"),
            verify=False,
        )

        s3.create_bucket(Bucket="jagiellonian-test", ACL="public-read-write")
        response = s3.list_objects_v2(Bucket="jagiellonian-test")

        if "Contents" in response:
            objects_to_delete = [{"Key": obj["Key"]} for obj in response["Contents"]]

            if objects_to_delete:
                s3.delete_objects(
                    Bucket="jagiellonian", Delete={"Objects": objects_to_delete}
                )

    def teardown_method(self):
        with create_session() as session:
            session.query(Connection).filter(
                Connection.conn_id == "aws_s3_minio_test"
            ).delete()

            session.query(Connection).filter(
                Connection.conn_id == "crossref_api_test"
            ).delete()

            session.commit()

        s3 = boto3.client(
            "s3",
            endpoint_url=f"http://{MINIO_HOST}:9000",
            aws_access_key_id="airflow",
            aws_secret_access_key="Airflow01",
            region_name="us-east-1",
            config=Config(signature_version="s3v4"),
            verify=False,
        )
        response = s3.list_objects_v2(Bucket="jagiellonian-test")

        if "Contents" in response:
            objects_to_delete = [{"Key": obj["Key"]} for obj in response["Contents"]]

            if objects_to_delete:
                s3.delete_objects(
                    Bucket="jagiellonian-test", Delete={"Objects": objects_to_delete}
                )

        s3.delete_bucket(Bucket="jagiellonian-test")

    @mock.patch.dict(
        os.environ,
        {
            "JAGIELLONIAN_BUCKET_NAME": "jagiellonian-test",
            "AWS_CONN_ID": "aws_s3_minio_test",
            "HTTP_CONN_ID": "crossref_api_test",
        },
    )
    @mock.patch("airflow.providers.http.hooks.http.HttpHook.run")
    def test_fetch_crossref_api(self, mock_http_run):
        mock_http_response = MagicMock()
        mock_http_response.json.return_value = {
            "message": {"items": [], "total-results": 0}
        }
        mock_http_response.raise_for_status = MagicMock()
        mock_http_run.return_value = mock_http_response

        s3 = boto3.client(
            "s3",
            endpoint_url=f"http://{MINIO_HOST}:9000",
            aws_access_key_id="airflow",
            aws_secret_access_key="Airflow01",
            region_name="us-east-1",
            config=Config(signature_version="s3v4"),
            verify=False,
        )
        s3.put_object(Bucket="jagiellonian-test", Key="test.json", Body=b"")

        task = self.dag.get_task("jagiellonian_fetch_crossref_api")
        function_to_unit_test = task.python_callable

        results = function_to_unit_test()

        assert mock_http_run.called

        called_endpoint = mock_http_run.call_args[1]["data"]["filter"]
        assert "from-created-date:" in called_endpoint

        assert results == []
