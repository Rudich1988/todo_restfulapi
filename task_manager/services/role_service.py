from task_manager.repositories.role_repository import RoleRepository
from task_manager.db import db_session


class RoleService:
    def __init__(self, repository=RoleRepository,
                 session=db_session):
        self.session = session
        self.repository = repository

    def get_roles(self):
        with self.session() as s:
            roles = self.repository(s).get_roles()
        return roles

    def get_role(self):
        with self.session() as s:
            role = self.repository(s).get_role()
        return role
