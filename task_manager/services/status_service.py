from task_manager.repositories.status_repository import StatusRepository
from task_manager.db import db_session


class StatusService:
    def __init__(self, repository=StatusRepository,
                 session=db_session):
        self.session = session
        self.repository = repository

    def get_statuses(self):
        with self.session() as s:
            statuses = self.repository(s).get_statuses()
        return statuses

    def get_status(self):
        with self.session() as s:
            status = self.repository(s).get_status()
        return status
