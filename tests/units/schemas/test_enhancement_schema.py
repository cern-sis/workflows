import json

import pytest
from schemas.enhancement_schema import EnhancementSchema


@pytest.mark.parametrize(
    "file_name, expected",
    [
        pytest.param(
            "correct.json", {}, id="test_enhancement_schema_with_correct_input"
        ),
        pytest.param(
            "missing_fields.json",
            {
                "abstracts": ["Missing data for required field."],
                "imprints": ["Missing data for required field."],
            },
            id="test_enhancement_schema_with_missing_fields",
        ),
        pytest.param(
            "empty.json",
            {
                "abstracts": ["Missing data for required field."],
                "acquisition_source": ["Missing data for required field."],
                "copyright": ["Missing data for required field."],
                "imprints": ["Missing data for required field."],
                "record_creation_date": ["Missing data for required field."],
                "titles": ["Missing data for required field."],
            },
            id="test_enhancement_schema_with_empty_json",
        ),
    ],
)
def test_enhancement_schema(file_name, expected, shared_datadir):
    file = (shared_datadir / "test_enchancement_schema" / file_name).read_text()
    validation = EnhancementSchema().validate(json.loads(file))
    assert validation == expected
