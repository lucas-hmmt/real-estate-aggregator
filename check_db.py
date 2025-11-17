from backend.db.connection import get_connection

with get_connection() as conn:
    cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    rows = cur.fetchall()

tables = [row["name"] for row in rows]
print(tables)
