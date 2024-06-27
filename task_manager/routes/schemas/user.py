from task_manager.models.users import User
from marshmallow import Schema, validate, fields


class UserRegistrationSchema(Schema):
    id = fields.Int()
    first_name = fields.Str(required=True, validate=validate.Length(min=1))
    last_name = fields.Str(required=True, validate=validate.Length(min=1))
    username = fields.Str(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=1))
    created_at = fields.DateTime(required=False)
    updated_at = fields.DateTime(required=False)


class UserLoginSchema(Schema):
    pass