import base64

import pytest
import requests
from common.enhancer import Enhancer
from common.enricher import Enricher
from common.utils import parse_without_names_spaces
from elsevier.elsevier_file_processing import parse_elsevier
from elsevier.metadata_parser import ElsevierMetadataParser
from elsevier.parser import ElsevierParser
from jsonschema import validate
from pytest import fixture


@fixture(scope="module")
def parser():
    return ElsevierParser()


@fixture(scope="module")
def metadata_parser():
    return ElsevierMetadataParser(
        file_path="extracted/CERNQ000000010669A/CERNQ000000010669",
    )


@fixture
def parsed_article(shared_datadir, parser, metadata_parser):
    with open(
        shared_datadir / "CERNQ000000010011" / "S0370269323000643" / "main.xml"
    ) as file:
        parsed_file = parser.parse(parse_without_names_spaces(file.read()))
    with open(shared_datadir / "CERNQ000000010011" / "dataset.xml") as file:
        parsed_files_with_metadata = metadata_parser.parse(
            parse_without_names_spaces(file.read()),
        )
        full_parsed_file = {**parsed_file, **parsed_files_with_metadata[0]}
        enhanced_file = Enhancer()("Elsevier", full_parsed_file)
        return Enricher()(enhanced_file)


@pytest.mark.vcr
def test_elsevier_validate_record(parsed_article):
    schema = requests.get(parsed_article["$schema"]).json()
    validate(parsed_article, schema)


@pytest.mark.vcr
def test_parse_elsevier_task_and_validation(shared_datadir):
    with open(
        shared_datadir / "CERNQ000000010011" / "S0370269323000643" / "main.xml", "rb"
    ) as file:
        metadata = {
            "dois": [{"value": "10.1016/j.physletb.2023.137730"}],
            "date_published": "2023-02-04",
            "collections": [{"primary": "PLB"}],
            "license": [
                {
                    "url": "http://creativecommons.org/licenses/by/3.0/",
                    "license": "CC-BY-3.0",
                }
            ],
            "files": {
                "pdf": "extracted/CERNQ000000010669A/CERNQ000000010669/S0370269323000643/main.pdf",
                "pdfa": "extracted/CERNQ000000010669A/CERNQ000000010669/S0370269323000643/main_a-2b.pdf",
                "xml": "extracted/CERNQ000000010669A/CERNQ000000010669/S0370269323000643/main.xml",
            },
            "publication_info": [{"journal_title": "PLB", "year": 2023}],
        }
        kwargs = {
            "params": {
                "file_content": base64.b64encode(file.read()).decode(),
                "metadata": metadata,
            }
        }
        article = parse_elsevier(**kwargs)

        assert len(article["authors"]) == 1023
        assert (
            article["title"]
            == "System-size dependence of the charged-particle pseudorapidity density at <math altimg='si1.svg'><msqrt><mrow><msub><mrow><mi>s</mi></mrow><mrow><mi mathvariant='normal'>NN</mi></mrow></msub></mrow></msqrt><mo linebreak='goodbreak' linebreakstyle='after'>=</mo><mn>5.02</mn><mspace width='0.2em' /><mtext>TeV</mtext></math> for pp, p <glyph name='sbnd' />Pb, and Pb <glyph name='sbnd' />Pb collisions"
        )
        enhanced_file = Enhancer()("Elsevier", article)
        enriched_file = Enricher()(enhanced_file)
        schema = requests.get(enriched_file["$schema"]).json()
        validate(enriched_file, schema)


@pytest.mark.vcr
def test_parse_elsevier_task_and_validation_address_line(shared_datadir):
    with open(shared_datadir / "address-line-valid" / "main_rjjlr.xml", "rb") as file:
        metadata = {
            "dois": [{"value": "10.1016/j.physletb.2022.137649"}],
            "date_published": "2023-02-04",
            "collections": [{"primary": "PLB"}],
            "license": [
                {
                    "url": "http://creativecommons.org/licenses/by/3.0/",
                    "license": "CC-BY-3.0",
                }
            ],
            "files": {
                "pdf": "extracted/address-line-valid/main.pdf",
                "pdfa": "extracted/address-line-valid/main_a-2b.pdf",
                "xml": "extracted/address-line-valid/main_rjjlr.xml",
            },
            "publication_info": [{"journal_title": "PLB", "year": 2023}],
        }
        kwargs = {
            "params": {
                "file_content": base64.b64encode(file.read()).decode(),
                "metadata": metadata,
            }
        }
        article = parse_elsevier(**kwargs)

        assert len(article["authors"]) == 1032
        assert (
            article["title"]
            == "Study of charged particle production at high <italic>p</italic> <inf>T</inf> using event topology in pp, p&#8211;Pb and Pb&#8211;Pb collisions at <math altimg='si1.svg'><msqrt><mrow><msub><mrow><mi>s</mi></mrow><mrow><mi mathvariant='normal'>NN</mi></mrow></msub></mrow></msqrt><mo linebreak='goodbreak' linebreakstyle='after'>=</mo><mn>5.02</mn></math> <hsp sp='0.20' />TeV"
        )
        enhanced_file = Enhancer()("Elsevier", article)
        enriched_file = Enricher()(enhanced_file)
        schema = requests.get(enriched_file["$schema"]).json()
        validate(enriched_file, schema)
