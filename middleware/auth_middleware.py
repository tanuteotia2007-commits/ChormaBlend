from functools import wraps
from flask import session, jsonify

def require_safety_session(f):
    """
    Middleware decorator protecting safety-related routes.
    Checks if the current Flask session has safety_unlocked set to True.
    Returns HTTP 401 with standard JSON error response if unauthenticated.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("safety_unlocked", False):
            return jsonify({
                "success": False,
                "message": "Authentication required"
            }), 401
        return f(*args, **kwargs)
    return decorated_function
