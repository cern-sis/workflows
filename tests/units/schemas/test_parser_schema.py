import json

import pytest
from schemas.parser_schema import ParserSchema


@pytest.mark.parametrize(
    "file_name, expected",
    [
        pytest.param("correct.json", {}, id="test_parser_schema_with_correct_input"),
        pytest.param(
            "missing_fields.json",
            {
                "abstract": ["Missing data for required field."],
                "title": ["Missing data for required field."],
                "authors": ["Missing data for required field."],
            },
            id="test_parser_schema_with_missing_fields",
        ),
        pytest.param(
            "empty.json",
            {
                "journal_doctype": ["Missing data for required field."],
                "dois": ["Missing data for required field."],
                "arxiv_eprints": ["Missing data for required field."],
                "page_nr": ["Missing data for required field."],
                "abstract": ["Missing data for required field."],
                "title": ["Missing data for required field."],
                "classification_numbers": ["Missing data for required field."],
                "authors": ["Missing data for required field."],
                "collaborations": ["Missing data for required field."],
                "journal_title": ["Missing data for required field."],
                "journal_issue": ["Missing data for required field."],
                "journal_volume": ["Missing data for required field."],
                "journal_artid": ["Missing data for required field."],
                "journal_fpage": ["Missing data for required field."],
                "journal_lpage": ["Missing data for required field."],
                "journal_year": ["Missing data for required field."],
                "date_published": ["Missing data for required field."],
                "related_article_doi": ["Missing data for required field."],
                "copyright_holder": ["Missing data for required field."],
                "copyright_year": ["Missing data for required field."],
                "license": ["Missing data for required field."],
                "collections": ["Missing data for required field."],
                "control_field": ["Missing data for required field."],
                "free_keywords": ["Missing data for required field."],
                "thesis_supervisor": ["Missing data for required field."],
                "thesis": ["Missing data for required field."],
                "urls": ["Missing data for required field."],
                "local_files": ["Missing data for required field."],
            },
            id="test_parser_schema_with_empty_obj",
        ),
    ],
)
def test_generic_parser_schema(file_name, expected, shared_datadir):
    file = (shared_datadir / "test_parser_schema" / file_name).read_text()
    validation = ParserSchema().validate(json.loads(file))
    assert validation == expected
