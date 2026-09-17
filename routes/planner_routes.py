from flask import Blueprint, request, jsonify
from database.db import query_db, execute_db

planner_bp = Blueprint("planner", __name__, url_prefix="/api/planner")

@planner_bp.route("", methods=["GET"])
def get_planner_items():
    """Retrieve all productivity planner items."""
    items = query_db("SELECT id, title, date, description, created_at FROM planner ORDER BY date ASC, id DESC")
    return jsonify({
        "success": True,
        "data": [
            {
                "id": it["id"],
                "title": it["title"],
                "date": it["date"],
                "description": it["description"] or "",
                "created_at": str(it["created_at"])
            }
            for it in items
        ]
    }), 200

@planner_bp.route("", methods=["POST"])
def create_planner_item():
    """Create a new productivity planner item."""
    data = request.get_json(silent=True)
    if not data or not str(data.get("title", "")).strip() or not str(data.get("date", "")).strip():
        return jsonify({
            "success": False,
            "message": "Title and date are required"
        }), 400

    title = str(data["title"]).strip()
    date_val = str(data["date"]).strip()
    description = str(data.get("description", "")).strip()

    res = execute_db(
        "INSERT INTO planner (title, date, description) VALUES (?, ?, ?)",
        (title, date_val, description)
    )
    item_id = res["lastrowid"]
    item = query_db("SELECT id, title, date, description, created_at FROM planner WHERE id = ?", (item_id,), one=True)

    return jsonify({
        "success": True,
        "data": {
            "id": item["id"],
            "title": item["title"],
            "date": item["date"],
            "description": item["description"] or "",
            "created_at": str(item["created_at"])
        }
    }), 201

@planner_bp.route("/<int:item_id>", methods=["PUT"])
def update_planner_item(item_id: int):
    """Update an existing productivity planner item."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "success": False,
            "message": "Update payload is required"
        }), 400

    existing = query_db("SELECT id, title, date, description FROM planner WHERE id = ?", (item_id,), one=True)
    if not existing:
        return jsonify({
            "success": False,
            "message": "Planner item not found"
        }), 404

    title = str(data["title"]).strip() if "title" in data and str(data["title"]).strip() else existing["title"]
    date_val = str(data["date"]).strip() if "date" in data and str(data["date"]).strip() else existing["date"]
    description = str(data["description"]).strip() if "description" in data else existing["description"]

    execute_db(
        "UPDATE planner SET title = ?, date = ?, description = ? WHERE id = ?",
        (title, date_val, description, item_id)
    )

    item = query_db("SELECT id, title, date, description, created_at FROM planner WHERE id = ?", (item_id,), one=True)
    return jsonify({
        "success": True,
        "data": {
            "id": item["id"],
            "title": item["title"],
            "date": item["date"],
            "description": item["description"] or "",
            "created_at": str(item["created_at"])
        }
    }), 200

@planner_bp.route("/<int:item_id>", methods=["DELETE"])
def delete_planner_item(item_id: int):
    """Delete a productivity planner item."""
    res = execute_db("DELETE FROM planner WHERE id = ?", (item_id,))
    if res["rowcount"] == 0:
        return jsonify({
            "success": False,
            "message": "Planner item not found"
        }), 404

    return jsonify({
        "success": True,
        "message": "Planner item deleted"
    }), 200
