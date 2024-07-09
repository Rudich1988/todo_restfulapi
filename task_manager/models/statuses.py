from sqlalchemy import text, ForeignKey, UniqueConstraint, BigInteger, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


from task_manager.db import ModelBase


class Status(ModelBase):
    __tablename__='statuses'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100))

    def __repr__(self):
        return f'{self.title}'