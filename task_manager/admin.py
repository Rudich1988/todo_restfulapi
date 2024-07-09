from functools import wraps

from flask import redirect, url_for, flash, render_template
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView


from task_manager.app import login_manager


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
        if current_user.user_roles:
            return current_user.is_authenticated and 'админ' == current_user.user_roles[0].title#current_user.is_admin
        return False
    
    def inaccessible_callback(self, name, **kwargs):
        flash('У Вас нет прав администратора', 'error')
        return redirect(url_for('home_routes.index'))


@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('Чтобы получить доступ к этой странице, пожалуйста, залогинтесь', 'info')
    return redirect(url_for('users_routes.login'))



'''
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
'''
