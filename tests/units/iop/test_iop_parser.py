import xml.etree.ElementTree as ET

from common.parsing.xml_extractors import RequiredFieldNotFoundExtractionError
from freezegun import freeze_time
from iop.iop_process_file import enhance_iop, enrich_iop, iop_validate_record
from iop.parser import IOPParser
from pytest import fixture, mark, param, raises


@fixture(scope="module")
def iop_parser():
    yield IOPParser()


@fixture
def article_without_abstract(shared_datadir):
    with open(shared_datadir / "without_abstract.xml") as f:
        yield ET.fromstring(f.read())


def test_article_without_abstract(iop_parser, article_without_abstract):
    with raises(RequiredFieldNotFoundExtractionError):
        assert iop_parser._publisher_specific_parsing(article_without_abstract)


@fixture
def article_without_arxiv(shared_datadir):
    with open(shared_datadir / "without_arxiv.xml") as f:
        yield ET.fromstring(f.read())


@fixture
def parsed_article_without_arxiv(iop_parser, article_without_arxiv):
    yield iop_parser._publisher_specific_parsing(article_without_arxiv)


def test_without_arxiv(parsed_article_without_arxiv):
    assert parsed_article_without_arxiv["arxiv_eprints"] == []


@fixture
def article_without_page_nr(shared_datadir):
    with open(shared_datadir / "without_page_nr.xml") as f:
        yield ET.fromstring(f.read())


@fixture
def parsed_article_without_page_nr(iop_parser, article_without_page_nr):
    yield iop_parser._publisher_specific_parsing(article_without_page_nr)


def test_page_nr_without_page_nr(parsed_article_without_page_nr):
    assert parsed_article_without_page_nr["page_nr"] == [0]


def test_iop_record_validation(iop_parser, parsed_article_without_page_nr):
    enhanced = enhance_iop(iop_parser._generic_parsing(parsed_article_without_page_nr))
    enriched = enrich_iop(enhanced)
    iop_validate_record(enriched)


@fixture
def article_without_doi(shared_datadir):
    with open(shared_datadir / "without_doi.xml") as f:
        yield ET.fromstring(f.read())


def parsed_article_without_doi(iop_parser, article_without_doi):
    with raises(RequiredFieldNotFoundExtractionError):
        return iop_parser._publisher_specific_parsing(article_without_doi)


@fixture
def article_just_with_required_fields(shared_datadir):
    with open(shared_datadir / "just_with_required_fields.xml") as f:
        yield ET.fromstring(f.read())


@fixture
def parsed_article_just_with_required_fields(
    iop_parser, article_just_with_required_fields
):
    yield iop_parser._publisher_specific_parsing(article_just_with_required_fields)


@mark.parametrize(
    "expected, key",
    [
        param(
            ["10.1088/1674-1137/ac66cc"],
            "dois",
            id="test_dois",
        ),
        param(
            "article",
            "journal_doctype",
            id="test_journal_doctype",
        ),
        param(
            [],
            "related_article_doi",
            id="test_related_article_doi",
        ),
        param(
            [],
            "arxiv_eprints",
            id="test_arxiv_eprints",
        ),
        param(
            [0],
            "page_nr",
            id="test_page_nr",
        ),
        param(
            'Solar, terrestrial, and supernova neutrino experiments are subject to muon-induced radioactive background. The China Jinping Underground Laboratory (CJPL), with its unique advantage of a 2400 m rock coverage and long distance from nuclear power plants, is ideal for MeV-scale neutrino experiments. Using a 1-ton prototype detector of the Jinping Neutrino Experiment (JNE), we detected 343 high-energy cosmic-ray muons and (7.86<inline-formula xmlns:ns0="http://www.w3.org/1999/xlink"><tex-math></tex-math><inline-graphic ns0:href="cpc_46_8_085001_M1.jpg" ns0:type="simple" /></inline-formula>3.97) muon-induced neutrons from an 820.28-day dataset at the first phase of CJPL (CJPL-I). Based on the muon-induced neutrons, we measured the corresponding muon-induced neutron yield in a liquid scintillator to be<inline-formula xmlns:ns0="http://www.w3.org/1999/xlink"><tex-math></tex-math><inline-graphic ns0:href="cpc_46_8_085001_M2.jpg" ns0:type="simple" /></inline-formula><inline-formula xmlns:ns0="http://www.w3.org/1999/xlink"><tex-math></tex-math><inline-graphic ns0:href="cpc_46_8_085001_M2-1.jpg" ns0:type="simple" /></inline-formula>&#956;<sup>&#8722;1</sup>g<sup>&#8722;1</sup>cm<sup>2</sup>at an average muon energy of 340 GeV. We provided the first study for such neutron background at CJPL. A global fit including this measurement shows a power-law coefficient of (0.75<inline-formula xmlns:ns0="http://www.w3.org/1999/xlink"><tex-math></tex-math><inline-graphic ns0:href="cpc_46_8_085001_M3.jpg" ns0:type="simple" /></inline-formula>0.02) for the dependence of the neutron yield at the liquid scintillator on muon energy.',
            "abstract",
            id="test_abstract",
        ),
        param(
            'Measurement of muon-induced neutron yield at the China Jinping Underground Laboratory<xref ref-type="fn" rid="cpc_46_8_085001_fn1">*</xref><fn id="cpc_46_8_085001_fn1"><label>*</label><p>Supported in part by the National Natural Science Foundation of China (11620101004, 11475093, 12127808), the Key Laboratory of Particle &amp; Radiation Imaging (TsinghuaUniversity), the CAS Center for Excellence in Particle Physics (CCEPP), and Guangdong Basic and Applied Basic Research Foundation (2019A1515012216). Portion of this work performed at Brookhaven National Laboratory is supported in part by the United States Department of Energy (DE-SC0012704)</p></fn>',
            "title",
            id="test_title",
        ),
        param(
            "",
            "subtitle",
            id="test_subtitle",
        ),
        param(
            [
                {
                    "surname": "Zhao",
                    "given_names": "Lin",
                    "affiliations": [
                        {
                            "value": "Department of Engineering Physics, Tsinghua University,China",
                            "country": "China",
                        },
                        {
                            "value": "Center for High Energy Physics, Tsinghua University,China",
                            "country": "China",
                        },
                    ],
                },
                {
                    "surname": "Luo",
                    "given_names": "Wentai",
                    "affiliations": [
                        {
                            "value": "School of Physical Sciences, University of Chinese Academy of Sciences,China",
                            "country": "China",
                        }
                    ],
                },
                {
                    "surname": "Bathe-Peters",
                    "given_names": "Lars",
                    "affiliations": [
                        {
                            "value": "Department of Engineering Physics, Tsinghua University,China",
                            "country": "China",
                        },
                        {
                            "value": "Institut für Physik, Technische Universität Berlin,Germany",
                            "country": "Germany",
                        },
                    ],
                },
                {
                    "surname": "Chen",
                    "given_names": "Shaomin",
                    "affiliations": [
                        {
                            "value": "Department of Engineering Physics, Tsinghua University,China",
                            "country": "China",
                        },
                        {
                            "value": "Center for High Energy Physics, Tsinghua University,China",
                            "country": "China",
                        },
                        {
                            "value": "Key Laboratory of Particle & Radiation Imaging (Tsinghua University),China",
                            "country": "China",
                        },
                    ],
                },
                {
                    "surname": "Chouaki",
                    "given_names": "Mourad",
                    "affiliations": [
                        {
                            "value": "Department of Engineering Physics, Tsinghua University,China",
                            "country": "China",
                        },
                        {
                            "value": "École Polytechnique Fédérale de Lausanne,Switzerland",
                            "country": "Switzerland",
                        },
                    ],
                },
                {
                    "surname": "Dou",
                    "given_names": "Wei",
                    "affiliations": [
                        {
                            "value": "Department of Engineering Physics, Tsinghua University,China",
                            "country": "China",
                        },
                        {
                            "value": "Center for High Energy Physics, Tsinghua University,China",
                            "country": "China",
                        },
                    ],
                },
                {
                    "surname": "Guo",
                    "given_names": "Lei",
                    "affiliations": [
                        {
                            "value": "Department of Engineering Physics, Tsinghua University,China",
                            "country": "China",
                        },
                        {
                            "value": "Center for High Energy Physics, Tsinghua University,China",
                            "country": "China",
                        },
                    ],
                },
                {
                    "surname": "Guo",
                    "given_names": "Ziyi",
                    "affiliations": [
                        {
                            "value": "Department of Engineering Physics, Tsinghua University,China",
                            "country": "China",
                        },
                        {
                            "value": "Center for High Energy Physics, Tsinghua University,China",
                            "country": "China",
                        },
                    ],
                },
                {
                    "surname": "Hussain",
                    "given_names": "Ghulam",
                    "affiliations": [
                        {
                            "value": "Department of Engineering Physics, Tsinghua University,China",
                            "country": "China",
                        },
                        {
                            "value": "Center for High Energy Physics, Tsinghua University,China",
                            "country": "China",
                        },
                    ],
                },
                {
                    "surname": "Li",
                    "given_names": "Jinjing",
                    "affiliations": [
                        {
                            "value": "Department of Engineering Physics, Tsinghua University,China",
                            "country": "China",
                        },
                        {
                            "value": "Center for High Energy Physics, Tsinghua University,China",
                            "country": "China",
                        },
                    ],
                },
                {
                    "surname": "Liang",
                    "given_names": "Ye",
                    "affiliations": [
                        {
                            "value": "Department of Engineering Physics, Tsinghua University,China",
                            "country": "China",
                        },
                        {
                            "value": "Center for High Energy Physics, Tsinghua University,China",
                            "country": "China",
                        },
                    ],
                },
                {
                    "surname": "Liu",
                    "given_names": "Qian",
                    "affiliations": [
                        {
                            "value": "School of Physical Sciences, University of Chinese Academy of Sciences,China",
                            "country": "China",
                        }
                    ],
                },
                {
                    "surname": "Luo",
                    "given_names": "Guang",
                    "affiliations": [
                        {
                            "value": "School of Physics, Sun Yat-Sen University,China",
                            "country": "China",
                        }
                    ],
                },
                {
                    "surname": "Qi",
                    "given_names": "Ming",
                    "affiliations": [
                        {
                            "value": "School of Physics, Nanjing University,China",
                            "country": "China",
                        }
                    ],
                },
                {
                    "surname": "Shao",
                    "given_names": "Wenhui",
                    "affiliations": [
                        {
                            "value": "Department of Engineering Physics, Tsinghua University,China",
                            "country": "China",
                        },
                        {
                            "value": "Center for High Energy Physics, Tsinghua University,China",
                            "country": "China",
                        },
                    ],
                },
                {
                    "surname": "Tang",
                    "given_names": "Jian",
                    "affiliations": [
                        {
                            "value": "School of Physics, Sun Yat-Sen University,China",
                            "country": "China",
                        }
                    ],
                },
                {
                    "surname": "Wan",
                    "given_names": "Linyan",
                    "affiliations": [
                        {
                            "value": "Department of Engineering Physics, Tsinghua University,China",
                            "country": "China",
                        },
                        {
                            "value": "Center for High Energy Physics, Tsinghua University,China",
                            "country": "China",
                        },
                    ],
                },
                {
                    "surname": "Wang",
                    "given_names": "Zhe",
                    "affiliations": [
                        {
                            "value": "Department of Engineering Physics, Tsinghua University,China",
                            "country": "China",
                        },
                        {
                            "value": "Center for High Energy Physics, Tsinghua University,China",
                            "country": "China",
                        },
                        {
                            "value": "Key Laboratory of Particle & Radiation Imaging (Tsinghua University),China",
                            "country": "China",
                        },
                    ],
                },
                {
                    "surname": "Wu",
                    "given_names": "Yiyang",
                    "affiliations": [
                        {
                            "value": "Department of Engineering Physics, Tsinghua University,China",
                            "country": "China",
                        },
                        {
                            "value": "Center for High Energy Physics, Tsinghua University,China",
                            "country": "China",
                        },
                    ],
                },
                {
                    "surname": "Xu",
                    "given_names": "Benda",
                    "affiliations": [
                        {
                            "value": "Department of Engineering Physics, Tsinghua University,China",
                            "country": "China",
                        },
                        {
                            "value": "Center for High Energy Physics, Tsinghua University,China",
                            "country": "China",
                        },
                        {
                            "value": "Key Laboratory of Particle & Radiation Imaging (Tsinghua University),China",
                            "country": "China",
                        },
                    ],
                },
                {
                    "surname": "Xu",
                    "given_names": "Tong",
                    "affiliations": [
                        {
                            "value": "Department of Engineering Physics, Tsinghua University,China",
                            "country": "China",
                        },
                        {
                            "value": "Center for High Energy Physics, Tsinghua University,China",
                            "country": "China",
                        },
                    ],
                },
                {
                    "surname": "Xu",
                    "given_names": "Weiran",
                    "affiliations": [
                        {
                            "value": "Department of Engineering Physics, Tsinghua University,China",
                            "country": "China",
                        },
                        {
                            "value": "Center for High Energy Physics, Tsinghua University,China",
                            "country": "China",
                        },
                    ],
                },
                {
                    "surname": "Yang",
                    "given_names": "Yuzi",
                    "affiliations": [
                        {
                            "value": "Department of Engineering Physics, Tsinghua University,China",
                            "country": "China",
                        },
                        {
                            "value": "Center for High Energy Physics, Tsinghua University,China",
                            "country": "China",
                        },
                    ],
                },
                {
                    "surname": "Yeh",
                    "given_names": "Minfang",
                    "affiliations": [
                        {
                            "value": "Brookhaven National Laboratory, Upton,USA",
                            "country": "USA",
                        }
                    ],
                },
                {
                    "surname": "Zhang",
                    "given_names": "Aiqiang",
                    "affiliations": [
                        {
                            "value": "Department of Engineering Physics, Tsinghua University,China",
                            "country": "China",
                        },
                        {
                            "value": "Center for High Energy Physics, Tsinghua University,China",
                            "country": "China",
                        },
                    ],
                },
                {
                    "surname": "Zhang",
                    "given_names": "Bin",
                    "affiliations": [
                        {
                            "value": "Department of Engineering Physics, Tsinghua University,China",
                            "country": "China",
                        },
                        {
                            "value": "Center for High Energy Physics, Tsinghua University,China",
                            "country": "China",
                        },
                    ],
                },
            ],
            "authors",
            id="test_authors",
        ),
        param(
            "2022-11-03",
            "date_published",
            id="test_date_published",
        ),
        param(
            "2022-11-03",
            "date_published",
            id="test_date_published",
        ),
        param(
            "2022",
            "copyright_year",
            id="test_date_published",
        ),
        param(
            "© 2022 Chinese Physical Society and the Institute of High Energy Physics of the Chinese Academy of Sciences and the Institute of Modern Physics of the Chinese Academy of Sciences and IOP Publishing Ltd",
            "copyright_statement",
            id="test_get_copyright_statements",
        ),
        param(
            [
                {
                    "license": "CC-BY-3.0",
                    "url": "http://creativecommons.org/licenses/by/3.0/",
                }
            ],
            "license",
            id="test_license",
        ),
    ],
)
@freeze_time("2022-11-03")
def test_IOP_just_with_required_fields(
    parsed_article_just_with_required_fields, expected, key
):
    assert parsed_article_just_with_required_fields[key] == expected


@fixture
def articles(shared_datadir):
    files = ["example1.xml", "example2.xml"]
    articles = []
    for file in files:
        with open(shared_datadir / file) as f:
            articles.append(ET.fromstring(f.read()))
    yield articles


@fixture
def parsed_articles(iop_parser, articles):
    yield [iop_parser._publisher_specific_parsing(article) for article in articles]


@mark.parametrize(
    "expected, key",
    [
        param(
            [["10.1088/1674-1137/ac66cc"], ["10.1088/1674-1137/ac763c"]],
            "dois",
            id="test_dois",
        ),
        param(
            ["article", "article"],
            "journal_doctype",
            id="test_journal_doctype",
        ),
        param(
            [],
            "related_article_doi",
            id="test_related_article_doi",
        ),
        param(
            [[{"value": "2108.04010"}], [{"value": "2107.07275"}]],
            "arxiv_eprints",
            id="test_arxiv_eprints",
        ),
        param(
            [[9], [18]],
            "page_nr",
            id="test_page_nr",
        ),
        param(
            [
                'Solar, terrestrial, and supernova neutrino experiments are subject to muon-induced radioactive background. The China Jinping Underground Laboratory (CJPL), with its unique advantage of a 2400 m rock coverage and long distance from nuclear power plants, is ideal for MeV-scale neutrino experiments. Using a 1-ton prototype detector of the Jinping Neutrino Experiment (JNE), we detected 343 high-energy cosmic-ray muons and (7.86<inline-formula xmlns:ns0="http://www.w3.org/1999/xlink"><tex-math></tex-math><inline-graphic ns0:href="cpc_46_8_085001_M1.jpg" ns0:type="simple" /></inline-formula>3.97) muon-induced neutrons from an 820.28-day dataset at the first phase of CJPL (CJPL-I). Based on the muon-induced neutrons, we measured the corresponding muon-induced neutron yield in a liquid scintillator to be<inline-formula xmlns:ns0="http://www.w3.org/1999/xlink"><tex-math></tex-math><inline-graphic ns0:href="cpc_46_8_085001_M2.jpg" ns0:type="simple" /></inline-formula><inline-formula xmlns:ns0="http://www.w3.org/1999/xlink"><tex-math></tex-math><inline-graphic ns0:href="cpc_46_8_085001_M2-1.jpg" ns0:type="simple" /></inline-formula>&#956;<sup>&#8722;1</sup>g<sup>&#8722;1</sup>cm<sup>2</sup>at an average muon energy of 340 GeV. We provided the first study for such neutron background at CJPL. A global fit including this measurement shows a power-law coefficient of (0.75<inline-formula xmlns:ns0="http://www.w3.org/1999/xlink"><tex-math></tex-math><inline-graphic ns0:href="cpc_46_8_085001_M3.jpg" ns0:type="simple" /></inline-formula>0.02) for the dependence of the neutron yield at the liquid scintillator on muon energy.',
                'In this study, we modify a scenario, originally proposed by Grimus and Lavoura, in order to obtain maximal values for the atmospheric mixing angle and<inline-formula xmlns:ns0="http://www.w3.org/1999/xlink"><tex-math></tex-math><inline-graphic ns0:href="cpc_46_10_103101_M1.jpg" ns0:type="simple" /></inline-formula>, violating the Dirac phase of the lepton sector. To achieve this, we employ<inline-formula xmlns:ns0="http://www.w3.org/1999/xlink"><tex-math></tex-math><inline-graphic ns0:href="cpc_46_10_103101_M2.jpg" ns0:type="simple" /></inline-formula>and some discrete symmetries in a type II seesaw model. To make predictions about the neutrino mass ordering and smallness of the reactor angle, we establish some conditions on the elements of the neutrino mass matrix of our model. Finally, we study the quark masses and mixing pattern within the framework of our model.',
            ],
            "abstract",
            id="test_abstract",
        ),
        param(
            [
                'Measurement of muon-induced neutron yield at the China Jinping Underground Laboratory<xref ref-type="fn" rid="cpc_46_8_085001_fn1">*</xref><fn id="cpc_46_8_085001_fn1"><label>*</label><p>Supported in part by the National Natural Science Foundation of China (11620101004, 11475093, 12127808), the Key Laboratory of Particle &amp; Radiation Imaging (TsinghuaUniversity), the CAS Center for Excellence in Particle Physics (CCEPP), and Guangdong Basic and Applied Basic Research Foundation (2019A1515012216). Portion of this work performed at Brookhaven National Laboratory is supported in part by the United States Department of Energy (DE-SC0012704)</p></fn>',
                'Lepton and quark mixing patterns with generalized<italic toggle="yes">CP</italic>transformations',
            ],
            "title",
            id="test_title",
        ),
        param(
            ["", ""],
            "subtitle",
            id="test_subtitle",
        ),
        param(
            [
                [
                    {
                        "surname": "Zhao",
                        "given_names": "Lin",
                        "affiliations": [
                            {
                                "value": "Department of Engineering Physics, Tsinghua University,China",
                                "country": "China",
                            },
                            {
                                "value": "Center for High Energy Physics, Tsinghua University,China",
                                "country": "China",
                            },
                        ],
                    },
                    {
                        "surname": "Luo",
                        "given_names": "Wentai",
                        "affiliations": [
                            {
                                "value": "School of Physical Sciences, University of Chinese Academy of Sciences,China",
                                "country": "China",
                            }
                        ],
                    },
                    {
                        "surname": "Bathe-Peters",
                        "given_names": "Lars",
                        "affiliations": [
                            {
                                "value": "Department of Engineering Physics, Tsinghua University,China",
                                "country": "China",
                            },
                            {
                                "value": "Institut für Physik, Technische Universität Berlin,Germany",
                                "country": "Germany",
                            },
                        ],
                    },
                    {
                        "surname": "Chen",
                        "given_names": "Shaomin",
                        "affiliations": [
                            {
                                "value": "Department of Engineering Physics, Tsinghua University,China",
                                "country": "China",
                            },
                            {
                                "value": "Center for High Energy Physics, Tsinghua University,China",
                                "country": "China",
                            },
                            {
                                "value": "Key Laboratory of Particle & Radiation Imaging (Tsinghua University),China",
                                "country": "China",
                            },
                        ],
                    },
                    {
                        "surname": "Chouaki",
                        "given_names": "Mourad",
                        "affiliations": [
                            {
                                "value": "Department of Engineering Physics, Tsinghua University,China",
                                "country": "China",
                            },
                            {
                                "value": "École Polytechnique Fédérale de Lausanne,Switzerland",
                                "country": "Switzerland",
                            },
                        ],
                    },
                    {
                        "surname": "Dou",
                        "given_names": "Wei",
                        "affiliations": [
                            {
                                "value": "Department of Engineering Physics, Tsinghua University,China",
                                "country": "China",
                            },
                            {
                                "value": "Center for High Energy Physics, Tsinghua University,China",
                                "country": "China",
                            },
                        ],
                    },
                    {
                        "surname": "Guo",
                        "given_names": "Lei",
                        "affiliations": [
                            {
                                "value": "Department of Engineering Physics, Tsinghua University,China",
                                "country": "China",
                            },
                            {
                                "value": "Center for High Energy Physics, Tsinghua University,China",
                                "country": "China",
                            },
                        ],
                    },
                    {
                        "surname": "Guo",
                        "given_names": "Ziyi",
                        "affiliations": [
                            {
                                "value": "Department of Engineering Physics, Tsinghua University,China",
                                "country": "China",
                            },
                            {
                                "value": "Center for High Energy Physics, Tsinghua University,China",
                                "country": "China",
                            },
                        ],
                    },
                    {
                        "surname": "Hussain",
                        "given_names": "Ghulam",
                        "affiliations": [
                            {
                                "value": "Department of Engineering Physics, Tsinghua University,China",
                                "country": "China",
                            },
                            {
                                "value": "Center for High Energy Physics, Tsinghua University,China",
                                "country": "China",
                            },
                        ],
                    },
                    {
                        "surname": "Li",
                        "given_names": "Jinjing",
                        "affiliations": [
                            {
                                "value": "Department of Engineering Physics, Tsinghua University,China",
                                "country": "China",
                            },
                            {
                                "value": "Center for High Energy Physics, Tsinghua University,China",
                                "country": "China",
                            },
                        ],
                    },
                    {
                        "surname": "Liang",
                        "given_names": "Ye",
                        "affiliations": [
                            {
                                "value": "Department of Engineering Physics, Tsinghua University,China",
                                "country": "China",
                            },
                            {
                                "value": "Center for High Energy Physics, Tsinghua University,China",
                                "country": "China",
                            },
                        ],
                    },
                    {
                        "surname": "Liu",
                        "given_names": "Qian",
                        "affiliations": [
                            {
                                "value": "School of Physical Sciences, University of Chinese Academy of Sciences,China",
                                "country": "China",
                            }
                        ],
                    },
                    {
                        "surname": "Luo",
                        "given_names": "Guang",
                        "affiliations": [
                            {
                                "value": "School of Physics, Sun Yat-Sen University,China",
                                "country": "China",
                            }
                        ],
                    },
                    {
                        "surname": "Qi",
                        "given_names": "Ming",
                        "affiliations": [
                            {
                                "value": "School of Physics, Nanjing University,China",
                                "country": "China",
                            }
                        ],
                    },
                    {
                        "surname": "Shao",
                        "given_names": "Wenhui",
                        "affiliations": [
                            {
                                "value": "Department of Engineering Physics, Tsinghua University,China",
                                "country": "China",
                            },
                            {
                                "value": "Center for High Energy Physics, Tsinghua University,China",
                                "country": "China",
                            },
                        ],
                    },
                    {
                        "surname": "Tang",
                        "given_names": "Jian",
                        "affiliations": [
                            {
                                "value": "School of Physics, Sun Yat-Sen University,China",
                                "country": "China",
                            }
                        ],
                    },
                    {
                        "surname": "Wan",
                        "given_names": "Linyan",
                        "affiliations": [
                            {
                                "value": "Department of Engineering Physics, Tsinghua University,China",
                                "country": "China",
                            },
                            {
                                "value": "Center for High Energy Physics, Tsinghua University,China",
                                "country": "China",
                            },
                        ],
                    },
                    {
                        "surname": "Wang",
                        "given_names": "Zhe",
                        "affiliations": [
                            {
                                "value": "Department of Engineering Physics, Tsinghua University,China",
                                "country": "China",
                            },
                            {
                                "value": "Center for High Energy Physics, Tsinghua University,China",
                                "country": "China",
                            },
                            {
                                "value": "Key Laboratory of Particle & Radiation Imaging (Tsinghua University),China",
                                "country": "China",
                            },
                        ],
                    },
                    {
                        "surname": "Wu",
                        "given_names": "Yiyang",
                        "affiliations": [
                            {
                                "value": "Department of Engineering Physics, Tsinghua University,China",
                                "country": "China",
                            },
                            {
                                "value": "Center for High Energy Physics, Tsinghua University,China",
                                "country": "China",
                            },
                        ],
                    },
                    {
                        "surname": "Xu",
                        "given_names": "Benda",
                        "affiliations": [
                            {
                                "value": "Department of Engineering Physics, Tsinghua University,China",
                                "country": "China",
                            },
                            {
                                "value": "Center for High Energy Physics, Tsinghua University,China",
                                "country": "China",
                            },
                            {
                                "value": "Key Laboratory of Particle & Radiation Imaging (Tsinghua University),China",
                                "country": "China",
                            },
                        ],
                    },
                    {
                        "surname": "Xu",
                        "given_names": "Tong",
                        "affiliations": [
                            {
                                "value": "Department of Engineering Physics, Tsinghua University,China",
                                "country": "China",
                            },
                            {
                                "value": "Center for High Energy Physics, Tsinghua University,China",
                                "country": "China",
                            },
                        ],
                    },
                    {
                        "surname": "Xu",
                        "given_names": "Weiran",
                        "affiliations": [
                            {
                                "value": "Department of Engineering Physics, Tsinghua University,China",
                                "country": "China",
                            },
                            {
                                "value": "Center for High Energy Physics, Tsinghua University,China",
                                "country": "China",
                            },
                        ],
                    },
                    {
                        "surname": "Yang",
                        "given_names": "Yuzi",
                        "affiliations": [
                            {
                                "value": "Department of Engineering Physics, Tsinghua University,China",
                                "country": "China",
                            },
                            {
                                "value": "Center for High Energy Physics, Tsinghua University,China",
                                "country": "China",
                            },
                        ],
                    },
                    {
                        "surname": "Yeh",
                        "given_names": "Minfang",
                        "affiliations": [
                            {
                                "value": "Brookhaven National Laboratory, Upton,USA",
                                "country": "USA",
                            }
                        ],
                    },
                    {
                        "surname": "Zhang",
                        "given_names": "Aiqiang",
                        "affiliations": [
                            {
                                "value": "Department of Engineering Physics, Tsinghua University,China",
                                "country": "China",
                            },
                            {
                                "value": "Center for High Energy Physics, Tsinghua University,China",
                                "country": "China",
                            },
                        ],
                    },
                    {
                        "surname": "Zhang",
                        "given_names": "Bin",
                        "affiliations": [
                            {
                                "value": "Department of Engineering Physics, Tsinghua University,China",
                                "country": "China",
                            },
                            {
                                "value": "Center for High Energy Physics, Tsinghua University,China",
                                "country": "China",
                            },
                        ],
                    },
                ],
                [
                    {
                        "surname": "Ganguly",
                        "given_names": "Joy",
                        "affiliations": [
                            {
                                "value": "Department of Physics, Indian Institute of Technology Hyderabad,India",
                                "country": "India",
                            }
                        ],
                    },
                    {
                        "surname": "Hundi",
                        "given_names": "Raghavendra Srikanth",
                        "affiliations": [
                            {
                                "value": "Department of Physics, Indian Institute of Technology Hyderabad,India",
                                "country": "India",
                            }
                        ],
                    },
                ],
            ],
            "authors",
            id="test_affiliations",
        ),
        param(
            ["2022-08-01", "2022-10-01"],
            "date_published",
            id="test_get_published_date",
        ),
        param(
            [
                [
                    {
                        "journal_title": "Chinese Physics C",
                        "journal_volume": "46",
                        "journal_year": 2022,
                        "journal_issue": "8",
                        "journal_artid": "085001",
                    }
                ],
                [
                    {
                        "journal_title": "Chinese Physics C",
                        "journal_volume": "46",
                        "journal_year": 2022,
                        "journal_issue": "10",
                        "journal_artid": "103101",
                    }
                ],
            ],
            "publication_info",
            id="test_publication_info",
        ),
        param(["2022", "2022"], "copyright_year", id="test_get_copyright_year"),
        param(
            [
                "© 2022 Chinese Physical Society and the Institute of High Energy Physics of the Chinese Academy of Sciences and the Institute of Modern Physics of the Chinese Academy of Sciences and IOP Publishing Ltd",
                "© 2022 Chinese Physical Society and the Institute of High Energy Physics of the Chinese Academy of Sciences and the Institute of Modern Physics of the Chinese Academy of Sciences and IOP Publishing Ltd",
            ],
            "copyright_statement",
            id="test_get_copyright_statements",
        ),
        param(
            [
                [
                    {
                        "license": "CC-BY-3.0",
                        "url": "http://creativecommons.org/licenses/by/3.0/",
                    }
                ],
                [
                    {
                        "license": "CC-BY-3.0",
                        "url": "http://creativecommons.org/licenses/by/3.0/",
                    }
                ],
            ],
            "license",
            id="test_get_license",
        ),
    ],
)
def test_oup_articles_parsing(parsed_articles, expected, key):
    for (
        expected_value,
        article,
    ) in zip(expected, parsed_articles):
        assert key in article
        assert article[key] == expected_value
