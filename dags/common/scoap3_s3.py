import os
from uuid import uuid4

import requests
from common.repository import IRepository
from common.s3_service import S3Service
from structlog import get_logger

logger = get_logger()

FILE_EXTENSIONS = {"pdf": ".pdf", "xml": ".xml", "pdfa": ".pdf"}


def update_filename_extension(filename, type):
    extension = FILE_EXTENSIONS.get(type, "")
    if filename.endswith(extension):
        return filename
    elif extension:
        if type == "pdfa":
            extension = ".a-2b.pdf"
        return f"{filename}{extension}"


class Scoap3Repository(IRepository):
    def __init__(self):
        super().__init__()
        self.bucket = os.getenv("SCOAP3_BUCKET_NAME", "scoap3")
        self.upload_dir = os.getenv("SCOAP3_BUCKET_UPLOAD_DIR", "files")
        self.upload_enabled = os.getenv("SCOAP3_REPO_S3_ENABLED", False)
        self.s3 = S3Service(self.bucket)
        self.client = self.s3.meta.client

    def copy_file(self, source_bucket, source_key, prefix=None, type=None):
        if not self.upload_enabled:
            return ""

        if not prefix:
            prefix = str(uuid4())

        copy_source = {"Bucket": source_bucket, "Key": source_key}
        filename = os.path.basename(source_key)
        filename = update_filename_extension(filename, type)
        destination_key = f"{self.upload_dir}/{prefix}/{filename}"

        logger.info("Copying file from", copy_source=copy_source)
        self.client.copy(
            copy_source,
            self.bucket,
            destination_key,
            ExtraArgs={
                "Metadata": {
                    "source_bucket": source_bucket,
                    "source_key": source_key,
                },
                "MetadataDirective": "REPLACE",
                "ACL": "public-read",
            },
        )
        logger.info(
            f"Copied file from {source_bucket}/{source_key} to {self.bucket}/{destination_key}"
        )
        return f"{self.bucket}/{destination_key}"

    def copy_files(self, bucket, files, prefix=None):
        copied_files = {}
        for type, path in files.items():
            try:
                copied_files[type] = self.copy_file(
                    bucket, path, prefix=prefix, type=type
                )
            except Exception as e:
                logger.error("Failed to copy file.", error=str(e), type=type, path=path)
        return copied_files

    def download_files(self, files, prefix=None):
        if not prefix:
            prefix = str(uuid4())

        downloaded_files = {}

        for type, url in files.items():
            try:
                downloaded_files[type] = self.download_and_upload_to_s3(
                    url, prefix=prefix, type=type
                )
                logger.info("Downloaded file", type=type, url=url)
            except Exception as e:
                logger.error(
                    "Failed to download file.", error=str(e), type=type, url=url
                )
        return downloaded_files

    def download_files_for_aps(self, files, prefix=None):
        if not prefix:
            prefix = str(uuid4())

        downloaded_files = {}

        for type, url in files.items():
            headers = {
                "Accept": f"application/{type}",
            }
            try:
                downloaded_files[type] = self.download_and_upload_to_s3(
                    url, prefix=prefix, headers=headers, type=type
                )
                logger.info("Downloaded file", type=type, url=url)
            except Exception as e:
                logger.error(
                    "Failed to download file.", error=str(e), type=type, url=url
                )
        return downloaded_files

    def download_and_upload_to_s3(self, url, prefix=None, headers=None, type=None):
        if not self.upload_enabled:
            return ""

        if not prefix:
            prefix = str(uuid4())

        filename = os.path.basename(url)
        filename = update_filename_extension(filename, type)
        destination_key = f"{self.upload_dir}/{prefix}/{filename}"

        response = requests.get(url, headers=headers)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logger.error("Failed to download file", error=str(e), url=url)
            return

        try:
            # Upload the file to S3
            self.client.put_object(
                Body=response.content,
                Bucket=self.bucket,
                Key=destination_key,
                Metadata={
                    "source_url": url,
                },
            )
            return f"{self.bucket}/{destination_key}"
        except Exception as e:
            logger.error(
                "Failed to upload file",
                error=str(e),
                bucket=self.bucket,
                key=destination_key,
            )
