from common.parsing.generic_parsing import (
    classification_numbers,
    collapse_initials,
    fix_publication_date,
    free_keywords,
    join,
    list_to_value_dict,
    parse_authors,
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
def test_parse_authors(test_input, expected):
    assert expected == parse_authors(test_input)
