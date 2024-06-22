from datetime import datetime

from sqlalchemy import text, ForeignKey, UniqueConstraint, BigInteger, ForeignKey, String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func
from flask_login.mixins import UserMixin

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
    is_active: Mapped[bool] = mapped_column(Boolean(), default=False)
    password: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(),
                                                 onupdate=func.now())

    #roles: Mapped[list] = relationship('UserRole', back_populates='users')
    tasks: Mapped[list["Task"]] = relationship(cascade="all,delete", back_populates='user')


    def get_hash_password(self, password):
        return generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)



'''
class UserRole(ModelBase):
    __table_name__='user_roles'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("user.id", on_delete='CASCADE'), unique=True)
    role_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("role.id", on_delete='CASCADE'), unique=True)

    user = Mapped['User'] = relationship('User', back_populates='roles')
    user = Mapped['Role'] = relationship('Role', back_populates='users')
'''