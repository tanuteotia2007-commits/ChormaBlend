from flask import Blueprint, request, jsonify
from database.db import query_db, execute_db

notes_bp = Blueprint("notes", __name__, url_prefix="/api/notes")

@notes_bp.route("", methods=["GET"])
def get_notes():
    """Retrieve all productivity notes."""
    notes = query_db("SELECT id, title, content, created_at, updated_at FROM notes ORDER BY id DESC")
    return jsonify({
        "success": True,
        "data": [
            {
                "id": n["id"],
                "title": n["title"],
                "content": n["content"],
                "created_at": str(n["created_at"]),
                "updated_at": str(n["updated_at"])
            }
            for n in notes
        ]
    }), 200

@notes_bp.route("", methods=["POST"])
def create_note():
    """Create a new productivity note."""
    data = request.get_json(silent=True)
    if not data or not str(data.get("title", "")).strip() or not str(data.get("content", "")).strip():
        return jsonify({
            "success": False,
            "message": "Title and content are required"
        }), 400

    title = str(data["title"]).strip()
    content = str(data["content"]).strip()

    res = execute_db(
        "INSERT INTO notes (title, content) VALUES (?, ?)",
        (title, content)
    )
    note_id = res["lastrowid"]
    note = query_db("SELECT id, title, content, created_at, updated_at FROM notes WHERE id = ?", (note_id,), one=True)

    return jsonify({
        "success": True,
        "data": {
            "id": note["id"],
            "title": note["title"],
            "content": note["content"],
            "created_at": str(note["created_at"]),
            "updated_at": str(note["updated_at"])
        }
    }), 201

@notes_bp.route("/<int:note_id>", methods=["PUT"])
def update_note(note_id: int):
    """Update an existing productivity note."""
    data = request.get_json(silent=True)
    if not data or not str(data.get("title", "")).strip() or not str(data.get("content", "")).strip():
        return jsonify({
            "success": False,
            "message": "Title and content are required"
        }), 400

    title = str(data["title"]).strip()
    content = str(data["content"]).strip()

    res = execute_db(
        "UPDATE notes SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (title, content, note_id)
    )

    if res["rowcount"] == 0:
        return jsonify({
            "success": False,
            "message": "Note not found"
        }), 404

    note = query_db("SELECT id, title, content, created_at, updated_at FROM notes WHERE id = ?", (note_id,), one=True)
    return jsonify({
        "success": True,
        "data": {
            "id": note["id"],
            "title": note["title"],
            "content": note["content"],
            "created_at": str(note["created_at"]),
            "updated_at": str(note["updated_at"])
        }
    }), 200

@notes_bp.route("/<int:note_id>", methods=["DELETE"])
def delete_note(note_id: int):
    """Delete a productivity note."""
    res = execute_db("DELETE FROM notes WHERE id = ?", (note_id,))
    if res["rowcount"] == 0:
        return jsonify({
            "success": False,
            "message": "Note not found"
        }), 404

    return jsonify({
        "success": True,
        "message": "Note deleted"
    }), 200
