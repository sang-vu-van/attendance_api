from marshmallow import Schema, fields, validate


class TaskUpdateSchema(Schema):
    """
    tasks/{id}
    """

    title = fields.Str(required=False, validate=validate.Length(min=1, max=150))
    detail = fields.Str(required=False, allow_none=True)
