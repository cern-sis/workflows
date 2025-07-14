import json
import os
from datetime import datetime, timezone

import pendulum
from airflow.decorators import dag, task
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.amazon.aws.transfers.http_to_s3 import HttpToS3Operator
from common.enhancer import Enhancer
from common.enricher import Enricher
from common.utils import create_or_update_article
from jagiellonian.parser import JagiellonianParser
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


@dag(schedule=None, start_date=pendulum.today("UTC").add(days=-1))
def jagiellonian_process_file():
    @task(task_id="jagiellonian-parse")
    def parse(**kwargs):
        if "params" in kwargs and "article" in kwargs["params"]:
            article = kwargs["params"]["article"]
            parsed = JagiellonianParser().parse(article)

            if "dois" not in parsed:
                raise ValueError("DOI not found in metadata")

            return parsed

    @task(task_id="jagiellonian-populate-files")
    def populate_files(parsed_file):
        aws_conn_id = os.getenv("AWS_CONN_ID", "aws_s3_minio")
        scoap3_bucket = os.getenv("SCOAP3_BUCKET_NAME", "scoap3")
        upload_dir = os.getenv("SCOAP3_BUCKET_UPLOAD_DIR", "files")

        if "files" not in parsed_file:
            return parsed_file

        doi = parsed_file.get("dois")[0]["value"]
        logger.info("Populating files", doi=doi)
        files = parsed_file.get("files")

        prefix = doi

        downloaded_files = {}

        for type, url in files.items():
            try:
                filename = os.path.basename(url)
                filename = update_filename_extension(filename, type)

                destination_key = f"{upload_dir}/{prefix}/{filename}"

                transfer_to_s3 = HttpToS3Operator(
                    task_id="transfer-to-s3",
                    http_conn_id=None,
                    endpoint=url,
                    s3_bucket=scoap3_bucket,
                    s3_key=destination_key,
                    aws_conn_id=aws_conn_id,
                    replace=True,
                )

                transfer_to_s3.execute(context={})

                downloaded_files[type] = f"{scoap3_bucket}/{destination_key}"
                logger.info("Downloaded file", type=type, url=url)
            except Exception as e:
                logger.error(
                    "Failed to download file", error=str(e), type=type, url=url
                )

        parsed_file["files"] = downloaded_files
        logger.info("Files populated", files=parsed_file["files"])

        return parsed_file

    @task(task_id="jagiellonian-enhance")
    def enhance(enhanced_file):
        return Enhancer()("Jagiellonian", enhanced_file)

    @task(task_id="jagiellonian-enrich")
    def enrich(enhanced_file):
        return Enricher()(enhanced_file)

    @task(task_id="jagiellonian-save-to-s3")
    def save_to_s3(enriched_file):
        s3_bucket = os.getenv("JAGIELLONIAN_BUCKET_NAME", "jagiellonian")
        aws_conn_id = os.getenv("AWS_CONN_ID", "aws_s3_minio")

        doi = enriched_file["dois"][0]["value"]
        key = f"{doi}_metadata_{(datetime.now(timezone.utc))}.json"

        s3_hook = S3Hook(aws_conn_id=aws_conn_id)

        s3_hook.load_string(
            string_data=json.dumps(enriched_file, indent=2),
            key=key,
            bucket_name=s3_bucket,
            replace=True,
        )

    @task()
    def create_or_update(enriched_file):
        create_or_update_article(enriched_file)

    parsed_file = parse()
    parsed_file_with_files = populate_files(parsed_file)
    enhanced_file = enhance(parsed_file_with_files)
    enriched_file = enrich(enhanced_file)
    save_to_s3(enriched_file=enriched_file)
    create_or_update(enriched_file)


dag_for_jagiellonian_files_processing = jagiellonian_process_file()
