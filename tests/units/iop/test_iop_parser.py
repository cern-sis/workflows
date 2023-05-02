import xml.etree.ElementTree as ET

from common.constants import ARXIV_EXTRACTION_PATTERN
from common.enhancer import Enhancer
from common.exceptions import UnknownLicense
from common.parsing.xml_extractors import RequiredFieldNotFoundExtractionError
from common.utils import parse_to_ET_element, preserve_cdata
from iop.parser import IOPParser
from pytest import fixture, mark, param, raises
from structlog.testing import capture_logs


@fixture
def parser():
    return IOPParser()


def test_doi(shared_datadir, parser):
    content = (shared_datadir / "just_required_fields.xml").read_text()
    article = parse_to_ET_element(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert parsed_article["dois"] == ["10.1088/1674-1137/ac66cc"]


def test_no_doi(shared_datadir, parser):
    content = (shared_datadir / "no_data.xml").read_text()
    article = parse_to_ET_element(content)
    with raises(RequiredFieldNotFoundExtractionError):
        parser._publisher_specific_parsing(article)


def test_no_doi_in_text(shared_datadir, parser):
    content = (shared_datadir / "just_fields_no_text_data.xml").read_text()
    article = parse_to_ET_element(content)
    with raises(RequiredFieldNotFoundExtractionError):
        parser._publisher_specific_parsing(article)


def test_journal_doctype(shared_datadir, parser):
    content = (shared_datadir / "just_required_fields.xml").read_text()
    article = parse_to_ET_element(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert parsed_article["journal_doctype"] == "article"


def test_no_journal_doctype(shared_datadir, parser):
    content = (shared_datadir / "without_journal_doc_type.xml").read_text()
    article = parse_to_ET_element(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert "journal_doctype" not in parsed_article


def test_no_journal_doctype_in_attribute(shared_datadir, parser):
    content = (
        shared_datadir / "without_journal_doc_type_attribute_value.xml"
    ).read_text()
    article = parse_to_ET_element(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert "journal_doctype" not in parsed_article


def test_journal_doctype_with_wrong_value(shared_datadir, parser):
    content = (shared_datadir / "all_fields_wrong_values.xml").read_text()
    article = parse_to_ET_element(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert "journal_doctype" not in parsed_article


def test_journal_doctype_log_error_with_wrong_value(shared_datadir):
    with capture_logs() as cap_logs:
        content = (shared_datadir / "all_fields_wrong_values.xml").read_text()
        content = preserve_cdata(content)
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
            {
                "class_name": "TextExtractor",
                "event": "subtitle is not found in XML",
                "log_level": "error",
            },
        ]


def test_journal_doctype_log_error_without_value(shared_datadir, parser):
    with capture_logs() as cap_logs:
        parser = IOPParser()
        content = (shared_datadir / "without_journal_doc_type.xml").read_text()
        content = preserve_cdata(content)
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
            {
                "class_name": "TextExtractor",
                "event": "subtitle is not found in XML",
                "log_level": "error",
            },
        ]


def test_related_article_doi(shared_datadir, parser):
    content = (shared_datadir / "related_article_dois.xml").read_text()
    article = parse_to_ET_element(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert parsed_article["related_article_doi"] == ["10.0000/0000-0000/aa00aa"]


def test_no_related_article_dois(shared_datadir, parser):
    content = (shared_datadir / "related_article_dois_no_path.xml").read_text()
    article = parse_to_ET_element(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert "related_article_doi" not in parsed_article


def test_related_article_dois_no_value(shared_datadir, parser):
    content = (shared_datadir / "related_article_dois_no_value.xml").read_text()
    article = parse_to_ET_element(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert "related_article_doi" not in parsed_article


def test_realted_article_dois_log_error_without_value(shared_datadir, parser):
    with capture_logs() as cap_logs:
        parser = IOPParser()
        content = (shared_datadir / "related_article_dois_no_path.xml").read_text()
        content = preserve_cdata(content)
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
            {
                "class_name": "TextExtractor",
                "event": "subtitle is not found in XML",
                "log_level": "error",
            },
        ]


def test_arxiv_eprints(shared_datadir, parser):
    content = (shared_datadir / "arxiv_eprints.xml").read_text()
    article = parse_to_ET_element(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert parsed_article["arxiv_eprints"] == [{"value": "2108.04010"}]


def test_no_arxiv_eprints(shared_datadir, parser):
    content = (shared_datadir / "no_arxiv_eprints.xml").read_text()
    article = parse_to_ET_element(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert "arxiv_eprints" not in parsed_article


def test_no_arxiv_eprints_value(shared_datadir, parser):
    content = (shared_datadir / "no_arxiv_eprints_value.xml").read_text()
    article = parse_to_ET_element(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert "arxiv_eprints" not in parsed_article


def test_no_arxiv_eprints_value_log_error_without_value(shared_datadir, parser):
    with capture_logs() as cap_logs:
        parser = IOPParser()
        content = (shared_datadir / "no_arxiv_eprints_value.xml").read_text()
        content = preserve_cdata(content)
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
            {
                "class_name": "TextExtractor",
                "event": "subtitle is not found in XML",
                "log_level": "error",
            },
        ]


def test_arxiv_eprints_value_with_version(shared_datadir, parser):
    content = (shared_datadir / "arxiv_eprints_with_version.xml").read_text()
    article = parse_to_ET_element(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert parsed_article["arxiv_eprints"] == [{"value": "2108.04010"}]


def test_wrong_arxiv_eprints_value_log_error_without_value(shared_datadir, parser):
    with capture_logs() as cap_logs:
        parser = IOPParser()
        content = (shared_datadir / "arxiv_eprint_wrong_value.xml").read_text()
        content = preserve_cdata(content)
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
            {
                "class_name": "TextExtractor",
                "event": "subtitle is not found in XML",
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
    article = parse_to_ET_element(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert parsed_article["page_nr"] == [9]


def test_no_page_nr_path(shared_datadir, parser):
    content = (shared_datadir / "no_page_nr_path.xml").read_text()
    article = parse_to_ET_element(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert "page_nr" not in parsed_article


def test_page_nr_wrong_value(shared_datadir, parser):
    content = (shared_datadir / "page_nr_wrong_value.xml").read_text()
    article = parse_to_ET_element(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert "page_nr" not in parsed_article


def test_page_nr_no_value(shared_datadir, parser):
    content = (shared_datadir / "page_nr_no_value.xml").read_text()
    article = parse_to_ET_element(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert "page_nr" not in parsed_article


def test_wrong_page_nr_value_log(shared_datadir, parser):
    with capture_logs() as cap_logs:
        parser = IOPParser()
        content = (shared_datadir / "page_nr_wrong_value.xml").read_text()
        content = preserve_cdata(content)
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
            {
                "class_name": "TextExtractor",
                "event": "subtitle is not found in XML",
                "log_level": "error",
            },
        ]


def test_date_published(shared_datadir, parser):
    content = (shared_datadir / "all_fields.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert parsed_article["date_published"] == "2022-06-01"
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


def test_abstract(shared_datadir, parser):
    content = (shared_datadir / "abstract.xml").read_text()
    article = parse_to_ET_element(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert (
        parsed_article["abstract"]
        == r"Solar, terrestrial, and supernova neutrino experiments are subject to muon-induc"
        r"ed radioactive background. The China Jinping Underground Laboratory (CJPL), with"
        r" its unique advantage of a 2400 m rock coverage and long distance from nuclear p"
        r"ower plants, is ideal for MeV-scale neutrino experiments. Using a 1-ton prototyp"
        r"e detector of the Jinping Neutrino Experiment (JNE), we detected 343 high-energy"
        r" cosmic-ray muons and (7.86 <inline-formula xmlns:ns0='http://www.w3.org/1999/xl"
        r"ink'> <tex-math> $ \pm $ </tex-math> <inline-graphic ns0:href='cpc_46_8_085001_M"
        r"1.jpg' ns0:type='simple' /> </inline-formula> 3.97) muon-induced neutrons from a"
        r"n 820.28-day dataset at the first phase of CJPL (CJPL-I). Based on the muon-indu"
        r"ced neutrons, we measured the corresponding muon-induced neutron yield in a liqu"
        r"id scintillator to be <inline-formula xmlns:ns0='http://www.w3.org/1999/xlink'> "
        r"<tex-math> $(3.44 \pm 1.86_{\rm stat.}\pm $ </tex-math> <inline-graphic ns0:href"
        r"='cpc_46_8_085001_M2.jpg' ns0:type='simple' /> </inline-formula> <inline-formula"
        r" xmlns:ns0='http://www.w3.org/1999/xlink'> <tex-math> $ 0.76_{\rm syst.})\times "
        r"10^{-4}$ </tex-math> <inline-graphic ns0:href='cpc_46_8_085001_M2-1.jpg' ns0:typ"
        r"e='simple' /> </inline-formula> &#956; <sup>&#8722;1</sup> g <sup>&#8722;1</sup>"
        r" cm <sup>2</sup> at an average muon energy of 340 GeV. We provided the first stu"
        r"dy for such neutron background at CJPL. A global fit including this measurement "
        r"shows a power-law coefficient of (0.75 <inline-formula xmlns:ns0='http://www.w3."
        r"org/1999/xlink'> <tex-math> $ \pm $ </tex-math> <inline-graphic ns0:href='cpc_46"
        r"_8_085001_M3.jpg' ns0:type='simple' /> </inline-formula> 0.02) for the dependenc"
        r"e of the neutron yield at the liquid scintillator on muon energy."
    )


def test_no_abstract(shared_datadir, parser):
    content = (shared_datadir / "no_abstract.xml").read_text()
    article = parse_to_ET_element(content)
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
    assert parsed_article["copyright_year"] == "2022"
    assert (
        parsed_article["copyright_statement"]
        == "© 2022 Chinese Physical Society and the Institute of High Energy Physics of the Chinese Academy of Sciences and the Institute of Modern Physics of the Chinese Academy of Sciences and IOP Publishing Ltd"
    )


def test_copyright_no_year(shared_datadir, parser):
    content = (shared_datadir / "no_copyright_year.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert (
        parsed_article["copyright_statement"]
        == "© 2022 Chinese Physical Society and the Institute of High Energy Physics of the Chinese Academy of Sciences and the Institute of Modern Physics of the Chinese Academy of Sciences and IOP Publishing Ltd"
    )


def test_copyright_no_year_value(shared_datadir, parser):
    content = (shared_datadir / "no_copyright_year_value.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert (
        parsed_article["copyright_statement"]
        == "© 2022 Chinese Physical Society and the Institute of High Energy Physics of the Chinese Academy of Sciences and the Institute of Modern Physics of the Chinese Academy of Sciences and IOP Publishing Ltd"
    )


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
            {
                "class_name": "TextExtractor",
                "event": "subtitle is not found in XML",
                "log_level": "error",
            },
        ]


def test_copyright_no_statement(shared_datadir, parser):
    content = (shared_datadir / "no_copyright_statement.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert parsed_article["copyright_year"] == "2022"


def test_copyright_no_statement_value(shared_datadir, parser):
    content = (shared_datadir / "no_copyright_statement_value.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert parsed_article["copyright_year"] == "2022"


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
            {
                "class_name": "TextExtractor",
                "event": "subtitle is not found in XML",
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


def test_licenses(shared_datadir, parser):
    content = (shared_datadir / "just_required_fields.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert parsed_article["license"] == [
        {"license": "CC-BY-3.0", "url": "http://creativecommons.org/licenses/by/3.0/"}
    ]


def test_no_licenses_and_no_statements(shared_datadir, parser):
    content = (shared_datadir / "no_license_and_no_statement_no_url.xml").read_text()
    article = ET.fromstring(content)
    with raises(RequiredFieldNotFoundExtractionError):
        parser._publisher_specific_parsing(article)


def test_no_abstract_value(shared_datadir, parser):
    content = (shared_datadir / "no_abstract_value.xml").read_text()
    article = parse_to_ET_element(content)
    with raises(RequiredFieldNotFoundExtractionError):
        parser._publisher_specific_parsing(article)


def test_publication_info_fields_values_just_year(shared_datadir, parser):
    content = (
        shared_datadir / "no_journal_tiltle_volume_issue_artid_values.xml"
    ).read_text()
    article = ET.fromstring(content)
    with raises(RequiredFieldNotFoundExtractionError):
        parser._publisher_specific_parsing(article)


def test_no_license_url(shared_datadir, parser):
    content = (shared_datadir / "no_license_url.xml").read_text()
    article = ET.fromstring(content)
    with raises(RequiredFieldNotFoundExtractionError):
        parser._publisher_specific_parsing(article)


def test_collaborations(shared_datadir, parser):
    content = (shared_datadir / "all_fields.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert parsed_article["collaborations"] == ["JNE collaboration"]


def test_no_collaborations(shared_datadir, parser):
    content = (shared_datadir / "just_required_fields.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert "collaborations" not in parsed_article


def test_no_collaborations_value(shared_datadir, parser):
    content = (shared_datadir / "no_collaboration_value.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert "collaborations" not in parsed_article


def test_title(shared_datadir, parser):
    content = (shared_datadir / "just_required_fields.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert (
        parsed_article["title"]
        == "Measurement of muon-induced neutron yield at the China Jinping Underground Laboratory <xref ref-type='fn' rid='cpc_46_8_085001_fn1'>*</xref> <fn id='cpc_46_8_085001_fn1'> <label>*</label> <p>Supported in part by the National Natural Science Foundation of China (11620101004, 11475093, 12127808), the Key Laboratory of Particle &amp; Radiation Imaging (TsinghuaUniversity), the CAS Center for Excellence in Particle Physics (CCEPP), and Guangdong Basic and Applied Basic Research Foundation (2019A1515012216). Portion of this work performed at Brookhaven National Laboratory is supported in part by the United States Department of Energy (DE-SC0012704)</p> </fn>"
    )


# Couldn't find original IOP articles, which have subtitle
# The data is falsified
def test_subtitle(shared_datadir, parser):
    content = (shared_datadir / "with_subtitle.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert parsed_article["subtitle"] == "Subtitle (pseudo data)"


def test_no_title(shared_datadir, parser):
    content = (shared_datadir / "no_title.xml").read_text()
    article = parse_to_ET_element(content)
    with raises(RequiredFieldNotFoundExtractionError):
        parser._publisher_specific_parsing(article)


def test_no_subtitle(shared_datadir, parser):
    content = (shared_datadir / "just_required_fields.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert "subtitle" not in parsed_article


def test_no_title_no_subtitle_values(shared_datadir, parser):
    content = (shared_datadir / "no_title_no_subtitle_values.xml").read_text()
    article = ET.fromstring(content)
    article = parse_to_ET_element(content)
    with raises(RequiredFieldNotFoundExtractionError):
        parser._publisher_specific_parsing(article)


def test_no_licenses_statement(shared_datadir, parser):
    content = (shared_datadir / "no_license_statement.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert parsed_article["license"] == [
        {"license": "CC-BY-3.0", "url": "http://creativecommons.org/licenses/by/3.0/"}
    ]


def test_unknown_license_in_license_URL(shared_datadir, parser):
    content = (shared_datadir / "unknown_license_in_license_URL.xml").read_text()
    article = ET.fromstring(content)
    with raises(UnknownLicense):
        parser._publisher_specific_parsing(article)


def test_cdata_with_regex():
    paseudo_aricle = """
    <article>
        <title>That's the title</title>
    <abstract>
        <p><?CDATA Data in Cdata ?>Data not in CDATA</p>
    </abstract>
    </article>
    """
    ET_article = parse_to_ET_element(paseudo_aricle)
    abstract_element = ET_article.find("abstract/p")
    abstract_text = abstract_element.text
    assert abstract_text == " Data in Cdata Data not in CDATA"

    title_element = ET_article.find("title")
    title_text = title_element.text
    assert title_text == "That's the title"

    string_abstract = ET.tostring(abstract_element)
    assert string_abstract == b"<p> Data in Cdata Data not in CDATA</p>\n    "


def test_cdata_without_regex():
    paseudo_aricle = """
    <article>
        <title>That's the title</title>
    <abstract>
        <p><?CDATA Data in Cdata ?>Data not in CDATA</p>
    </abstract>
    </article>
    """
    ET_article = ET.fromstring(paseudo_aricle)
    p_element_content = ET.tostring(ET_article.find("abstract"))
    assert (
        p_element_content
        == b"<abstract>\n        <p>Data not in CDATA</p>\n    </abstract>\n    "
    )

    abstract_element = ET_article.find("abstract/p")
    abstract_text = abstract_element.text
    assert abstract_text == "Data not in CDATA"

    title_element = ET_article.find("title")
    title_text = title_element.text
    assert title_text == "That's the title"

    string_abstract = ET.tostring(abstract_element)
    assert string_abstract == b"<p>Data not in CDATA</p>\n    "


def test_title_starting_with_tags(shared_datadir, parser):
    content = (shared_datadir / "aca95c.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser._publisher_specific_parsing(article)
    assert (
        parsed_article["title"]
        == "<italic toggle='yes'>R</italic>-Symmetric NMSSM <xref ref-type='fn' rid='cpc_47_4_043105_fn1'>*</xref> <fn id='cpc_47_4_043105_fn1'><label>*</label><p>Supported in part by the National Natural Science Foundation of China (11775039), the High-level Talents Research and Startup Foundation Projects for Doctors of Zhoukou Normal University (ZKNUC2021006), and Scientific research projects of universities in Henan Province, China (23A140027).</p></fn>"
    )


def test_title_starting_with_tags_after_enhancer(shared_datadir, parser):
    content = (shared_datadir / "aca95c.xml").read_text()
    article = ET.fromstring(content)
    parsed_article = parser.parse(article)
    enhanced_file = Enhancer()("IOP", parsed_article)
    assert (
        enhanced_file["titles"][0]["title"]
        == "<italic toggle='yes'>R</italic>-Symmetric NMSSM <xref ref-type='fn' rid='cpc_47_4_043105_fn1'>*</xref>"
    )
