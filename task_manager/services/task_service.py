from datetime import datetime as dt

from marshmallow import ValidationError

from task_manager.repositories.task_repository import TaskRepository
from task_manager.routes.schemas.task import TaskSchema, TaskAutoSchema



class TaskService:
    def __init__(self, session = TaskRepository(),
                 task_schema = TaskSchema(),
                 tasks_schema = TaskAutoSchema(many=True)):
        self.session = session
        self._task_schema = task_schema
        self._tasks_schema = tasks_schema

    def get_all_tasks(self):
        tasks = self.session.get_all_tasks()
        return self._tasks_schema.dump(tasks)
    
    def get_task(self, task_id):
        try:
            task = self.session.get_task(task_id)
        except:
            raise ValidationError
        return self._task_schema.dump(task)
    
    def add_task(self, data):
        try:          
            validated_data = self._task_schema.load(data)
            task = self.session.create_task(**validated_data)
        except:
            raise ValidationError
        return self._task_schema.dump(task)
    
    def update_task(self, task_id, data):
        try: 
            validate_data = self._task_schema.load(data)
            task = self.session.update_task(task_id, **validate_data)
        except:
            raise ValidationError
        return self._task_schema.dump(task)
    
    def delete_task(self, task_id):
        try:
            self.session.delete_task(task_id)
        except:
            raise ValidationError
        return f'Task id: {task_id} deleted'
