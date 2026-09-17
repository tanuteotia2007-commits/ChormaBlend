import os
import json
import logging
from flask import current_app

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a calm, supportive, and practical personal safety planning assistant for women.
Your guidance must be:
- Strictly non-confrontational and de-escalating.
- Practical, discreet, and actionable.
- Focused on personal safety, communication with trusted circles, and situational awareness.
- Never encourage violence, confrontation, or dangerous behavior.
- Do NOT pretend to be an emergency service, police officer, lawyer, or physician.

Given the user's situation, urgency level, location context, and preferences, generate a concise list of 4 to 6 concrete, calm safety steps.
Return ONLY a valid JSON array of strings, with no surrounding markdown formatting or additional explanation.
Example format:
[
  "Step 1 description...",
  "Step 2 description...",
  "Step 3 description..."
]
"""

def get_fallback_plan(situation: str, urgency: str, location_context: str) -> list[str]:
    """Provide a reliable, practical fallback plan if Gemini API is unreachable or unconfigured."""
    urgency_lower = (urgency or "").lower()
    loc_lower = (location_context or "").lower()

    if "high" in urgency_lower or "immediate" in urgency_lower:
        return [
            "Move calmly toward a well-lit, populated area with visible staff, security, or bystanders.",
            "Discreetly open your trusted contacts list and share your live location or send a pre-set check-in message.",
            "Keep your phone accessible in your hand or pocket with emergency speed-dial ready.",
            "Avoid engaging or escalating with anyone creating tension; focus on exiting to a safe zone.",
            "If in immediate physical danger, contact official local emergency dispatch without hesitation."
        ]
    elif "transit" in loc_lower or "commute" in loc_lower or "station" in loc_lower:
        return [
            "Position yourself near the conductor, driver, station attendant, or groups of fellow commuters.",
            "Keep one ear free if listening to audio to maintain 360-degree situational awareness.",
            "Send an estimated arrival time and route updates to a trusted contact.",
            "Have your transport card or exit strategy ready before reaching your stop to avoid delays."
        ]
    else:
        return [
            "Take a quiet moment to evaluate your immediate exits, lighting, and proximity to trusted people.",
            "Verify that your essential documents and emergency contacts are updated in your secure storage.",
            "Establish a routine check-in schedule with a close friend or family member.",
            "Identify safe intermediary locations along your typical routes (e.g., open pharmacies, staffed stores, community centers)."
        ]

def generate_safety_plan(situation: str, urgency: str = "medium", location_context: str = "", preferences: str = "") -> list[str]:
    """Generate a structured safety plan using Gemini API, or gracefully fall back to default safety rules."""
    api_key = current_app.config.get("GEMINI_API_KEY", "").strip()

    if not api_key:
        logger.warning("GEMINI_API_KEY not configured. Using fallback safety guidance.")
        return get_fallback_plan(situation, urgency, location_context)

    prompt = f"""Situation: {situation}
Urgency Level: {urgency}
Location Context: {location_context}
Preferences: {preferences}

Generate 4 to 6 practical, calm safety steps formatted strictly as a JSON array of strings:"""

    # Attempt calling the Gemini API
    try:
        # Try google.genai client first
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"{SYSTEM_PROMPT}\n\n{prompt}"
            )
            raw_text = response.text.strip()
        except ImportError:
            # Fall back to google.generativeai if installed
            import google.generativeai as genai_legacy
            genai_legacy.configure(api_key=api_key)
            model = genai_legacy.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=SYSTEM_PROMPT
            )
            response = model.generate_content(prompt)
            raw_text = response.text.strip()

        # Parse JSON output from model
        # Remove potential markdown triple backticks if present
        if raw_text.startswith("```"):
            lines = raw_text.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            raw_text = "\n".join(lines).strip()

        parsed_plan = json.loads(raw_text)
        if isinstance(parsed_plan, list) and all(isinstance(step, str) for step in parsed_plan):
            return parsed_plan
        else:
            logger.warning("Gemini output was not a valid list of strings: %s", raw_text)
            return get_fallback_plan(situation, urgency, location_context)

    except Exception as exc:
        logger.error("Gemini API call encountered an error: %s", exc)
        return get_fallback_plan(situation, urgency, location_context)
