import json
import os
from datetime import datetime, timezone
from unittest import mock

import boto3
import pytest
from airflow.models import Connection, DagBag, DagRun, TaskInstance
from airflow.utils.session import create_session
from botocore.config import Config


@pytest.fixture(scope="class")
def dagbag():
    return DagBag(dag_folder="dags/", include_examples=False)


@pytest.mark.usefixtures("dagbag")
class TestJagiellonianProcessFile:
    def setup_method(self):
        with create_session() as session:
            session.query(Connection).filter(
                Connection.conn_id == "aws_s3_minio_test"
            ).delete()
            conn = Connection(
                conn_id="aws_s3_minio_test",
                conn_type="aws",
                host="s3",
                port=9000,
                login="airflow",
                password="Airflow01",
                extra=json.dumps(
                    {
                        "endpoint_url": "http://s3:9000",
                        "region_name": "us-east-1",
                        "verify": False,
                    }
                ),
            )
            session.add(conn)

            session.commit()

        self.dag_id = "jagiellonian_process_file"
        self.execution_date = datetime.now(timezone.utc)

        self.dag = DagBag(dag_folder="dags/", include_examples=False).get_dag(
            self.dag_id
        )
        assert self.dag is not None, f"DAG {self.dag_id} failed to load"

        s3 = boto3.client(
            "s3",
            endpoint_url="http://s3:9000",
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
            session.query(TaskInstance).filter(
                TaskInstance.dag_id == self.dag_id
            ).delete(synchronize_session="fetch")

            session.query(DagRun).filter(DagRun.dag_id == self.dag_id).delete(
                synchronize_session="fetch"
            )

            session.query(Connection).filter(
                Connection.conn_id == "aws_s3_minio_test"
            ).delete()

            session.commit()

        s3 = boto3.client(
            "s3",
            endpoint_url="http://s3:9000",
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
        },
    )
    def test_save_to_s3(self):
        sample_article = {
            "title": "Test Article",
            "authors": ["Author 1", "Author 2"],
            "abstract": "This is a test abstract",
            "dois": [{"value": "10.1234/test.123"}],
            "files": [],
        }

        task = self.dag.get_task("jagiellonian-save-to-s3")
        function_to_unit_test = task.python_callable

        function_to_unit_test(sample_article)

        s3 = boto3.client(
            "s3",
            endpoint_url="http://s3:9000",
            aws_access_key_id="airflow",
            aws_secret_access_key="Airflow01",
            region_name="us-east-1",
            config=Config(signature_version="s3v4"),
            verify=False,
        )

        response = s3.list_objects_v2(Bucket="jagiellonian-test")

        assert "10.1234-test.123" in response["Contents"][0]["Key"]

    @mock.patch.dict(
        os.environ,
        {
            "SCOAP3_BUCKET_NAME": "jagiellonian-test",
            "SCOAP3_BUCKET_UPLOAD_DIR": "files",
            "AWS_CONN_ID": "aws_s3_minio_test",
        },
    )
    @mock.patch("requests.get")
    def test_populate_files(self, mock_get):
        mock_response = mock.Mock()
        mock_response.content = b"This is a test PDF content"
        mock_response.raise_for_status = mock.Mock()
        mock_get.return_value = mock_response

        sample_article = {
            "title": "Test Article",
            "authors": ["Author 1", "Author 2"],
            "abstract": "This is a test abstract",
            "dois": [{"value": "10.1234/test.123"}],
            "files": {
                "pdf": "https://example.com/article.pdf",
                "xml": "https://example.com/article.xml",
            },
        }

        task = self.dag.get_task("jagiellonian-populate-files")
        function_to_unit_test = task.python_callable

        result = function_to_unit_test(sample_article)

        assert mock_get.call_count == 2
        mock_get.assert_any_call("https://example.com/article.pdf")
        mock_get.assert_any_call("https://example.com/article.xml")

        s3 = boto3.client(
            "s3",
            endpoint_url="http://s3:9000",
            aws_access_key_id="airflow",
            aws_secret_access_key="Airflow01",
            region_name="us-east-1",
            config=Config(signature_version="s3v4"),
            verify=False,
        )

        response = s3.list_objects_v2(Bucket="jagiellonian-test")

        assert "Contents" in response
        assert len(response["Contents"]) == 2

        safe_doi = "10.1234-test.123"
        uploaded_keys = [obj["Key"] for obj in response["Contents"]]

        assert any(f"files/{safe_doi}/article.pdf" in key for key in uploaded_keys)
        assert any(f"files/{safe_doi}/article.xml" in key for key in uploaded_keys)

        assert "files" in result
        assert "pdf" in result["files"]
        assert "xml" in result["files"]
        assert (
            result["files"]["pdf"] == f"jagiellonian-test/files/{safe_doi}/article.pdf"
        )
        assert (
            result["files"]["xml"] == f"jagiellonian-test/files/{safe_doi}/article.xml"
        )
