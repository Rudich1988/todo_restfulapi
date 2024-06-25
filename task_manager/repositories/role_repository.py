from task_manager.models.roles import Role
from task_manager.db import Session


class RoleRepository:
    def __init__(self, db_session=Session()):
        self.db_session = db_session

    def get_roles(self):
        return self.db_session.query(Role).all()

