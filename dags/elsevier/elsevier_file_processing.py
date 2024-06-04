import pendulum
from airflow.decorators import dag, task
from common.enhancer import Enhancer
from common.enricher import Enricher
from common.exceptions import EmptyOutputFromPreviousTask
from common.scoap3_s3 import Scoap3Repository
from common.utils import (
    create_or_update_article,
    parse_without_names_spaces,
    upload_json_to_s3,
)
from elsevier.parser import ElsevierParser
from elsevier.repository import ElsevierRepository
from inspire_utils.inspire_utils import get_value
from structlog import get_logger

logger = get_logger()


def parse_elsevier(**kwargs):
    xml_content_bytes = kwargs["params"]["file_content"]

    xml = parse_without_names_spaces(xml_content_bytes)
    parser = ElsevierParser()
    parsed = parser.parse(xml)
    try:
        metadata = kwargs["params"]["metadata"]
    except KeyError:
        raise Exception("Record is missing metadata. Exiting run.")
    return {**parsed, **metadata}


def enhance_elsevier(parsed_file):
    return Enhancer()("Elsevier", parsed_file)


def enrich_elsevier(enhanced_file):
    return Enricher()(enhanced_file)


@dag(schedule=None, start_date=pendulum.today("UTC").add(days=-1))
def elsevier_process_file():

    s3_client = ElsevierRepository()

    @task()
    def parse(**kwargs):
        xml_path = kwargs["params"]["file_name"]
        xml_content_bytes = s3_client.get_by_id(xml_path)
        kwargs["params"]["file_content"] = xml_content_bytes
        return parse_elsevier(**kwargs)

    @task()
    def enhance(parsed_file):
        if parsed_file:
            return parsed_file and enhance_elsevier(parsed_file)
        raise EmptyOutputFromPreviousTask("parse_metadata")

    @task()
    def populate_files(parsed_file):
        if "files" not in parsed_file:
            logger.info("No files to populate")
            return parsed_file

        logger.info("Populating files", files=parsed_file["files"])

        s3_client_bucket = s3_client.bucket
        s3_scoap3_client = Scoap3Repository()
        doi = get_value(parsed_file, "dois.value[0]")
        files = s3_scoap3_client.copy_files(
            s3_client_bucket, parsed_file["files"], prefix=doi
        )
        parsed_file["files"] = files
        logger.info("Files populated", files=parsed_file["files"])
        return parsed_file

    @task()
    def enrich(enhanced_file):
        if enhanced_file:
            return enrich_elsevier(enhanced_file)
        raise EmptyOutputFromPreviousTask("enhanced_file_with_metadata")

    @task()
    def save_to_s3(enriched_file):
        upload_json_to_s3(json_record=enriched_file, repo=s3_client)

    @task()
    def create_or_update(enriched_file):
        create_or_update_article(enriched_file)

    parsed_file = parse()
    enhanced_file = enhance(parsed_file)
    enhanced_file_with_files = populate_files(enhanced_file)
    enriched_file = enrich(enhanced_file_with_files)
    save_to_s3(enriched_file=enriched_file)
    create_or_update(enriched_file)


Elsevier_file_processing = elsevier_process_file()
