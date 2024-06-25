from datetime import datetime

from sqlalchemy import text, ForeignKey, UniqueConstraint, BigInteger, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from task_manager.db import ModelBase


class Role(ModelBase):
    __tablename__='roles'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100))
    
    role_users: Mapped[list["User"]] = relationship(back_populates='user_roles', secondary='users_roles')

    def __repr__(self):
        return f'{self.title}'
