from flask import request, jsonify
from models import db, Task, serialize_task

# Route to add a new To-Do task
def add_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description', '')

    if not title:
        return jsonify({"error": "Title is required"}), 400

    new_task = Task(title=title, description=description)
    db.session.add(new_task)
    db.session.commit()

    return jsonify(serialize_task(new_task)), 201

# Route to display list of To-Do tasks
def get_tasks():
    tasks = Task.query.all()
    return jsonify([serialize_task(task) for task in tasks])

# Route to edit a particular To-Do task
def update_task(id):
    task = db.session.get(Task, id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.is_completed = data.get('is_completed', task.is_completed)
    db.session.commit()

    return jsonify(serialize_task(task))

# Route to delete a particular To-Do task
def delete_task(id):
    task = db.session.get(Task, id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Task deleted successfully"})

# Route to delete all To-Do tasks
def delete_all_tasks():
    Task.query.delete()
    db.session.commit()

    return jsonify({"message": "All tasks deleted successfully"})