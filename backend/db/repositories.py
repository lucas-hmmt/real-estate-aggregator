"""
High-level database access functions ("repositories").

This module provides simple functions that hide raw SQL from the rest of
the application: API, scraping engine, etc.

All functions open and close their own connections using `get_connection()`.
"""

import sqlite3
from typing import Any, Dict, Iterable, List, Optional, Tuple

from .connection import get_connection

# Columns we insert for new buildings (a_id is auto-incremented).
BUILDING_INSERT_COLUMNS: Tuple[str, ...] = (
    "a_url",
    "a_title",
    "a_city",
    "a_postalCode",
    "a_price",
    "a_surfaceArea",
    "a_description",
    "a_images",
    "a_publicationDate",
    "a_dpe",
    "a_ges",
    "llm_residential_office",
    "llm_nbFlats",
    "llm_flatSizes",
    "llm_other",
    "c_treated",
    "c_INSEE",
    "c_pricePerSqMeter",
    "c_taxHab",
    "c_taxFonc",
    "c_vacancy",
    "c_vacancyCat",
    "c_revenue",
    "c_revenueCat",
    "c_dept",
    "c_region",
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
    """Convert a sqlite3.Row to a plain dict."""
    return dict(row)


# ---------------------------------------------------------------------------
# Buildings (Table 1)
# ---------------------------------------------------------------------------

def get_all_buildings(limit: Optional[int] = None, offset: int = 0) -> List[Dict[str, Any]]:
    """
    Return all buildings, optionally paginated.

    :param limit: maximum number of rows to return (None = no limit)
    :param offset: starting offset (for pagination)
    """
    sql = "SELECT * FROM buildings ORDER BY a_id DESC"
    params: List[Any] = []

    if limit is not None:
        sql += " LIMIT ? OFFSET ?"
        params.extend([limit, offset])

    with get_connection() as conn:
        cur = conn.execute(sql, params)
        rows = cur.fetchall()

    return [_row_to_dict(row) for row in rows]


def get_buildings_count() -> int:
    """Return total number of buildings in the database."""
    with get_connection() as conn:
        cur = conn.execute("SELECT COUNT(*) AS cnt FROM buildings")
        row = cur.fetchone()
    return int(row["cnt"]) if row is not None else 0


def get_building_by_id(a_id: int) -> Optional[Dict[str, Any]]:
    """Return a single building by its primary key (a_id), or None."""
    with get_connection() as conn:
        cur = conn.execute("SELECT * FROM buildings WHERE a_id = ?", (a_id,))
        row = cur.fetchone()

    return _row_to_dict(row) if row is not None else None


def building_exists_by_url(a_url: str) -> bool:
    """Check if a building with the given URL already exists."""
    with get_connection() as conn:
        cur = conn.execute(
            "SELECT 1 FROM buildings WHERE a_url = ? LIMIT 1",
            (a_url,),
        )
        row = cur.fetchone()
    return row is not None


def insert_building(building: Dict[str, Any]) -> int:
    """
    Insert a new building into the database.

    `building` should be a dict with keys matching BUILDING_INSERT_COLUMNS.
    Missing keys will default to None, except `c_treated` which defaults to 0.

    Returns the new `a_id`.
    """
    values: List[Any] = []
    for col in BUILDING_INSERT_COLUMNS:
        if col == "c_treated":
            values.append(building.get(col, 0))  # ensure default 0
        else:
            values.append(building.get(col))

    placeholders = ", ".join("?" for _ in BUILDING_INSERT_COLUMNS)
    columns_sql = ", ".join(BUILDING_INSERT_COLUMNS)
    sql = f"INSERT INTO buildings ({columns_sql}) VALUES ({placeholders})"

    with get_connection() as conn:
        cur = conn.execute(sql, values)
        conn.commit()
        return int(cur.lastrowid)


def get_untreated_buildings() -> List[Dict[str, Any]]:
    """
    Return all buildings where c_treated = 0.

    Useful for post-processing / enrichment.
    """
    with get_connection() as conn:
        cur = conn.execute(
            "SELECT * FROM buildings WHERE c_treated = 0 ORDER BY a_id ASC"
        )
        rows = cur.fetchall()

    return [_row_to_dict(row) for row in rows]


def update_building_fields(a_id: int, updates: Dict[str, Any]) -> None:
    """
    Generic partial update: sets specific columns on a building row.

    Example:
        update_building_fields(123, {"c_pricePerSqMeter": 4500, "c_treated": 1})
    """
    if not updates:
        return

    columns = list(updates.keys())
    values = list(updates.values())
    set_clause = ", ".join(f"{col} = ?" for col in columns)
    sql = f"UPDATE buildings SET {set_clause} WHERE a_id = ?"
    values.append(a_id)

    with get_connection() as conn:
        conn.execute(sql, values)
        conn.commit()


# ---------------------------------------------------------------------------
# Cart (Table 4)
# ---------------------------------------------------------------------------

def get_cart_buildings() -> List[Dict[str, Any]]:
    """
    Return all buildings currently in the cart (TABLE 4),
    joined with full building information (TABLE 1).
    """
    sql = """
        SELECT b.*
        FROM buildings AS b
        JOIN cart AS c ON c.id = b.a_id
        ORDER BY b.a_id DESC
    """
    with get_connection() as conn:
        cur = conn.execute(sql)
        rows = cur.fetchall()

    return [_row_to_dict(row) for row in rows]


def add_to_cart(a_id: int) -> None:
    """Add a building to the cart. If already present, this is a no-op."""
    with get_connection() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO cart (id) VALUES (?)",
            (a_id,),
        )
        conn.commit()


def remove_from_cart(a_id: int) -> None:
    """Remove a building from the cart (if present)."""
    with get_connection() as conn:
        conn.execute("DELETE FROM cart WHERE id = ?", (a_id,))
        conn.commit()


def clear_cart() -> None:
    """Remove all buildings from the cart."""
    with get_connection() as conn:
        conn.execute("DELETE FROM cart")
        conn.commit()


# ---------------------------------------------------------------------------
# Search links (Table 2) & sources (Table 3)
# ---------------------------------------------------------------------------

def get_search_links() -> List[Dict[str, Any]]:
    """
    Return all search links (TABLE 2).

    Each row is a dict with:
        - id
        - link
        - source
    """
    with get_connection() as conn:
        cur = conn.execute(
            "SELECT id, link, source FROM search_links ORDER BY id ASC"
        )
        rows = cur.fetchall()

    return [_row_to_dict(row) for row in rows]


def add_search_link(link: str, source: str) -> int:
    """
    Add a new search link for a given source website.

    Returns the new search_links.id.
    """
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO search_links (link, source) VALUES (?, ?)",
            (link, source),
        )
        conn.commit()
        return int(cur.lastrowid)


def get_sources() -> List[str]:
    """Return the list of available sources (e.g. 'Bienici', 'SeLoger')."""
    with get_connection() as conn:
        cur = conn.execute("SELECT source FROM sources ORDER BY source ASC")
        rows = cur.fetchall()

    return [row["source"] for row in rows]
