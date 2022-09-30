import xml.etree.ElementTree as ET

from oup.parser import OUPParser
from pytest import fixture


@fixture(scope="module")
def iop_parser():
    return OUPParser()


@fixture
def articles(shared_datadir):
    articles = []
    # file_names = os.listdir(shared_datadir)
    # # for file_name in file_names:
    with open(shared_datadir / "ptac108.xml") as file:
        articles.append(ET.fromstring(file.read()))
    return articles


@fixture()
def parsed_articles(iop_parser, articles):
    return [iop_parser._publisher_specific_parsing(article) for article in articles]


def test_dois(parsed_articles):
    dois = ["10.1093/ptep/ptac108"]
    for doi, article in zip(dois, parsed_articles):
        assert "dois" in article
        assert article["dois"] == [doi]


def test_journal_doctype(parsed_articles):
    journal_doctypes = ["article"]
    for journal_doctype, article in zip(journal_doctypes, parsed_articles):
        assert "journal_doctype" in article
        assert article["journal_doctype"] == journal_doctype
