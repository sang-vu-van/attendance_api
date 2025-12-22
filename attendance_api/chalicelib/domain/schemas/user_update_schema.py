from marshmallow import Schema, fields, validate


class UserUpdateSchema(Schema):
    """
    PATCH: không bắt buộc gửi username
    nhưng nếu gửi thì phải đúng rule
    """

    username = fields.Str(required=False, validate=validate.Length(min=3, max=50))
