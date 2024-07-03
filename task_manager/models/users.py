from datetime import datetime

from sqlalchemy import text, ForeignKey, UniqueConstraint, BigInteger, ForeignKey, String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func
from flask_login.mixins import UserMixin
#from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, roles_required

from task_manager.db import ModelBase


#from task_manager.db import Session
#from task_manager.app import login_manager


class User(ModelBase, UserMixin):
    __tablename__='users'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    username: Mapped[str] = mapped_column(String(100), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    about_me: Mapped[str] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=False)
    is_admin: Mapped[bool] = mapped_column(Boolean(), default=False)
    password: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(),
                                                 onupdate=func.now())

    user_roles: Mapped["Role"] = relationship(back_populates='role_users', secondary='users_roles')
    #task_author: Mapped["Task"] = relationship(back_populates='user', foreign_keys='author', cascade="all,delete")
    #task_executor: Mapped["Task"] = relationship(back_populates='user')#, foreign_keys='executor')

    def get_hash_password(self, password):
        return generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)


class UsersRoles(ModelBase):
    __tablename__='users_roles'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete='CASCADE'), primary_key=True)
    role_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("roles.id", ondelete='CASCADE'), primary_key=True)

    #user = Mapped['User'] = relationship('User', back_populates='roles')
    #user = Mapped['Role'] = relationship('Role', back_populates='users')
