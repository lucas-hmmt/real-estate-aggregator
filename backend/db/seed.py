"""
Seed initial data into the SQLite database:

- Table 3: sources
    - "Bienici"
    - "SeLoger"
- Table 2: search_links
    - link = "https://www.seloger.com/classified-search?distributionTypes=Buy&estateTypes=Building&locations=AD06FR60"
      source = "SeLoger"

Usage (from project root):

    python backend/db/init_db.py        # (first time only, to create DB)
    python backend/db/seed_initial_data.py
"""

import sqlite3
from pathlib import Path

# Same DB location as in init_db.py / connection.py
DB_PATH = Path(__file__).resolve().parent / "realestate.db"


def seed():
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Database file not found at {DB_PATH}. "
            "Run `python backend/db/init_db.py` first to create it."
        )

    conn = sqlite3.connect(DB_PATH)

    try:
        cur = conn.cursor()

        # --- Table 3: sources ----------------------------------------------
        # Ensure the two sources exist (idempotent)
        cur.execute(
            "INSERT OR IGNORE INTO sources (source) VALUES (?)",
            ("Bienici",),
        )
        cur.execute(
            "INSERT OR IGNORE INTO sources (source) VALUES (?)",
            ("SeLoger",),
        )

        # --- Table 2: search_links -----------------------------------------
        se_loger_url = (
            "https://www.seloger.com/classified-search?distributionTypes=Buy"
            "&estateTypes=Building&locations=AD06FR60"
        )
        se_loger_source = "SeLoger"

        # Check if this link already exists to avoid duplicates
        cur.execute(
            """
            SELECT id FROM search_links
            WHERE link = ? AND source = ?
            """,
            (se_loger_url, se_loger_source),
        )
        row = cur.fetchone()

        if row is None:
            cur.execute(
                """
                INSERT INTO search_links (link, source)
                VALUES (?, ?)
                """,
                (se_loger_url, se_loger_source),
            )
            print("Inserted initial SeLoger search link into Table 2.")
        else:
            print("SeLoger search link already present in Table 2 (id = {}).".format(row[0]))

        conn.commit()
        print("Sources seeded successfully into Table 3.")
        print(f"Done. Database at: {DB_PATH}")

    finally:
        conn.close()


if __name__ == "__main__":
    seed()
