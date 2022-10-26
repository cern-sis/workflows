import os

import boto3
from botocore.client import Config


def S3Service(bucket):
    return boto3.resource(
        "s3",
        endpoint_url=os.getenv("S3_ENDPOINT", "http://localhost:9000"),
        aws_access_key_id=os.getenv("S3_USERNAME", "airflow"),
        aws_secret_access_key=os.getenv("S3_PASSWORD", "Airflow01"),
        config=Config(signature_version="s3v4"),
        region_name=os.getenv("S3_REGION", "us-east-1"),
    ).Bucket(bucket)
