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
    page_nrs = [
        "Open-closed homotopy algebra in superstring field theory",
        'Generating string field theory solutions with matter operators from<ns0:italic xmlns:ns0="http://specifications.silverchair.com/xsd/1/24/SCJATS-journalpublishing.xsd">KBc</ns0:italic>algebra',
        'Study of<ns0:italic xmlns:ns0="http://specifications.silverchair.com/xsd/1/24/SCJATS-journalpublishing.xsd">F</ns0:italic>-wave bottom mesons in heavy quark effective theory',
    ]
    for page_nr, article in zip(page_nrs, parsed_articles):
        assert article["title"] == page_nr
