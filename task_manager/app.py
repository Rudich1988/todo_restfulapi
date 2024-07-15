from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_wtf.csrf import CSRFProtect
#from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, roles_required

from task_manager.config.base import Config
from task_manager.db import Session
from flask_socketio import SocketIO


app = Flask(__name__, template_folder='routes/templates')
app.config.from_object(Config)

socketio = SocketIO(app)

csrf = CSRFProtect(app)

login_manager = LoginManager(app)
mail = Mail(app)

from task_manager.routes.tasks_routes import *
from task_manager.routes.users_routes import *
from task_manager.routes.home_routes import *


app.register_blueprint(home_bp)
app.register_blueprint(tasks_bp)
app.register_blueprint(users_bp)


from task_manager.models import *
from task_manager.admin import *

admin = Admin(app, index_view=MyAdminIndexView())

admin.add_view(UserView(User, Session()))
admin.add_view(RoleView(Role, Session()))
admin.add_view(TaskView(Task,Session()))

#user_datastore = SQLAlchemyUserDatastore(Session, User, Role)
#security = Security(app, user_datastore)
