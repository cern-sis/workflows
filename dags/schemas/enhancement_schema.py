from marshmallow import Schema, fields


class Abstracts(Schema):
    value = fields.Str(
        required=True, error_messages={"required": "Value in abstracts is required"}
    )
    source = fields.Str(
        required=True, error_messages={"required": "Source in abstracts is required"}
    )


class AquisitionSource(Schema):
    source = fields.Str(
        required=True,
        error_messages={"required": "Source in aquisition source is required"},
    )
    method = fields.Str(
        required=True,
        error_messages={"required": "Method in aquisition source is required"},
    )
    date = fields.DateTime(
        required=True,
        error_messages={"required": "Date in aquisition source is required"},
    )
    submission_number = fields.Str(
        required=True,
        error_messages={
            "required": "Submission number in aquisition source is required"
        },
    )


class CopyRight(Schema):
    holder = fields.Str(
        required=True,
        error_messages={"required": "Holder in copy right source is required"},
    )
    year = fields.Int(
        required=True,
        error_messages={"required": "Year in copy right source is required"},
    )
    statement = fields.Str(
        required=True,
        error_messages={"required": "Statement in copy right source is required"},
    )
    material = fields.Str(
        required=True,
        error_messages={"required": "Material in copy right source is required"},
    )


class Imprints(Schema):
    date = fields.Date(
        required=True,
        error_messages={"required": "Date in imprints source is required"},
    )
    publisher = fields.Str(
        required=True,
        error_messages={"required": "Date in imprints source is required"},
    )


class Titles(Schema):
    title = fields.Str(
        required=True, error_messages={"required": "Tile in titles source is required"}
    )
    subtitle = fields.Str(
        required=True,
        error_messages={"required": "Subtitle in subtitle source is required"},
    )
    source = fields.Str(
        required=True,
        error_messages={"required": "Source in titles source is required"},
    )


class EnhancementSchema(Schema):
    abstracts = fields.List(fields.Nested(Abstracts()), required=True)
    acquisition_source = fields.Nested(AquisitionSource(), required=True)
    copyright = fields.List(fields.Nested(CopyRight()), required=True)
    imprints = fields.List(fields.Nested(Imprints()), required=True)
    record_creation_date = fields.DateTime(required=True)
    titles = fields.List(fields.Nested(Titles()), required=True)
