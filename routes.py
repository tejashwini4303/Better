from flask import Blueprint, request, jsonify
from models import db, Task, Comment

routes = Blueprint("routes", __name__)

# ----------------- TASK CRUD -----------------

@routes.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    print("Received data:", data)   # debug line
    if not data or "title" not in data:
        return {"error": "Missing 'title'"}, 400
    new_task = Task(title=data["title"])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task added", "task": {"id": new_task.id, "title": new_task.title}}), 201

@routes.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{"id": t.id, "title": t.title} for t in tasks])

@routes.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    task.title = data["title"]
    db.session.commit()
    return jsonify({"message": "Task updated", "task": {"id": task.id, "title": task.title}})

@routes.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"})

# ----------------- COMMENT CRUD -----------------

@routes.route("/tasks/<int:task_id>/comments", methods=["POST"])
def add_comment(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    if not data or "text" not in data:
        return {"error": "Missing 'text'"}, 400
    new_comment = Comment(text=data["text"], task=task)
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({"message": "Comment added", "comment": {"id": new_comment.id, "text": new_comment.text}}), 201

@routes.route("/tasks/<int:task_id>/comments", methods=["GET"])
def get_comments(task_id):
    task = Task.query.get_or_404(task_id)
    comments = [{"id": c.id, "text": c.text} for c in task.comments]
    return jsonify(comments)

@routes.route("/comments/<int:comment_id>", methods=["PUT"])
def update_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    data = request.get_json()
    comment.text = data["text"]
    db.session.commit()
    return jsonify({"message": "Comment updated", "comment": {"id": comment.id, "text": comment.text}})

@routes.route("/comments/<int:comment_id>", methods=["DELETE"])
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return jsonify({"message": "Comment deleted"})
