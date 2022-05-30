from marshmallow import Schema, fields


class ValueDict(Schema):
    value = fields.Str(required=True)


class Affiliations(Schema):
    value = fields.Str(required=True)
    organization = fields.Str(required=True)
    country = fields.Str(required=True)


class Author(Schema):
    surname = fields.Str(required=True)
    given_names = fields.Str(required=True)
    email = fields.Str(required=True)
    affiliations = fields.List(fields.Nested(Affiliations()))
    full_name = fields.Str(required=True)


class License(Schema):
    license = fields.Str(required=True)
    url = fields.Str(required=True)


class ParserSchema(Schema):
    journal_doctype = fields.Str(required=True)
    dois = fields.List(fields.Str(), required=True)
    arxiv_eprints = fields.List(fields.Nested(ValueDict()), required=True)
    page_nr = fields.List(fields.Int(), required=True)
    abstract = fields.Str(required=True)
    title = fields.Str(required=True)
    classification_numbers = fields.List(fields.Str(), required=True)
    authors = fields.List(fields.Nested(Author()), required=True)
    collaborations = fields.List(fields.Str(), required=True)
    journal_title = fields.Str(required=True)
    journal_issue = fields.Str(required=True)
    journal_volume = fields.Str(required=True)
    journal_artid = fields.Str(required=True)
    journal_fpage = fields.Str(required=True)
    journal_lpage = fields.Str(required=True)
    journal_year = fields.Int(required=True)
    date_published = fields.Date(required=True)
    related_article_doi = fields.List(fields.Str(), required=True)
    copyright_holder = fields.Str(required=True)
    # Really copy right year is a string?
    copyright_year = fields.Str(required=True)
    license = fields.List(fields.Nested(License()), required=True)
    collections = fields.List(fields.Str(), required=True)
    control_field = fields.List(fields.Str(), required=True)
    free_keywords = fields.List(fields.Str(), required=True)
    # is thesis supervisor really the same as author?
    thesis_supervisor = fields.List(fields.Nested(Author()), required=True)
    thesis = fields.List(fields.Str(), required=True)
    urls = fields.List(fields.Str(), required=True)
    local_files = fields.List(fields.Str(), required=True)
