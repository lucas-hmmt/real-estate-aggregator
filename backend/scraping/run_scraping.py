from __future__ import annotations

"""
Manual entrypoint for the scraping pipeline.

Recommended usage (from project root):

    python -m backend.scraping.run_scraping

This will:

1. Read search links from Table 2 (search_links).
2. Use the SeLoger scraper (and other sources when added) to collect ad URLs.
3. Write `backend/scraping/data/output/urls_aggregated.csv`.
4. Scrape each ad URL not already in Table 1 (buildings) and insert them.

Enrichment (CSV-based + LLM) will be plugged in AFTER the scraping pipeline.
"""

from .engine import run_full_scraping


def main() -> None:
  # Adjust max_pages_per_search as you wish
  run_full_scraping(max_pages_per_search=3)

  # ------------------------------------------------------------------
  # Enrichment hooks (to be implemented later)
  #
  #   from .enrichment.csv_enrichment import run_csv_enrichment
  #   from .enrichment.llm_enrichment import run_llm_enrichment
  #
  #   print("[STEP 4] Running CSV-based enrichment...")
  #   run_csv_enrichment()
  #
  #   print("[STEP 5] Running LLM-based enrichment...")
  #   run_llm_enrichment()
  # ------------------------------------------------------------------


if __name__ == "__main__":
  main()
