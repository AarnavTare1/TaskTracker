# app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

#####################################################
# 1. CREATE AND CONFIGURE THE FLASK APP
#####################################################
app = Flask(__name__)
CORS(app)

# Update with your actual PostgreSQL URI
# e.g. 'postgresql://postgres:PASSWORD@localhost:5432/task_tracker'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:abe@localhost:5432/task_tracker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#####################################################
# 2. INIT SQLALCHEMY
#####################################################
db = SQLAlchemy(app)

#####################################################
# 3. CREATE THE MODEL
#####################################################
class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Task {self.title}>'

#####################################################
# 4. CREATE TABLES (Quick Setup)
#####################################################
with app.app_context():
    db.create_all()

#####################################################
# 5. ROUTES
#####################################################
@app.route('/')
def home():
    return "Hello from the single-file Flask backend!"

@app.route('/api/tasks/', methods=['GET'])
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

@app.route('/api/tasks/', methods=['POST'])
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

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
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

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'}), 200

#####################################################
# 6. RUN
#####################################################
if __name__ == '__main__':
    # Debug mode for development
    app.run(debug=True, port=5000)
