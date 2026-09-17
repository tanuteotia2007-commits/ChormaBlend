import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

class Config:
    """Centralized application configuration."""
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-safety-secret-key-987654321")
    SAFETY_PASSCODE = os.getenv("SAFETY_PASSCODE", "4321").strip()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173").rstrip("/")
    
    # Storage settings
    STORAGE_DIR = BASE_DIR / "storage"
    UPLOAD_FOLDER = STORAGE_DIR / "documents"
    DATABASE_PATH = STORAGE_DIR / "invisible_help.db"
    
    # 16 MB maximum file upload limit
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "doc", "docx"}
    
    # Session cookie configuration for cross-port localhost dev
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False  # False allows cookies over HTTP on localhost
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours
