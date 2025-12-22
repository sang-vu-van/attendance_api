from marshmallow import Schema, fields, validate


class ProjectCreateSchema(Schema):
    """
    #POST /projects
    """

    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    owner_id = fields.Int(required=True)
