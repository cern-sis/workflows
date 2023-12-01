import json

import pendulum
import requests
from airflow.decorators import dag, task
from aps.parser import APSParser
from common.enhancer import Enhancer
from common.enricher import Enricher
from common.utils import create_or_update_article
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
    return enriched_file


@dag(schedule=None, start_date=pendulum.today("UTC").add(days=-1))
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

    @task()
    def create_or_update(enriched_file):
        create_or_update_article(enriched_file)

    parsed_file = parse()
    enhanced_file = enchance(parsed_file)
    enriched_file = enrich(enhanced_file)
    validated_record = validate_record(enriched_file)
    create_or_update(validated_record)


dag_for_aps_files_processing = aps_process_file()
