from common.constants import COUNTRY_PARSING_PATTERN, ORGANIZATION_PARSING_PATTERN

affiliation_string = (
    "Department of Physics, University of Oregon, Eugene, Oregon 97403, USA"
)


def test_country_regex():
    assert "USA" == COUNTRY_PARSING_PATTERN.search(affiliation_string).group(0)


def test_organization_regex():
    assert (
        "Department of Physics, University of Oregon, Eugene, Oregon 97403"
        == ORGANIZATION_PARSING_PATTERN.sub("", affiliation_string)
    )
