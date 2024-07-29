from flask import jsonify, make_response, Blueprint, request, render_template, flash, redirect, url_for
from flask_login import logout_user, login_required, current_user
from flask_socketio import emit

from task_manager.services.user_service import UserService
from task_manager.routes.forms.user_forms import UserCreateForm, UserLoginForm, UserDeleteForm, UserUpdateForm
from task_manager.repositories.user_repository import UserRepository
from task_manager.app import socketio
from task_manager.repositories.task_repository import TaskRepository


users_bp = Blueprint('users_routes', __name__)


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user_data = request.form.to_dict()
            #try:
            UserService().login_user(user_data)
            flash('Вы успешно зашли в систему', 'success')
            return render_template('index.html')
            #except:
             #   flash('Вы ввели неправильные логин или пароль, либо Ваша учётная запись не активна', 'error')
              #  return render_template('/users/login.html', form=form)
    return render_template('/users/login.html', form=form)

@users_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы разлогинены', 'info')
    return render_template('index.html')


@users_bp.route('/registration', methods=['GET', 'POST'])
def registration():
    form = UserCreateForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            #try:
            user_data = request.form.to_dict()
            user_data['user_roles'] = form.user_roles.data
            UserService().add_user(user_data)
            return render_template('users/email_confirmation.html')
            #except:
             #   flash('Пользователь с таким именем или email уже есть.', 'error')
              #  return render_template('users/registration.html', form=form)
    return render_template('users/registration.html', form=form)


@users_bp.route('/profile/<int:id>')
@login_required
def get_profile(id):
    form = UserDeleteForm()
    #try:
    user = UserService().get_user(id)
    return render_template('users/profile.html', user=user, form=form)
    #except:
     #   flash('Такого пользователя нет')
      #  return render_template('index.html')


@users_bp.route('/update_user/<int:id>', methods=['GET', 'POST'])
@login_required
def update_user(id):
    try:
        user = UserService().get_user(id)
        form = UserUpdateForm(obj=user)
    except:
        flash('Запрашиваемого пользователя нет', 'error')
        return render_template('index.html')
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                if current_user.id == user.id:
                    data = request.form.to_dict()
                    UserService().update_user(id, data)
                    flash('Пользователь успешно обновлен', 'success')
                    return redirect(url_for('users_routes.get_profile', id=id))
                flash('Невозможно изменить пользователя', 'error')
                return redirect(url_for('users_routes.get_profile', id=id))
            except:
                flash('Не удалось изменить данные пользователя', 'error')
                return render_template('users/profile.html', form=form, id=id)
    return render_template('users/update_user.html', form=form, id=id)


@users_bp.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    #try:
    user = UserService().get_user(id)
    if current_user.id == user.id:
        UserService().delete_user(id)
        flash('Пользователь успешно удален', 'success')
        return redirect(url_for('users_routes.login'))
    flash('Невозможно удалить пользователя', 'error')
    return redirect(url_for('tasks_routes.show_all_tasks'))
    #except:
     #   flash('Запрашиваемого пользователя нет', 'error')
      #  return redirect(url_for('tasks_routes.show_all_tasks'))


@users_bp.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        UserService().confirm_email(token)
        flash('Ваша учётная запись активирована.', 'success')
        return redirect(url_for('users_routes.login'))
    except:
        flash('Не удалось активировать Вашу учётную запись', 'error')
        return redirect(url_for('users_routes.login'))
