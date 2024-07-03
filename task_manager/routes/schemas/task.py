#from task_manager.app import ma
from task_manager.models.tasks import Task
from marshmallow import Schema, validate, fields


class TaskSchema(Schema):
    id = fields.Int()
    title = fields.Str(required=False, validate=validate.Length(min=1))
    description = fields.Str(required=False)
    created_at = fields.DateTime(required=False)
    updated_at = fields.DateTime(required=False)
    author = fields.Integer()
    executor = fields.Integer(required=False)


#class TaskAutoSchema(ma.SQLAlchemyAutoSchema):
#    class Meta:
#        model = Task
    
