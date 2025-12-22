from marshmallow import Schema, fields, validate


class ProjectUpdateSchema(Schema):
    """
    PATCH /projects/{id}
    """

    name = fields.Str(required=False, validate=validate.Length(min=1, max=100))
