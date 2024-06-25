'''
from flask import jsonify, make_response, Blueprint, request, render_template, redirect, url_for, flash

from flask_admin import login_required, current_user

from task_manager.app import app


home_bp = Blueprint('admin_routes', __name__)


@home_bp.route('/admin')
@login_required
def admin():
    if current_user.username == 'admin':
        return render_template('admin.html'), 200
'''