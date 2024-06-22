from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail

from task_manager.config.base import Config


app = Flask(__name__, template_folder='routes/templates')
app.config.from_object(Config)

login_manager = LoginManager(app)
mail = Mail(app)

from task_manager.routes.tasks_routes import *
from task_manager.routes.users_routes import *
from task_manager.routes.home_routes import *

app.register_blueprint(home_bp)
app.register_blueprint(tasks_bp)
app.register_blueprint(users_bp)


from task_manager.models import *

