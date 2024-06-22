from flask import jsonify, make_response, Blueprint, request, render_template, flash, redirect, url_for
from flask_login import logout_user, login_required
from werkzeug.security import generate_password_hash

from task_manager.services.user_service import UserService
from task_manager.routes.forms.user_forms import UserCreateForm, UserLoginForm


users_bp = Blueprint('users_routes', __name__)


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user_data = request.form.to_dict()
            try:
                UserService().login_user(user_data)
                flash('Вы успешно зашли в систему', 'success')
                return render_template('index.html')
            except:
                flash('Вы ввели неправильные логин или пароль, либо Ваша учётная запись не активна', 'error')
                return render_template('/users/login.html', form=form)
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
            try:
                user_data = request.form.to_dict()
                UserService().add_user(user_data)
                return render_template('users/email_confirmation.html')
            except:
                flash('Пользователь с таким именем или email уже есть.', 'error')
                return render_template('users/registration.html', form=form)
    return render_template('users/registration.html', form=form)


@users_bp.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        UserService().confirm_email(token)
        flash('Ваша учётная запись активирована.', 'success')
        return redirect(url_for('users_routes.login'))
    except:
        flash('Не удалось активировать Вашу учётную запись', 'error')
        return redirect(url_for('users_routes.login'))








'''
@users_bp.route('/registration', methods=['GET', 'POST'])
def registration():
    form = UserCreateForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                user_data = request.form.to_dict()
                UserService().add_user(user_data)
                flash('Вы успешно зарегестрированы', 'success')
                return redirect(url_for('users_routes.login'))
            except:
                flash('Пользователь с таким именем уже есть.', 'error')
                return render_template('users/registration.html', form=form)
    return render_template('users/registration.html', form=form)
'''