import pytest
from common.cleanup import (
    clean_affiliation_for_author,
    clean_all_affiliations_for_author,
    clean_collaboration,
    clean_whitespace_characters,
    convert_html_subsripts_to_latex,
    remove_specific_tags)
from common.mappings import MATHML_ELEMENTS


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

    
xml = "<div><p>example<h1> h1 example</h1></p></div>"
xml_just_p = "<p>example h1 example</p>"
xml_just_div = "<div>example h1 example</div>"
xml_div_and_h1 = "<div>example<h1> h1 example</h1></div>"
xml_title = "<article-title id='1'><label>example</label></article-title>"
xml_just_title = "<article-title>example</article-title>"
xml_just_title_with_id = '<article-title id="1">example</article-title>'


@pytest.mark.parametrize(
    "test_input, expected, tags, attributes",
    [
        pytest.param(xml, xml_just_p, ["p"], [], id="test_keep_p"),
        pytest.param(xml, xml_just_div, ["div"], [], id="test_keep_div"),
        pytest.param(xml, xml_div_and_h1, ["div", "h1"], [], id="test_keep_div_and_h1"),
        pytest.param(
            xml_title, xml_just_title, ["article-title"], [], id="test_keep_just_title"
        ),
        pytest.param(
            xml_title,
            xml_just_title_with_id,
            ["article-title"],
            ["id"],
            id="test_keep_just_title_with_id",
        ),
    ],
)
def test_remove_specific_tags(test_input, expected, tags, attributes):
    assert (
        remove_specific_tags(test_input, tags=tags, attributes=attributes) == expected
    )

def test_remove_specific_tags_with_mathML(shared_datadir):
    file_with_mathML = (shared_datadir / "file_with_mathML.xml").read_text()
    cleaned_file_with_mathML = (
        shared_datadir / "cleaned_file_with_mathML.xml"
    ).read_text()
    output = remove_specific_tags(file_with_mathML, tags=MATHML_ELEMENTS)
    assert clean_whitespace_characters(output) == clean_whitespace_characters(
        cleaned_file_with_mathML
    )


xml_with_label = "<aff>Affiliation<label>Label</label><aff/>"
xml_with_label_and_spaces = "<aff>  Affiliation  <label>La bel </label><aff/>"
xml_no_label = "<aff>Affiliation<sup>1</sup><aff/>"
just_label = "<label>Label</label>"

xml_no_label_expected_value = "Affiliation1"
expected_output = "Affiliation"
expected_value_just_label = ""


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


@pytest.mark.parametrize(
    "test_input, expected",
    [
        pytest.param(
            xml_with_label,
            expected_output,
            id="test_clean_tags_from_affiliations_for_author",
        ),
        pytest.param(
            xml_with_label_and_spaces,
            expected_output,
            id="test_clean_tags_from_affiliations_for_author_with_spaces",
        ),
        pytest.param(
            xml_no_label,
            xml_no_label_expected_value,
            id="test_clean_tags_from_affiliations_for_author_no_label",
        ),
        pytest.param(
            just_label,
            expected_value_just_label,
            id="test_clean_tags_from_affiliations_for_author_just_label",
        ),
    ],
)
def test_clean_affiliation_for_author(test_input, expected):
    assert clean_affiliation_for_author(test_input) == expected


affiliations = [
    {"value": xml_with_label},
    {"value": xml_with_label_and_spaces},
    {"value": xml_no_label},
    {"value": just_label},
]
test_object = {"affiliations": affiliations}

expected_affiliations = [
    {"value": expected_output},
    {"value": expected_output},
    {"value": xml_no_label_expected_value},
    {"value": expected_value_just_label},
]
exptected_test_object = {"affiliations": expected_affiliations}

empty = {"affiliations": []}


@pytest.mark.parametrize(
    "test_input, expected",
    [
        pytest.param(
            test_object,
            exptected_test_object,
            id="test_clean_affiliations_for_author",
        ),
        pytest.param(
            empty,
            empty,
            id="test_clean_empty_affiliations_for_author",
        ),
    ],
)
def test_clean_all_affiliations_for_author(test_input, expected):
    assert clean_all_affiliations_for_author(test_input) == expected
