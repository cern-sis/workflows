import os
import xml.etree.ElementTree as ET

from oup.parser import OUPParser
from pytest import fixture


@fixture(scope="module")
def iop_parser():
    return OUPParser()


@fixture
def articles(shared_datadir):
    articles = []
    file_names = os.listdir(shared_datadir)
    for file_name in file_names:
        with open(shared_datadir / file_name) as file:
            articles.append(ET.fromstring(file.read()))
    return articles


@fixture()
def parsed_articles(iop_parser, articles):
    return [iop_parser._publisher_specific_parsing(article) for article in articles]


def test_dois(parsed_articles):
    dois = ["10.1093/ptep/ptac108", "10.1093/ptep/ptac120", "10.1093/ptep/ptac113"]

    for doi, article in zip(dois, parsed_articles):
        assert article["dois"] == [doi]


def test_journal_doctype(parsed_articles):
    journal_doctypes = ["article", "article", "article"]
    for journal_doctype, article in zip(journal_doctypes, parsed_articles):
        assert article["journal_doctype"] == journal_doctype


def test_arxiv_eprints(parsed_articles):
    arxiv_eprints = [
        {"value": "2204.01249"},
        {"value": "2205.14599"},
        {"value": "2207.02498"},
    ]
    for arxiv_eprint, article in zip(arxiv_eprints, parsed_articles):
        assert article["arxiv_eprints"] == arxiv_eprint


def test_page_nr(parsed_articles):
    page_nrs = [27, 16, 13]
    for page_nr, article in zip(page_nrs, parsed_articles):
        assert article["page_nr"] == page_nr


def test_abstract(parsed_articles):
    abstracts = [
        "We construct open-closed superstring interactions based on the open-closed homotopy algebra structure. This provides a classical open superstring field theory on general closed-superstring-field backgrounds described by classical solutions of the nonlinear equation of motion of the closed superstring field theory. We also give the corresponding WZW-like action through the map connecting the homotopy-based and WZW-like formulations.",
        'The<ns0:italic xmlns:ns0="http://specifications.silverchair.com/xsd/1/24/SCJATS-journalpublishing.xsd">KBc</ns0:italic>algebra is a subalgebra that has been used to construct classical solutions in Witten&#8217;s open string field theory, such as the tachyon vacuum solution. The main purpose of this paper is to give various operator sets that satisfy the<ns0:italic xmlns:ns0="http://specifications.silverchair.com/xsd/1/24/SCJATS-journalpublishing.xsd">KBc</ns0:italic>algebra. In addition, since those sets can contain matter operators arbitrarily, we can reproduce the solution of Kiermaier, Okawa, and Soler, and that of Erler and Maccaferri. Starting with a single D-brane solution on the tachyon vacuum, we replace the original<ns0:italic xmlns:ns0="http://specifications.silverchair.com/xsd/1/24/SCJATS-journalpublishing.xsd">KBc</ns0:italic>in it with an appropriate set to generate each of the above solutions. Thus, it is expected that the<ns0:italic xmlns:ns0="http://specifications.silverchair.com/xsd/1/24/SCJATS-journalpublishing.xsd">KBc</ns0:italic>algebra, combined with the single D-brane solution, leads to a more unified description of classical solutions.',
        'We study<ns0:italic xmlns:ns0="http://specifications.silverchair.com/xsd/1/24/SCJATS-journalpublishing.xsd">F</ns0:italic>-wave bottom mesons in heavy quark effective theory. The available experimental and theoretical data is used to calculate the masses of<ns0:italic xmlns:ns0="http://specifications.silverchair.com/xsd/1/24/SCJATS-journalpublishing.xsd">F</ns0:italic>-wave bottom mesons. The decay widths of bottom mesons are analyzed to find upper bounds for the associated couplings. We also construct Regge trajectories for our predicted data in the (<ns0:italic xmlns:ns0="http://specifications.silverchair.com/xsd/1/24/SCJATS-journalpublishing.xsd">J, M</ns0:italic><ns0:sup xmlns:ns0="http://specifications.silverchair.com/xsd/1/24/SCJATS-journalpublishing.xsd">2</ns0:sup>) plane, and our results nicely fit on Regge lines. Our results may provide crucial information for future experimental studies.',
    ]
    for abstract, article in zip(abstracts, parsed_articles):
        assert article["abstract"] == abstract


def test_title(parsed_articles):
    titles = [
        "Open-closed homotopy algebra in superstring field theory",
        'Generating string field theory solutions with matter operators from<ns0:italic xmlns:ns0="http://specifications.silverchair.com/xsd/1/24/SCJATS-journalpublishing.xsd">KBc</ns0:italic>algebra',
        'Study of<ns0:italic xmlns:ns0="http://specifications.silverchair.com/xsd/1/24/SCJATS-journalpublishing.xsd">F</ns0:italic>-wave bottom mesons in heavy quark effective theory',
    ]
    for tilte, article in zip(titles, parsed_articles):
        assert article["title"] == tilte


def test_authors(parsed_articles):
    authors = [
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
                "surname": "Hata",
                "given_names": "Hiroyuki",
                "email": False,
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
                "email": False,
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
        [
            {
                "surname": "Garg",
                "given_names": "Ritu",
                "email": "rgarg_phd19@thapar.edu",
                "affiliations": [
                    {
                        "institution": "School of Physics and Materials Science, Thapar Institute of Engineering and Technology",
                        "country": "INDIA",
                    }
                ],
            },
            {
                "surname": "Upadhyay",
                "given_names": "A",
                "email": False,
                "affiliations": [
                    {
                        "institution": "School of Physics and Materials Science, Thapar Institute of Engineering and Technology",
                        "country": "INDIA",
                    }
                ],
            },
        ],
    ]
    for author, article in zip(authors, parsed_articles):
        assert article["authors"] == author


def test_date_published(parsed_articles):
    dates_published = ["2022-08-18", "2022-09-02", "2022-08-27"]
    for date_published, article in zip(dates_published, parsed_articles):
        assert article["date_published"] == date_published


def test_journal_title(parsed_articles):
    journal_titles = [
        "Progress of Theoretical and Experimental Physics",
        "Progress of Theoretical and Experimental Physics",
        "Progress of Theoretical and Experimental Physics",
    ]
    for journal_title, article in zip(journal_titles, parsed_articles):
        assert article["journal_title"] == journal_title


def test_journal_issue(parsed_articles):
    journal_issues = ["9", "9", "9"]
    for journal_issue, article in zip(journal_issues, parsed_articles):
        assert article["journal_issue"] == journal_issue


def test_volume(parsed_articles):
    volumes = ["2022", "2022", "2022"]
    for volume, article in zip(volumes, parsed_articles):
        assert article["journal_volume"] == volume


def test_journal_artid(parsed_articles):
    journal_artids = ["093B07", "093B09", "093B08"]
    for journal_artid, article in zip(journal_artids, parsed_articles):
        assert article["journal_artid"] == journal_artid


def test_journal_year(parsed_articles):
    volumes = ["2022", "2022", "2022"]
    for volume, article in zip(volumes, parsed_articles):
        assert article["journal_year"] == volume


def test_copyright_statement(parsed_articles):
    copyright_statements = [
        "© The Author(s) 2022. Published by Oxford University Press on behalf of the Physical Society of Japan.",
        "© The Author(s) 2022. Published by Oxford University Press on behalf of the Physical Society of Japan.",
        "© The Author(s) 2022. Published by Oxford University Press on behalf of the Physical Society of Japan.",
    ]
    for copyright_statement, article in zip(copyright_statements, parsed_articles):
        assert article["copyright_statement"] == copyright_statement


def test_copyright_year(parsed_articles):
    copyright_years = [2022, 2022, 2022]
    for copyright_year, article in zip(copyright_years, parsed_articles):
        assert article["copyright_year"] == copyright_year


def test_copyright_holder(parsed_articles):
    copyright_holders = ["", "", ""]
    for copyright_holder, article in zip(copyright_holders, parsed_articles):
        assert article["copyright_holder"] == copyright_holder


def test_license(parsed_articles):
    licenses = [
        [
            {
                "license": "CC-BY-4.0",
                "url": "https://creativecommons.org/licenses/by/4.0/",
            }
        ],
        [
            {
                "license": "CC-BY-4.0",
                "url": "https://creativecommons.org/licenses/by/4.0/",
            }
        ],
        [
            {
                "license": "CC-BY-4.0",
                "url": "https://creativecommons.org/licenses/by/4.0/",
            }
        ],
    ]
    for license, article in zip(licenses, parsed_articles):
        assert article["license"] == license


def test_collections(parsed_articles):
    collections = [
        ["Progress of Theoretical and Experimental Physics"],
        ["Progress of Theoretical and Experimental Physics"],
        ["Progress of Theoretical and Experimental Physics"],
    ]
    for collection, article in zip(collections, parsed_articles):
        assert article["collections"] == collection
