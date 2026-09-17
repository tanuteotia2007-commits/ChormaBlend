import io
import pytest
from app import create_app

@pytest.fixture
def app(tmp_path):
    """Create test application instance with temporary database and storage."""
    test_storage = tmp_path / "storage"
    test_upload = test_storage / "documents"
    test_db = test_storage / "test_invisible_help.db"

    test_config = {
        "TESTING": True,
        "STORAGE_DIR": test_storage,
        "UPLOAD_FOLDER": test_upload,
        "DATABASE_PATH": test_db,
        "SAFETY_PASSCODE": "4321",
        "GEMINI_API_KEY": ""  # Test fallback behavior cleanly
    }

    application = create_app(test_config=test_config)
    yield application

@pytest.fixture
def client(app):
    """Test client preserving cookies across requests."""
    return app.test_client()

# ==========================================
# 1. Health Check Test
# ==========================================
def test_health_check(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "running" in data["message"].lower()

# ==========================================
# 2. Notes CRUD Tests
# ==========================================
def test_notes_crud(client):
    # 1. List initially empty
    res = client.get("/api/notes")
    assert res.status_code == 200
    assert res.get_json()["data"] == []

    # 2. Validation error on missing fields
    res = client.post("/api/notes", json={"title": "No content"})
    assert res.status_code == 400

    # 3. Create note
    res = client.post("/api/notes", json={"title": "Meeting Notes", "content": "Review palette"})
    assert res.status_code == 201
    created = res.get_json()["data"]
    assert created["title"] == "Meeting Notes"
    note_id = created["id"]

    # 4. Update note
    res = client.put(f"/api/notes/{note_id}", json={"title": "Updated Notes", "content": "Updated content"})
    assert res.status_code == 200
    assert res.get_json()["data"]["title"] == "Updated Notes"

    # 5. Delete note
    res = client.delete(f"/api/notes/{note_id}")
    assert res.status_code == 200
    assert res.get_json()["success"] is True

    # 6. Delete again -> 404
    res = client.delete(f"/api/notes/{note_id}")
    assert res.status_code == 404

# ==========================================
# 3. Todos CRUD Tests
# ==========================================
def test_todos_crud(client):
    # Create todo
    res = client.post("/api/todos", json={"title": "Design layout", "completed": False})
    assert res.status_code == 201
    todo_id = res.get_json()["data"]["id"]

    # List todos
    res = client.get("/api/todos")
    assert res.status_code == 200
    assert len(res.get_json()["data"]) == 1

    # Toggle completion
    res = client.put(f"/api/todos/{todo_id}", json={"completed": True})
    assert res.status_code == 200
    assert res.get_json()["data"]["completed"] is True

    # Delete todo
    res = client.delete(f"/api/todos/{todo_id}")
    assert res.status_code == 200

# ==========================================
# 4. Planner CRUD Tests
# ==========================================
def test_planner_crud(client):
    # Create planner item
    res = client.post("/api/planner", json={"title": "Design Review", "date": "2026-09-20", "description": "UI review"})
    assert res.status_code == 201
    item_id = res.get_json()["data"]["id"]

    # Read planner items
    res = client.get("/api/planner")
    assert res.status_code == 200
    assert len(res.get_json()["data"]) == 1

    # Update item
    res = client.put(f"/api/planner/{item_id}", json={"title": "Updated Review", "date": "2026-09-21"})
    assert res.status_code == 200
    assert res.get_json()["data"]["title"] == "Updated Review"

    # Delete item
    res = client.delete(f"/api/planner/{item_id}")
    assert res.status_code == 200

# ==========================================
# 5. Auth & Stealth Access Tests
# ==========================================
def test_auth_flow(client):
    # Check initial status -> unauthenticated
    res = client.get("/api/auth/status")
    assert res.status_code == 200
    assert res.get_json()["authenticated"] is False

    # Try invalid passcode
    res = client.post("/api/auth/unlock", json={"passcode": "wrong_pass"})
    assert res.status_code == 401
    assert res.get_json()["success"] is False

    # Unlock with valid passcode
    res = client.post("/api/auth/unlock", json={"passcode": "4321"})
    assert res.status_code == 200
    assert res.get_json()["success"] is True

    # Check status -> authenticated
    res = client.get("/api/auth/status")
    assert res.status_code == 200
    assert res.get_json()["authenticated"] is True

    # Quick exit
    res = client.post("/api/auth/exit")
    assert res.status_code == 200
    assert res.get_json()["success"] is True

    # Check status after exit -> unauthenticated
    res = client.get("/api/auth/status")
    assert res.status_code == 200
    assert res.get_json()["authenticated"] is False

# ==========================================
# 6. Protected Routes Auth Enforcement
# ==========================================
def test_protected_routes_unauthenticated(client):
    # Without session, all safety endpoints must return 401
    res = client.get("/api/documents")
    assert res.status_code == 401

    res = client.get("/api/contacts")
    assert res.status_code == 401

    res = client.post("/api/emergency/sos", json={"contact_ids": [1]})
    assert res.status_code == 401

    res = client.post("/api/ai/safety-plan", json={"situation": "late walk"})
    assert res.status_code == 401

# ==========================================
# 7. Contacts CRUD (Authenticated)
# ==========================================
def test_contacts_crud(client):
    # Unlock safety dashboard first
    client.post("/api/auth/unlock", json={"passcode": "4321"})

    # Create contact
    res = client.post("/api/contacts", json={"name": "Sarah Jenkins", "phone": "+1-555-0199", "relationship": "Sister"})
    assert res.status_code == 201
    contact_id = res.get_json()["data"]["id"]

    # List contacts
    res = client.get("/api/contacts")
    assert res.status_code == 200
    assert len(res.get_json()["data"]) == 1

    # Update contact
    res = client.put(f"/api/contacts/{contact_id}", json={"name": "Sarah Jenkins", "phone": "+1-555-9999", "relationship": "Sister"})
    assert res.status_code == 200
    assert res.get_json()["data"]["phone"] == "+1-555-9999"

    # Delete contact
    res = client.delete(f"/api/contacts/{contact_id}")
    assert res.status_code == 200

# ==========================================
# 8. Emergency SOS (Authenticated)
# ==========================================
def test_emergency_sos(client):
    # Unlock safety dashboard
    client.post("/api/auth/unlock", json={"passcode": "4321"})

    # Add trusted contact
    c_res = client.post("/api/contacts", json={"name": "Alex", "phone": "+1-555-1111", "relationship": "Friend"})
    contact_id = c_res.get_json()["data"]["id"]

    # Trigger SOS with valid contact
    res = client.post("/api/emergency/sos", json={"contact_ids": [contact_id]})
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["status"] == "prototype_processed"
    assert "event_id" in data

    # Trigger SOS with nonexistent contact -> 400
    res = client.post("/api/emergency/sos", json={"contact_ids": [9999]})
    assert res.status_code == 400

# ==========================================
# 9. Document Vault (Authenticated)
# ==========================================
def test_document_vault(client):
    # Unlock safety dashboard
    client.post("/api/auth/unlock", json={"passcode": "4321"})

    # Disallowed file extension (.exe)
    bad_file = (io.BytesIO(b"binary data"), "virus.exe")
    res = client.post("/api/documents", data={"file": bad_file}, content_type="multipart/form-data")
    assert res.status_code == 400

    # Valid file upload (.pdf)
    good_file = (io.BytesIO(b"%PDF-1.4 simulated pdf document content"), "lease_contract.pdf")
    res = client.post("/api/documents", data={"file": good_file}, content_type="multipart/form-data")
    assert res.status_code == 201
    doc_id = res.get_json()["data"]["id"]

    # List documents
    res = client.get("/api/documents")
    assert res.status_code == 200
    assert len(res.get_json()["data"]) == 1

    # Download document
    res = client.get(f"/api/documents/{doc_id}/download")
    assert res.status_code == 200
    assert b"%PDF-1.4" in res.data

    # Delete document
    res = client.delete(f"/api/documents/{doc_id}")
    assert res.status_code == 200

    # Verify deleted
    res = client.get(f"/api/documents/{doc_id}/download")
    assert res.status_code == 404

# ==========================================
# 10. AI Safety Planner (Authenticated)
# ==========================================
def test_ai_safety_planner(client):
    # Unlock safety dashboard
    client.post("/api/auth/unlock", json={"passcode": "4321"})

    # Request plan
    res = client.post("/api/ai/safety-plan", json={
        "situation": "Walking home alone at night through quiet train station",
        "urgency": "medium",
        "location_context": "transit station",
        "preferences": "discreet"
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert isinstance(data["plan"], list)
    assert len(data["plan"]) > 0
    assert all(isinstance(step, str) for step in data["plan"])
