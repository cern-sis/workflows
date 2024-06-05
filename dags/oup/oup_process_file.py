import base64

import pendulum
import requests
from airflow.decorators import dag, task
from inspire_utils.inspire_utils import get_value
from jsonschema import validate
from common.enhancer import Enhancer
from common.enricher import Enricher
from common.exceptions import EmptyOutputFromPreviousTask
from common.scoap3_s3 import Scoap3Repository
from common.utils import (
    create_or_update_article,
    parse_without_names_spaces,
    upload_json_to_s3,
)
from oup.parser import OUPParser
from oup.repository import OUPRepository
from structlog import get_logger

logger = get_logger()


def oup_parse_file(**kwargs):
    if "params" not in kwargs or "file" not in kwargs["params"]:
        raise KeyError("There was no 'file' parameter. Exiting run.")
    encoded_xml = kwargs["params"]["file"]
    file_name = kwargs["params"]["file_name"]
    xml_bytes = base64.b64decode(encoded_xml)
    xml = parse_without_names_spaces(xml_bytes.decode("utf-8"))

    parser = OUPParser(file_name)
    parsed = parser.parse(xml)

    return parsed


def oup_enhance_file(parsed_file):
    return Enhancer()("OUP", parsed_file)


def oup_enrich_file(enhanced_file):
    return Enricher()(enhanced_file)


def oup_validate_record(enriched_file):
    schema = requests.get(enriched_file["$schema"]).json()
    validate(enriched_file, schema)
    return enriched_file


@dag(schedule=None, start_date=pendulum.today("UTC").add(days=-1))
def scoap3_oup_process_file():
    s3_client = OUPRepository()

    @task()
    def parse_file(**kwargs):
        return oup_parse_file(**kwargs)

    @task()
    def enhance_file(parsed_file):
        if not parsed_file:
            raise EmptyOutputFromPreviousTask("parse_file")
        return oup_enhance_file(parsed_file)

    @task()
    def enrich_file(enhanced_file):
        if not enhanced_file:
            raise EmptyOutputFromPreviousTask("enhance_file")
        return oup_enrich_file(enhanced_file)

    @task()
    def populate_files(parsed_file):
        if "files" not in parsed_file:
            logger.info("No files to populate")
            return parsed_file

        logger.info("Populating files", files=parsed_file["files"])

        s3_client_bucket = OUPRepository().bucket
        s3_scoap3_client = Scoap3Repository()
        doi = get_value(parsed_file, "dois.value[0]")
        files = s3_scoap3_client.copy_files(
            s3_client_bucket, parsed_file["files"], prefix=doi
        )
        parsed_file["files"] = files
        logger.info("Files populated", files=parsed_file["files"])
        return parsed_file

    @task()
    def create_or_update(enriched_file):
        create_or_update_article(enriched_file)

    @task()
    def save_to_s3(enriched_file):
        upload_json_to_s3(json_record=enriched_file, repo=s3_client)

    parsed_file = parse_file()
    enhanced_file = enhance_file(parsed_file)
    enhanced_file_with_files = populate_files(enhanced_file)
    enriched_file = enrich_file(enhanced_file_with_files)
    save_to_s3(enriched_file=enriched_file)
    create_or_update(enriched_file)


dag_taskflow = scoap3_oup_process_file()
