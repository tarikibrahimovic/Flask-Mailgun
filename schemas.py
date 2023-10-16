from marshmallow import Schema, fields, validate


class PlainUserSchema(Schema):
    email = fields.Email(data_key="email", required=True)
    password = fields.Str(data_key="password", required=True, validate=validate.Length(min=1, max=30))


class RegisterSchema(PlainUserSchema):
    username = fields.Str(data_key="username", required=True, validate=validate.Length(min=1, max=64))


class VerifySchema(PlainUserSchema):
    verified = fields.Str(data_key="verified", required=True, validate=validate.Length(min=1, max=6))
