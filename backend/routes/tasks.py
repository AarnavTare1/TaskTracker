# backend/routes/tasks.py

from flask import Blueprint, request, jsonify
# Relative imports: two dots means "go up one directory" from routes to backend, then import 'app' and 'models'
from ..app import db
from ..models import Task

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    tasks_list = [
        {
            'id': t.id,
            'title': t.title,
            'completed': t.completed
        }
        for t in tasks
    ]
    return jsonify(tasks_list), 200

@tasks_bp.route('/', methods=['POST'])
def create_task():
    data = request.get_json()
    new_task = Task(
        title=data['title'],
        completed=data.get('completed', False)
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({
        'id': new_task.id,
        'title': new_task.title,
        'completed': new_task.completed
    }), 201

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.completed = data.get('completed', task.completed)
    db.session.commit()
    return jsonify({
        'id': task.id,
        'title': task.title,
        'completed': task.completed
    }), 200

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'}), 200
