import xml.etree.ElementTree as ET

import pytest
from hindawi.hindawi_file_processing import enhance_hindawi
from hindawi.parser import HindawiParser


@pytest.fixture(scope="module")
def hindawi_parser():
    return HindawiParser()


@pytest.fixture
def articles(shared_datadir):
    articles = []
    files = ["example1.xml", "example2.xml", "example4.xml"]

    for file in files:
        with open(shared_datadir / file) as file:
            articles.append(ET.fromstring(file.read()))
    return articles


@pytest.fixture
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
    ],
)
def test_hindawi_parsing(parsed_articles, expected, key):
    for (
        expected_value,
        article,
    ) in zip(expected, parsed_articles):
        assert enhance_hindawi(article).get(key) == expected_value
