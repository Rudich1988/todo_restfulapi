from functools import wraps

from flask import redirect, url_for, flash, render_template
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView


class UserView(ModelView):
    column_exclude_list = ['password',]

class RoleView(ModelView):
    column_exclude_list = []

class TaskView(ModelView):
    column_exclude_list = []



class MyAdminIndexView(AdminIndexView):
    def __init__(self, **kwargs):
        super(MyAdminIndexView, self).__init__(**kwargs)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    
    def inaccessible_callback(self, name, **kwargs):
        flash('У Вас нет прав администратора', 'error')
        return redirect(url_for('home_routes.index'))








def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('У Вас нет прав администратора', 'error')
            return redirect(url_for('users_routes.login'))
        if not current_user.is_admin:
            flash('У Вас нет прав администратора', 'error')
            return redirect(url_for('users_routes.login'))
        return func(*args, **kwargs)
    return decorated_function
