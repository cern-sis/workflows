import json

from utils import (
    build_countries_list_values,
    get_affiliations,
    get_authors,
    get_country_with_highest_gdp,
    get_most_important_country,
    get_primary_category,
)


def test_get_authors(shared_datadir):
    record = json.loads((shared_datadir / "record.json").read_text())
    expected_output = [
        {
            "full_name": "NNNN, SSSS",
            "surname": "NNNN",
            "affiliations": [{"country": "Japan", "value": "Department of Physics"}],
            "given_names": "Yuta",
        },
        {
            "full_name": "HHHH, OOOOO",
            "surname": "HHHH",
            "affiliations": [{"country": "Japan", "value": "Department of Physics"}],
            "given_names": "OOOOO",
            "email": "email.com",
        },
    ]
    assert get_authors(record) == expected_output


def test_get_primary_category(shared_datadir):
    expected = "hep-ph"
    record = json.loads((shared_datadir / "record.json").read_text())
    assert expected == get_primary_category(record)


def test_get_affiliations():
    authors = [
        {
            "affiliations": [
                {"country": "Japan", "value": "Department Example"},
                {"country": "Germany", "value": "Department Example"},
                {
                    "country": "HUMAN CHECK",
                },
            ],
        },
        {
            "affiliations": [
                {"country": "Japan", "value": "Department Example"},
                {"value": "Department Example"},
                {"country": "Palestine", "value": "Department Example"},
            ],
        },
    ]
    expected = [
        ["Japan", "Germany", "UNKNOWN"],
        ["Japan", "UNKNOWN", "West Bank and Gaza"],
    ]
    assert expected == get_affiliations(authors)


def test_get_country_with_highest_gdp():
    countries = ["Japan", "UNKNOWN", "Germany"]
    gdps = {"Japan": "1", "UNKNOWN": "0", "Germany": "2"}
    assert "Germany" == get_country_with_highest_gdp(countries, gdps)


def test_get_most_important_country():
    gdps = {
        "Japan": "1",
        "UNKNOWN": "0",
        "Germany": "2",
        "Lithuania": "1",
        "Greece": "1",
    }
    countries = ["Japan", "UNKNOWN", "Germany", "Lithuania", "Greece"]
    assert "Germany" == get_most_important_country(countries, gdps)
    countries = ["Japan", "UNKNOWN", "Germany", "Lithuania", "Greece", "KEK"]
    assert "Japan" == get_most_important_country(countries, gdps)
    countries = ["Japan", "UNKNOWN", "Germany", "Lithuania", "Greece", "KEK", "DESY"]
    assert "Germany" == get_most_important_country(countries, gdps)
    countries = [
        "Japan",
        "UNKNOWN",
        "Germany",
        "Lithuania",
        "Greece",
        "KEK",
        "DESY",
        "CERN",
    ]
    assert "CERN" == get_most_important_country(countries, gdps)
    countries = ["UNKNOWN"]
    assert "UNKNOWN" == get_most_important_country(countries, gdps)


def test_build_countries_list_values():
    countries = [
        "Japan",
        "UNKNOWN",
        "UNKNOWN",
        "Germany",
        "Lithuania",
        "Latvia",
        "Greece",
        "CERN",
        "Finland",
        "RANDOM",
    ]
    all_countires = [
        "Japan",
        "UNKNOWN",
        "Germany",
        "Lithuania",
        "Greece",
        "CERN",
        "Pseudo Country 1",
        "Pseudo Country 2",
        "Latvia",
        "Finland",
    ]
    assert build_countries_list_values(countries, all_countires) == [
        10.0,
        30.0,
        10.0,
        10.0,
        10.0,
        10.0,
        0.0,
        0.0,
        10.0,
        10.0,
    ]
