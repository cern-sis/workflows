import xml.etree.ElementTree as ET

import pendulum
import requests
from airflow.decorators import dag, task
from common.enhancer import Enhancer
from common.enricher import Enricher
from common.exceptions import EmptyOutputFromPreviousTask
from common.utils import create_or_update_article
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
    return enriched_file


@dag(schedule=None, start_date=pendulum.today("UTC").add(days=-1))
def hindawi_file_processing():
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
    def validate_record(enriched_file):
        if not enriched_file:
            raise EmptyOutputFromPreviousTask("enrich")
        return hindawi_validate_record(enriched_file)

    @task()
    def create_or_update(enriched_file):
        create_or_update_article(enriched_file)

    parsed_file = parse()
    enhanced_file = enhance(parsed_file)
    enriched_file = enrich(enhanced_file)
    validated_record = validate_record(enriched_file)
    create_or_update(validated_record)


Hindawi_file_processing = hindawi_file_processing()
