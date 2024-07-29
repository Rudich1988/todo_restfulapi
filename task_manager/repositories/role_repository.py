from task_manager.models.roles import Role

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
    def __init__(self, session):
        self.session = session

    def get_roles(self):
        roles = self.session.query(Role).filter(Role.title != 'админ').all()
        return roles

    def get_role(self, **kwargs):
        role = self.session.query(Role).filter_by(**kwargs)[0]
        return role
