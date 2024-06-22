from task_manager.models.users import User
from task_manager.db import Session
from task_manager.app import login_manager


@login_manager.user_loader
def user_loader(user_id):
    return Session().query(User).get(user_id)


class UserRepository:
    def __init__(self, db_session=Session()):
        self.db_session = db_session

    def get_user(self, **kwargs):
        user = self.db_session.query(User).filter_by(**kwargs).first()
        return user

    def add_user(self, **kwargs):
        user = User(**kwargs)
        self.db_session.add(user)
        self.db_session.commit()
        return user

    def update_user(self, user_id, **kwargs):
        user = self.get_user(**{'id': user_id})
        for key, value in kwargs.items():
            setattr(user, key, value)
        self.db_session.commit()
        return user
