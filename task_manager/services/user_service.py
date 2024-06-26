from flask import url_for
from itsdangerous import URLSafeTimedSerializer
from flask_login import login_user
from flask_mail import Message

from task_manager.repositories.user_repository import UserRepository
from task_manager.routes.schemas.user import UserLoginSchema, UserRegistrationSchema
from task_manager.models.users import User
from task_manager.config.base import Config
from task_manager.app import mail


from task_manager.models.roles import Role
from task_manager.db import Session



class UserService:
    def __init__(self, session = UserRepository(),
                 user_login_schema = UserLoginSchema(),
                 user_schema = UserRegistrationSchema(),
                 users_schema = UserRegistrationSchema(many=True)):
        self.session = session
        self._user_schema = user_schema
        self._users_schema = users_schema
        self._login_schema = user_login_schema

    def get_user(self, user_id):
        user = self.session.get_user(**{'id': user_id})
        return self._user_schema.dump(user)

    def generate_token(self, email):
        serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
        token = serializer.dumps(email, salt=Config.SECURITY_PASSWORD_SALT)
        return token

    def confirm_token(self, token):
        serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
        email = serializer.loads(token, salt=Config.SECURITY_PASSWORD_SALT)
        return email

    def send_email(self, email):
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

    def confirm_email(self, token):
        email = self.confirm_token(token)
        data = {'email': email}
        user = self.session.get_user(**data)
        user.is_active = True
        self.session.update_user(user.id, **data)

    def add_user(self, data):
        if data['password1'] == data['password2']:
            data['password'] = User().get_hash_password(data['password1'])
        data = self._user_schema.dump(data)
        user = self.session.add_user(**data)
        self.send_email(user.email)
        return data

    def login_user(self, user_data):
        data = self._login_schema.dump(user_data)
        user = self.session.get_user(**data)
        if user.check_password(user_data['password']) and user.is_active:
            current_user = user
        login_user(current_user)
        return user_data
