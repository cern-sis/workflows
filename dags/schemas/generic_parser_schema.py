from marshmallow import Schema, fields
from schemas.parser_schema import Affiliations, Author, License, ValueDict


class ClassificationNumber(Schema):
    classification_number = fields.Str(required=True)
    standard = fields.Str(required=True)


class Collection(Schema):
    primary = fields.Str(required=True)


class FreeKeyword(Schema):
    source = fields.Str(required=True)
    value = fields.Str(required=True)


class ThesisSupervisor(Schema):
    affiliations = fields.List(fields.Nested(Affiliations()), required=True)
    full_name = fields.Str(required=True)


class PublicationInfo(Schema):
    artid = fields.Str(required=True)
    journal_issue = fields.Str(required=True)
    journal_title = fields.Str(required=True)
    journal_volume = fields.Str(required=True)
    material = fields.Str(required=True)
    page_end = fields.Str(required=True)
    page_start = fields.Str(required=True)
    year = fields.Int(required=True)


class GenericParserSchema(Schema):
    abstract = fields.Str(required=True)
    arxiv_eprints = fields.List(fields.Nested(ValueDict()), required=True)
    authors = fields.List(fields.Nested(Author()), required=True)
    classification_numbers = fields.List(
        fields.Nested(ClassificationNumber()), required=True
    )
    collaborations = fields.List(fields.Nested(ValueDict()), required=True)
    collections = fields.List(fields.Nested(Collection()), required=True)
    control_field = fields.Str(required=True)
    copyright_holder = fields.Str(required=True)
    copyright_year = fields.Str(required=True)
    date_published = fields.Date(required=True)
    dois = fields.List(fields.Nested(ValueDict()), required=True)
    free_keywords = fields.List(fields.Nested(FreeKeyword()), required=True)
    license = fields.List(fields.Nested(License()), required=True)
    local_files = fields.List(fields.Nested(ValueDict()), required=True)
    page_nr = fields.List(fields.Int(required=True))
    publication_info = fields.List(fields.Nested(PublicationInfo()), required=True)
    thesis = fields.Str(required=True)
    thesis_supervisor = fields.List(fields.Nested(ThesisSupervisor()), required=True)
    title = fields.Str(required=True)
    urls = fields.List(fields.Nested(ValueDict()), required=True)
