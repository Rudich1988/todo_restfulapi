from flask_login import login_user, current_user

from task_manager.repositories.task_repository import TaskRepository
from task_manager.repositories.status_repository import StatusRepository
from task_manager.routes.schemas.task import TaskSchema
from task_manager.services.user_service import UserService



class TaskService:
    def __init__(self, session = TaskRepository(),
                 task_schema = TaskSchema(),
                 tasks_schema = TaskSchema(many=True)):
        self.session = session
        self._task_schema = task_schema
        self._tasks_schema = tasks_schema

    def get_all_tasks(self):
        tasks = self.session.get_all_tasks()
        return tasks
    
    def get_task(self, task_id):
        task = self.session.get_task(**{'id': task_id})
        return task
    
    def add_task(self, data):
        task_data = self._task_schema.dump(data)
        task_data['status_id'] = data['status']
        self.session.create_task(**task_data)
        return task_data
    
    def update_task(self, task_id, data):
        task_data = self._task_schema.dump(data)
        task_data['status_id'] = data['status']
        self.session.update_task(task_id, **task_data)
        return task_data
    
    def delete_task(self, task_id):
        self.session.delete_task(**{'id': task_id})
        return f'Task id: {task_id} deleted'
    
    def execute_task(self, task_id):
        #task = TaskRepository().get_task(**{'id': id})
        status = StatusRepository().get_status(**{'title': 'в работе'})
        self.update_task(task_id, {'status': status.id, 'executor': current_user.id})
        UserService().update_user(current_user.id, {'task_executor': task_id})
        return task_id

