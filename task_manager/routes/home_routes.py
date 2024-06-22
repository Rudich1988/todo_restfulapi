from flask import jsonify, make_response, Blueprint, request, render_template, redirect, url_for, flash

from flask_wtf import CSRFProtect
from flask_bootstrap import Bootstrap5

from task_manager.app import app


home_bp = Blueprint('home_routes', __name__)

bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)


@home_bp.route('/')
def index():
    return render_template('index.html'), 200
