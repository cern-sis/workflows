import xml.etree.ElementTree as ET

from common.parsing.xml_extractors import RequiredFieldNotFoundExtractionError
from iop.parser import IOPParser
from pytest import fixture, raises


@fixture(scope="module")
def iop_parser():
    yield IOPParser()


@fixture
def happy_path_article(shared_datadir):
    with open(shared_datadir / "example1.xml") as f:
        return ET.fromstring(f.read())


@fixture
def parsed_happy_path_article(iop_parser, happy_path_article):
    yield iop_parser._publisher_specific_parsing(happy_path_article)


def test_happy_path_article(parsed_happy_path_article):
    print(parsed_happy_path_article["authors"])
    assert [
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
                {"value": "Brookhaven National Laboratory, Upton,USA", "country": "USA"}
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
    ] == parsed_happy_path_article["authors"]


@fixture
def article_without_authors(shared_datadir):
    with open(shared_datadir / "without_authors.xml") as f:
        return ET.fromstring(f.read())


def test_parse_without_authors_article(iop_parser, article_without_authors):
    with raises(RequiredFieldNotFoundExtractionError):
        assert iop_parser._publisher_specific_parsing(article_without_authors)


@fixture
def author_without_name(shared_datadir):
    with open(shared_datadir / "author_without_name.xml") as f:
        return ET.fromstring(f.read())


def test_parsed_author_without_name(iop_parser, author_without_name):
    with raises(RequiredFieldNotFoundExtractionError):
        assert iop_parser._publisher_specific_parsing(author_without_name)


@fixture
def author_without_surname(shared_datadir):
    with open(shared_datadir / "author_without_surname.xml") as f:
        return ET.fromstring(f.read())


def test_parsed_author_without_surnname(iop_parser, author_without_surname):
    with raises(RequiredFieldNotFoundExtractionError):
        assert iop_parser._publisher_specific_parsing(author_without_surname)


@fixture
def author_without_affiliations(shared_datadir):
    with open(shared_datadir / "author_without_affiliations.xml") as f:
        return ET.fromstring(f.read())


def test_parsed_author_without_affiliations(iop_parser, author_without_affiliations):
    with raises(RequiredFieldNotFoundExtractionError):
        assert iop_parser._publisher_specific_parsing(author_without_affiliations)


@fixture
def author_affiliations_just_with_ref(shared_datadir):
    with open(shared_datadir / "affiliations_just_with_ref.xml") as f:
        return ET.fromstring(f.read())


def test_parsed_author_affiliations_just_with_ref(
    iop_parser, author_affiliations_just_with_ref
):
    with raises(RequiredFieldNotFoundExtractionError):
        assert iop_parser._publisher_specific_parsing(author_affiliations_just_with_ref)


@fixture
def author_affiliations_just_with_collab(shared_datadir):
    with open(shared_datadir / "just_with_collab.xml") as f:
        return ET.fromstring(f.read())


def test_parsed_author_affiliations_just_with_collab(
    iop_parser, author_affiliations_just_with_collab
):
    with raises(RequiredFieldNotFoundExtractionError):
        assert iop_parser._publisher_specific_parsing(
            author_affiliations_just_with_collab
        )


@fixture
def article_with_collab_and_author(shared_datadir):
    with open(shared_datadir / "with_collab_and_author.xml") as f:
        return ET.fromstring(f.read())


@fixture
def parsed_article_with_collab_and_author(iop_parser, article_with_collab_and_author):
    yield iop_parser._publisher_specific_parsing(article_with_collab_and_author)


def test_parsed_article_with_collab_and_author(parsed_article_with_collab_and_author):
    assert [
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
        }
    ] == parsed_article_with_collab_and_author["authors"]
