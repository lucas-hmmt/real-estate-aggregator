from __future__ import annotations

from typing import Any, Dict, List

import io
import csv

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from .db import repositories as db_repo  # 👈 note the `.db` (relative import)


app = FastAPI(title="Real Estate Aggregator API")

# ---------------------------------------------------------
# CORS (useful in dev if you ever call localhost:8000 directly)
# ---------------------------------------------------------
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Models for request bodies
# ---------------------------------------------------------

class SearchLinkCreate(BaseModel):
    url: str
    source: str


# ---------------------------------------------------------
# Buildings endpoints
# ---------------------------------------------------------

@app.get("/api/buildings")
def list_buildings() -> List[Dict[str, Any]]:
    """
    Return all buildings in the DB (Table 1).
    """
    return db_repo.get_all_buildings()


@app.get("/api/buildings/{building_id}")
def get_building(building_id: int) -> Dict[str, Any]:
    """
    Return one building by a_id, or 404.
    """
    building = db_repo.get_building_by_id(building_id)
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    return building


# ---------------------------------------------------------
# Cart endpoints (Table 4)
# ---------------------------------------------------------

@app.get("/api/cart")
def get_cart() -> List[Dict[str, Any]]:
    """
    Return all buildings currently in the cart (join of Table 4 + Table 1).
    """
    return db_repo.get_cart_buildings()


@app.post("/api/cart/{building_id}")
def add_cart_item(building_id: int) -> Dict[str, str]:
    """
    Add a building to the cart.
    """
    # Optional: ensure building exists
    building = db_repo.get_building_by_id(building_id)
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")

    db_repo.add_to_cart(building_id)
    return {"status": "ok"}


@app.delete("/api/cart/{building_id}")
def remove_cart_item(building_id: int) -> Dict[str, str]:
    """
    Remove a building from the cart.
    """
    db_repo.remove_from_cart(building_id)
    return {"status": "ok"}


# ---------------------------------------------------------
# Settings endpoints (Table 2 & 3)
# ---------------------------------------------------------

@app.get("/api/settings/search-links")
def list_search_links() -> List[Dict[str, Any]]:
    """
    Return all search links (Table 2).
    """
    return db_repo.get_search_links()


@app.get("/api/settings/sources")
def list_sources() -> List[str]:
    """
    Return all possible sources (Table 3).
    """
    return db_repo.get_sources()


@app.post("/api/settings/search-links")
def create_search_link(payload: SearchLinkCreate) -> Dict[str, Any]:
    """
    Add a new search link (URL + source).
    """
    # Minimal validation
    if not payload.url.strip():
        raise HTTPException(status_code=400, detail="URL is required")
    if not payload.source.strip():
        raise HTTPException(status_code=400, detail="Source is required")

    if payload.source not in db_repo.get_sources():
        raise HTTPException(status_code=400, detail="Unknown source")

    new_id = db_repo.add_search_link(payload.url.strip(), payload.source.strip())
    return {"id": new_id, "url": payload.url.strip(), "source": payload.source.strip()}


# ---------------------------
