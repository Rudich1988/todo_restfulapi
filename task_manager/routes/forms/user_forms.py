from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from wtforms_sqlalchemy.fields import QuerySelectMultipleField

from task_manager.repositories.role_repository import RoleRepository
from task_manager.models.roles import Role
from task_manager.db import Session, db_session


#ROLES = Session().query(Role).all()


ROLES = RoleRepository().get_roles()


class UserCreateForm(FlaskForm):
    first_name = StringField('Имя', validators=[DataRequired(), Length(1, 100)],
                        render_kw={"placeholder": "Введите имя"})
    last_name = StringField('Фамилия', validators=[DataRequired(), Length(1, 100)],
                        render_kw={"placeholder": "Введите фамилию"})
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(1, 100)],
                           render_kw={"placeholder": "Введите имя пользователя"})
    email = StringField("Email",  validators=[DataRequired(), Email(message='Некорректный email')],
                        render_kw={"placeholder": "Введите адрес электронной почты"})
    about_me = TextAreaField('Обо мне', render_kw={"placeholder": "Расскажите о себе"})
    password1 = PasswordField('Пароль',
                              render_kw={"placeholder": "Введите пароль"},
                              validators=[DataRequired(), Length(6, 200)])
    password2 = PasswordField('',
                              render_kw={"placeholder": "Повторите пароль"},
                              validators=[DataRequired(), Length(6, 200),
                                          EqualTo('password1',
                                                  message='Пароли не совпадают')])
    user_roles = QuerySelectMultipleField('Roles', query_factory=lambda: ROLES, get_label='title')
    submit = SubmitField('Создать', render_kw={"class": "btn btn"})


class UserLoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(1, 100)],
                           render_kw={"placeholder": "Введите имя пользователя"})
    password = PasswordField('Пароль',
                             render_kw={"placeholder": "Введите пароль"},
                             validators=[DataRequired(), Length(1, 200)])
    submit = SubmitField('Войти', render_kw={"class": "btn btn"})
    

class UserDeleteForm(FlaskForm):
    submit = SubmitField('Удалить', render_kw={"class": "btn btn"})


