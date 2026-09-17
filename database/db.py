import sqlite3
from flask import g, current_app

def get_db():
    """Retrieve or create SQLite connection for the current request context."""
    if "db" not in g:
        db_path = current_app.config["DATABASE_PATH"]
        g.db = sqlite3.connect(
            str(db_path),
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # Enable foreign keys and row factory for dict-like access
        g.db.execute("PRAGMA foreign_keys = ON;")
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """Close the SQLite connection on application context teardown."""
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db(app):
    """Ensure storage directory exists and initialize SQLite tables according to DATABASE_SCHEMA.md."""
    # Ensure storage directories exist
    storage_dir = app.config["STORAGE_DIR"]
    storage_dir.mkdir(parents=True, exist_ok=True)
    upload_dir = app.config["UPLOAD_FOLDER"]
    upload_dir.mkdir(parents=True, exist_ok=True)

    db_path = app.config["DATABASE_PATH"]
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        completed INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS planner (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        date TEXT NOT NULL,
        description TEXT DEFAULT '',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        relationship TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original_filename TEXT NOT NULL,
        stored_filename TEXT NOT NULL UNIQUE,
        filepath TEXT NOT NULL,
        file_size INTEGER NOT NULL,
        mime_type TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emergency_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        contact_ids TEXT NOT NULL,
        status TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()

def query_db(query, args=(), one=False):
    """Execute a read query and return list of dictionaries (or single dict if one=True)."""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    result = [dict(row) for row in rv]
    return (result[0] if result else None) if one else result

def execute_db(query, args=()):
    """Execute an INSERT, UPDATE, or DELETE query and commit changes."""
    db = get_db()
    cur = db.cursor()
    cur.execute(query, args)
    db.commit()
    last_id = cur.lastrowid
    rowcount = cur.rowcount
    cur.close()
    return {"lastrowid": last_id, "rowcount": rowcount}
