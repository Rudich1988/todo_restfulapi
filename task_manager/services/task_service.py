from flask_login import login_user, current_user

from task_manager.repositories.task_repository import TaskRepository
from task_manager.repositories.status_repository import StatusRepository
from task_manager.routes.schemas.task import TaskSchema
from task_manager.services.user_service import UserService
from task_manager.db import db_session



class TaskService:
    def __init__(self, repository=TaskRepository,
                 session=db_session,
                 task_schema=TaskSchema(),
                 tasks_schema=TaskSchema(many=True)):
        self.repository = repository
        self.session = db_session
        self._task_schema = task_schema
        self._tasks_schema = tasks_schema

    def get_all_tasks(self):
        with self.session() as s:
            tasks = self.repository(s).get_all_tasks()
        return tasks
    
    def get_task(self, task_id):
        with self.session() as s:
            task = self.repository(s).get_task(**{'id': task_id})
        return task
    
    def add_task(self, data):
        task_data = self._task_schema.dump(data)
        task_data['status_id'] = data['status']
        with self.session as s:
            self.repository(s).create_task(**task_data)
        return task_data
    
    def update_task(self, task_id, data):
        task_data = self._task_schema.dump(data)
        task_data['status_id'] = data['status']
        with self.session() as s:
            self.repository(s).update_task(task_id, **task_data)
        return task_data
    
    def delete_task(self, task_id):
        with self.session() as s:
            self.repository(s).delete_task(**{'id': task_id})
        return f'Task id: {task_id} deleted'
    
    def execute_task(self, task_id):
        #task = TaskRepository().get_task(**{'id': id})
        with self.session() as s:
            status = StatusRepository(s).get_status(**{'title': 'в работе'})
        self.update_task(task_id, {'status': status.id, 'executor': current_user.id})
        UserService().update_user(current_user.id, {'task_executor': task_id})
        return task_id

