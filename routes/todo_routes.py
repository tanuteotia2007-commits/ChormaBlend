from flask import Blueprint, request, jsonify
from database.db import query_db, execute_db

todo_bp = Blueprint("todo", __name__, url_prefix="/api/todos")

@todo_bp.route("", methods=["GET"])
def get_todos():
    """Retrieve all productivity todos."""
    todos = query_db("SELECT id, title, completed, created_at FROM todos ORDER BY id DESC")
    return jsonify({
        "success": True,
        "data": [
            {
                "id": t["id"],
                "title": t["title"],
                "completed": bool(t["completed"]),
                "created_at": str(t["created_at"])
            }
            for t in todos
        ]
    }), 200

@todo_bp.route("", methods=["POST"])
def create_todo():
    """Create a new productivity todo."""
    data = request.get_json(silent=True)
    if not data or not str(data.get("title", "")).strip():
        return jsonify({
            "success": False,
            "message": "Title is required"
        }), 400

    title = str(data["title"]).strip()
    completed = 1 if data.get("completed", False) else 0

    res = execute_db(
        "INSERT INTO todos (title, completed) VALUES (?, ?)",
        (title, completed)
    )
    todo_id = res["lastrowid"]
    todo = query_db("SELECT id, title, completed, created_at FROM todos WHERE id = ?", (todo_id,), one=True)

    return jsonify({
        "success": True,
        "data": {
            "id": todo["id"],
            "title": todo["title"],
            "completed": bool(todo["completed"]),
            "created_at": str(todo["created_at"])
        }
    }), 201

@todo_bp.route("/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id: int):
    """Update an existing productivity todo (title and/or completion state)."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "success": False,
            "message": "Update payload is required"
        }), 400

    existing = query_db("SELECT id, title, completed FROM todos WHERE id = ?", (todo_id,), one=True)
    if not existing:
        return jsonify({
            "success": False,
            "message": "Todo not found"
        }), 404

    title = str(data["title"]).strip() if "title" in data and str(data["title"]).strip() else existing["title"]
    completed = 1 if data.get("completed", existing["completed"]) else 0

    execute_db(
        "UPDATE todos SET title = ?, completed = ? WHERE id = ?",
        (title, completed, todo_id)
    )

    todo = query_db("SELECT id, title, completed, created_at FROM todos WHERE id = ?", (todo_id,), one=True)
    return jsonify({
        "success": True,
        "data": {
            "id": todo["id"],
            "title": todo["title"],
            "completed": bool(todo["completed"]),
            "created_at": str(todo["created_at"])
        }
    }), 200

@todo_bp.route("/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id: int):
    """Delete a productivity todo."""
    res = execute_db("DELETE FROM todos WHERE id = ?", (todo_id,))
    if res["rowcount"] == 0:
        return jsonify({
            "success": False,
            "message": "Todo not found"
        }), 404

    return jsonify({
        "success": True,
        "message": "Todo deleted"
    }), 200
