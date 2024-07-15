from task_manager.models.roles import Role
from task_manager.db import Session, db_session as db_s

'''
class RoleRepository:
    def __init__(self, db_session=Session()):
        self.db_session = db_session

    def get_roles(self):
        return self.db_session.query(Role).filter(Role.title != 'админ').all()
    
    def get_role(self, **kwargs):
        role = self.db_session.query(Role).filter_by(**kwargs)[0]
        return role
'''
class RoleRepository:
    def __init__(self, db_session=db_s):
        self.db_session = db_session

    def get_roles(self):
        with self.db_session() as db:
            roles = db.query(Role).filter(Role.title != 'админ').all()
        return roles
    
    def get_role(self, **kwargs):
        with self.db_session() as db:
            role = db.query(Role).filter_by(**kwargs)[0]
        return role


