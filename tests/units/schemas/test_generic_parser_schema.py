import json

import pytest
from schemas.generic_parser_schema import GenericParserSchema


@pytest.mark.parametrize(
    "file_name, expected",
    [
        pytest.param(
            "correct.json", {}, id="test_generic_parser_schema_with_correct_input"
        ),
        pytest.param(
            "missing_fields.json",
            {
                "abstract": ["Missing data for required field."],
                "authors": ["Missing data for required field."],
            },
            id="test_generic_parser_schema_with_missing_fields",
        ),
        pytest.param(
            "empty.json",
            {
                "abstract": ["Missing data for required field."],
                "arxiv_eprints": ["Missing data for required field."],
                "authors": ["Missing data for required field."],
                "classification_numbers": ["Missing data for required field."],
                "collaborations": ["Missing data for required field."],
                "collections": ["Missing data for required field."],
                "control_field": ["Missing data for required field."],
                "copyright_holder": ["Missing data for required field."],
                "copyright_year": ["Missing data for required field."],
                "date_published": ["Missing data for required field."],
                "dois": ["Missing data for required field."],
                "free_keywords": ["Missing data for required field."],
                "license": ["Missing data for required field."],
                "local_files": ["Missing data for required field."],
                "publication_info": ["Missing data for required field."],
                "thesis": ["Missing data for required field."],
                "thesis_supervisor": ["Missing data for required field."],
                "title": ["Missing data for required field."],
                "urls": ["Missing data for required field."],
            },
            id="test_generic_parser_schema_with_empty_json",
        ),
    ],
)
def test_generic_parser_schema(file_name, expected, shared_datadir):
    file = (shared_datadir / "test_generic_parser_schema" / file_name).read_text()
    validation = GenericParserSchema().validate(json.loads(file))
    assert validation == expected
