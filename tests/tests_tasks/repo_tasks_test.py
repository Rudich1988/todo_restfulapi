

# это в env migrations
'''
import os

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from dotenv import load_dotenv

from task_manager.db import ModelBase
from task_manager.models import *

load_dotenv()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", os.getenv('DATABASE_URL'))

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = ModelBase.metadata
'''

# это в работе с консолью

'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('mysql+mysqlconnector://rudi4:password@localhost/task_manager')
Session = sessionmaker(bind=engine)
session = Session()
from task_manager.models.users import User
results = session.query(User).all()
user = session.add(User(first_name='hjk', last_name='uio', username='hui1', password='morozki1988', email='exampl1e@mail.ru', is_active=1))
'''


# versions
'''
from werkzeug.security import generate_password_hash
from sqlalchemy import orm

from task_manager.config.base import Config
from task_manager.models.users import User
from task_manager.models.roles import Role
from task_manager.models.statuses import Status


admin_password = generate_password_hash(Config.ADMIN_PASSWORD)

'''

'''
bind = op.get_bind()
session = orm.Session(bind=bind)
password = User().get_hash_password(password=Config.ADMIN_PASSWORD)
user = session.execute(sa.insert(User).values(first_name='my_name', last_name='my_last_name', username='admin', email='admin@mail.ru', is_active=True, is_admin=True, password=password))
executor = session.execute(sa.insert(Role).values(title='исполнитель'))
author = session.execute(sa.insert(Role).values(title='заказчик'))
status1 = session.execute(sa.insert(Status).values(title='свободна'))
status2 = session.execute(sa.insert(Status).values(title='в работе'))
status3 = session.execute(sa.insert(Status).values(title='завершена'))
'''
