import pytest
from common.cleanup import clean_whitespace_characters

expected_string = "Simple input with spaces"
string = " Simple input with spaces "
string_with_double_spaces = " Simple   input   with    spaces "
string_with_new_lines = " Simple   input  \n  with  \n spaces "


@pytest.mark.parametrize(
    "test_input, expected",
    [
        pytest.param(string, expected_string, id="test_clean_whitespace_characters"),
        pytest.param(
            string_with_double_spaces,
            expected_string,
            id="test_clean_whitespace_characters_double_spaces",
        ),
        pytest.param(
            string_with_new_lines,
            expected_string,
            id="test_clean_whitespace_characters_with_new_lines",
        ),
    ],
)
def test_clean_whitespace_characters(test_input, expected):
    output = clean_whitespace_characters(test_input)
    assert output == expected
