import json
from database.db import query_db, execute_db

def process_sos(contact_ids: list[int]):
    """
    Validate contact IDs against the database and record a prototype emergency event.
    Clearly notes prototype processing without claiming live SMS delivery.
    """
    if not isinstance(contact_ids, list) or len(contact_ids) == 0:
        raise ValueError("Valid contact_ids list is required")

    # Verify existing contacts in SQLite
    placeholders = ",".join("?" for _ in contact_ids)
    existing_contacts = query_db(
        f"SELECT id, name, phone FROM contacts WHERE id IN ({placeholders})",
        tuple(contact_ids)
    )

    if not existing_contacts:
        raise ValueError("None of the specified contact IDs exist in trusted contacts")

    # Record prototype emergency event in database
    contact_ids_json = json.dumps([c["id"] for c in existing_contacts])
    res = execute_db(
        "INSERT INTO emergency_events (contact_ids, status) VALUES (?, ?)",
        (contact_ids_json, "prototype_processed")
    )

    return {
        "success": True,
        "message": "SOS request processed",
        "event_id": res["lastrowid"],
        "status": "prototype_processed"
    }
