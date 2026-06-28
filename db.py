"""SQLite-backed storage for image version management.

Projects group related backup images under one base folder; each image
belongs to a project and carries a free-text version label.
"""

import os
import sqlite3
from datetime import datetime

DB_PATH = os.path.expanduser("~/.local/share/pisafe-gui/images.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    folder TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    version_label TEXT NOT NULL,
    file_path TEXT NOT NULL,
    source_disk TEXT,
    size_bytes INTEGER,
    notes TEXT,
    created_at TEXT NOT NULL
);
"""


def _connect():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    return conn


def create_project(name, folder):
    with _connect() as conn:
        cur = conn.execute(
            "INSERT INTO projects (name, folder, created_at) VALUES (?, ?, ?)",
            (name, folder, datetime.now().isoformat(timespec="seconds")),
        )
        return cur.lastrowid


def list_projects():
    with _connect() as conn:
        rows = conn.execute(
            "SELECT id, name, folder FROM projects ORDER BY name"
        ).fetchall()
        return [{"id": r[0], "name": r[1], "folder": r[2]} for r in rows]


def get_project(project_id):
    with _connect() as conn:
        row = conn.execute(
            "SELECT id, name, folder FROM projects WHERE id = ?", (project_id,)
        ).fetchone()
        return {"id": row[0], "name": row[1], "folder": row[2]} if row else None


def delete_project(project_id):
    with _connect() as conn:
        conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))


def next_version_label(project_id):
    with _connect() as conn:
        count = conn.execute(
            "SELECT COUNT(*) FROM images WHERE project_id = ?", (project_id,)
        ).fetchone()[0]
        return f"v{count + 1}"


def add_image(project_id, version_label, file_path, source_disk=None, size_bytes=None, notes=None):
    with _connect() as conn:
        cur = conn.execute(
            "INSERT INTO images (project_id, version_label, file_path, source_disk, "
            "size_bytes, notes, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (project_id, version_label, file_path, source_disk, size_bytes, notes,
             datetime.now().isoformat(timespec="seconds")),
        )
        return cur.lastrowid


def list_images(project_id):
    with _connect() as conn:
        rows = conn.execute(
            "SELECT id, version_label, file_path, source_disk, size_bytes, notes, created_at "
            "FROM images WHERE project_id = ? ORDER BY created_at DESC",
            (project_id,),
        ).fetchall()
        return [
            {
                "id": r[0], "version_label": r[1], "file_path": r[2],
                "source_disk": r[3], "size_bytes": r[4], "notes": r[5],
                "created_at": r[6],
            }
            for r in rows
        ]


def get_image(image_id):
    with _connect() as conn:
        row = conn.execute(
            "SELECT id, project_id, file_path FROM images WHERE id = ?", (image_id,)
        ).fetchone()
        return {"id": row[0], "project_id": row[1], "file_path": row[2]} if row else None


def delete_image(image_id, delete_file=False):
    if delete_file:
        img = get_image(image_id)
        if img:
            try:
                os.remove(img["file_path"])
            except OSError:
                pass
    with _connect() as conn:
        conn.execute("DELETE FROM images WHERE id = ?", (image_id,))
