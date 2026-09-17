from flask import Blueprint, request, jsonify
from services.auth_service import verify_passcode, unlock_safety_session, clear_safety_session, is_safety_unlocked

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.route("/unlock", methods=["POST"])
def unlock():
    """Handle secret passcode authentication to unlock the safety dashboard."""
    data = request.get_json(silent=True)
    if not data or "passcode" not in data or not str(data["passcode"]).strip():
        return jsonify({
            "success": False,
            "message": "Passcode is required"
        }), 400

    passcode = str(data["passcode"]).strip()
    if verify_passcode(passcode):
        unlock_safety_session()
        return jsonify({
            "success": True,
            "message": "Access granted"
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": "Invalid passcode"
        }), 401

@auth_bp.route("/status", methods=["GET"])
def status():
    """Return whether current session has safety access."""
    return jsonify({
        "authenticated": is_safety_unlocked()
    }), 200

@auth_bp.route("/exit", methods=["POST"])
def exit_safety():
    """Quick exit: immediately invalidate safety session and return success."""
    clear_safety_session()
    return jsonify({
        "success": True,
        "message": "Safety session closed"
    }), 200
