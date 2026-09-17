# Invisible Help — Backend ("Chroma Blend")

Privacy-first women's safety web prototype disguised as a normal productivity website.

---

## 📁 Project Structure

```
backend/
├── app.py                     # Flask application factory, routes, and error handling
├── config.py                  # Configuration loader (.env)
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Standard Python gitignore (protects secrets and database)
├── API_CONTRACT.md            # Complete REST API specification
├── DATABASE_SCHEMA.md         # Canonical SQLite database schema
├── database/
│   └── db.py                  # Tanu's SQLite connection & initialization layer
├── middleware/
│   └── auth_middleware.py     # @require_safety_session decorator
├── services/
│   ├── auth_service.py        # Passcode checking & session management
│   ├── ai_service.py          # Gemini AI Safety Planner + fallback
│   ├── document_service.py    # Local file vault & SQLite metadata
│   └── emergency_service.py   # Contact verification & SOS logging
├── routes/
│   ├── auth_routes.py         # /api/auth (unlock, status, exit)
│   ├── notes_routes.py        # /api/notes (Notes CRUD)
│   ├── todo_routes.py         # /api/todos (Todos CRUD)
│   ├── planner_routes.py      # /api/planner (Planner CRUD)
│   ├── ai_routes.py           # /api/ai/safety-plan (Protected)
│   ├── document_routes.py     # /api/documents (Protected)
│   ├── contact_routes.py      # /api/contacts (Protected)
│   └── emergency_routes.py    # /api/emergency/sos (Protected)
├── storage/
│   └── documents/             # Vault storage
└── tests/
    └── test_backend.py        # Complete pytest test suite
```

---

## 🚀 Quick Setup & Run in VS Code

### 1. Create Virtual Environment & Install Dependencies
```bash
# In terminal inside backend folder:
python -m venv venv

# Windows activate:
.\venv\Scripts\activate

# Mac/Linux activate:
# source venv/bin/activate

# Install requirements:
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Update `.env` if you have a Gemini API key (optional, fallback is built-in). Default passcode: `4321`.

### 3. Run Automated Tests
```bash
pytest tests/test_backend.py -v
```

### 4. Run the Backend Server
```bash
python app.py
```
Server runs on: `http://localhost:5000`  
Health check: `http://localhost:5000/api/health`

---

## 🐙 Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit: Real Flask backend for Invisible Help"
git branch -M main
git remote add origin <YOUR_GITHUB_REPO_URL>
git push -u origin main
```
*(Note: `.env` and `invisible_help.db` are ignored by `.gitignore` so secrets are never pushed).*
