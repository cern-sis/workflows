import json

import pytest
from jagiellonian.parser import JagiellonianParser


@pytest.fixture(scope="module")
def parser():
    return JagiellonianParser()


@pytest.fixture
def article(shared_datadir):
    json_response = (shared_datadir / "json_response_content.json").read_text()
    return json.loads(json_response)


def test_parsed_articles(parser, article):
    parsed_article = parser._publisher_specific_parsing(article)

    expected = {
        "dois": ["10.5506/aphyspolb.56.3-a7"],
        "journal_doctype": "article",
        "page_nr": [1],
        "arxiv_eprints": [{"value": "2503.12208"}],
        "abstract": 'The instanton vacuum provides an effective description of chiral symmetry breaking by local topological fluctuations of the gauge fields, as observed in lattice QCD simulations. The resulting effective dynamics at momenta below \\(1/\\bar \\rho \\approx 0.6\\) GeV explains the basic features of light-quark correlation functions and is used extensively in studies of hadron structure. The instanton fields also make definite contributions to the gluonic structure of light hadrons, as expressed in the matrix elements of composite quark–gluon or gluon operators. The article reviews the gluonic structure of light hadrons (nucleon, pion) induced by instantons. This includes: &lt;span class="it"&gt;(i)&lt;/span&gt; twist-2 parton distributions and momentum sum rule; &lt;span class="it"&gt;(ii)&lt;/span&gt; twist-3 angular momentum and spin-orbit interactions; &lt;span class="it"&gt;(iii)&lt;/span&gt; twist-3 and twist-4 quark–gluon correlations and power corrections; &lt;span class="it"&gt;(iv)&lt;/span&gt; trace anomaly and hadron mass decomposition; &lt;span class="it"&gt;(v)&lt;/span&gt; scalar gluon form factors and mechanical properties; &lt;span class="it"&gt;(vi)&lt;/span&gt; axial anomaly and pseudoscalar gluon form factors. It also discusses possible further applications of the methods and recent developments including gauge field configurations beyond instantons. Abstract Published by the Jagiellonian University 2025 authors',
        "title": "Gluonic Structure from Instantons",
        "authors": [
            {
                "full_name": "C. Weiss",
                "given_names": "C.",
                "surname": "Weiss",
                "orcid": "0000-0003-0296-5802",
                "affiliations": [
                    {
                        "value": "Theory Center, Jefferson Lab",
                        "organization": "Theory Center, Jefferson Lab",
                        "ror": "https://ror.org/02vwzrd76",
                    }
                ],
            }
        ],
        "journal_title": "Acta Physica Polonica B",
        "journal_issue": "3",
        "journal_volume": "56",
        "journal_year": 2025,
        "date_published": "2025-04-16",
        "acceptance_date": "2025-03-15",
        "reception_date": "2025-02-27",
        "copyright_holder": "The authors",
        "copyright_year": 2025,
        "copyright_statement": "2025 The authors",
        "license": [
            {
                "url": "https://creativecommons.org/licenses/by/4.0/",
                "license": "CC-BY-4.0",
            }
        ],
        "collections": ["HEP", "Citeable", "Published"],
        "field_categories": [{"term": "hep-ph", "scheme": "arXiv", "source": ""}],
        "files": {
            "pdf": "https://www.actaphys.uj.edu.pl/fulltext?series=Reg&vol=56&aid=3-A7",
            "pdfa": "https://www.actaphys.uj.edu.pl/fulltext?series=Reg&vol=56&aid=3-A7&fmt=pdfa",
        },
    }

    assert parsed_article == expected
