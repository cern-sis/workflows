import xml.etree.ElementTree as ET

from common.constants import ARXIV_EXTRACTION_PATTERN
from common.parsing.xml_extractors import RequiredFieldNotFoundExtractionError
from iop.parser import IOPParser
from pytest import fixture, mark, param, raises
from structlog.testing import capture_logs


@fixture
def parser():
    return IOPParser()


def test_doi(shared_datadir, parser):
    content = (shared_datadir / "just_required_fields.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert parsed_article["dois"] == ["10.1088/1674-1137/ac66cc"]


def test_no_doi(shared_datadir, parser):
    content = (shared_datadir / "no_data.xml").read_text()
    article = ET.fromstring(content)
    with raises(RequiredFieldNotFoundExtractionError):
        parser._publisher_specific_parsing(article)


def test_no_doi_in_text(shared_datadir, parser):
    content = (shared_datadir / "just_fields_no_text_data.xml").read_text()
    article = ET.fromstring(content)
    with raises(RequiredFieldNotFoundExtractionError):
        parser._publisher_specific_parsing(article)


def test_journal_doctype(shared_datadir, parser):
    content = (shared_datadir / "just_required_fields.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert parsed_article["journal_doctype"] == "article"


def test_no_journal_doctype(shared_datadir, parser):
    content = (shared_datadir / "without_journal_doc_type.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert "journal_doctype" not in parsed_article


def test_no_journal_doctype_in_attribute(shared_datadir, parser):
    content = (
        shared_datadir / "without_journal_doc_type_attribute_value.xml"
    ).read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert "journal_doctype" not in parsed_article


def test_journal_doctype_with_wrong_value(shared_datadir, parser):
    content = (shared_datadir / "all_fields_wrong_values.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert "journal_doctype" not in parsed_article


def test_journal_doctype_log_error_with_wrong_value(shared_datadir):
    with capture_logs() as cap_logs:
        content = (shared_datadir / "all_fields_wrong_values.xml").read_text()
        article = ET.fromstring(content)
        parser = IOPParser()
        parser._publisher_specific_parsing(article)
        assert cap_logs == [
            {
                "class_name": "IOPParser",
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "Parsing dois for article",
                "log_level": "info",
            },
            {
                "class_name": "IOPParser",
                "dois": "10.1088/1674-1137/ac66cc",
                "article_type": "no-data",
                "event": "Unmapped article type",
                "log_level": "error",
            },
        ]


def test_journal_doctype_log_error_without_value(shared_datadir, parser):
    with capture_logs() as cap_logs:
        parser = IOPParser()
        content = (shared_datadir / "without_journal_doc_type.xml").read_text()
        article = ET.fromstring(content)
        parser._publisher_specific_parsing(article)
        assert cap_logs == [
            {
                "class_name": "IOPParser",
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "Parsing dois for article",
                "log_level": "info",
            },
            {
                "class_name": "IOPParser",
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "Article-type is not found in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "institution is not found in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "country is not found in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "institution is not found in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "country is not found in XML",
                "log_level": "error",
            },
            {
                "class_name": "IOPParser",
                "event": "Cannot find month of date_published in XML",
                "log_level": "error",
            },
            {
                "class_name": "IOPParser",
                "event": "Cannot find day of date_published in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "journal_volume is not found in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "journal_issue is not found in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "journal_artid is not found in XML",
                "log_level": "error",
            },
        ]


def test_related_article_doi(shared_datadir, parser):
    content = (shared_datadir / "related_article_dois.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert parsed_article["related_article_doi"] == ["10.0000/0000-0000/aa00aa"]


def test_no_related_article_dois(shared_datadir, parser):
    content = (shared_datadir / "related_article_dois_no_path.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert "related_article_doi" not in parsed_article


def test_related_article_dois_no_value(shared_datadir, parser):
    content = (shared_datadir / "related_article_dois_no_value.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert "related_article_doi" not in parsed_article


def test_realted_article_dois_log_error_without_value(shared_datadir, parser):
    with capture_logs() as cap_logs:
        parser = IOPParser()
        content = (shared_datadir / "related_article_dois_no_path.xml").read_text()
        article = ET.fromstring(content)
        parser._publisher_specific_parsing(article)
        assert cap_logs == [
            {
                "class_name": "IOPParser",
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "Parsing dois for article",
                "log_level": "info",
            },
            {
                "class_name": "IOPParser",
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "No related article dois found",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "institution is not found in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "country is not found in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "institution is not found in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "country is not found in XML",
                "log_level": "error",
            },
            {
                "class_name": "IOPParser",
                "event": "Cannot find month of date_published in XML",
                "log_level": "error",
            },
            {
                "class_name": "IOPParser",
                "event": "Cannot find day of date_published in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "journal_volume is not found in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "journal_issue is not found in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "journal_artid is not found in XML",
                "log_level": "error",
            },
        ]


def test_arxiv_eprints(shared_datadir, parser):
    content = (shared_datadir / "arxiv_eprints.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert parsed_article["arxiv_eprints"] == [{"value": "2108.04010"}]


def test_no_arxiv_eprints(shared_datadir, parser):
    content = (shared_datadir / "no_arxiv_eprints.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert "arxiv_eprints" not in parsed_article


def test_no_arxiv_eprints_value(shared_datadir, parser):
    content = (shared_datadir / "no_arxiv_eprints_value.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert "arxiv_eprints" not in parsed_article


def test_no_arxiv_eprints_value_log_error_without_value(shared_datadir, parser):
    with capture_logs() as cap_logs:
        parser = IOPParser()
        content = (shared_datadir / "no_arxiv_eprints_value.xml").read_text()
        article = ET.fromstring(content)
        parser._publisher_specific_parsing(article)
        assert cap_logs == [
            {
                "class_name": "IOPParser",
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "Parsing dois for article",
                "log_level": "info",
            },
            {
                "class_name": "IOPParser",
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "No arXiv eprints found",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "institution is not found in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "country is not found in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "institution is not found in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "country is not found in XML",
                "log_level": "error",
            },
            {
                "class_name": "IOPParser",
                "event": "Cannot find month of date_published in XML",
                "log_level": "error",
            },
            {
                "class_name": "IOPParser",
                "event": "Cannot find day of date_published in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "journal_volume is not found in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "journal_issue is not found in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "journal_artid is not found in XML",
                "log_level": "error",
            },
        ]


def test_arxiv_eprints_value_with_version(shared_datadir, parser):
    content = (shared_datadir / "arxiv_eprints_with_version.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert parsed_article["arxiv_eprints"] == [{"value": "2108.04010"}]


def test_wrong_arxiv_eprints_value_log_error_without_value(shared_datadir, parser):
    with capture_logs() as cap_logs:
        parser = IOPParser()
        content = (shared_datadir / "arxiv_eprint_wrong_value.xml").read_text()
        article = ET.fromstring(content)
        parsed_article = parser._publisher_specific_parsing(article)
        assert "arxiv_eprints" not in parsed_article
        assert cap_logs == [
            {
                "class_name": "IOPParser",
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "Parsing dois for article",
                "log_level": "info",
            },
            {
                "class_name": "IOPParser",
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "The arXiv value is not valid.",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "institution is not found in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "country is not found in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "institution is not found in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "country is not found in XML",
                "log_level": "error",
            },
            {
                "class_name": "IOPParser",
                "event": "Cannot find month of date_published in XML",
                "log_level": "error",
            },
            {
                "class_name": "IOPParser",
                "event": "Cannot find day of date_published in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "journal_volume is not found in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "journal_issue is not found in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "journal_artid is not found in XML",
                "log_level": "error",
            },
        ]


@fixture
@mark.parametrize(
    "input, expected",
    [
        param("1111.111123", "1111.111123", id="test_arxiv_value_with_digits"),
        param(
            "1111.111wtwtwvqv1",
            "1111.111wtwtwvq",
            id="test_arxiv_value_with_digits_and_letters_and_version",
        ),
        param(
            "1111.111123v1",
            "1111.111123",
            id="test_arxiv_value_with_digits_and_version",
        ),
    ],
)
def test_arxiv_extraction_pattern(expected, input):
    assert ARXIV_EXTRACTION_PATTERN.sub("", input) == expected


def test_page_nr(shared_datadir, parser):
    content = (shared_datadir / "page_nr.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert parsed_article["page_nr"] == [9]


def test_no_page_nr_path(shared_datadir, parser):
    content = (shared_datadir / "no_page_nr_path.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert "page_nr" not in parsed_article


def test_page_nr_wrong_value(shared_datadir, parser):
    content = (shared_datadir / "page_nr_wrong_value.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert "page_nr" not in parsed_article


def test_page_nr_no_value(shared_datadir, parser):
    content = (shared_datadir / "page_nr_no_value.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert "page_nr" not in parsed_article


def test_wrong_page_nr_value_log(shared_datadir, parser):
    with capture_logs() as cap_logs:
        parser = IOPParser()
        content = (shared_datadir / "page_nr_wrong_value.xml").read_text()
        article = ET.fromstring(content)
        parsed_article = parser._publisher_specific_parsing(article)
        assert "page_nr" not in parsed_article
        assert cap_logs == [
            {
                "class_name": "IOPParser",
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "Parsing dois for article",
                "log_level": "info",
            },
            {"value": "abc", "event": "Cannot parse to integer", "log_level": "error"},
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "institution is not found in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "country is not found in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "institution is not found in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "country is not found in XML",
                "log_level": "error",
            },
            {
                "class_name": "IOPParser",
                "event": "Cannot find month of date_published in XML",
                "log_level": "error",
            },
            {
                "class_name": "IOPParser",
                "event": "Cannot find day of date_published in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "journal_volume is not found in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "journal_issue is not found in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "journal_artid is not found in XML",
                "log_level": "error",
            },
        ]


def test_date_published(shared_datadir, parser):
    content = (shared_datadir / "all_fields.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert parsed_article["date_published"] == "2022-08-01"
    assert parsed_article["journal_year"] == 2022


def test_authors(shared_datadir, parser):
    content = (shared_datadir / "all_fields.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    parsed_article["authors"] == [
        {
            "surname": "Zhao",
            "given_names": "Lin",
            "affiliations": [
                {
                    "institution": "Department of Engineering Physics, Tsinghua University, China",
                    "country": "China",
                },
                {
                    "institution": "Center for High Energy Physics, Tsinghua University, China",
                    "country": "China",
                },
            ],
        },
        {
            "surname": "Luo",
            "given_names": "Wentai",
            "affiliations": [
                {
                    "institution": "School of Physical Sciences, University of Chinese Academy of Sciences, China",
                    "country": "China",
                }
            ],
        },
        {
            "surname": "Bathe-Peters",
            "given_names": "Lars",
            "affiliations": [
                {
                    "institution": "Department of Engineering Physics, Tsinghua University, China",
                    "country": "China",
                },
                {
                    "institution": "Institut für Physik, Technische Universität Berlin, Germany",
                    "country": "Germany",
                },
            ],
        },
        {
            "surname": "Chen",
            "given_names": "Shaomin",
            "affiliations": [
                {
                    "institution": "Department of Engineering Physics, Tsinghua University, China",
                    "country": "China",
                },
                {
                    "institution": "Center for High Energy Physics, Tsinghua University, China",
                    "country": "China",
                },
                {
                    "institution": "Key Laboratory of Particle & Radiation Imaging (Tsinghua University), China",
                    "country": "China",
                },
            ],
        },
        {
            "surname": "Chouaki",
            "given_names": "Mourad",
            "affiliations": [
                {
                    "institution": "Department of Engineering Physics, Tsinghua University, China",
                    "country": "China",
                },
                {
                    "institution": "École Polytechnique Fédérale de Lausanne, Switzerland",
                    "country": "Switzerland",
                },
            ],
        },
        {
            "surname": "Dou",
            "given_names": "Wei",
            "affiliations": [
                {
                    "institution": "Department of Engineering Physics, Tsinghua University, China",
                    "country": "China",
                },
                {
                    "institution": "Center for High Energy Physics, Tsinghua University, China",
                    "country": "China",
                },
            ],
        },
        {
            "surname": "Guo",
            "given_names": "Lei",
            "affiliations": [
                {
                    "institution": "Department of Engineering Physics, Tsinghua University, China",
                    "country": "China",
                },
                {
                    "institution": "Center for High Energy Physics, Tsinghua University, China",
                    "country": "China",
                },
            ],
        },
        {
            "surname": "Guo",
            "given_names": "Ziyi",
            "affiliations": [
                {
                    "institution": "Department of Engineering Physics, Tsinghua University, China",
                    "country": "China",
                },
                {
                    "institution": "Center for High Energy Physics, Tsinghua University, China",
                    "country": "China",
                },
            ],
        },
        {
            "surname": "Hussain",
            "given_names": "Ghulam",
            "affiliations": [
                {
                    "institution": "Department of Engineering Physics, Tsinghua University, China",
                    "country": "China",
                },
                {
                    "institution": "Center for High Energy Physics, Tsinghua University, China",
                    "country": "China",
                },
            ],
        },
        {
            "surname": "Li",
            "given_names": "Jinjing",
            "affiliations": [
                {
                    "institution": "Department of Engineering Physics, Tsinghua University, China",
                    "country": "China",
                },
                {
                    "institution": "Center for High Energy Physics, Tsinghua University, China",
                    "country": "China",
                },
            ],
        },
        {
            "surname": "Liang",
            "given_names": "Ye",
            "affiliations": [
                {
                    "institution": "Department of Engineering Physics, Tsinghua University, China",
                    "country": "China",
                },
                {
                    "institution": "Center for High Energy Physics, Tsinghua University, China",
                    "country": "China",
                },
            ],
        },
        {
            "surname": "Liu",
            "given_names": "Qian",
            "affiliations": [
                {
                    "institution": "School of Physical Sciences, University of Chinese Academy of Sciences, China",
                    "country": "China",
                }
            ],
        },
        {
            "surname": "Luo",
            "given_names": "Guang",
            "affiliations": [
                {
                    "institution": "School of Physics, Sun Yat-Sen University, China",
                    "country": "China",
                }
            ],
        },
        {
            "surname": "Qi",
            "given_names": "Ming",
            "affiliations": [
                {
                    "institution": "School of Physics, Nanjing University, China",
                    "country": "China",
                }
            ],
        },
        {
            "surname": "Shao",
            "given_names": "Wenhui",
            "affiliations": [
                {
                    "institution": "Department of Engineering Physics, Tsinghua University, China",
                    "country": "China",
                },
                {
                    "institution": "Center for High Energy Physics, Tsinghua University, China",
                    "country": "China",
                },
            ],
        },
        {
            "surname": "Tang",
            "given_names": "Jian",
            "affiliations": [
                {
                    "institution": "School of Physics, Sun Yat-Sen University, China",
                    "country": "China",
                }
            ],
        },
        {
            "surname": "Wan",
            "given_names": "Linyan",
            "affiliations": [
                {
                    "institution": "Department of Engineering Physics, Tsinghua University, China",
                    "country": "China",
                },
                {
                    "institution": "Center for High Energy Physics, Tsinghua University, China",
                    "country": "China",
                },
            ],
        },
        {
            "surname": "Wang",
            "given_names": "Zhe",
            "affiliations": [
                {
                    "institution": "Department of Engineering Physics, Tsinghua University, China",
                    "country": "China",
                },
                {
                    "institution": "Center for High Energy Physics, Tsinghua University, China",
                    "country": "China",
                },
                {
                    "institution": "Key Laboratory of Particle & Radiation Imaging (Tsinghua University), China",
                    "country": "China",
                },
            ],
        },
        {
            "surname": "Wu",
            "given_names": "Yiyang",
            "affiliations": [
                {
                    "institution": "Department of Engineering Physics, Tsinghua University, China",
                    "country": "China",
                },
                {
                    "institution": "Center for High Energy Physics, Tsinghua University, China",
                    "country": "China",
                },
            ],
        },
        {
            "surname": "Xu",
            "given_names": "Benda",
            "affiliations": [
                {
                    "institution": "Department of Engineering Physics, Tsinghua University, China",
                    "country": "China",
                },
                {
                    "institution": "Center for High Energy Physics, Tsinghua University, China",
                    "country": "China",
                },
                {
                    "institution": "Key Laboratory of Particle & Radiation Imaging (Tsinghua University), China",
                    "country": "China",
                },
            ],
        },
        {
            "surname": "Xu",
            "given_names": "Tong",
            "affiliations": [
                {
                    "institution": "Department of Engineering Physics, Tsinghua University, China",
                    "country": "China",
                },
                {
                    "institution": "Center for High Energy Physics, Tsinghua University, China",
                    "country": "China",
                },
            ],
        },
        {
            "surname": "Xu",
            "given_names": "Weiran",
            "affiliations": [
                {
                    "institution": "Department of Engineering Physics, Tsinghua University, China",
                    "country": "China",
                },
                {
                    "institution": "Center for High Energy Physics, Tsinghua University, China",
                    "country": "China",
                },
            ],
        },
        {
            "surname": "Yang",
            "given_names": "Yuzi",
            "affiliations": [
                {
                    "institution": "Department of Engineering Physics, Tsinghua University, China",
                    "country": "China",
                },
                {
                    "institution": "Center for High Energy Physics, Tsinghua University, China",
                    "country": "China",
                },
            ],
        },
        {
            "surname": "Yeh",
            "given_names": "Minfang",
            "affiliations": [
                {
                    "institution": "Brookhaven National Laboratory, Upton, USA",
                    "country": "USA",
                }
            ],
        },
        {
            "surname": "Zhang",
            "given_names": "Aiqiang",
            "affiliations": [
                {
                    "institution": "Department of Engineering Physics, Tsinghua University, China",
                    "country": "China",
                },
                {
                    "institution": "Center for High Energy Physics, Tsinghua University, China",
                    "country": "China",
                },
            ],
        },
        {
            "surname": "Zhang",
            "given_names": "Bin",
            "affiliations": [
                {
                    "institution": "Department of Engineering Physics, Tsinghua University, China",
                    "country": "China",
                },
                {
                    "institution": "Center for High Energy Physics, Tsinghua University, China",
                    "country": "China",
                },
            ],
        },
    ]


def test_no_authors(shared_datadir, parser):
    content = (shared_datadir / "no_authors.xml").read_text()
    article = ET.fromstring(content)
    with raises(RequiredFieldNotFoundExtractionError):
        parser._publisher_specific_parsing(article)


def test_no_month_published(shared_datadir, parser):
    content = (shared_datadir / "no_month_published.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert parsed_article["journal_year"] == 2022
    assert parsed_article["date_published"] == "2022"


def test_no_day_published(shared_datadir, parser):
    content = (shared_datadir / "no_day_published.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert parsed_article["date_published"] == "2022-08"
    assert parsed_article["journal_year"] == 2022


def test_no_year_published(shared_datadir, parser):
    content = (shared_datadir / "no_year_published.xml").read_text()
    article = ET.fromstring(content)
    with raises(RequiredFieldNotFoundExtractionError):
        parser._publisher_specific_parsing(article)


def test_no_authors_institutions(shared_datadir, parser):
    content = (shared_datadir / "no_authors_institutions.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert parsed_article["authors"] == [
        {
            "surname": "Zhao",
            "given_names": "Lin",
            "affiliations": [{"country": "China"}, {"country": "China"}],
        }
    ]


def test_no_authors_country(shared_datadir, parser):
    content = (shared_datadir / "no_authors_country.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert parsed_article["authors"] == [{"given_names": "Lin", "surname": "Zhao"}]


def test_no_authors_and_institutions_country(shared_datadir, parser):
    content = (shared_datadir / "no_authors_and_institutions_country.xml").read_text()
    article = ET.fromstring(content)
    with raises(RequiredFieldNotFoundExtractionError):
        parser._publisher_specific_parsing(article)


def test_authors_with_missing_fields(shared_datadir, parser):
    content = (shared_datadir / "authors_with_missing_fields.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert parsed_article["authors"] == [
        {
            "surname": "Zhao",
            "given_names": "林",  # the author misses given_names, so it's taken from name-style="eastern"
            "affiliations": [
                {
                    "country": "China",
                    "institution": "Department of Engineering Physics, Tsinghua University, China",
                },
                {
                    "country": "China",
                    "institution": "Department of Engineering Physics, Tsinghua University, China",
                },
            ],
        },
        {
            "surname": "Test1",  # the author misses given_names
            "affiliations": [
                {
                    "country": "China",
                    "institution": "Department of Engineering Physics, Tsinghua University, China",
                },
                {
                    "country": "China",
                    "institution": "Department of Engineering Physics, Tsinghua University, China",
                },
            ],
        },
        {
            "affiliations": [  # the author misses given_names and name
                {
                    "country": "China",
                    "institution": "Department of Engineering Physics, Tsinghua University, China",
                },
                {
                    "country": "China",
                    "institution": "Department of Engineering Physics, Tsinghua University, China",
                },
            ]
        },
    ]


def test_copyright(shared_datadir, parser):
    content = (shared_datadir / "just_required_fields.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert parsed_article["copyright"] == [
        {
            "year": "2022",
            "copyright_statement": "© 2022 Chinese Physical Society and the Institute of High Energy Physics of the Chinese Academy of Sciences and the Institute of Modern Physics of the Chinese Academy of Sciences and IOP Publishing Ltd",
        }
    ]


def test_copyright_no_year(shared_datadir, parser):
    content = (shared_datadir / "no_copyright_year.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert parsed_article["copyright"] == [
        {
            "copyright_statement": "© 2022 Chinese Physical Society and the Institute of High Energy Physics of the Chinese Academy of Sciences and the Institute of Modern Physics of the Chinese Academy of Sciences and IOP Publishing Ltd"
        }
    ]


def test_copyright_no_year_value(shared_datadir, parser):
    content = (shared_datadir / "no_copyright_year_value.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert parsed_article["copyright"] == [
        {
            "copyright_statement": "© 2022 Chinese Physical Society and the Institute of High Energy Physics of the Chinese Academy of Sciences and the Institute of Modern Physics of the Chinese Academy of Sciences and IOP Publishing Ltd"
        }
    ]


def test_copyright_no_years_logs(shared_datadir, parser):
    with capture_logs() as cap_logs:
        parser = IOPParser()
        content = (shared_datadir / "no_copyright_year.xml").read_text()
        article = ET.fromstring(content)
        parser._publisher_specific_parsing(article)
        assert cap_logs == [
            {
                "class_name": "IOPParser",
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "Parsing dois for article",
                "log_level": "info",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "institution is not found in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "country is not found in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "institution is not found in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "country is not found in XML",
                "log_level": "error",
            },
            {
                "class_name": "IOPParser",
                "event": "Cannot find month of date_published in XML",
                "log_level": "error",
            },
            {
                "class_name": "IOPParser",
                "event": "Cannot find day of date_published in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "copyright_year is not found in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "journal_volume is not found in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "journal_issue is not found in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "journal_artid is not found in XML",
                "log_level": "error",
            },
        ]


def test_copyright_no_statement(shared_datadir, parser):
    content = (shared_datadir / "no_copyright_statement.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert parsed_article["copyright"] == [{"year": "2022"}]


def test_copyright_no_statement_value(shared_datadir, parser):
    content = (shared_datadir / "no_copyright_statement_value.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert parsed_article["copyright"] == [{"year": "2022"}]


def test_copyright_no_statement_logs(shared_datadir, parser):
    with capture_logs() as cap_logs:
        parser = IOPParser()
        content = (shared_datadir / "no_copyright_statement.xml").read_text()
        article = ET.fromstring(content)
        parser._publisher_specific_parsing(article)
        assert cap_logs == [
            {
                "class_name": "IOPParser",
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "Parsing dois for article",
                "log_level": "info",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "institution is not found in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "country is not found in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "institution is not found in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "country is not found in XML",
                "log_level": "error",
            },
            {
                "class_name": "IOPParser",
                "event": "Cannot find month of date_published in XML",
                "log_level": "error",
            },
            {
                "class_name": "IOPParser",
                "event": "Cannot find day of date_published in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "copyright_statement is not found in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "journal_volume is not found in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "journal_issue is not found in XML",
                "log_level": "error",
            },
            {
                "dois": "10.1088/1674-1137/ac66cc",
                "event": "journal_artid is not found in XML",
                "log_level": "error",
            },
        ]


def test_publication_info(shared_datadir, parser):
    content = (shared_datadir / "all_fields.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert parsed_article["journal_title"] == "Chinese Physics C"
    assert parsed_article["journal_volume"] == "46"
    assert parsed_article["journal_issue"] == "8"
    assert parsed_article["journal_artid"] == "085001"
    assert parsed_article["journal_year"] == 2022

def test_publication_info_just_journal_title_year(shared_datadir, parser):
    content = (shared_datadir / "just_journal_year.xml").read_text()
    article = ET.fromstring(content)
    with raises(RequiredFieldNotFoundExtractionError):
        parser._publisher_specific_parsing(article)

def test_publication_info_fields_values_just_year(shared_datadir, parser):
    content = (
        shared_datadir / "no_journal_tiltle_volume_issue_artid_values.xml"
    ).read_text()
    article = ET.fromstring(content)
    with raises(RequiredFieldNotFoundExtractionError):
        parser._publisher_specific_parsing(article)