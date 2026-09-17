from flask import Blueprint, request, jsonify
from middleware.auth_middleware import require_safety_session
from database.db import query_db, execute_db

contact_bp = Blueprint("contacts", __name__, url_prefix="/api/contacts")

@contact_bp.route("", methods=["GET"])
@require_safety_session
def get_contacts():
    """Retrieve all trusted emergency contacts."""
    contacts = query_db("SELECT id, name, phone, relationship, created_at FROM contacts ORDER BY id ASC")
    return jsonify({
        "success": True,
        "data": [
            {
                "id": c["id"],
                "name": c["name"],
                "phone": c["phone"],
                "relationship": c["relationship"],
                "created_at": str(c["created_at"])
            }
            for c in contacts
        ]
    }), 200

@contact_bp.route("", methods=["POST"])
@require_safety_session
def create_contact():
    """Add a new trusted emergency contact."""
    data = request.get_json(silent=True)
    if not data or not str(data.get("name", "")).strip() or not str(data.get("phone", "")).strip() or not str(data.get("relationship", "")).strip():
        return jsonify({
            "success": False,
            "message": "Name, phone, and relationship are required"
        }), 400

    name = str(data["name"]).strip()
    phone = str(data["phone"]).strip()
    relationship = str(data["relationship"]).strip()

    res = execute_db(
        "INSERT INTO contacts (name, phone, relationship) VALUES (?, ?, ?)",
        (name, phone, relationship)
    )
    contact_id = res["lastrowid"]
    contact = query_db("SELECT id, name, phone, relationship, created_at FROM contacts WHERE id = ?", (contact_id,), one=True)

    return jsonify({
        "success": True,
        "data": {
            "id": contact["id"],
            "name": contact["name"],
            "phone": contact["phone"],
            "relationship": contact["relationship"],
            "created_at": str(contact["created_at"])
        }
    }), 201

@contact_bp.route("/<int:contact_id>", methods=["PUT"])
@require_safety_session
def update_contact(contact_id: int):
    """Update an existing trusted contact."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "success": False,
            "message": "Update payload is required"
        }), 400

    existing = query_db("SELECT id, name, phone, relationship FROM contacts WHERE id = ?", (contact_id,), one=True)
    if not existing:
        return jsonify({
            "success": False,
            "message": "Contact not found"
        }), 404

    name = str(data["name"]).strip() if "name" in data and str(data["name"]).strip() else existing["name"]
    phone = str(data["phone"]).strip() if "phone" in data and str(data["phone"]).strip() else existing["phone"]
    relationship = str(data["relationship"]).strip() if "relationship" in data and str(data["relationship"]).strip() else existing["relationship"]

    execute_db(
        "UPDATE contacts SET name = ?, phone = ?, relationship = ? WHERE id = ?",
        (name, phone, relationship, contact_id)
    )

    contact = query_db("SELECT id, name, phone, relationship, created_at FROM contacts WHERE id = ?", (contact_id,), one=True)
    return jsonify({
        "success": True,
        "data": {
            "id": contact["id"],
            "name": contact["name"],
            "phone": contact["phone"],
            "relationship": contact["relationship"],
            "created_at": str(contact["created_at"])
        }
    }), 200

@contact_bp.route("/<int:contact_id>", methods=["DELETE"])
@require_safety_session
def delete_contact(contact_id: int):
    """Delete a trusted contact."""
    res = execute_db("DELETE FROM contacts WHERE id = ?", (contact_id,))
    if res["rowcount"] == 0:
        return jsonify({
            "success": False,
            "message": "Contact not found"
        }), 404

    return jsonify({
        "success": True,
        "message": "Contact deleted"
    }), 200
