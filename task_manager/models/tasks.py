from datetime import datetime

from sqlalchemy.sql import func
from sqlalchemy import text, ForeignKey, UniqueConstraint, BigInteger, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from task_manager.db import ModelBase


class Task(ModelBase):
    __tablename__='tasks'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(),
                                                 onupdate=func.now()) 
    status_id: Mapped[int] = mapped_column(ForeignKey("statuses.id"))  
    author: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'))
    executor: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='SET NULL'), nullable=True)
    
    author_1: Mapped['User'] = relationship(foreign_keys=[author], backref='task_author')
    executor_2: Mapped['User'] = relationship(foreign_keys=[executor], backref='task_executor')
    status: Mapped['Status'] = relationship(backref='tasks')
