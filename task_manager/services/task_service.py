from datetime import datetime as dt

from marshmallow import ValidationError

from task_manager.repositories.task_repository import TaskRepository
from task_manager.routes.schemas.task import TaskSchema



class TaskService:
    def __init__(self, session = TaskRepository(),
                 task_schema = TaskSchema(),
                 tasks_schema = TaskSchema(many=True)):
        self.session = session
        self._task_schema = task_schema
        self._tasks_schema = tasks_schema

    def get_all_tasks(self):
        tasks = self.session.get_all_tasks()
        return self._tasks_schema.dump(tasks)
    
    def get_task(self, task_id):
        task = self.session.get_task(**{'id': task_id})
        return self._task_schema.dump(task)
    
    def add_task(self, data):
        task_data = self._task_schema.dump(data)
        self.session.create_task(**task_data)
        return data
    
    def update_task(self, task_id, data):
        task_data = self._task_schema.dump(data)
        task = self.session.update_task(task_id, **task_data)
        return self._task_schema.dump(task)
    
    def delete_task(self, task_id):
        self.session.delete_task(**{'id': task_id})
        return f'Task id: {task_id} deleted'
