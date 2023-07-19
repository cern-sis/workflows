import pytest
from common.enhancer import Enhancer
from freezegun import freeze_time

publisher = "Springer"

generic_pseudo_parser_output = {
    "abstract": "this is abstracts",
    "copyright_holder": "copyright_holder",
    "copyright_year": "2020",
    "copyright_statement": "copyright_statement",
    "copyright_material": "copyright_material",
    "date_published": "2022-05-20",
    "title": "title",
    "subtitle": "subtitle",
}


expected_output = {
    "abstracts": [{"value": "this is abstracts", "source": publisher}],
    "acquisition_source": {
        "source": publisher,
        "method": publisher,
        "date": "2022-05-20T00:00:00",
    },
    "copyright": [
        {
            "holder": "copyright_holder",
            "year": "2020",
            "statement": "copyright_statement",
            "material": "copyright_material",
        }
    ],
    "imprints": [{"date": "2022-05-20", "publisher": publisher}],
    "record_creation_date": "2022-05-20T00:00:00",
    "titles": [{"title": "title", "subtitle": "subtitle", "source": publisher}],
}

empty_generic_pseudo_parser_output = {
    "abstract": "",
    "copyright_holder": "",
    "copyright_year": "",
    "copyright_statement": "",
    "copyright_material": "",
    "date_published": "",
    "title": "",
    "subtitle": "",
}


expected_output_from_empty_input = {
    "abstracts": [{"value": "", "source": publisher}],
    "acquisition_source": {
        "source": publisher,
        "method": publisher,
        "date": "2022-05-20T00:00:00",
    },
    "copyright": [{"holder": "", "year": "", "statement": "", "material": ""}],
    "imprints": [{"date": "", "publisher": publisher}],
    "record_creation_date": "2022-05-20T00:00:00",
    "titles": [{"title": "", "subtitle": "", "source": publisher}],
}
input_with_affiliation_of_cooperation_agreement_with_CERN = {
    "abstract": "this is abstracts",
    "authors": [
        {
            "affiliations": [
                {
                    "country": "Switzerland",
                    "organization": "International laboratory covered by a cooperation agreement with CERN",
                    "value": "International laboratory covered by a cooperation agreement with CERN, Geneva, Switzerland",
                }
            ],
            "email": "test@email.com",
            "full_name": "Test Surname, Test names",
            "given_names": "Test names",
            "surname": "Test Surname",
            "orcid": "Test Id",
        }
    ],
    "copyright_holder": "copyright_holder",
    "copyright_year": "2020",
    "copyright_statement": "copyright_statement",
    "copyright_material": "copyright_material",
    "date_published": "2022-05-20",
    "title": "title",
    "subtitle": "subtitle",
}
input_with_affiliation_of_cooperation_agreement_with_CERN_no_country = {
    "abstract": "this is abstracts",
    "authors": [
        {
            "affiliations": [
                {
                    "organization": "International laboratory covered by a cooperation agreement with CERN",
                    "value": "International laboratory covered by a cooperation agreement with CERN, Geneva, Switzerland",
                }
            ],
            "email": "test@email.com",
            "full_name": "Test Surname, Test names",
            "given_names": "Test names",
            "surname": "Test Surname",
            "orcid": "Test Id",
        }
    ],
    "copyright_holder": "copyright_holder",
    "copyright_year": "2020",
    "copyright_statement": "copyright_statement",
    "copyright_material": "copyright_material",
    "date_published": "2022-05-20",
    "title": "title",
    "subtitle": "subtitle",
}
expected_output_with_affiliation_of_cooperation_agreement_with_CERN = {
    "abstracts": [{"value": "this is abstracts", "source": publisher}],
    "authors": [
        {
            "affiliations": [
                {
                    "organization": "International laboratory covered by a cooperation agreement with CERN",
                    "value": "International laboratory covered by a cooperation agreement with CERN, Geneva, Switzerland",
                }
            ],
            "email": "test@email.com",
            "full_name": "Test Surname, Test names",
            "given_names": "Test names",
            "surname": "Test Surname",
            "orcid": "Test Id",
        }
    ],
    "acquisition_source": {
        "source": publisher,
        "method": publisher,
        "date": "2022-05-20T00:00:00",
    },
    "copyright": [
        {
            "holder": "copyright_holder",
            "year": "2020",
            "statement": "copyright_statement",
            "material": "copyright_material",
        }
    ],
    "imprints": [{"date": "2022-05-20", "publisher": publisher}],
    "record_creation_date": "2022-05-20T00:00:00",
    "titles": [{"title": "title", "subtitle": "subtitle", "source": publisher}],
}

input_with_correct_affiliation = {
    "abstract": "this is abstracts",
    "authors": [
        {
            "affiliations": [
                {
                    "country": "Switzerland",
                    "organization": "CERN",
                    "value": "CERN, Geneva, Switzerland",
                }
            ],
            "email": "test@email.com",
            "full_name": "Test Surname, Test names",
            "given_names": "Test names",
            "surname": "Test Surname",
            "orcid": "Test Id",
        }
    ],
    "copyright_holder": "copyright_holder",
    "copyright_year": "2020",
    "copyright_statement": "copyright_statement",
    "copyright_material": "copyright_material",
    "date_published": "2022-05-20",
    "title": "title",
    "subtitle": "subtitle",
}
output_with_correct_affiliation = {
    "abstracts": [{"value": "this is abstracts", "source": publisher}],
    "authors": [
        {
            "affiliations": [
                {
                    "country": "Switzerland",
                    "organization": "CERN",
                    "value": "CERN, Geneva, Switzerland",
                }
            ],
            "email": "test@email.com",
            "full_name": "Test Surname, Test names",
            "given_names": "Test names",
            "surname": "Test Surname",
            "orcid": "Test Id",
        }
    ],
    "acquisition_source": {
        "source": publisher,
        "method": publisher,
        "date": "2022-05-20T00:00:00",
    },
    "copyright": [
        {
            "holder": "copyright_holder",
            "year": "2020",
            "statement": "copyright_statement",
            "material": "copyright_material",
        }
    ],
    "imprints": [{"date": "2022-05-20", "publisher": publisher}],
    "record_creation_date": "2022-05-20T00:00:00",
    "titles": [{"title": "title", "subtitle": "subtitle", "source": publisher}],
}


@pytest.mark.parametrize(
    "test_input, expected, publisher",
    [
        pytest.param(generic_pseudo_parser_output, expected_output, publisher),
        pytest.param(
            empty_generic_pseudo_parser_output,
            expected_output_from_empty_input,
            publisher,
        ),
        pytest.param(
            input_with_affiliation_of_cooperation_agreement_with_CERN,
            expected_output_with_affiliation_of_cooperation_agreement_with_CERN,
            publisher,
        ),
        pytest.param(
            input_with_correct_affiliation, output_with_correct_affiliation, publisher
        ),
        pytest.param(
            input_with_affiliation_of_cooperation_agreement_with_CERN_no_country,
            expected_output_with_affiliation_of_cooperation_agreement_with_CERN,
            publisher,
        ),
    ],
)
@freeze_time("2022-05-20")
def test_all_contructors(test_input, expected, publisher):
    enhancement = Enhancer()
    enhanced = enhancement(item=test_input, publisher=publisher)
    assert enhanced == expected
