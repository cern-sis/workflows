import xml.etree.ElementTree as ET

from common.parsing.xml_extractors import RequiredFieldNotFoundExtractionError
from iop.iop_process_file import enhance_iop, enrich_iop, iop_validate_record
from iop.parser import IOPParser
from pytest import fixture, raises


@fixture(scope="module")
def iop_parser():
    return IOPParser()


@fixture
def article_without_abstract(shared_datadir):
    with open(shared_datadir / "without_abstract.xml") as f:
        return ET.fromstring(f.read())


def test_article_without_abstract(iop_parser, article_without_abstract):
    with raises(RequiredFieldNotFoundExtractionError):
        assert iop_parser._publisher_specific_parsing(article_without_abstract)


@fixture
def article_without_page_nr(shared_datadir):
    with open(shared_datadir / "without_page_nr.xml") as f:
        return ET.fromstring(f.read())


@fixture
def parsed_article_without_page_nr(iop_parser, article_without_page_nr):
    return iop_parser._publisher_specific_parsing(article_without_page_nr)


def test_page_nr_without_page_nr(parsed_article_without_page_nr):
    assert parsed_article_without_page_nr["page_nr"] == [0]  # Default value


def test_iop_record_validation(iop_parser, parsed_article_without_page_nr):
    enhanced = enhance_iop(iop_parser._generic_parsing(parsed_article_without_page_nr))
    enriched = enrich_iop(enhanced)
    iop_validate_record(enriched)


@fixture
def articles(shared_datadir):
    files = ["example1.xml", "example2.xml"]
    articles = []
    for file in files:
        with open(shared_datadir / file) as f:
            articles.append(ET.fromstring(f.read()))
    return articles


@fixture
def parsed_articles(iop_parser, articles):
    return [iop_parser._publisher_specific_parsing(article) for article in articles]


def test_dois(parsed_articles):
    dois = ["10.1088/1674-1137/ac66cc", "10.1088/1674-1137/ac763c"]
    for doi, article in zip(dois, parsed_articles):
        assert article["dois"] == [doi]


def test_journal_doctype(parsed_articles):
    doctype = ["article", "article"]
    for doctype, article in zip(doctype, parsed_articles):
        assert article["journal_doctype"] == doctype


def test_related_article_doi(parsed_articles):
    for article in parsed_articles:
        assert article["related_article_doi"] == []


def test_arxiv_eprints(parsed_articles):
    arxiv_eprints = [{"value": "2108.04010"}, {"value": "2107.07275"}]
    for arxiv_eprint, article in zip(arxiv_eprints, parsed_articles):
        assert article["arxiv_eprints"] == [arxiv_eprint]


def test_page_nr(parsed_articles):
    page_nrs = [9, 18]
    for page_nr, article in zip(page_nrs, parsed_articles):
        assert article["page_nr"] == [page_nr]


def test_abstract(parsed_articles):
    abstracts = [
        'Solar, terrestrial, and supernova neutrino experiments are subject to muon-induced radioactive background. The China Jinping Underground Laboratory (CJPL), with its unique advantage of a 2400 m rock coverage and long distance from nuclear power plants, is ideal for MeV-scale neutrino experiments. Using a 1-ton prototype detector of the Jinping Neutrino Experiment (JNE), we detected 343 high-energy cosmic-ray muons and (7.86<inline-formula xmlns:ns0="http://www.w3.org/1999/xlink"><tex-math></tex-math><inline-graphic ns0:href="cpc_46_8_085001_M1.jpg" ns0:type="simple" /></inline-formula>3.97) muon-induced neutrons from an 820.28-day dataset at the first phase of CJPL (CJPL-I). Based on the muon-induced neutrons, we measured the corresponding muon-induced neutron yield in a liquid scintillator to be<inline-formula xmlns:ns0="http://www.w3.org/1999/xlink"><tex-math></tex-math><inline-graphic ns0:href="cpc_46_8_085001_M2.jpg" ns0:type="simple" /></inline-formula><inline-formula xmlns:ns0="http://www.w3.org/1999/xlink"><tex-math></tex-math><inline-graphic ns0:href="cpc_46_8_085001_M2-1.jpg" ns0:type="simple" /></inline-formula>&#956;<sup>&#8722;1</sup>g<sup>&#8722;1</sup>cm<sup>2</sup>at an average muon energy of 340 GeV. We provided the first study for such neutron background at CJPL. A global fit including this measurement shows a power-law coefficient of (0.75<inline-formula xmlns:ns0="http://www.w3.org/1999/xlink"><tex-math></tex-math><inline-graphic ns0:href="cpc_46_8_085001_M3.jpg" ns0:type="simple" /></inline-formula>0.02) for the dependence of the neutron yield at the liquid scintillator on muon energy.',
        'In this study, we modify a scenario, originally proposed by Grimus and Lavoura, in order to obtain maximal values for the atmospheric mixing angle and<inline-formula xmlns:ns0="http://www.w3.org/1999/xlink"><tex-math></tex-math><inline-graphic ns0:href="cpc_46_10_103101_M1.jpg" ns0:type="simple" /></inline-formula>, violating the Dirac phase of the lepton sector. To achieve this, we employ<inline-formula xmlns:ns0="http://www.w3.org/1999/xlink"><tex-math></tex-math><inline-graphic ns0:href="cpc_46_10_103101_M2.jpg" ns0:type="simple" /></inline-formula>and some discrete symmetries in a type II seesaw model. To make predictions about the neutrino mass ordering and smallness of the reactor angle, we establish some conditions on the elements of the neutrino mass matrix of our model. Finally, we study the quark masses and mixing pattern within the framework of our model.',
    ]
    for abstract, article in zip(abstracts, parsed_articles):
        print(article["abstract"])
        assert article["abstract"] == abstract


def test_title(parsed_articles):
    titles = [
        'Measurement of muon-induced neutron yield at the China Jinping Underground Laboratory<xref ref-type="fn" rid="cpc_46_8_085001_fn1">*</xref><fn id="cpc_46_8_085001_fn1"><label>*</label><p>Supported in part by the National Natural Science Foundation of China (11620101004, 11475093, 12127808), the Key Laboratory of Particle &amp; Radiation Imaging (TsinghuaUniversity), the CAS Center for Excellence in Particle Physics (CCEPP), and Guangdong Basic and Applied Basic Research Foundation (2019A1515012216). Portion of this work performed at Brookhaven National Laboratory is supported in part by the United States Department of Energy (DE-SC0012704)</p></fn>',
        'Lepton and quark mixing patterns with generalized<italic toggle="yes">CP</italic>transformations',
    ]
    for title, article in zip(titles, parsed_articles):
        assert article["title"] == title


def test_subtitle(parsed_articles):
    for article in parsed_articles:
        assert article["subtitle"] == ""


def test_affiliations(parsed_articles):
    authors = [
        [
            {
                "surname": "Zhao",
                "given_names": "Lin",
                "affiliations": [
                    {
                        "value": "Department of Engineering Physics, Tsinghua University,China",
                        "country": "China",
                    }
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
                    }
                ],
            },
            {
                "surname": "Chen",
                "given_names": "Shaomin",
                "affiliations": [
                    {
                        "value": "Department of Engineering Physics, Tsinghua University,China",
                        "country": "China",
                    }
                ],
            },
            {
                "surname": "Chouaki",
                "given_names": "Mourad",
                "affiliations": [
                    {
                        "value": "Department of Engineering Physics, Tsinghua University,China",
                        "country": "China",
                    }
                ],
            },
            {
                "surname": "Dou",
                "given_names": "Wei",
                "affiliations": [
                    {
                        "value": "Department of Engineering Physics, Tsinghua University,China",
                        "country": "China",
                    }
                ],
            },
            {
                "surname": "Guo",
                "given_names": "Lei",
                "affiliations": [
                    {
                        "value": "Department of Engineering Physics, Tsinghua University,China",
                        "country": "China",
                    }
                ],
            },
            {
                "surname": "Guo",
                "given_names": "Ziyi",
                "affiliations": [
                    {
                        "value": "Department of Engineering Physics, Tsinghua University,China",
                        "country": "China",
                    }
                ],
            },
            {
                "surname": "Hussain",
                "given_names": "Ghulam",
                "affiliations": [
                    {
                        "value": "Department of Engineering Physics, Tsinghua University,China",
                        "country": "China",
                    }
                ],
            },
            {
                "surname": "Li",
                "given_names": "Jinjing",
                "affiliations": [
                    {
                        "value": "Department of Engineering Physics, Tsinghua University,China",
                        "country": "China",
                    }
                ],
            },
            {
                "surname": "Liang",
                "given_names": "Ye",
                "affiliations": [
                    {
                        "value": "Department of Engineering Physics, Tsinghua University,China",
                        "country": "China",
                    }
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
                    }
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
                    }
                ],
            },
            {
                "surname": "Wang",
                "given_names": "Zhe",
                "affiliations": [
                    {
                        "value": "Department of Engineering Physics, Tsinghua University,China",
                        "country": "China",
                    }
                ],
            },
            {
                "surname": "Wu",
                "given_names": "Yiyang",
                "affiliations": [
                    {
                        "value": "Department of Engineering Physics, Tsinghua University,China",
                        "country": "China",
                    }
                ],
            },
            {
                "surname": "Xu",
                "given_names": "Benda",
                "affiliations": [
                    {
                        "value": "Department of Engineering Physics, Tsinghua University,China",
                        "country": "China",
                    }
                ],
            },
            {
                "surname": "Xu",
                "given_names": "Tong",
                "affiliations": [
                    {
                        "value": "Department of Engineering Physics, Tsinghua University,China",
                        "country": "China",
                    }
                ],
            },
            {
                "surname": "Xu",
                "given_names": "Weiran",
                "affiliations": [
                    {
                        "value": "Department of Engineering Physics, Tsinghua University,China",
                        "country": "China",
                    }
                ],
            },
            {
                "surname": "Yang",
                "given_names": "Yuzi",
                "affiliations": [
                    {
                        "value": "Department of Engineering Physics, Tsinghua University,China",
                        "country": "China",
                    }
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
                    }
                ],
            },
            {
                "surname": "Zhang",
                "given_names": "Bin",
                "affiliations": [
                    {
                        "value": "Department of Engineering Physics, Tsinghua University,China",
                        "country": "China",
                    }
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
    ]
    for author, article in zip(authors, parsed_articles):
        assert article["authors"] == author


def test_get_published_date(parsed_articles):
    doctypes = ["2022-08-01", "2022-10-01"]
    for doctype, article in zip(doctypes, parsed_articles):
        assert article["date_published"] == doctype


def test_publication_info(parsed_articles):
    publications_info = [
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
    ]
    for publication_info, article in zip(publications_info, parsed_articles):
        assert article["publication_info"] == publication_info


def test_get_date_published(parsed_articles):
    published_dates = ["2022-08-01", "2022-10-01"]
    for published_date, article in zip(published_dates, parsed_articles):
        assert article["date_published"] == published_date


def test_get_copyright_year(parsed_articles):
    copyright_years = ["2022", "2022"]
    for copyright_year, article in zip(copyright_years, parsed_articles):
        assert article["copyright_year"] == copyright_year


def test_get_copyright_statements(parsed_articles):
    copyright_statements = [
        "© 2022 Chinese Physical Society and the Institute of High Energy Physics of the Chinese Academy of Sciences and the Institute of Modern Physics of the Chinese Academy of Sciences and IOP Publishing Ltd",
        "© 2022 Chinese Physical Society and the Institute of High Energy Physics of the Chinese Academy of Sciences and the Institute of Modern Physics of the Chinese Academy of Sciences and IOP Publishing Ltd",
    ]
    for copyright_statement, article in zip(copyright_statements, parsed_articles):
        assert article["copyright_statement"] == copyright_statement


def test_get_license(parsed_articles):
    licenses = [
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
    ]
    for license, article in zip(licenses, parsed_articles):
        assert article["license"] == license
