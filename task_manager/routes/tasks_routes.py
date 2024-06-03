from flask import jsonify, make_response, Blueprint, request

from task_manager.services.task_service import TaskService


tasks_bp = Blueprint('tasks_routes', __name__)


@tasks_bp.route('/tasks', methods=['GET'])
def show_all_tasks():
    tasks = TaskService().get_all_tasks()
    return jsonify(tasks)


@tasks_bp.route('/tasks', methods=["POST"])
def create_task():
    try:
        task_data = request.json
        task = TaskService().add_task(task_data)
    except:
        return make_response(jsonify({'error': 'Error create task'}), 404)
    return jsonify(task)


@tasks_bp.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    try:
        task = TaskService().get_task(id)
    except:
        return make_response(jsonify({'error': 'Error: task not found'}), 404)
    return jsonify(task)


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
