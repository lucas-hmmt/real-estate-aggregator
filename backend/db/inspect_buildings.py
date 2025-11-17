from __future__ import annotations

"""
Quick helper to inspect the first 10 rows of the `buildings` table.

Usage (from project root):

    python -m backend.db.inspect_buildings

This will:

- Connect to backend/db/realestate.db
- Print the total number of rows in `buildings`
- Print the first 10 rows as dictionaries
"""

from typing import Any, Dict

from .connection import get_connection  # uses the same DB path as the app


def main() -> None:
    with get_connection() as conn:
        # Total count
        cur = conn.execute("SELECT COUNT(*) AS cnt FROM buildings")
        row = cur.fetchone()
        total = row["cnt"] if row is not None else 0
        print(f"Total buildings in DB: {total}")

        # First 10 rows
        cur = conn.execute(
            "SELECT * FROM buildings ORDER BY a_id ASC LIMIT 10"
        )
        rows = cur.fetchall()

    if not rows:
        print("No rows found in `buildings` table.")
        return

    print("\nFirst 10 rows:")
    for i, r in enumerate(rows, start=1):
        d: Dict[str, Any] = dict(r)
        print(f"\nRow #{i}:")
        for k, v in d.items():
            print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
