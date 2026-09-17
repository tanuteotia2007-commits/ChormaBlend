# API_CONTRACT.md
Shared REST API specification between React Frontend (Shab & Ankit) and Flask Backend (Vaishnavi & Senior Backend).

## Base URL
- Development: `http://localhost:5000`

## Headers & Session Rules
- Content-Type: `application/json` (except for `/api/documents` file upload which uses `multipart/form-data`)
- Authentication / Session: Cookie-based Flask session. Frontend calls must always specify `credentials: "include"` in `fetch` (or `withCredentials: true` in `axios`).
- Protected routes require an active safety session (unlocked via `/api/auth/unlock`). If unauthenticated, all protected routes return `HTTP 401 Unauthorized`.

---

## 1. Health Check
### `GET /api/health`
- **Auth**: None
- **Success Response (200 OK)**:
```json
{
  "success": true,
  "message": "Backend is running"
}
```

---

## 2. Authentication & Stealth Access
### `POST /api/auth/unlock`
- **Auth**: None
- **Trigger**: Long-press on "Chroma Blend" logo/header in frontend.
- **Request Body**:
```json
{
  "passcode": "4321"
}
```
- **Success Response (200 OK)**:
```json
{
  "success": true,
  "message": "Access granted"
}
```
- **Error Responses**:
  - Missing passcode: `400 Bad Request`
    ```json
    {"success": false, "message": "Passcode is required"}
    ```
  - Invalid passcode: `401 Unauthorized`
    ```json
    {"success": false, "message": "Invalid passcode"}
    ```

### `GET /api/auth/status`
- **Auth**: None
- **Success Response (200 OK)**:
```json
{
  "authenticated": true
}
```
*(or `{"authenticated": false}` if no active safety session)*

### `POST /api/auth/exit`
- **Auth**: None
- **Trigger**: Quick Exit button click.
- **Success Response (200 OK)**:
```json
{
  "success": true,
  "message": "Safety session closed"
}
```

---

## 3. Disguised Productivity Workspace (Public)

### Notes API
#### `GET /api/notes`
- **Success Response (200 OK)**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "Meeting Notes",
      "content": "Discuss color palette and typography.",
      "created_at": "2026-09-17 11:45:00",
      "updated_at": "2026-09-17 11:45:00"
    }
  ]
}
```

#### `POST /api/notes`
- **Request Body**:
```json
{
  "title": "Design Specs",
  "content": "Hex codes: #4A90E2, #50E3C2"
}
```
- **Success Response (201 Created)**:
```json
{
  "success": true,
  "data": {
    "id": 2,
    "title": "Design Specs",
    "content": "Hex codes: #4A90E2, #50E3C2",
    "created_at": "2026-09-17 11:46:00",
    "updated_at": "2026-09-17 11:46:00"
  }
}
```
- **Error Response (400 Bad Request)**:
```json
{
  "success": false,
  "message": "Title and content are required"
}
```

#### `PUT /api/notes/<id>`
- **Request Body**:
```json
{
  "title": "Updated Specs",
  "content": "Updated hex codes."
}
```
- **Success Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    "id": 2,
    "title": "Updated Specs",
    "content": "Updated hex codes.",
    "created_at": "2026-09-17 11:46:00",
    "updated_at": "2026-09-17 11:47:00"
  }
}
```
- **Error Response (404 Not Found)**:
```json
{
  "success": false,
  "message": "Note not found"
}
```

#### `DELETE /api/notes/<id>`
- **Success Response (200 OK)**:
```json
{
  "success": true,
  "message": "Note deleted"
}
```
- **Error Response (404 Not Found)**:
```json
{
  "success": false,
  "message": "Note not found"
}
```

---

### To-Do API
#### `GET /api/todos`
- **Success Response (200 OK)**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "Review mockup sketches",
      "completed": false,
      "created_at": "2026-09-17 11:45:00"
    }
  ]
}
```

#### `POST /api/todos`
- **Request Body**:
```json
{
  "title": "Wireframe export",
  "completed": false
}
```
- **Success Response (201 Created)**:
```json
{
  "success": true,
  "data": {
    "id": 2,
    "title": "Wireframe export",
    "completed": false,
    "created_at": "2026-09-17 11:46:00"
  }
}
```

#### `PUT /api/todos/<id>`
- **Request Body**:
```json
{
  "title": "Wireframe export",
  "completed": true
}
```
- **Success Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    "id": 2,
    "title": "Wireframe export",
    "completed": true,
    "created_at": "2026-09-17 11:46:00"
  }
}
```

#### `DELETE /api/todos/<id>`
- **Success Response (200 OK)**:
```json
{
  "success": true,
  "message": "Todo deleted"
}
```

---

### Planner API
#### `GET /api/planner`
- **Success Response (200 OK)**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "Sprint Planning",
      "date": "2026-09-18",
      "description": "Align on sprint deliverables.",
      "created_at": "2026-09-17 11:45:00"
    }
  ]
}
```

#### `POST /api/planner`
- **Request Body**:
```json
{
  "title": "Design Sync",
  "date": "2026-09-19",
  "description": "Review brand guidelines."
}
```
- **Success Response (201 Created)**:
```json
{
  "success": true,
  "data": {
    "id": 2,
    "title": "Design Sync",
    "date": "2026-09-19",
    "description": "Review brand guidelines.",
    "created_at": "2026-09-17 11:46:00"
  }
}
```

#### `PUT /api/planner/<id>`
- **Request Body**:
```json
{
  "title": "Design Sync (Rescheduled)",
  "date": "2026-09-20",
  "description": "Review brand guidelines."
}
```
- **Success Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    "id": 2,
    "title": "Design Sync (Rescheduled)",
    "date": "2026-09-20",
    "description": "Review brand guidelines.",
    "created_at": "2026-09-17 11:46:00"
  }
}
```

#### `DELETE /api/planner/<id>`
- **Success Response (200 OK)**:
```json
{
  "success": true,
  "message": "Planner item deleted"
}
```

---

## 4. Protected Safety Dashboard APIs
*(All endpoints below return `401 Unauthorized` with `{"success": false, "message": "Authentication required"}` if safety session is not active)*

### AI Safety Planner
#### `POST /api/ai/safety-plan`
- **Auth**: Required
- **Request Body**:
```json
{
  "situation": "Feeling unsafe during late commute",
  "urgency": "medium",
  "location_context": "transit station",
  "preferences": "discreet actions"
}
```
- **Success Response (200 OK)**:
```json
{
  "success": true,
  "plan": [
    "Stay in well-lit areas with transit staff or other passengers nearby.",
    "Keep emergency contacts on speed dial and share your live transit route with a trusted friend.",
    "Keep phone charged, avoid headphones in both ears, and trust your intuition if you feel uncomfortable.",
    "Identify nearest customer service booths or emergency help kiosks at the next stop."
  ]
}
```

---

### Secure Document Vault
#### `GET /api/documents`
- **Auth**: Required
- **Success Response (200 OK)**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "filename": "lease_agreement.pdf",
      "file_size": 245760,
      "mime_type": "application/pdf",
      "created_at": "2026-09-17 11:50:00"
    }
  ]
}
```

#### `POST /api/documents`
- **Auth**: Required
- **Headers**: `Content-Type: multipart/form-data`
- **Body**: Form data key: `file`
- **Allowed Extensions**: `pdf`, `png`, `jpg`, `jpeg`, `doc`, `docx`
- **Max File Size**: 16 MB
- **Success Response (201 Created)**:
```json
{
  "success": true,
  "data": {
    "id": 2,
    "filename": "identification_card.png",
    "file_size": 512000,
    "mime_type": "image/png",
    "created_at": "2026-09-17 11:52:00"
  }
}
```
- **Error Responses**:
  - Missing file: `400 Bad Request` (`{"success": false, "message": "No file part in request"}`)
  - Disallowed type: `400 Bad Request` (`{"success": false, "message": "File type not allowed"}`)
  - Oversized file: `413 Payload Too Large` (`{"success": false, "message": "File exceeds maximum allowed size (16MB)"}`)

#### `GET /api/documents/<id>/download`
- **Auth**: Required
- **Success Response (200 OK)**: Binary file stream with `Content-Disposition: attachment; filename="..."`
- **Error Response (404 Not Found)**:
```json
{
  "success": false,
  "message": "Document not found"
}
```

#### `DELETE /api/documents/<id>`
- **Auth**: Required
- **Success Response (200 OK)**:
```json
{
  "success": true,
  "message": "Document deleted"
}
```

---

### Trusted Contacts
#### `GET /api/contacts`
- **Auth**: Required
- **Success Response (200 OK)**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Sarah Jenkins",
      "phone": "+1-555-0199",
      "relationship": "Sister",
      "created_at": "2026-09-17 11:45:00"
    }
  ]
}
```

#### `POST /api/contacts`
- **Auth**: Required
- **Request Body**:
```json
{
  "name": "Alex Rivera",
  "phone": "+1-555-0144",
  "relationship": "Trusted Friend"
}
```
- **Success Response (201 Created)**:
```json
{
  "success": true,
  "data": {
    "id": 2,
    "name": "Alex Rivera",
    "phone": "+1-555-0144",
    "relationship": "Trusted Friend",
    "created_at": "2026-09-17 11:53:00"
  }
}
```

#### `PUT /api/contacts/<id>`
- **Auth**: Required
- **Request Body**:
```json
{
  "name": "Alex Rivera",
  "phone": "+1-555-0188",
  "relationship": "Best Friend"
}
```
- **Success Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    "id": 2,
    "name": "Alex Rivera",
    "phone": "+1-555-0188",
    "relationship": "Best Friend",
    "created_at": "2026-09-17 11:53:00"
  }
}
```

#### `DELETE /api/contacts/<id>`
- **Auth**: Required
- **Success Response (200 OK)**:
```json
{
  "success": true,
  "message": "Contact deleted"
}
```

---

### Emergency SOS Trigger
#### `POST /api/emergency/sos`
- **Auth**: Required
- **Request Body**:
```json
{
  "contact_ids": [1, 2]
}
```
- **Success Response (200 OK)**:
```json
{
  "success": true,
  "message": "SOS request processed",
  "event_id": 1,
  "status": "prototype_processed"
}
```
- **Error Responses**:
  - Missing/invalid IDs: `400 Bad Request` (`{"success": false, "message": "Valid contact_ids array is required"}`)
