from common.parsing.generic_parsing import (
    classification_numbers,
    clear_unnecessary_fields,
    collapse_initials,
    fix_publication_date,
    free_keywords,
    join,
    list_to_value_dict,
    merge_dois,
    parse_author,
    parse_thesis_supervisors,
    publication_info,
    remove_empty_values,
    split_fullname,
    take_first,
)
from pytest import mark, param

take_first_expected = "TestValue"


@mark.parametrize(
    "test_input, expected",
    [
        param([None, "TestValue"], take_first_expected, id="Array contains None"),
        param(["", "TestValue"], take_first_expected, id="Array contains empty string"),
        param(["TestValue"], take_first_expected, id="Array correct value"),
        param([None, ""], None, id="Array is incorrect"),
    ],
)
def test_take_first(test_input, expected):
    assert expected == take_first(test_input)


@mark.parametrize(
    "test_input, expected",
    [
        param([], [], id="Array is empty"),
        param(
            [1, "TestValue", None, ""],
            [{"value": 1}, {"value": "TestValue"}],
            id="Array contains multiple values",
        ),
    ],
)
def test_list_to_value_dict(test_input, expected):
    assert expected == list_to_value_dict(test_input)


def test_list_to_value_dict_with_custom_key():
    assert [
        {"my_key": 1},
        {"my_key": "TestValue"},
    ] == list_to_value_dict([1, "TestValue", None], "my_key")


@mark.parametrize(
    "test_input, expected",
    [
        param([], "", id="Array is empty"),
        param(
            ["", "TestValue", "Test"],
            "TestValue Test",
            id="Array contains multiple values",
        ),
    ],
)
def test_join(test_input, expected):
    assert expected == join(test_input)


def test_join_with_custom_separator():
    assert "TestValue,Test" == join(["", "TestValue", "Test"], ",")


@mark.parametrize(
    "test_input, expected",
    [
        param([], [], id="Array is empty"),
        param(
            ["", "TestValue", "Test"],
            [
                {"standard": "PACS", "classification_number": "TestValue"},
                {"standard": "PACS", "classification_number": "Test"},
            ],
            id="Array contains multiple values",
        ),
    ],
)
def test_classification_numbers(test_input, expected):
    assert expected == classification_numbers(test_input)


def test_classification_numbers_with_custom_standard():
    assert [
        {"standard": "test_standard", "classification_number": "TestValue"}
    ] == classification_numbers(["", "TestValue"], "test_standard")


@mark.parametrize(
    "test_input, expected",
    [
        param([], [], id="Array is empty"),
        param(
            ["", "TestValue", "Test"],
            [
                {"source": "author", "value": "TestValue"},
                {"source": "author", "value": "Test"},
            ],
            id="Array contains multiple values",
        ),
    ],
)
def test_free_keywords(test_input, expected):
    assert expected == free_keywords(test_input)


def test_free_keywords_with_custom_source():
    assert [{"source": "test_source", "value": "TestValue"}] == free_keywords(
        ["", "TestValue"], "test_source"
    )


@mark.parametrize(
    "test_input, expected",
    [
        param("", "", id="Publication date is empty"),
        param("3", "0003-01-01", id="Publication date contains one value"),
        param("3-2", "0003-02-01", id="Publication date contains two values"),
        param("1999-10-05", "1999-10-05", id="Publication date is correct"),
    ],
)
def test_fix_publication_date(test_input, expected):
    assert expected == fix_publication_date(test_input)


@mark.parametrize(
    "test_input, expected",
    [
        param("Doe, John Magic", ("Doe", "John Magic")),
        param("Doe Boe, John Magic", ("Doe Boe", "John Magic")),
        param("John Magic Doe", ("Doe", "John Magic")),
        param("John Magic Doe Boe", ("Boe", "John Magic Doe")),
        param("", ("", ""), id="Author is empty"),
    ],
)
def test_split_fullname(test_input, expected):
    assert expected == split_fullname(test_input)


def test_collapse_initials():
    assert "F.M. Lastname" == collapse_initials("F. M. Lastname")


@mark.parametrize(
    "test_input, expected",
    [
        param(
            {"surname": "Test Surname"},
            {"full_name": "Test Surname", "surname": "Test Surname"},
            id="Only surname is present",
        ),
        param(
            {"raw_name": "Firstname Lastname"},
            {
                "full_name": "Lastname, Firstname",
                "raw_name": "Firstname Lastname",
                "given_names": "Firstname",
                "surname": "Lastname",
            },
            id="Only raw_name is present",
        ),
    ],
)
def test_parse_author(test_input, expected):
    assert expected == parse_author(test_input)


@mark.parametrize(
    "test_input, expected",
    [
        param(
            {"surname": "Test Surname", "affiliations": "Test Affiliation"},
            {"full_name": "Test Surname", "affiliations": "Test Affiliation"},
            id="Only surname is present",
        ),
        param(
            {"raw_name": "Firstname Lastname", "affiliations": "Test Affiliation"},
            {"full_name": "Lastname, Firstname", "affiliations": "Test Affiliation"},
            id="Only raw_name is present",
        ),
    ],
)
def test_parse_thesis_supervisors(test_input, expected):
    assert expected == parse_thesis_supervisors(test_input)


@mark.parametrize(
    "test_input, expected",
    [
        param(
            {
                "journal_title": "Test Value",
                "journal_volume": "Test Value",
                "journal_year": "2022",
                "journal_issue": "Test Value",
                "journal_artid": "",
                "journal_fpage": "",
                "journal_lpage": "",
                "journal_doctype": "",
                "pubinfo_freetext": "",
                "another_field": "Test Another Field",
            },
            [
                {
                    "journal_title": "Test Value",
                    "journal_volume": "Test Value",
                    "year": 2022,
                    "journal_issue": "Test Value",
                    "artid": "",
                    "page_start": "",
                    "page_end": "",
                    "material": "",
                    "pubinfo_freetext": "",
                }
            ],
            id="Some values populated",
        ),
        param(
            {
                "journal_title": "NUPHB",
                "journal_volume": "Test Value",
                "journal_year": "2022",
                "journal_issue": "Test Value",
                "journal_artid": "",
                "journal_fpage": "",
                "journal_lpage": "",
                "journal_doctype": "",
                "pubinfo_freetext": "",
                "another_field": "Test Another Field",
            },
            [
                {
                    "journal_title": "Nuclear Physics B",
                    "journal_volume": "Test Value",
                    "year": 2022,
                    "journal_issue": "Test Value",
                    "artid": "",
                    "page_start": "",
                    "page_end": "",
                    "material": "",
                    "pubinfo_freetext": "",
                }
            ],
            id="Test journal title NUPHB to Nuclear Physics B",
        ),
        param(
            {
                "journal_title": "PLB",
                "journal_volume": "Test Value",
                "journal_year": "2022",
                "journal_issue": "Test Value",
                "journal_artid": "",
                "journal_fpage": "",
                "journal_lpage": "",
                "journal_doctype": "",
                "pubinfo_freetext": "",
                "another_field": "Test Another Field",
            },
            [
                {
                    "journal_title": "Physics Letters B",
                    "journal_volume": "Test Value",
                    "year": 2022,
                    "journal_issue": "Test Value",
                    "artid": "",
                    "page_start": "",
                    "page_end": "",
                    "material": "",
                    "pubinfo_freetext": "",
                }
            ],
            id="Test journal title PLB to Physics Letters B",
        ),
        param(
            {
                "journal_title": "Test Value",
                "journal_volume": "Test Value",
                "journal_year": "2022",
                "journal_issue": "Test Value",
                "another_field": "Test Another Field",
            },
            [
                {
                    "journal_title": "Test Value",
                    "journal_volume": "Test Value",
                    "year": 2022,
                    "journal_issue": "Test Value",
                    "artid": "",
                    "page_start": "",
                    "page_end": "",
                    "material": "",
                    "pubinfo_freetext": "",
                }
            ],
            id="Some values missing",
        ),
        param(
            {
                "journal_title": "Test Value",
                "journal_volume": "Test Value",
                "journal_year": "2022",
                "journal_issue": "Test Value",
                "journal_artid": "Test Value",
                "journal_fpage": 1,
                "journal_lpage": 25,
                "journal_doctype": "Test Value",
                "pubinfo_freetext": "Test Value",
                "another_field": "Test Another Field",
            },
            [
                {
                    "journal_title": "Test Value",
                    "journal_volume": "Test Value",
                    "year": 2022,
                    "journal_issue": "Test Value",
                    "artid": "Test Value",
                    "page_start": 1,
                    "page_end": 25,
                    "material": "Test Value",
                    "pubinfo_freetext": "Test Value",
                }
            ],
            id="All values populated",
        ),
    ],
)
def test_publication_info(test_input, expected):
    assert expected == publication_info(test_input)


@mark.parametrize(
    "test_input, expected",
    [
        param(
            {"dois": ["test_doi_1"], "related_article_doi": ["test_doi_2"]},
            ["test_doi_1", "test_doi_2"],
            id="Both fields contain values",
        ),
        param(
            {"dois": ["test_doi_1"], "related_article_doi": []},
            ["test_doi_1"],
            id="Only dois contains values",
        ),
        param(
            {"dois": [], "related_article_doi": ["test_doi_2"]},
            ["test_doi_2"],
            id="Only related_article_doi contains values",
        ),
        param(
            {"dois": [], "related_article_doi": []},
            [],
            id="None contains values",
        ),
        param(
            {"dois": ["test_doi_1"]},
            ["test_doi_1"],
            id="related_article_doi is missing",
        ),
    ],
)
def test_merge_dois(test_input, expected):
    assert expected == merge_dois(test_input)


def test_clear_unnecessary_fields():
    article = {
        "journal_title": "Test Value",
        "journal_volume": "Test Value",
        "journal_year": "Test Value",
        "journal_issue": "Test Value",
        "journal_artid": "Test Value",
        "journal_fpage": "Test Value",
        "journal_lpage": "Test Value",
        "journal_doctype": "Test Value",
        "pubinfo_freetext": "Test Value",
        "related_article_doi": "Test Value",
    }
    assert {} == clear_unnecessary_fields(article)


def test_remove_empty_values():
    article = {
        "dict_full": {"key": "value"},
        "array_full": ["value"],
        "dict_half_empty": {
            "key": "value",
            "empty": None,
            "empty_array": [],
            "empty_dict": {},
        },
        "array_half_empty": [["value"], [], "test", {}],
        "empty_array": [],
        "empty_dict": [],
        "empty_value": None,
        "empty_nested_dicts": {"key": {"key": {"key": None}}},
    }
    assert {
        "dict_full": {"key": "value"},
        "array_full": ["value"],
        "dict_half_empty": {"key": "value"},
        "array_half_empty": [["value"], "test"],
    } == remove_empty_values(article)
