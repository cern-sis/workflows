import os
import xml.etree.ElementTree as ET

from common.parsing.xml_extractors import RequiredFieldNotFoundExtractionError
from common.utils import parse_without_names_spaces
from oup.parser import OUPParser
from pytest import fixture, raises


@fixture(scope="module")
def parser():
    return OUPParser()


@fixture
def valid_articles(shared_datadir):
    articles = []
    valid_article_names = ["ptac108.xml", "ptac113.xml", "ptac120.xml", "ptab170.xml"]
    for filename in sorted(valid_article_names):
        with open(os.path.join(shared_datadir, filename)) as file:
            articles.append(parse_without_names_spaces(file.read()))
    yield articles


@fixture()
def parsed_articles(parser, valid_articles):
    yield [parser._publisher_specific_parsing(article) for article in valid_articles]


def test_dois(parsed_articles):
    dois = [
        "10.1093/ptep/ptac108",
        "10.1093/ptep/ptac120",
        "10.1093/ptep/ptac113",
        "10.1093/ptep/ptab170",
    ]
    dois_parsed_article = [article["dois"][0] for article in parsed_articles]
    assert set(dois) == set(dois_parsed_article)


def test_no_doi_article(shared_datadir, parser):
    article_name = "ptac108_without_doi.xml"
    with open(shared_datadir / article_name) as file:
        content = parse_without_names_spaces(file.read())
        with raises(RequiredFieldNotFoundExtractionError):
            parser._publisher_specific_parsing(content)


def test_no_doi_value_article(shared_datadir, parser):
    article_name = "ptac108_without_doi_value.xml"
    with open(shared_datadir / article_name) as file:
        content = parse_without_names_spaces(file.read())
        with raises(RequiredFieldNotFoundExtractionError):
            parser._publisher_specific_parsing(content)


def test_page_nr(parsed_articles):
    page_nrs = [10, 13, 16, 27]
    page_nrs_parsed_article = [article["page_nr"] for article in parsed_articles]
    assert sorted(page_nrs) == sorted(page_nrs_parsed_article)


def test_no_page_nr(shared_datadir, parser):
    article_name = "ptac113_without_page_nr.xml"
    with open(shared_datadir / article_name) as file:
        content = parse_without_names_spaces(file.read())
        article = parser._publisher_specific_parsing(content)
        assert "page_nr" not in article


def test_no_page_nr_value(shared_datadir, parser):
    article_name = "ptac113_without_page_nr_value.xml"
    with open(shared_datadir / article_name) as file:
        content = parse_without_names_spaces(file.read())
        article = parser._publisher_specific_parsing(content)
        assert "page_nr" not in article


def test_no_page_nr_count(shared_datadir, parser):
    article_name = "ptac113_without_page_nr_count.xml"
    with open(shared_datadir / article_name) as file:
        content = parse_without_names_spaces(file.read())
        article = parser._publisher_specific_parsing(content)
        assert "page_nr" not in article


def test_journal_doc_types(parsed_articles):
    doc_types = sorted(["article", "article", "article", "other"])
    parsed_articles_types = sorted(
        [article["journal_doctype"] for article in parsed_articles]
    )
    assert parsed_articles_types == doc_types


def test_no_doc_type_article(shared_datadir, parser):
    article_name = "ptac113_without_journal_doc_type.xml"
    with open(shared_datadir / article_name) as file:
        content = parse_without_names_spaces(file.read())
        article = parser._publisher_specific_parsing(content)
        assert "journal_doctype" not in article


@fixture
def other_doc_type_article(shared_datadir, parser):
    article_name = "ptac113_other_journal_doc_type.xml"
    with open(shared_datadir / article_name) as file:
        content = parse_without_names_spaces(file.read())
        yield parser._publisher_specific_parsing(content)


def test_other_journal_doc_types(other_doc_type_article):
    assert "other" == other_doc_type_article["journal_doctype"]


def test_arxiv(parsed_articles):
    doc_types = [
        {"value": "2111.09468"},
        {"value": "2204.01249"},
        {"value": "2207.02498"},
        {"value": "2205.14599"},
    ]
    for doc_type, article_doc_type in zip(doc_types, parsed_articles):
        assert doc_type == article_doc_type["arxiv_eprints"]


def test_no_arxiv(shared_datadir, parser):
    article_name = "ptac120_no_arxiv_value.xml"
    with open(shared_datadir / article_name) as file:
        content = parse_without_names_spaces(file.read())
        article = parser._publisher_specific_parsing(content)
        assert "arxiv_eprints" not in article


def test_authors(parsed_articles):
    authors = [
        [
            {
                "surname": "Iwazaki",
                "given_names": "Aiichi",
                "email": "a_iwazaki@hotmail.com",
                "affiliations": [
                    {
                        "institution": "International Economics and Politics, Nishogakusha University",
                        "country": "Japan",
                    }
                ],
            }
        ],
        [
            {
                "surname": "Kunitomo",
                "given_names": "Hiroshi",
                "email": "kunitomo@yukawa.kyoto-u.ac.jp",
                "affiliations": [
                    {
                        "institution": "Center for Gravitational Physics and Quantum Information, Yukawa Institute for Theoretical Physics",
                        "country": "Japan",
                    }
                ],
            }
        ],
        [
            {
                "surname": "Garg",
                "given_names": "Ritu",
                "email": "rgarg_phd19@thapar.edu",
                "affiliations": [
                    {
                        "institution": "School of Physics and Materials Science, Thapar Institute of Engineering and Technology",
                        "country": "India",
                    }
                ],
            },
            {
                "surname": "Upadhyay",
                "given_names": "A",
                "email": None,
                "affiliations": [
                    {
                        "institution": "School of Physics and Materials Science, Thapar Institute of Engineering and Technology",
                        "country": "India",
                    }
                ],
            },
        ],
        [
            {
                "surname": "Hata",
                "given_names": "Hiroyuki",
                "email": None,
                "affiliations": [
                    {
                        "institution": "Department of Physics, Kyoto University",
                        "country": "Japan",
                    }
                ],
            },
            {
                "surname": "Takeda",
                "given_names": "Daichi",
                "email": None,
                "affiliations": [
                    {
                        "institution": "Department of Physics, Kyoto University",
                        "country": "Japan",
                    }
                ],
            },
            {
                "surname": "Yoshinaka",
                "given_names": "Jojiro",
                "email": "george.yoshinaka@gauge.scphys.kyoto-u.ac.jp",
                "affiliations": [
                    {
                        "institution": "Department of Physics, Kyoto University",
                        "country": "Japan",
                    }
                ],
            },
        ],
    ]
    parsed_authors = [article["authors"] for article in parsed_articles]
    assert authors == parsed_authors


def test_no_authors(shared_datadir, parser):
    article_name = "patc120_without_authors.xml"
    with open(shared_datadir / article_name) as file:
        content = parse_without_names_spaces(file.read())
        with raises(RequiredFieldNotFoundExtractionError):
            parser._publisher_specific_parsing(content)


def test_no_authors_names(shared_datadir, parser):
    article_name = "ptac120_without_authors_names.xml"
    expected_output = [
        {
            "surname": "Hata",
            "given_names": None,
            "email": None,
            "affiliations": [
                {
                    "institution": "Department of Physics, Kyoto University",
                    "country": "Japan",
                }
            ],
        },
        {
            "surname": "Takeda",
            "given_names": None,
            "email": None,
            "affiliations": [
                {
                    "institution": "Department of Physics, Kyoto University",
                    "country": "Japan",
                }
            ],
        },
        {
            "surname": "Yoshinaka",
            "given_names": None,
            "email": "george.yoshinaka@gauge.scphys.kyoto-u.ac.jp",
            "affiliations": [
                {
                    "institution": "Department of Physics, Kyoto University",
                    "country": "Japan",
                }
            ],
        },
    ]

    with open(shared_datadir / article_name) as file:
        content = parse_without_names_spaces(file.read())
        parsed_article = parser._publisher_specific_parsing(content)
        assert parsed_article["authors"] == expected_output


def test_no_authors_value(shared_datadir, parser):
    article_name = "ptac120_without_authors_value.xml"
    with open(shared_datadir / article_name) as file:
        content = parse_without_names_spaces(file.read())
        with raises(RequiredFieldNotFoundExtractionError):
            parser._publisher_specific_parsing(content)


def test_abstract(parsed_articles):
    abstracts = [
        'We propose a method of detecting the dark matter axion by using two slabs of a conductor. The flat surfaces are set face to face, parallel to each other. An external magnetic field  <italic>B</italic> parallel to the surfaces is applied. Radiation converted from the axion arises between the two slabs. When we tune the spacing  <italic>l</italic> between the two surfaces such that  <italic>l</italic> = &#960;/ <italic>m</italic> <sub> <italic>a</italic> </sub> with axion mass  <italic>m</italic> <sub> <italic>a</italic> </sub>, a resonance occurs so that the radiation becomes strong. Furthermore, the electric current flowing on the surface of the slabs is enhanced. We show that the electric current is large enough to be detectable at the resonance. It reaches 0.7 &#215; 10 <sup> &#8722;9</sup>&#8201;A&#8201; <inline-formula> <tex-math id="TM0001" notation="LaTeX">$(10^{-5}\\, \\mbox{eV}/m_a)^{1/2} \\, (B/5\\, \\mbox{T}) \\, (L/10\\, \\mbox{cm}) \\, (\\sigma /3.3\\times 10^7 \\, \\rm eV)$</tex-math> </inline-formula> using 6N copper for the square slabs with side length  <italic>L</italic> and high electrical conductivity &#963; at temperature  <italic>T</italic> &#8764; 1&#8201;K. The power of the Joule heating is  <inline-formula> <tex-math id="TM0002" notation="LaTeX">$0.3\\times 10^{-22} \\, \\mbox{W} \\, (B/5 \\, \\mbox{T})^2 \\, (10^{-5} \\, \\mbox{eV}/m_a)^{1/2} \\, (L/10 \\, \\mbox{cm})^2 \\, (\\sigma /3.3\\times 10^7 \\, \\rm eV)$</tex-math> </inline-formula>. When we amplify the power using an LC circuit with factor  <italic>Q</italic> <sub> LC</sub>, the signal-to-noise ratio is  <inline-formula> <tex-math id="TM0003" notation="LaTeX">$4.5\\times 10^{4} \\, (Q_\\mathrm{LC}/10^6) \\, (B/5 \\, \\mbox{T})^2 \\, (t_\\mathrm{obs}/1\\, \\mathrm{s})^{1/2}\\, (10^{-5} \\, \\mbox{eV}/m_a) \\, (L/10 \\, \\mbox{cm})^2 \\, (\\sigma /3.3\\times 10^7 \\, \\rm eV)$</tex-math> </inline-formula> with an observation time of  <italic>t</italic> <sub>obs</sub>.',
        "We construct open-closed superstring interactions based on the open-closed homotopy algebra structure. This provides a classical open superstring field theory on general closed-superstring-field backgrounds described by classical solutions of the nonlinear equation\xa0of motion of the closed superstring field theory. We also give the corresponding WZW-like action through the map connecting the homotopy-based and WZW-like formulations.",
        "We study <italic>F</italic> -wave bottom mesons in heavy quark effective theory. The available experimental and theoretical data is used to calculate the masses of <italic>F</italic> -wave bottom mesons. The decay widths of bottom mesons are analyzed to find upper bounds for the associated couplings. We also construct Regge trajectories for our predicted data in the ( <italic>J, M</italic> <sup>2</sup> ) plane, and our results nicely fit on Regge lines. Our results may provide crucial information for future experimental studies.",
        "The <italic>KBc</italic> algebra is a subalgebra that has been used to construct classical solutions in Witten&#8217;s open string field theory, such as the tachyon vacuum solution. The main purpose of this paper is to give various operator sets that satisfy the <italic>KBc</italic> algebra. In addition, since those sets can contain matter operators arbitrarily, we can reproduce the solution of Kiermaier, Okawa, and Soler, and that of Erler and Maccaferri. Starting with a single D-brane solution on the tachyon vacuum, we replace the original <italic>KBc</italic> in it with an appropriate set to generate each of the above solutions. Thus, it is expected that the <italic>KBc</italic> algebra, combined with the single D-brane solution, leads to a more unified description of classical solutions.",
    ]

    abstracts_parsed_article = [article["abstract"] for article in parsed_articles]
    assert set(abstracts) == set(abstracts_parsed_article)


def test_no_abstract(shared_datadir, parser):
    article_name = "ptac120_no_abstract.xml"
    with open(shared_datadir / article_name) as file:
        content = ET.fromstring(file.read())
        with raises(RequiredFieldNotFoundExtractionError):
            parser._publisher_specific_parsing(content)


def test_no_abstract_value(shared_datadir, parser):
    article_name = "ptac120_no_abstract_value.xml"
    with open(shared_datadir / article_name) as file:
        content = ET.fromstring(file.read())
        with raises(RequiredFieldNotFoundExtractionError):
            parser._publisher_specific_parsing(content)


def test_titles(parsed_articles):
    titles = [
        "Detectable electric current induced by the dark matter axion in a conductor",
        "Open-closed homotopy algebra in superstring field theory",
        "Study of <italic>F</italic> -wave bottom mesons in heavy quark effective theory",
        "Generating string field theory solutions with matter operators from <italic>KBc</italic> algebra",
    ]
    titles_parsed_article = [article["title"] for article in parsed_articles]
    assert set(titles) == set(titles_parsed_article)


def test_no_title(shared_datadir, parser):
    article_name = "ptac108_no_title.xml"
    with open(shared_datadir / article_name) as file:
        content = ET.fromstring(file.read())
        with raises(RequiredFieldNotFoundExtractionError):
            parser._publisher_specific_parsing(content)


def test_journal_volume(parsed_articles):
    journal_volumes = ["2022", "2022", "2022", "2022"]
    journal_volumes_parsed_article = [
        article["journal_volume"] for article in parsed_articles
    ]
    assert set(journal_volumes) == set(journal_volumes_parsed_article)


def test_no_journal_volume(shared_datadir, parser):
    article_name = "ptab170_no_journal_volume.xml"
    with open(shared_datadir / article_name) as file:
        content = parse_without_names_spaces(file.read())
        with raises(RequiredFieldNotFoundExtractionError):
            parser._publisher_specific_parsing(content)


def test_no_title_value(shared_datadir, parser):
    article_name = "ptac108_no_title_value.xml"
    with open(shared_datadir / article_name) as file:
        content = ET.fromstring(file.read())
        with raises(RequiredFieldNotFoundExtractionError):
            parser._publisher_specific_parsing(content)


def test_date_published(parsed_articles):
    expected_date = ["2022-01-12", "2022-08-18", "2022-08-27", "2022-09-02"]
    dates = [article["date_published"] for article in parsed_articles]
    assert sorted(expected_date) == sorted(dates)


def test_no_date_published(shared_datadir, parser):
    article_name = "ptac108_no_date_published.xml"
    with open(shared_datadir / article_name) as file:
        content = parse_without_names_spaces(file.read())
        article = parser._publisher_specific_parsing(content)
        assert "date_published" not in article


def test_no_date_published_value(shared_datadir, parser):
    article_name = "ptac108_no_date_published_value.xml"
    with open(shared_datadir / article_name) as file:
        content = parse_without_names_spaces(file.read())
        article = parser._publisher_specific_parsing(content)
        assert "date_published" not in article


def test_journal_issue(parsed_articles):
    doc_types = sorted(["2", "9", "9", "9"])
    parsed_articles_types = sorted(
        [article["journal_issue"] for article in parsed_articles]
    )
    assert parsed_articles_types == doc_types


def test_no_journal_issue_article(shared_datadir, parser):
    article_name = "ptac113_no_journal_issue.xml"
    with open(shared_datadir / article_name) as file:
        content = parse_without_names_spaces(file.read())
        article = parser._publisher_specific_parsing(content)
        assert "journal_issue" not in article


def test_no_journal_issue_value_article(shared_datadir, parser):
    article_name = "ptac113_no_journal_issue_value.xml"
    with open(shared_datadir / article_name) as file:
        content = parse_without_names_spaces(file.read())
        article = parser._publisher_specific_parsing(content)
        assert "journal_issue" not in article


def test_no_journal_volume_value(shared_datadir, parser):
    article_name = "ptab170_no_journal_volume_value.xml"
    with open(shared_datadir / article_name) as file:
        content = parse_without_names_spaces(file.read())
        with raises(RequiredFieldNotFoundExtractionError):
            parser._publisher_specific_parsing(content)


def test_journal_year(parsed_articles):
    journal_volumes = ["2022", "2022", "2022", "2022"]
    journal_volumes_parsed_article = [
        article["journal_year"] for article in parsed_articles
    ]
    assert set(journal_volumes) == set(journal_volumes_parsed_article)


def test_no_journal_year(shared_datadir, parser):
    article_name = "ptab170_no_journal_volume.xml"
    with open(shared_datadir / article_name) as file:
        content = parse_without_names_spaces(file.read())
        with raises(RequiredFieldNotFoundExtractionError):
            parser._publisher_specific_parsing(content)


def test_no_year_volume_value(shared_datadir, parser):
    article_name = "ptab170_no_journal_volume_value.xml"
    with open(shared_datadir / article_name) as file:
        content = parse_without_names_spaces(file.read())
        with raises(RequiredFieldNotFoundExtractionError):
            parser._publisher_specific_parsing(content)


def test_journal_artid(parsed_articles):
    journal_artids = ["021B01", "093B07", "093B08", "093B09"]
    journal_artids_parsed_article = [
        article["journal_artid"] for article in parsed_articles
    ]
    assert set(journal_artids) == set(journal_artids_parsed_article)


def test_no_journal_artid(shared_datadir, parser):
    article_name = "ptac120_without_journal_artid.xml"
    with open(shared_datadir / article_name) as file:
        content = parse_without_names_spaces(file.read())
        article = parser._publisher_specific_parsing(content)
        assert "journal_artid" not in article


def test_copyright_year(parsed_articles):
    copyright_years = [2022, 2022, 2022, 2022]
    copyright_years_parsed_article = [
        article["copyright_year"] for article in parsed_articles
    ]
    assert set(copyright_years) == set(copyright_years_parsed_article)


def test_no_copyright_year(shared_datadir, parser):
    article_name = "ptac120_without_copyright_year.xml"
    with open(shared_datadir / article_name) as file:
        content = parse_without_names_spaces(file.read())
        article = parser._publisher_specific_parsing(content)
        assert "copyright_year" not in article


def test_no_copyright_year_value(shared_datadir, parser):
    article_name = "ptac120_without_copyright_year_value.xml"
    with open(shared_datadir / article_name) as file:
        content = parse_without_names_spaces(file.read())
        article = parser._publisher_specific_parsing(content)
        assert "copyright_year" not in article


def test_journal_title(parsed_articles):
    journal_titles = [
        "Progress of Theoretical and Experimental Physics",
        "Progress of Theoretical and Experimental Physics",
        "Progress of Theoretical and Experimental Physics",
        "Progress of Theoretical and Experimental Physics",
    ]
    journal_titles_parsed_article = [
        article["journal_title"] for article in parsed_articles
    ]
    assert journal_titles == journal_titles_parsed_article


def test_no_journal_title(shared_datadir, parser):
    article_name = "ptab170_no_journal_title.xml"
    with open(shared_datadir / article_name) as file:
        content = parse_without_names_spaces(file.read())
        article = parser._publisher_specific_parsing(content)
        article["journal_title"] == "Prog. Theor. Exp. Phys"


def test_no_journal_title_and_pubmed(shared_datadir, parser):
    article_name = "ptab170_no_journal_title_and_pubmed.xml"
    with open(shared_datadir / article_name) as file:
        content = parse_without_names_spaces(file.read())
        article = parser._publisher_specific_parsing(content)
        article["journal_title"] == "PTEPHY"


def test_no_journal_title_no_pubmed_no_publisher(shared_datadir, parser):
    article_name = "ptab170_no_journal_title_no_pubmed_no_publisher.xml"
    with open(shared_datadir / article_name) as file:
        content = ET.fromstring(file.read())
        with raises(RequiredFieldNotFoundExtractionError):
            parser._publisher_specific_parsing(content)


def test_licenses(parsed_articles):
    licenses = [
        [
            {
                "url": "https://creativecommons.org/licenses/by/4.0/",
                "license": "CC-BY-4.0",
            }
        ],
        [
            {
                "url": "https://creativecommons.org/licenses/by/4.0/",
                "license": "CC-BY-4.0",
            }
        ],
        [
            {
                "url": "https://creativecommons.org/licenses/by/4.0/",
                "license": "CC-BY-4.0",
            }
        ],
        [
            {
                "url": "https://creativecommons.org/licenses/by/4.0/",
                "license": "CC-BY-4.0",
            }
        ],
    ]
    licenses_parsed_article = [article["license"] for article in parsed_articles]
    print(licenses)
    assert licenses == licenses_parsed_article


def test_licenses_no_license(shared_datadir, parser):
    article_name = "ptac113_without_license.xml"
    with open(shared_datadir / article_name) as file:
        content = ET.fromstring(file.read())
        with raises(RequiredFieldNotFoundExtractionError):
            parser._publisher_specific_parsing(content)


def test_no_journal_title_value(shared_datadir, parser):
    article_name = "ptab170_no_journal_title_value.xml"
    with open(shared_datadir / article_name) as file:
        content = parse_without_names_spaces(file.read())
        article = parser._publisher_specific_parsing(content)
        article["journal_title"] == "Prog. Thezor. Exp. Phys"


def test_no_journal_title_and_pubmed_value(shared_datadir, parser):
    article_name = "ptab170_no_journal_title_and_pubmed_value.xml"
    with open(shared_datadir / article_name) as file:
        content = parse_without_names_spaces(file.read())
        article = parser._publisher_specific_parsing(content)
        article["journal_title"] == "PTEPHY"


def test_no_journal_title_no_pubmed_no_publisher_value(shared_datadir, parser):
    article_name = "ptab170_no_journal_title_no_pubmed_no_publisher_value.xml"
    with open(shared_datadir / article_name) as file:
        content = ET.fromstring(file.read())
        with raises(RequiredFieldNotFoundExtractionError):
            parser._publisher_specific_parsing(content)


def test_licenses_no_license_value(shared_datadir, parser):
    article_name = "ptac113_without_license_value.xml"
    with open(shared_datadir / article_name) as file:
        content = ET.fromstring(file.read())
        with raises(RequiredFieldNotFoundExtractionError):
            parser._publisher_specific_parsing(content)


def test_collections(parsed_articles):
    collections = [
        "Progress of Theoretical and Experimental Physics",
        "Progress of Theoretical and Experimental Physics",
        "Progress of Theoretical and Experimental Physics",
        "Progress of Theoretical and Experimental Physics",
    ]
    collections_parsed_article = [
        article["collections"][0] for article in parsed_articles
    ]
    assert set(collections) == set(collections_parsed_article)
