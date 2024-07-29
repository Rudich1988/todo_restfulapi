from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, scoped_session

from task_manager.config.base import Config


class ModelBase(DeclarativeBase):
    pass

engine = create_engine(Config.DATABASE_URL, echo=False)

#Session = sessionmaker(bind=engine)
SessionFactory = sessionmaker(bind=engine)

# Создайте объект scoped_session
Session = scoped_session(SessionFactory)

@contextmanager
def db_session():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()
