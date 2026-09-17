import hmac
from flask import session, current_app

def verify_passcode(input_passcode: str) -> bool:
    """Compare input passcode with configured SAFETY_PASSCODE in a timing-safe manner."""
    if not input_passcode:
        return False
    configured_passcode = current_app.config.get("SAFETY_PASSCODE", "4321")
    return hmac.compare_digest(str(input_passcode).strip(), str(configured_passcode).strip())

def unlock_safety_session():
    """Mark the session as authenticated for the safety dashboard."""
    session["safety_unlocked"] = True
    session.permanent = True

def clear_safety_session():
    """Clear safety authentication flags from the session."""
    session.pop("safety_unlocked", None)

def is_safety_unlocked() -> bool:
    """Check if the current session has safety access."""
    return bool(session.get("safety_unlocked", False))
