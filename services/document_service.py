import os
import uuid
import mimetypes
from pathlib import Path
from werkzeug.utils import secure_filename
from flask import current_app
from database.db import query_db, execute_db

def allowed_file(filename: str) -> bool:
    """Check if the filename has an allowed extension."""
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in current_app.config["ALLOWED_EXTENSIONS"]

def list_documents():
    """Retrieve all document metadata from SQLite."""
    rows = query_db("SELECT id, original_filename, file_size, mime_type, created_at FROM documents ORDER BY id DESC")
    return [
        {
            "id": row["id"],
            "filename": row["original_filename"],
            "file_size": row["file_size"],
            "mime_type": row["mime_type"],
            "created_at": str(row["created_at"])
        }
        for row in rows
    ]

def save_document(file_storage):
    """
    Validate, securely save uploaded file to disk, and record metadata in SQLite.
    Returns the created document metadata dict.
    """
    if not file_storage or not file_storage.filename:
        raise ValueError("No file provided or filename is empty")

    original_filename = secure_filename(file_storage.filename)
    if not original_filename:
        original_filename = "document"

    if not allowed_file(file_storage.filename):
        raise ValueError(f"File type not allowed. Allowed extensions: {', '.join(current_app.config['ALLOWED_EXTENSIONS'])}")

    ext = original_filename.rsplit(".", 1)[1].lower() if "." in original_filename else "bin"
    stored_filename = f"{uuid.uuid4().hex}.{ext}"

    upload_dir = Path(current_app.config["UPLOAD_FOLDER"])
    upload_dir.mkdir(parents=True, exist_ok=True)
    destination_path = upload_dir / stored_filename

    # Save to disk
    file_storage.save(str(destination_path))
    file_size = destination_path.stat().st_size

    # Detect MIME type
    mime_type, _ = mimetypes.guess_type(original_filename)
    if not mime_type:
        mime_type = "application/octet-stream"

    # Save metadata in SQLite
    relative_path = f"storage/documents/{stored_filename}"
    res = execute_db(
        """
        INSERT INTO documents (original_filename, stored_filename, filepath, file_size, mime_type)
        VALUES (?, ?, ?, ?, ?)
        """,
        (original_filename, stored_filename, relative_path, file_size, mime_type)
    )

    doc_id = res["lastrowid"]
    created_doc = query_db("SELECT id, original_filename, file_size, mime_type, created_at FROM documents WHERE id = ?", (doc_id,), one=True)
    return {
        "id": created_doc["id"],
        "filename": created_doc["original_filename"],
        "file_size": created_doc["file_size"],
        "mime_type": created_doc["mime_type"],
        "created_at": str(created_doc["created_at"])
    }

def get_document_for_download(doc_id: int):
    """Retrieve document metadata and resolve absolute filesystem path for download."""
    doc = query_db("SELECT id, original_filename, stored_filename, mime_type FROM documents WHERE id = ?", (doc_id,), one=True)
    if not doc:
        return None

    upload_dir = Path(current_app.config["UPLOAD_FOLDER"])
    file_path = upload_dir / doc["stored_filename"]

    if not file_path.exists():
        return None

    return {
        "file_path": file_path,
        "filename": doc["original_filename"],
        "mime_type": doc["mime_type"]
    }

def delete_document(doc_id: int) -> bool:
    """Delete document physical file and remove metadata row from SQLite."""
    doc = query_db("SELECT stored_filename FROM documents WHERE id = ?", (doc_id,), one=True)
    if not doc:
        return False

    upload_dir = Path(current_app.config["UPLOAD_FOLDER"])
    file_path = upload_dir / doc["stored_filename"]
    if file_path.exists():
        try:
            file_path.unlink()
        except OSError:
            pass

    execute_db("DELETE FROM documents WHERE id = ?", (doc_id,))
    return True
