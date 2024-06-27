from task_manager.models.tasks import Task
from task_manager.db import Session


class TaskRepository:
    def __init__(self, db_session=Session()):
        self.db_session = db_session

    def get_all_tasks(self):
        tasks = self.db_session.query(Task).all()
        return tasks

    def create_task(self, **kwargs):
        task = Task(**kwargs)
        self.db_session.add(task)
        self.db_session.commit()

    def get_task(self, **kwargs):
        task = self.db_session.query(Task).filter_by(**kwargs)[0]
        return task
    
    def update_task(self, task_id, **kwargs):
        task = self.get_task(**{'id': task_id})
        for key, value in kwargs.items():
            setattr(task, key, value)
        self.db_session.commit()
        return task
    
    def delete_task(self, **kwargs):
        task = self.get_task(**kwargs)
        print(task)
        self.db_session.delete(task)
        self.db_session.commit()
