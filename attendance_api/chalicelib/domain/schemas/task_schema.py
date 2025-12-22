from marshmallow import Schema, fields, validate


class TaskCreateSchema(Schema):
    """
    POST /tasks
    """

    title = fields.Str(required=True, validate=validate.Length(min=1, max=150))
    detail = fields.Str(required=False, allow_none=True)
    project_id = fields.Int(required=True)
