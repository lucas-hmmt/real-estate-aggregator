"""
Database package for the real-estate aggregator.

This package provides:

- A SQLite connection helper (`get_connection`)
- Utility functions to create and access the database (via repositories)

Typical usage from elsewhere in the backend:

    from backend.db.connection import get_connection
    from backend.db import repositories as db_repo
"""

from .connection import get_connection, DB_PATH  # re-export for convenience
