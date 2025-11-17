from __future__ import annotations

"""
Scraping engine.

Pipeline:

1. Read search links from DB (Table 2: search_links).
2. For each search link, use the appropriate source scraper to collect ad URLs.
3. Save an aggregated CSV of all ad URLs (url + source).
4. For each URL, if not already in Table 1 (buildings), fetch ad data and insert.

Enrichment steps (CSV-based + LLM) will run AFTER this pipeline; see TODOs.
"""

import csv
from pathlib import Path
from typing import Dict, List

from ..db import repositories as db_repo      # ✅ go up to backend, then into db
from .sources import get_source_by_name       # ✅ same package (scraping)


# Directory and file for aggregated URLs CSV
OUTPUT_DIR = Path(__file__).resolve().parent / "data" / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
AGGREGATED_URLS_CSV = OUTPUT_DIR / "urls_aggregated.csv"


def collect_ad_urls(max_pages_per_search: int = 3) -> List[Dict[str, str]]:
    """
    Phase 1: read search links from DB, collect ad URLs per source, and
    write them into a single aggregated CSV.

    Returns:
        List of dicts with keys:
            - "url"
            - "source"
    """
    search_links = db_repo.get_search_links()
    all_rows: List[Dict[str, str]] = []
    seen = set()  # (url, source) pairs

    for row in search_links:
        search_url = row["link"]
        source_name = row["source"]

        source = get_source_by_name(source_name)
        if not source:
            print(
                f"[WARN] No scraper implemented for source '{source_name}'. "
                f"Skipping search URL: {search_url}"
            )
            continue

        print(f"[INFO] Collecting ad URLs from {source_name} search: {search_url}")
        try:
            urls = source.list_ad_urls(search_url, max_pages=max_pages_per_search)
        except Exception as exc:
            print(
                f"[ERROR] Failed to collect URLs for source '{source_name}' "
                f"search '{search_url}': {exc}"
            )
            continue

        for url in urls:
            key = (url, source_name)
            if key not in seen:
                seen.add(key)
                all_rows.append({"url": url, "source": source_name})

    # Write aggregated CSV
    with AGGREGATED_URLS_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["url", "source"])
        writer.writeheader()
        writer.writerows(all_rows)

    print(
        f"[INFO] Collected {len(all_rows)} unique ad URLs from "
        f"{len(search_links)} search links."
    )
    print(f"[INFO] Aggregated URLs written to: {AGGREGATED_URLS_CSV}")
    return all_rows


def load_urls_from_csv() -> List[Dict[str, str]]:
    """
    Utility to re-load URLs from the aggregated CSV.

    (Not strictly necessary, but mirrors the spec: "It creates an aggregated CSV
    file with all the URLs, THEN component (2) is used to extract the ad data.")
    """
    if not AGGREGATED_URLS_CSV.exists():
        print(
            f"[WARN] Aggregated CSV {AGGREGATED_URLS_CSV} does not exist. "
            "Run collect_ad_urls() first."
        )
        return []

    rows: List[Dict[str, str]] = []
    with AGGREGATED_URLS_CSV.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if "url" in row and "source" in row:
                rows.append({"url": row["url"], "source": row["source"]})
    return rows


def scrape_ads_from_urls(rows: List[Dict[str, str]]) -> None:
    """
    Phase 2: given a list of {url, source} dicts, fetch ad data and insert
    into Table 1 (buildings) if not already present.
    """
    for row in rows:
        url = row["url"]
        source_name = row["source"]

        if db_repo.building_exists_by_url(url):
            print(f"[SKIP] Already in DB: {url}")
            continue

        source = get_source_by_name(source_name)
        if not source:
            print(
                f"[WARN] No scraper implemented for source '{source_name}'. "
                f"Skipping ad URL: {url}"
            )
            continue

        print(f"[INFO] Scraping {source_name} ad: {url}")
        try:
            building_data = source.fetch_ad_data(url)
        except Exception as exc:
            print(f"[ERROR] Failed to fetch ad data for {url}: {exc}")
            continue

        try:
            inserted_id = db_repo.insert_building(building_data)
            print(f"[OK] Inserted building a_id={inserted_id} from {url}")
        except Exception as exc:
            print(f"[ERROR] Failed to insert building for {url}: {exc}")


def run_full_scraping(max_pages_per_search: int = 3) -> None:
    """
    Run the full scraping pipeline (without enrichment):

    1. Collect URLs and write them to urls_aggregated.csv
    2. Reload URLs from that CSV
    3. Scrape each ad and insert new buildings into Table 1

    Enrichment (CSV-based + LLM) will be called after this in a later step.
    """
    print("[STEP 1] Collecting ad URLs from search links...")
    collect_ad_urls(max_pages_per_search=max_pages_per_search)

    print("[STEP 2] Loading URLs from aggregated CSV...")
    rows = load_urls_from_csv()

    print("[STEP 3] Scraping ad pages and inserting into DB...")
    scrape_ads_from_urls(rows)

    # ------------------------------------------------------------------
    # TODO (Enrichment Phase)
    #
    # After scraping, we will run:
    #
    #   - CSV-based enrichment (Table 1 c_XXX fields)
    #   - LLM-based enrichment (Table 1 llm_XXX fields)
    #
    # For example (to be implemented later):
    #
    #   from scraping.enrichment.csv_enrichment import run_csv_enrichment
    #   from scraping.enrichment.llm_enrichment import run_llm_enrichment
    #
    #   print("[STEP 4] Running CSV-based enrichment...")
    #   run_csv_enrichment()
    #
    #   print("[STEP 5] Running LLM-based enrichment...")
    #   run_llm_enrichment()
    # ------------------------------------------------------------------
    print("[DONE] Scraping pipeline completed (without enrichment).")
