from flask import Blueprint, request, jsonify
from middleware.auth_middleware import require_safety_session
from services.emergency_service import process_sos

emergency_bp = Blueprint("emergency", __name__, url_prefix="/api/emergency")

@emergency_bp.route("/sos", methods=["POST"])
@require_safety_session
def trigger_sos():
    """
    Handle one-tap SOS prototype alert.
    Protected route: requires active safety session.
    Records emergency audit log in SQLite without falsely claiming live SMS delivery.
    """
    data = request.get_json(silent=True)
    if not data or "contact_ids" not in data or not isinstance(data["contact_ids"], list) or len(data["contact_ids"]) == 0:
        return jsonify({
            "success": False,
            "message": "Valid contact_ids array is required"
        }), 400

    try:
        contact_ids = [int(cid) for cid in data["contact_ids"]]
        result = process_sos(contact_ids)
        return jsonify(result), 200
    except ValueError as val_err:
        return jsonify({
            "success": False,
            "message": str(val_err)
        }), 400
    except Exception as exc:
        return jsonify({
            "success": False,
            "message": f"SOS processing failed: {str(exc)}"
        }), 500
