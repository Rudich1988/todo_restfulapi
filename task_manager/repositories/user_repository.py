from task_manager.models.users import User
from task_manager.db import Session
from task_manager.app import login_manager


@login_manager.user_loader
def user_loader(user_id):
    return Session().query(User).get(user_id)

'''
class UserRepository:
    def __init__(self, db_session=Session()):
        self.db_session = db_session

    def get_users(self):
        users = self.db_session.query(User).all()
        return users

    def get_user(self, **kwargs):
        user = self.db_session.query(User).filter_by(**kwargs)[0]
        return user

    def add_user(self, **kwargs):
        user_object = User(**kwargs)
        user = self.db_session.merge(user_object)
        self.db_session.add(user)
        self.db_session.commit()
        return user

    def update_user(self, user_id, **kwargs):
        user = self.get_user(**{'id': user_id})
        for key, value in kwargs.items():
            setattr(user, key, value)
        self.db_session.commit()
        return user
    
    def delete_user(self, **kwargs):
        user = self.get_user(**kwargs)
        self.db_session.delete(user)
        self.db_session.commit()
'''


class UserRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_users(self):
        users = self.db_session.query(User).all()
        return users

    def get_user(self, **kwargs):
        user = self.db_session.query(User).filter_by(**kwargs)[0]
        return user

    def add_user(self, **kwargs):
        user_object = User(**kwargs)
        user = self.db_session.merge(user_object)
        self.db_session.add(user)
        #self.db_session.commit()
        return user

    def update_user(self, user_id, **kwargs):
        user = self.get_user(**{'id': user_id})
        for key, value in kwargs.items():
            setattr(user, key, value)
        #self.db_session.commit()
        return user

    def delete_user(self, **kwargs):
        user = self.get_user(**kwargs)
        self.db_session.delete(user)
        #self.db_session.commit()

