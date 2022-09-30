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
        assert "dois" in article
        assert article["dois"] == [doi]


def test_journal_doctype(parsed_articles):
    journal_doctypes = ["article", "article", "article"]
    for journal_doctype, article in zip(journal_doctypes, parsed_articles):
        assert "journal_doctype" in article
        assert article["journal_doctype"] == journal_doctype


def test_arxiv_eprints(parsed_articles):
    arxiv_eprints = [
        {"value": "2204.01249"},
        {"value": "2205.14599"},
        {"value": "2207.02498"},
    ]
    for arxiv_eprint, article in zip(arxiv_eprints, parsed_articles):
        assert "arxiv_eprints" in article
        assert article["arxiv_eprints"] == arxiv_eprint


def test_page_nr(parsed_articles):
    page_nrs = [27, 16, 13]
    for page_nr, article in zip(page_nrs, parsed_articles):
        assert "page_nr" in article
        assert article["page_nr"] == page_nr


def test_abstract(parsed_articles):
    abstracts = [
        "We construct open-closed superstring interactions based on the open-closed homotopy algebra structure. This provides a classical open superstring field theory on general closed-superstring-field backgrounds described by classical solutions of the nonlinear equation of motion of the closed superstring field theory. We also give the corresponding WZW-like action through the map connecting the homotopy-based and WZW-like formulations.",
        "The",
        "",
    ]
    for abstract, article in zip(abstracts, parsed_articles):
        assert "abstract" in article
        assert article["abstract"] == abstract
