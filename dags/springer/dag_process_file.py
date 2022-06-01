import base64
import xml.etree.ElementTree as ET

import airflow
import requests
from airflow.decorators import dag, task
from common.enhancer import Enhancer
from common.enricher import Enricher
from jsonschema import validate
from springer.parser import SpringerParser


def springer_parse_file(**kwargs):
    if "params" in kwargs and "file" in kwargs["params"]:
        encoded_xml = kwargs["params"]["file"]
        xml_bytes = base64.b64decode(encoded_xml)
        xml = ET.fromstring(xml_bytes.decode("utf-8"))

        parser = SpringerParser()
        parsed = parser.parse(xml)

        return parsed
    raise Exception("There was no 'file' parameter. Exiting run.")


def springer_enhance_file(parsed_file):
    return Enhancer()("Springer", parsed_file)


def springer_enrich_file(enhanced_file):
    return Enricher()(enhanced_file)


def springer_validate_record(enriched_file):
    schema = requests.get(enriched_file["$schema"]).json()
    validate(enriched_file, schema)


@dag(start_date=airflow.utils.dates.days_ago(0))
def springer_process_file():
    @task()
    def parse_file(**kwargs):
        return springer_parse_file(**kwargs)

    @task()
    def enhance_file(parsed_file):
        return springer_enhance_file(parsed_file)

    @task()
    def enrich_file(enhanced_file):
        return springer_enrich_file(enhanced_file)

    @task()
    def validate_record(enriched_file):
        springer_validate_record(enriched_file)

    parsed_file = parse_file()
    enhanced_file = enhance_file(parsed_file)
    enriched_file = enrich_file(enhanced_file)
    validate_record(enriched_file)


dag_taskflow = springer_process_file()

{
    "dois": [{"value": "10.1140/epjc/s10052-019-6540-y"}],
    "arxiv_eprints": [{"value": "1807.07447v1", "categories": ["hep-ex"]}],
    "page_nr": [45],
    "abstract": "This paper describes a strategy for a general search used by the ATLAS Collaboration to find potential indications of new physics. Events are classified according to their final state into many event classes. For each event class an automated search algorithm tests whether the data are compatible with the Monte Carlo simulated expectation in several distributions sensitive to the effects of new physics. The significance of a deviation is quantified using pseudo-experiments. A data selection with a significant deviation defines a signal region for a dedicated follow-up analysis with an improved background expectation. The analysis of the data-derived signal regions on a new dataset allows a statistical interpretation without the large look-elsewhere effect. The sensitivity of the approach is discussed using Standard Model processes and benchmark signals of new physics. As an example, results are shown for 3.2 fb $$^{-1}$$ of proton–proton collision data at a centre-of-mass energy of 13 $$\\text {TeV}$$ collected with the ATLAS detector at the LHC in 2015, in which more than 700 event classes and more than $$10^5$$ regions have been analysed. No significant deviations are found and consequently no data-derived signal regions for a follow-up analysis have been defined.",
    "collaborations": [{"value": "ATLAS Collaboration"}],
    "license": [
        {"license": "CC-BY-4.0", "url": "https://creativecommons.org/licenses//by/4.0"}
    ],
    "collections": [{"primary": "European Physical Journal C"}],
    "publication_info": [
        {
            "journal_title": "European Physical Journal C",
            "journal_volume": "79",
            "year": 2019,
            "journal_issue": "2",
            "artid": "s10052-019-6540-y",
            "page_start": "1",
            "page_end": "45",
            "material": "article",
        }
    ],
    "abstracts": [{"source": "Springer"}],
    "acquisition_source": {
        "source": "Springer",
        "method": "Springer",
        "date": "2022-06-01T17:07:24.153583",
        "submission_number": "path/to/the/file",
    },
    "copyright": [
        {"holder": "CERN for the benefit of the ATLAS collaboration", "year": "2019"}
    ],
    "imprints": [{"date": "2019-02-06", "publisher": "Springer"}],
    "record_creation_date": "2022-06-01T17:07:24.153583",
    "titles": [
        {
            "title": "A strategy for a general search for new phenomena using data-derived signal regions and its application within the ATLAS experiment",
            "source": "Springer",
        }
    ],
    "$schema": "http://repo.qa.scoap3.org/schemas/hep.json",
}
