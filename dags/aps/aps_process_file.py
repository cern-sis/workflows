import json

import airflow
import requests
from airflow.decorators import dag, task
from aps.parser import APSParser
from common.enhancer import Enhancer
from common.enricher import Enricher
from jsonschema import validate


def parse_aps(data):
    parser = APSParser()
    parsed = parser.parse(data)
    return parsed


def enhance_aps(parsed_file):
    return Enhancer()("APS", parsed_file)


def enrich_aps(enhanced_file):
    return Enricher()(enhanced_file)


def aps_validate_record(enriched_file):
    schema = requests.get(enriched_file["$schema"]).json()
    validate(enriched_file, schema)


@dag(schedule_interval=None, start_date=airflow.utils.dates.days_ago(0))
def aps_process_file():
    @task()
    def parse(**kwargs):
        if "params" in kwargs and "article" in kwargs["params"]:
            article = json.loads(kwargs["params"]["article"])
            return parse_aps(article)

    @task()
    def enchance(parsed_file):
        return parsed_file and enhance_aps(parsed_file)

    @task()
    def enrich(enhanced_file):
        return enhanced_file and enrich_aps(enhanced_file)

    @task()
    def validate_record(enriched_file):
        return enriched_file and aps_validate_record(enriched_file)

    parsed_file = parse()
    enhanced_file = enchance(parsed_file)
    enriched_file = enrich(enhanced_file)
    validate_record(enriched_file)


dag_for_aps_files_processing = aps_process_file()
