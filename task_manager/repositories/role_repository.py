from task_manager.models.roles import Role
from task_manager.db import Session, db_session as db


class RoleRepository:
    def __init__(self, db_session=db()):
        self.db_session = db_session

    def get_roles(self):
        return self.db_session.query(Role).filter(Role.title != 'админ').all()
    
    def get_role(self, **kwargs):
        role = self.db_session.query(Role).filter_by(**kwargs)[0]
        return role

