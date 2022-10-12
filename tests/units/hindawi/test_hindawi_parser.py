import xml.etree.ElementTree as ET

import pytest
from common.parsing.xml_extractors import RequiredFieldNotFoundExtractionError
from hindawi.hindawi_file_processing import (
    enhance_hindawi,
    enrich_hindawi,
    hindawi_validate_record,
)
from hindawi.parser import HindawiParser


@pytest.fixture(scope="module")
def hindawi_parser():
    return HindawiParser()


@pytest.fixture()
def articles(shared_datadir):
    articles = []
    files = ["example1.xml", "example2.xml", "example4.xml"]

    for file in files:
        with open(shared_datadir / file) as file:
            articles.append(ET.fromstring(file.read()))
    return articles


@pytest.fixture()
def parsed_articles(hindawi_parser, articles):
    return [hindawi_parser._publisher_specific_parsing(article) for article in articles]


@pytest.mark.parametrize(
    "expected, key",
    [
        pytest.param(
            [
                ["10.1155/2019/3465159"],
                ["10.1155/2022/5287693"],
                ["10.1155/2022/2755821"],
            ],
            "dois",
            id="test_dois",
        ),
        pytest.param(
            [
                [
                    {
                        "raw_name": "Entem, David R.",
                        "affiliations": [
                            {
                                "value": "Grupo de Física Nuclear and Instituto Universitario de Física Fundamental y Matemáticas (IUFFyM), Universidad de Salamanca, E-37008 Salamanca, Spain",
                                "organization": "Grupo de Física Nuclear and Instituto Universitario de Física Fundamental y Matemáticas (IUFFyM), Universidad de Salamanca, E-37008 Salamanca",
                                "country": "Spain",
                            }
                        ],
                        "orcid": "ORCID-0000-0003-2376-6255",
                    },
                    {
                        "raw_name": "Ortega, Pablo G.",
                        "affiliations": [
                            {
                                "value": "Grupo de Física Nuclear and Instituto Universitario de Física Fundamental y Matemáticas (IUFFyM), Universidad de Salamanca, E-37008 Salamanca, Spain",
                                "organization": "Grupo de Física Nuclear and Instituto Universitario de Física Fundamental y Matemáticas (IUFFyM), Universidad de Salamanca, E-37008 Salamanca",
                                "country": "Spain",
                            }
                        ],
                    },
                    {
                        "raw_name": "Fernández, Francisco",
                        "affiliations": [
                            {
                                "value": "Grupo de Física Nuclear and Instituto Universitario de Física Fundamental y Matemáticas (IUFFyM), Universidad de Salamanca, E-37008 Salamanca, Spain",
                                "organization": "Grupo de Física Nuclear and Instituto Universitario de Física Fundamental y Matemáticas (IUFFyM), Universidad de Salamanca, E-37008 Salamanca",
                                "country": "Spain",
                            }
                        ],
                    },
                ],
                [
                    {
                        "raw_name": "Li, Ying",
                        "affiliations": [
                            {
                                "value": "Department of Physics, Yantai University, Yantai 264005, China",
                                "organization": "Department of Physics, Yantai University, Yantai 264005",
                                "country": "China",
                            }
                        ],
                        "orcid": "https://orcid.org/0000-0002-1337-7662",
                    },
                    {
                        "raw_name": "Liu, Wen-Feng",
                        "affiliations": [
                            {
                                "value": "Department of Physics, Yantai University, Yantai 264005, China",
                                "organization": "Department of Physics, Yantai University, Yantai 264005",
                                "country": "China",
                            }
                        ],
                        "orcid": "https://orcid.org/0000-0002-9549-1863",
                    },
                    {
                        "raw_name": "Zou, Zhi-Tian",
                        "affiliations": [
                            {
                                "value": "Department of Physics, Yantai University, Yantai 264005, China",
                                "organization": "Department of Physics, Yantai University, Yantai 264005",
                                "country": "China",
                            }
                        ],
                        "orcid": "https://orcid.org/0000-0002-6985-8174",
                    },
                ],
                [
                    {
                        "raw_name": "Wei, Yan-Bing",
                        "affiliations": [
                            {
                                "value": "Physik Department T31, James-Franck-Straße 1, Technische Universität München, D85748 Garching, Germany",
                                "organization": "Physik Department T31, James-Franck-Straße 1, Technische Universität München, D85748 Garching",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "https://orcid.org/0000-0001-5917-5786",
                    },
                    {
                        "raw_name": "Shen, Yue-Long",
                        "affiliations": [
                            {
                                "value": "College of Physics and Photoelectric Engineering, Ocean University of China, Qingdao 266100, China",
                                "organization": "College of Physics and Photoelectric Engineering, Ocean University of China, Qingdao 266100",
                                "country": "China",
                            }
                        ],
                    },
                ],
            ],
            "authors",
            id="test_authors",
        ),
        pytest.param(
            [
                "In recent years, the discovery in quarkonium spectrum of several states not predicted by the naive quark model has awakened a lot of interest. A possible description of such states requires the enlargement of the quark model by introducing quark-antiquark pair creation or continuum coupling effects. The unquenching of the quark models is a way to take these new components into account. In the spirit of the Cornell Model, this is usually done by coupling perturbatively a quark-antiquark state with definite quantum numbers to the meson-meson channel with the closest threshold. In this work we present a method to coupled quark-antiquark states with meson-meson channels, taking into account effectively the nonperturbative coupling to all quark-antiquark states with the same quantum numbers. The method will be applied to the study of the X(3872) resonance and a comparison with the perturbative calculation will be performed.",
                'Three-body<ns0:math xmlns:ns0="http://www.w3.org/1998/Math/MathML" id="M3"><ns0:mi>B</ns0:mi></ns0:math>decays not only significantly broaden the study of<ns0:math xmlns:ns0="http://www.w3.org/1998/Math/MathML" id="M4"><ns0:mi>B</ns0:mi></ns0:math>meson decay mechanisms but also provide information of resonant particles. Because of complicate dynamics, it is very hard for us to study the whole phase space in a specific approach. In this review, we take<ns0:math xmlns:ns0="http://www.w3.org/1998/Math/MathML" id="M5"><ns0:mi>B</ns0:mi><ns0:mo>&#10230;</ns0:mo><ns0:mi>K</ns0:mi><ns0:mfenced open="(" close=")"><ns0:mrow><ns0:mi mathvariant="script">R</ns0:mi><ns0:mo>&#10230;</ns0:mo></ns0:mrow></ns0:mfenced><ns0:msup><ns0:mrow><ns0:mi>K</ns0:mi></ns0:mrow><ns0:mrow><ns0:mo>+</ns0:mo></ns0:mrow></ns0:msup><ns0:msup><ns0:mrow><ns0:mi>K</ns0:mi></ns0:mrow><ns0:mrow><ns0:mo>&#8722;</ns0:mo></ns0:mrow></ns0:msup></ns0:math>decays as examples and show the application of the perturbative QCD (PQCD) approach in studying the quasi-two-body<ns0:math xmlns:ns0="http://www.w3.org/1998/Math/MathML" id="M6"><ns0:mi>B</ns0:mi></ns0:math>decays, where two particles move collinearly with large energy and the bachelor one recoils back. To describe the dynamics of two collinear particles, the<ns0:math xmlns:ns0="http://www.w3.org/1998/Math/MathML" id="M7"><ns0:mi>S</ns0:mi></ns0:math>,<ns0:math xmlns:ns0="http://www.w3.org/1998/Math/MathML" id="M8"><ns0:mi>P</ns0:mi></ns0:math>, and<ns0:math xmlns:ns0="http://www.w3.org/1998/Math/MathML" id="M9"><ns0:mi>D</ns0:mi></ns0:math>-wave functions of kaon-pair with different waves are introduced. By keeping the transverse momenta, all possible diagrams including the hard spectator diagrams and annihilation ones can be calculated in PQCD approach. Most results are well consistent with the current measurements from BaBar, Belle, and LHCb experiments. Moreover, under the narrow-width approximation, we can extract the branching fractions of the two-body decays involving the resonant states and also predict the branching fractions of the corresponding quasi-two-body decays<ns0:math xmlns:ns0="http://www.w3.org/1998/Math/MathML" id="M10"><ns0:mi>B</ns0:mi><ns0:mo>&#10230;</ns0:mo><ns0:mi>K</ns0:mi><ns0:mfenced open="(" close=")"><ns0:mrow><ns0:mi mathvariant="script">R</ns0:mi><ns0:mo>&#10230;</ns0:mo></ns0:mrow></ns0:mfenced><ns0:msup><ns0:mrow><ns0:mi>&#960;</ns0:mi></ns0:mrow><ns0:mrow><ns0:mo>+</ns0:mo></ns0:mrow></ns0:msup><ns0:msup><ns0:mrow><ns0:mi>&#960;</ns0:mi></ns0:mrow><ns0:mrow><ns0:mo>&#8722;</ns0:mo></ns0:mrow></ns0:msup></ns0:math>. All predictions are expected to be tested in the ongoing LHCb and Belle-II experiments.',
                'In this review, we discuss the calculation of the<ns0:math xmlns:ns0="http://www.w3.org/1998/Math/MathML" id="M3"><ns0:mi>B</ns0:mi><ns0:mo>&#10230;</ns0:mo><ns0:mi>P</ns0:mi><ns0:mo>,</ns0:mo><ns0:mi>V</ns0:mi></ns0:math>form factors within the framework of the light-cone sum rules with the light-cone distribution amplitudes of the<ns0:math xmlns:ns0="http://www.w3.org/1998/Math/MathML" id="M4"><ns0:mi>B</ns0:mi></ns0:math>-meson. A detailed introduction to the definition, scale evolution, and phenomenological models of the<ns0:math xmlns:ns0="http://www.w3.org/1998/Math/MathML" id="M5"><ns0:mi>B</ns0:mi></ns0:math>-meson distribution amplitudes is presented. We show two equivalent approaches of calculating the next-to-leading order QCD corrections to the sum rules for the form factors, i.e., the method of regions and the step-by-step matching in the soft-collinear effective theory. The power suppressed corrections to the<ns0:math xmlns:ns0="http://www.w3.org/1998/Math/MathML" id="M6"><ns0:mi>B</ns0:mi><ns0:mo>&#10230;</ns0:mo><ns0:mi>P</ns0:mi><ns0:mo>,</ns0:mo><ns0:mi>V</ns0:mi></ns0:math>form factors especially the contributions from the higher-twist<ns0:math xmlns:ns0="http://www.w3.org/1998/Math/MathML" id="M7"><ns0:mi>B</ns0:mi></ns0:math>-meson distribution amplitudes are displayed. We also present numerical results of the form factors including both the QCD and the power corrections, and phenomenological applications of the predicted form factors such as the determination of the CKM matrix element<ns0:math xmlns:ns0="http://www.w3.org/1998/Math/MathML" id="M8"><ns0:mfenced open="|" close="|"><ns0:mrow><ns0:msub><ns0:mrow><ns0:mi>V</ns0:mi></ns0:mrow><ns0:mrow><ns0:mi>u</ns0:mi><ns0:mi>b</ns0:mi></ns0:mrow></ns0:msub></ns0:mrow></ns0:mfenced></ns0:math>.',
            ],
            "abstract",
            id="test_abstract",
        ),
        pytest.param(
            [
                "Unquenching the <italic>Quark <b>Model</b></italic> in a Nonperturbative Scheme",
                'Charmless Quasi-Two-Body<ns0:math xmlns:ns0="http://www.w3.org/1998/Math/MathML" id="M1"><ns0:mi>B</ns0:mi></ns0:math>Decays in Perturbative QCD Approach: Taking<ns0:math xmlns:ns0="http://www.w3.org/1998/Math/MathML" id="M2"><ns0:mi>B</ns0:mi><ns0:mo>&#10230;</ns0:mo><ns0:mi>K</ns0:mi><ns0:mfenced open="(" close=")"><ns0:mrow><ns0:mi mathvariant="script">R</ns0:mi><ns0:mo>&#10230;</ns0:mo></ns0:mrow></ns0:mfenced><ns0:msup><ns0:mrow><ns0:mi>K</ns0:mi></ns0:mrow><ns0:mrow><ns0:mo>+</ns0:mo></ns0:mrow></ns0:msup><ns0:msup><ns0:mrow><ns0:mi>K</ns0:mi></ns0:mrow><ns0:mrow><ns0:mo>&#8722;</ns0:mo></ns0:mrow></ns0:msup></ns0:math>as Examples',
                '<ns0:math xmlns:ns0="http://www.w3.org/1998/Math/MathML" id="M1"><ns0:mi>B</ns0:mi><ns0:mo>&#10230;</ns0:mo><ns0:mi>P</ns0:mi><ns0:mo>,</ns0:mo><ns0:mi>V</ns0:mi></ns0:math>Form Factors with the<ns0:math xmlns:ns0="http://www.w3.org/1998/Math/MathML" id="M2"><ns0:mi>B</ns0:mi></ns0:math>-Meson Light-Cone Sum Rules',
            ],
            "title",
            id="test_title",
        ),
        pytest.param(
            ["2019-05-02", "2022-02-22", "2022-02-22"],
            "date_published",
            id="test_date_published",
        ),
        pytest.param([[7], [8], [29]], "page_nr", id="test_page_nr"),
        pytest.param(
            [
                [
                    {
                        "journal_title": "Advances in High Energy Physics",
                        "journal_volume": "2019",
                        "journal_year": "2019",
                    }
                ],
                [
                    {
                        "journal_title": "Advances in High Energy Physics",
                        "journal_volume": "2022",
                        "journal_year": "2022",
                    }
                ],
                [
                    {
                        "journal_title": "Advances in High Energy Physics",
                        "journal_volume": "2022",
                        "journal_year": "2022",
                    }
                ],
            ],
            "publication_info",
            id="test_publication_info",
        ),
        pytest.param(
            [
                [{"value": "1901.02484"}],
                [{"value": "2112.00315"}],
                [{"value": "2112.01500"}],
            ],
            "arxiv_eprints",
            id="test_arxiv_eprints",
        ),
        pytest.param(
            [
                "Copyright © 2019 Pablo G. Ortega et al.",
                "Copyright © 2022 Wen-Feng Liu et al.",
                "Copyright © 2022 Yue-Long Shen and Yan-Bing Wei.",
            ],
            "copyright_statement",
            id="test_copyright_statement",
        ),
        pytest.param(
            ["2019", "2022", "2022"], "copyright_year", id="test_test_copyright_year"
        ),
        pytest.param(
            [
                [
                    {
                        "license": "CC-BY-3.0",
                        "url": "http://creativecommons.org/licenses/by/3.0/",
                    }
                ],
                [
                    {
                        "url": "http://creativecommons.org/licenses/by/3.0/",
                        "license": "CC-BY-3.0",
                    }
                ],
                [
                    {
                        "url": "http://creativecommons.org/licenses/by/3.0/",
                        "license": "CC-BY-3.0",
                    }
                ],
            ],
            "license",
            id="test_license",
        ),
    ],
)
def test_hindawi_parsing(parsed_articles, expected, key):
    for (
        expected_value,
        article,
    ) in zip(expected, parsed_articles):
        assert article[key] == expected_value


@pytest.fixture()
def article_without_doi(shared_datadir):
    with open(shared_datadir / "without_doi.xml") as f:
        return ET.fromstring(f.read())


def test_parse_article_without_doi(hindawi_parser, article_without_doi):
    with pytest.raises(RequiredFieldNotFoundExtractionError):
        hindawi_parser._publisher_specific_parsing(article_without_doi)


@pytest.fixture()
def article_without_page_nr(shared_datadir):
    with open(shared_datadir / "without_page_nr.xml") as f:
        return ET.fromstring(f.read())


def test_parse_article_without_page_nr(hindawi_parser, article_without_page_nr):
    hindawi_parser._publisher_specific_parsing(article_without_page_nr)


@pytest.fixture()
def parsed_article_without_page_nr(hindawi_parser, article_without_page_nr):
    return hindawi_parser._publisher_specific_parsing(article_without_page_nr)


def test_page_nr(parsed_article_without_page_nr):
    assert parsed_article_without_page_nr["page_nr"] == [0]  # Default value


def test_hindawi_record_validation(hindawi_parser, parsed_article_without_page_nr):
    enhanced = enhance_hindawi(
        hindawi_parser._generic_parsing(parsed_article_without_page_nr)
    )
    enriched = enrich_hindawi(enhanced)
    hindawi_validate_record(enriched)
