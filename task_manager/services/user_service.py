from datetime import datetime as dt

from flask import jsonify, make_response, Blueprint, request, render_template, flash, redirect, url_for
from itsdangerous import URLSafeTimedSerializer
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message

from task_manager.repositories.user_repository import UserRepository
from task_manager.routes.schemas.user import UserSchema
from task_manager.models.users import User
from task_manager.config.base import Config
from task_manager.app import mail



class UserService:
    def __init__(self, session = UserRepository(),
                 user_schema = UserSchema(),
                 users_schema = UserSchema(many=True)):
        self.session = session
        self._user_schema = user_schema
        self._users_schema = users_schema

    def generate_token(self, email):
        serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
        token = serializer.dumps(email, salt=Config.SECURITY_PASSWORD_SALT)
        return token

    def confirm_token(self, token):
        serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
        email = serializer.loads(token, salt=Config.SECURITY_PASSWORD_SALT)
        print(email)
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
            del data['password1']
            del data['password2']
            del data['submit']
            del data['csrf_token']
        user = self.session.add_user(**data)
        self.send_email(user.email)
        return data

    def login_user(self, user_data):
        del user_data['csrf_token']
        del user_data['submit']
        password = user_data['password']
        del user_data['password']
        user = self.session.get_user(**user_data)
        if user.check_password(password) and user.is_active:
            current_user = user
        login_user(current_user)
        return user_data
