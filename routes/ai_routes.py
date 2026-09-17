from flask import Blueprint, request, jsonify
from middleware.auth_middleware import require_safety_session
from services.ai_service import generate_safety_plan

ai_bp = Blueprint("ai", __name__, url_prefix="/api/ai")

@ai_bp.route("/safety-plan", methods=["POST"])
@require_safety_session
def safety_plan():
    """
    Generate an actionable, calm, supportive personal safety plan using Gemini AI.
    Protected route: requires unlocked safety session.
    """
    data = request.get_json(silent=True)
    if not data or not str(data.get("situation", "")).strip():
        return jsonify({
            "success": False,
            "message": "Situation description is required"
        }), 400

    situation = str(data["situation"]).strip()
    urgency = str(data.get("urgency", "medium")).strip()
    location_context = str(data.get("location_context", "")).strip()
    preferences = str(data.get("preferences", "")).strip()

    try:
        plan_steps = generate_safety_plan(
            situation=situation,
            urgency=urgency,
            location_context=location_context,
            preferences=preferences
        )
        return jsonify({
            "success": True,
            "plan": plan_steps
        }), 200
    except Exception as exc:
        return jsonify({
            "success": False,
            "message": "Failed to generate safety plan. Please try again or consult trusted contacts."
        }), 500
