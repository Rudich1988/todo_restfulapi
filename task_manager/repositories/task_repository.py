from task_manager.models.tasks import Task
from task_manager.app import db


class TaskRepository:
    def __init__(self, db_session=db.session):
        self.db_session = db_session

    def get_all_tasks(self):
        tasks = Task.query.all()
        return tasks

    def create_task(self, **kwargs):
        task = Task(**kwargs)
        self.db_session.add(task)
        self.db_session.commit()
        return task
    
    def get_task(self, task_id):
        task = Task.query.get_or_404(task_id)
        return task

    def update_task(self, task_id, **kwargs):
        task = self.get_task(task_id)
        for key, value in kwargs.items():
            setattr(task, key, value)
        self.db_session.commit()
        return task
    
    def delete_task(self, task_id):
        task = self.get_task(task_id)
        print(task)
        self.db_session.delete(task)
        self.db_session.commit()
