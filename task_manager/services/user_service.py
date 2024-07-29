from typing import Dict

from flask import url_for
from itsdangerous import URLSafeTimedSerializer
from flask_login import login_user, current_user
from flask_mail import Message

from task_manager.repositories.user_repository import UserRepository
from task_manager.routes.schemas.user import UserLoginSchema, UserRegistrationSchema, UserUpdateSchema
from task_manager.models.users import User
from task_manager.config.base import Config
from task_manager.app import mail
from task_manager.db import db_session


from task_manager.repositories.role_repository import RoleRepository
from task_manager.db import Session



class UserService:
    def __init__(self, repository=UserRepository,
                 session=db_session,
                 user_login_schema=UserLoginSchema(),
                 user_update_schema=UserUpdateSchema(),
                 user_schema=UserRegistrationSchema(),
                 users_schema=UserRegistrationSchema(many=True)):
        self.repository = repository
        self.session = session
        self._user_schema = user_schema
        self._users_schema = users_schema
        self._login_schema = user_login_schema
        self._update_schema = user_update_schema

    def get_user(self, user_id: int) -> Dict:
        with self.session() as s:
            user = self.repository(s).get_user(**{'id': user_id})
        return self._user_schema.dump(user)

    def generate_token(self, email: str) -> str:
        serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
        token = serializer.dumps(email, salt=Config.SECURITY_PASSWORD_SALT)
        return token

    def confirm_token(self, token: str) -> str:
        serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
        email = serializer.loads(token, salt=Config.SECURITY_PASSWORD_SALT)
        return email

    def send_email(self, email: str) -> None:
        subject = 'Подтвердите свой email'
        token = self.generate_token(email)       
        message = Message(
            subject,
            recipients=[email],
            sender=Config.MAIL_USERNAME,
        )
        link = url_for('users_routes.confirm_email', token=token, _external=True)
        message.body = 'Для подтверждения Вашей электронной почты пройдите по ссылке {}'.format(link)
        mail.send(message)

    def confirm_email(self, token: str) -> None:
        email = self.confirm_token(token)
        data = {'email': email}
        with self.session() as s:
            user = self.repository(s).get_user(**data)
        user.is_active = True
        with self.session() as s:
            self.repository(s).update_user(user.id, **data)

    def add_user(self, data: Dict) -> Dict:
        if data['password1'] == data['password2']:
            data['password'] = User().get_hash_password(data['password1'])
        user_data = self._user_schema.dump(data)
        user_data['user_roles'] = data['user_roles']
        with self.session() as s:
            user = self.repository(s).add_user(**user_data)
        self.send_email(user.email)
        return user_data


    def login_user(self, user_data: Dict) -> Dict:
        data = self._login_schema.dump(user_data)
        with self.session() as s:
            user = self.repository(s).get_user(**data)
            if user.check_password(user_data['password']) and user.is_active:
                current_user = user
            login_user(current_user)
            return user_data
    
    def update_user(self, user_id, data):
        user_data = self._update_schema.dump(data)
        with self.session as s:
            user = self.repository(s).update_user(user_id, **user_data)
        return self._update_schema.dump(user)
    
    def delete_user(self, user_id):
        with self.session() as s:
            self.repository(s).delete_user(**{'id': user_id})
        return f'User id: {user_id} deleted'
