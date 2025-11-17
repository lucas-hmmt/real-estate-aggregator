"""
Low-level SQLite connection helper.

All parts of the backend (API, scraping engine, enrichment) should use
`get_connection()` to talk to the database, so we centralize:

- DB file location
- row_factory (dict-like rows)
- foreign key enforcement
"""

import sqlite3
from pathlib import Path

# Path to the SQLite database file (created by init_db.py)
DB_PATH = Path(__file__).resolve().parent / "realestate.db"


def get_connection() -> sqlite3.Connection:
    """
    Open a new SQLite connection to the project database.

    - Enables foreign keys.
    - Uses sqlite3.Row for row_factory so rows can be cast to dicts easily.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn
