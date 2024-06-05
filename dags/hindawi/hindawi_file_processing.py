import xml.etree.ElementTree as ET

import pendulum
from airflow.decorators import dag, task
from inspire_utils.inspire_utils import get_value
from common.enhancer import Enhancer
from common.enricher import Enricher
from common.exceptions import EmptyOutputFromPreviousTask
from common.scoap3_s3 import Scoap3Repository
from common.utils import create_or_update_article, upload_json_to_s3
from hindawi.parser import HindawiParser
from hindawi.repository import HindawiRepository
from structlog import get_logger

logger = get_logger()


def parse_hindawi(xml):
    parser = HindawiParser()
    return parser.parse(xml)


def enhance_hindawi(parsed_file):
    return Enhancer()("Hindawi", parsed_file)


def enrich_hindawi(enhanced_file):
    return Enricher()(enhanced_file)


@dag(schedule=None, start_date=pendulum.today("UTC").add(days=-1))
def scoap3_hindawi_file_processing():
    s3_client = HindawiRepository()

    @task()
    def parse(**kwargs):
        record = kwargs.get("params", {}).get("record")
        if not record:
            return None
        xml = ET.fromstring(record)
        return parse_hindawi(xml)

    @task()
    def enhance(parsed_file):
        if not parsed_file:
            raise EmptyOutputFromPreviousTask("parse")
        return enhance_hindawi(parsed_file)

    @task()
    def enrich(enhanced_file):
        if not enhanced_file:
            raise EmptyOutputFromPreviousTask("enhance")
        return enrich_hindawi(enhanced_file)

    @task()
    def populate_files(parsed_file):
        if "dois" not in parsed_file:
            return parsed_file

        doi = get_value(parsed_file, "dois.value[0]")
        logger.info("Populating files", doi=doi)
        doi_part = doi.split("10.1155/")[1]
        files = {
            "pdf": f"http://downloads.hindawi.com/journals/ahep/{doi_part}.pdf",
            "pdfa": f"http://downloads.hindawi.com/journals/ahep/{doi_part}.a.pdf",
            "xml": f"http://downloads.hindawi.com/journals/ahep/{doi_part}.xml",
        }
        s3_scoap3_client = Scoap3Repository()
        downloaded_files = s3_scoap3_client.download_files(files, prefix=doi)
        parsed_file["files"] = downloaded_files
        logger.info("Files populated", files=parsed_file["files"])
        return parsed_file

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


Hindawi_file_processing = scoap3_hindawi_file_processing()
