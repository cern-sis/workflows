import pytest
from common.cleanup import (
    clean_collaboration,
    clean_whitespace_characters,
    convert_html_subsripts_to_latex,
)

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
    assert clean_whitespace_characters(test_input) == expected


expected_string_sup = "$^{3}$"
sup = "<sup>3</sup>"
expected_string_sub = "$_{3}$"
sub = "<sub>3</sub>"
expected_string_inf = "$_{3}$"
inf = "<inf>3</inf>"

expected_string_sup_extended = (
    '<p content-type="scoap3">Article funded by SCOAP$^{3}$</p>'
)
sup_extended = '<p content-type="scoap3">Article funded by SCOAP<sup>3</sup></p>'
expected_string_sub_extended = (
    '<p content-type="scoap3">Article funded by SCOAP$_{3}$</p>'
)
sub_extended = '<p content-type="scoap3">Article funded by SCOAP<sub>3</sub></p>'
expected_string_inf_extended = (
    '<p content-type="scoap3">Article funded by SCOAP$_{3}$</p>'
)
inf_extended = '<p content-type="scoap3">Article funded by SCOAP<inf>3</inf></p>'

no_tags = '<p content-type="scoap3">Article funded by SCOAP</p>'


@pytest.mark.parametrize(
    "test_input, expected",
    [
        pytest.param(
            sup, expected_string_sup, id="test_convert_html_subsripts_to_latex_sup"
        ),
        pytest.param(
            sub, expected_string_sub, id="test_convert_html_subsripts_to_latex_sub"
        ),
        pytest.param(
            inf, expected_string_inf, id="test_convert_html_subsripts_to_latex_inf"
        ),
        pytest.param(
            sup_extended,
            expected_string_sup_extended,
            id="test_convert_html_subsripts_to_latex_sup_extended",
        ),
        pytest.param(
            sub_extended,
            expected_string_sub_extended,
            id="test_convert_html_subsripts_to_latex_sub_extended",
        ),
        pytest.param(
            inf_extended,
            expected_string_inf_extended,
            id="test_convert_html_subsripts_to_latex_inf_extended",
        ),
        pytest.param(
            no_tags, no_tags, id="test_convert_html_subsripts_to_latex_no_tags"
        ),
    ],
)
def test_convert_html_subsripts_to_latex(test_input, expected):
    assert convert_html_subsripts_to_latex(test_input) == expected


collaboration_string = (
    "Kavli Institute for the Physics and Mathematics of the Universe (WPI)"
)
collaboration_string_with_two_spaces = (
    "Kavli Institute for the  Physics and Mathematics of the Universe (WPI)"
)

collaboration_string_cleaned = (
    "Kavli Institute Physics and Mathematics of the Universe (WPI)"
)


@pytest.mark.parametrize(
    "test_input, expected",
    [
        pytest.param(
            collaboration_string,
            collaboration_string_cleaned,
            id="test_collaboration_string",
        ),
        pytest.param(
            collaboration_string_with_two_spaces,
            collaboration_string_cleaned,
            id="test_collaboration_string_with_two_spaces",
        ),
        pytest.param(
            collaboration_string_cleaned,
            collaboration_string_cleaned,
            id="test_collaboration_string_with_cleaned_value",
        ),
    ],
)
def test_clean_collaboration(test_input, expected):
    assert clean_collaboration(test_input) == expected
