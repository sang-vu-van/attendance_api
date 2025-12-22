from marshmallow import Schema, fields, validate


class UserCreateSchema(Schema):
    """
    POST /users
    """

    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
