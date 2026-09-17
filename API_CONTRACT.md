# API_CONTRACT.md — Invisible Help / Chroma Blend

This is the shared contract between frontend (Shab, Ankit) and backend
(Vaishnavi, Tanu). Do not rename endpoints or fields without updating this
file and telling the team first.

All responses are JSON. All safety-area endpoints rely on the Flask session
cookie — the frontend always sends `credentials: 'include'`.

Generic shapes:
- Success: `{ "success": true, "data": ... }` (or endpoint-specific fields, noted below)
- Error: `{ "success": false, "message": "human readable message" }`

---

## AUTH

### POST /api/auth/unlock
Auth required: no
Request: `{ "passcode": "string" }`
Success: `{ "success": true, "message": "Access granted" }` — also sets the Flask session cookie
Error: `{ "success": false, "message": "Invalid passcode" }`

### GET /api/auth/status
Auth required: session cookie (no error if absent)
Success: `{ "authenticated": true }` or `{ "authenticated": false }`

### POST /api/auth/exit
Auth required: session cookie
Success: `{ "success": true }` — invalidates the safety session

---

## PRODUCTIVITY (visible workspace — no auth required)

### Notes
- `GET /api/notes` → `{ "success": true, "data": [{ "id": 1, "content": "..." }] }`
- `POST /api/notes` → body `{ "content": "string" }` → `{ "success": true, "data": { "id": 1, "content": "..." } }`
- `PUT /api/notes/{note_id}` → body `{ "content": "string" }` → `{ "success": true }`
- `DELETE /api/notes/{note_id}` → `{ "success": true }`

### To-Do
- `GET /api/todos` → `{ "success": true, "data": [{ "id": 1, "task": "...", "completed": false }] }`
- `POST /api/todos` → body `{ "task": "string", "completed": false }` → `{ "success": true, "data": {...} }`
- `PUT /api/todos/{todo_id}` → body `{ "completed": true }` (partial update) → `{ "success": true }`
- `DELETE /api/todos/{todo_id}` → `{ "success": true }`

### Planner
- `GET /api/planner` → `{ "success": true, "data": [{ "id": 1, "title": "...", "scheduled_for": "2026-09-20" }] }`
- `POST /api/planner` → body `{ "title": "string", "scheduled_for": "YYYY-MM-DD" | null }` → `{ "success": true, "data": {...} }`
- `PUT /api/planner/{item_id}` → body (any subset of fields) → `{ "success": true }`
- `DELETE /api/planner/{item_id}` → `{ "success": true }`

---

## AI — Safety Planner

Auth required: session cookie

### POST /api/ai/safety-plan
Request:
```json
{
  "situation": "string (required)",
  "urgency": "low | medium | high",
  "location_context": "string (optional)",
  "preferences": "string (optional)"
}
```
Success: `{ "success": true, "plan": ["step one", "step two", "..."] }`
Error / fallback: `{ "success": false, "message": "The planning service is unavailable right now." }`

---

## DOCUMENTS — Secure Document Vault

Auth required: session cookie

- `GET /api/documents` → `{ "success": true, "data": [{ "id": 1, "filename": "id.pdf", "created_at": "..." }] }`
- `POST /api/documents` → `multipart/form-data`, field name **`file`** → `{ "success": true, "data": { "id": 1, "filename": "..." } }`
- `DELETE /api/documents/{document_id}` → `{ "success": true }`
- `GET /api/documents/{document_id}/download` → raw file stream (not JSON)

Limits: max file size enforced server-side (frontend soft-checks 10MB; backend is the real limit — keep both in sync).

---

## CONTACTS — Trusted Contacts

Auth required: session cookie

- `GET /api/contacts` → `{ "success": true, "data": [{ "id": 1, "name": "...", "phone": "...", "relationship": "..." }] }`
- `POST /api/contacts` → body `{ "name": "string", "phone": "string", "relationship": "string (optional)" }` → `{ "success": true, "data": {...} }`
- `PUT /api/contacts/{contact_id}` → body (any subset) → `{ "success": true }`
- `DELETE /api/contacts/{contact_id}` → `{ "success": true }`

---

## EMERGENCY — SOS

Auth required: session cookie

### POST /api/emergency/sos
Request: `{ "contact_ids": [1, 2] }`
Success (prototype/demo mode — MUST be labeled as such by backend message):
`{ "success": true, "message": "Prototype SOS recorded — no real message was sent." }`
Error: `{ "success": false, "message": "..." }`

Frontend never claims a real message was delivered beyond what this response says.

---

## Error codes the frontend handles explicitly
400, 401, 403, 404, 413 (file too large), 500, and network failure (no response at all).

## Changing this contract
1. Edit this file first.
2. Post the diff to the team channel.
3. Update `src/services/api.js` (frontend) and the Flask routes (backend) together.
4. Retest the affected flow end-to-end before merging to `main`.
