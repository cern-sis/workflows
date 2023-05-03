import xml.etree.ElementTree as ET

import airflow
import requests
from airflow.decorators import dag, task
from common.enhancer import Enhancer
from common.enricher import Enricher
from hindawi.parser import HindawiParser
from jsonschema import validate


def parse_hindawi(xml):
    parser = HindawiParser()
    return parser.parse(xml)


def enhance_hindawi(parsed_file):
    return Enhancer()("Hindawi", parsed_file)


def enrich_hindawi(enhanced_file):
    return Enricher()(enhanced_file)


def hindawi_validate_record(enriched_file):
    schema = requests.get(enriched_file["$schema"]).json()
    validate(enriched_file, schema)


@dag(schedule=None, start_date=airflow.utils.dates.days_ago(0))
def hindawi_file_processing():
    @task()
    def parse(**kwargs):
        record = kwargs.get("params", {}).get("record")
        if not record:
            return None
        xml = ET.fromstring(record)
        return parse_hindawi(xml)

    @task()
    def enchance(parsed_file):
        return parsed_file and enhance_hindawi(parsed_file)

    @task()
    def enrich(enhanced_file):
        return enhanced_file and enrich_hindawi(enhanced_file)

    @task()
    def validate_record(enriched_file):
        return enriched_file and hindawi_validate_record(enriched_file)

    parsed_file = parse()
    enhanced_file = enchance(parsed_file)
    enriched_file = enrich(enhanced_file)
    validate_record(enriched_file)


Hindawi_file_processing = hindawi_file_processing()
