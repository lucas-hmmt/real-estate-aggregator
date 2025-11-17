"""
Script to create / initialize the SQLite database from schema.sql.

Usage (from project root):

    python backend/db/init_db.py

This will create a file called `realestate.db` in the same folder as this script.
"""

import sqlite3
from pathlib import Path

# Database file will live in backend/db/realestate.db
DB_PATH = Path(__file__).resolve().parent / "realestate.db"
SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"


def init_db() -> None:
    """Create the SQLite database and apply the schema."""
    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(f"Schema file not found: {SCHEMA_PATH}")

    # Connect to SQLite; the file is created if it does not exist
    conn = sqlite3.connect(DB_PATH)

    try:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            schema_sql = f.read()

        # Apply the full schema (tables, indexes, initial data)
        conn.executescript(schema_sql)
        conn.commit()
        print(f"Database initialized successfully at: {DB_PATH}")
    finally:
        conn.close()


if __name__ == "__main__":
    init_db()
