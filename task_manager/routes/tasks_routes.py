from flask import jsonify, make_response, Blueprint, request, render_template, flash, redirect, url_for
from flask_login import logout_user, login_required, current_user

from task_manager.services.task_service import TaskService
from task_manager.routes.forms.task_forms import TaskCreateForm


tasks_bp = Blueprint('tasks_routes', __name__)


@tasks_bp.route('/tasks', methods=['GET'])
def show_all_tasks():
    tasks = TaskService().get_all_tasks()
    return render_template('tasks/show_tasks.html', tasks=tasks)


@tasks_bp.route('/create_task', methods=['GET', 'POST'])
@login_required
def create_task():
    form = TaskCreateForm()
    if request.method == 'POST':
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
def get_task(id):
    try:
        task = TaskService().get_task(id)
    except:
        flash('Запрашиваемой задачи нет', 'error')
        return render_template('index.html')
    return render_template('tasks/show_task_data.html', task=task)


@tasks_bp.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    try:
        data = request.json
        task = TaskService().update_task(id, data)
    except:
        return make_response(jsonify({'error': 'Error update task'}), 404)
    return jsonify(task)

@tasks_bp.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    try:
        message = TaskService().delete_task(id)
    except:
        return make_response(jsonify({'error': 'Error delete task'}), 404)
    return make_response(jsonify({'success': message}), 200)
