# DATABASE_SCHEMA.md
Canonical SQLite Database Schema for "Invisible Help" (Tanu & Backend).

Database Engine: SQLite 3  
Default Database File: `backend/storage/invisible_help.db`

---

## 1. Table: `notes`
Stores user notes for the disguised productivity interface.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique note identifier |
| `title` | TEXT | NOT NULL | Title of the note |
| `content` | TEXT | NOT NULL | Body content of the note |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Creation timestamp |
| `updated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Last modified timestamp |

---

## 2. Table: `todos`
Stores checklist/tasks for the disguised productivity interface.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique task identifier |
| `title` | TEXT | NOT NULL | Task description |
| `completed` | INTEGER | DEFAULT 0 | 0 = false, 1 = true |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Creation timestamp |

---

## 3. Table: `planner`
Stores calendar/agenda events for the disguised productivity interface.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique planner item identifier |
| `title` | TEXT | NOT NULL | Event title |
| `date` | TEXT | NOT NULL | Event date (YYYY-MM-DD or formatted) |
| `description` | TEXT | DEFAULT '' | Additional details |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Creation timestamp |

---

## 4. Table: `contacts`
Stores trusted emergency contacts inside the hidden safety dashboard.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique contact identifier |
| `name` | TEXT | NOT NULL | Contact full name |
| `phone` | TEXT | NOT NULL | Phone number |
| `relationship` | TEXT | NOT NULL | Relationship (e.g. Sister, Friend) |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Creation timestamp |

---

## 5. Table: `documents`
Stores metadata for uploaded documents in the Secure Document Vault.
*(Actual physical files are stored in `backend/storage/documents/`)*

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique document identifier |
| `original_filename` | TEXT | NOT NULL | Original uploaded filename |
| `stored_filename` | TEXT | NOT NULL UNIQUE | Secure UUID-based disk filename |
| `filepath` | TEXT | NOT NULL | Full relative storage path |
| `file_size` | INTEGER | NOT NULL | Size in bytes |
| `mime_type` | TEXT | NOT NULL | MIME content type |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Upload timestamp |

---

## 6. Table: `emergency_events`
Stores prototype audit log of triggered SOS alerts.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique event identifier |
| `contact_ids` | TEXT | NOT NULL | JSON string or comma-separated contact IDs |
| `status` | TEXT | NOT NULL | Status (e.g. 'prototype_processed') |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Event trigger timestamp |

---

## Table Creation DDL

```sql
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    completed INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS planner (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    date TEXT NOT NULL,
    description TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    relationship TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_filename TEXT NOT NULL,
    stored_filename TEXT NOT NULL UNIQUE,
    filepath TEXT NOT NULL,
    file_size INTEGER NOT NULL,
    mime_type TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS emergency_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contact_ids TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
