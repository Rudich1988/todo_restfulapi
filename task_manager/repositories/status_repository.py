from task_manager.models.statuses import Status
from task_manager.db import Session, db_session as db


class StatusRepository:
    def __init__(self, db_session=db()):
        self.db_session = db_session

    def get_statuses(self):
        return self.db_session.query(Status).all()
    
    def get_status(self, **kwargs):
        status = self.db_session.query(Status).filter_by(**kwargs)[0]
        return status
