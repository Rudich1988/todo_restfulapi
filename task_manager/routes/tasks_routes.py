from flask import jsonify, make_response, Blueprint, request, render_template, flash, redirect, url_for
from flask_login import logout_user, login_required, current_user
#from flask_security import roles_required

from task_manager.services.task_service import TaskService
from task_manager.routes.forms.task_forms import TaskCreateForm, DeleteForm, TaskUpdateForm
from task_manager.repositories.task_repository import TaskRepository
from task_manager.services.user_service import UserService


tasks_bp = Blueprint('tasks_routes', __name__)


@tasks_bp.route('/tasks', methods=['GET'])
@login_required
def show_all_tasks():
    tasks = TaskService().get_all_tasks()
    return render_template('tasks/show_tasks.html', tasks=tasks)


@tasks_bp.route('/create_task', methods=['GET', 'POST'])
#@roles_required('author') 
@login_required
def create_task():
    form = TaskCreateForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                task_data = request.form.to_dict()
                task_data['user_id'] = current_user.id
                TaskService().add_task(task_data)
                flash('Задача успешно создана', 'success')
                return redirect(url_for('tasks_routes.show_all_tasks'))
            except:
                flash('Не получилось создать задачу')
                return render_template('tasks/create_task.html', form=form)
    return render_template('tasks/create_task.html', form=form)


@tasks_bp.route('/task/<int:id>', methods=['GET'])
@login_required
def get_task(id):
    form = DeleteForm()
    try:
        task = TaskService().get_task(id)
        author = UserService().get_user(task['user_id'])['username']
        return render_template('tasks/show_task_data.html',
                               task=task, form=form, author=author)
    except:
        flash('Запрашиваемой задачи нет', 'error')
        return render_template('index.html')


@tasks_bp.route('/update_task/<int:id>', methods=['GET', 'POST'])
@login_required
def update_task(id):
    try:
        task = TaskRepository().get_task(**{'id': id})
        form = TaskUpdateForm(obj=task)
    except:
        flash('Запрашиваемой задачи нет', 'error')
        return render_template('index.html')
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                if current_user.id == task.user_id:
                    data = request.form.to_dict()
                    TaskService().update_task(id, data)
                    flash('Задача успешно обновлена', 'success')
                    return redirect(url_for('tasks_routes.show_all_tasks'))
                flash('Невозможно изменить задачу, Вы не её автор', 'error')
                return redirect(url_for('tasks_routes.show_all_tasks'))
            except:
                flash('Не удалось изменить данные задачи', 'error')
                return render_template('tasks/update_task.html', form=form, id=id)
    return render_template('tasks/update_task.html', form=form, id=id)


@tasks_bp.route('/delete_task/<int:id>', methods=['POST'])
def delete_task(id):
    try:
        task = TaskRepository().get_task(**{'id': id})
        if current_user.id == task.user_id:
            TaskService().delete_task(id)
            flash('Задача успешно удалена', 'success')
            return redirect(url_for('tasks_routes.show_all_tasks'))
        flash('Невозможно удалить задачу. Вы не являетесь её автором', 'error')
        return redirect(url_for('tasks_routes.show_all_tasks'))
    except:
        flash('Запрашиваемой задачи нет')
        return redirect(url_for('tasks_routes.show_all_tasks'))
