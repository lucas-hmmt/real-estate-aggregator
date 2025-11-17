from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List, Optional

import requests


class BaseSource(ABC):
    """
    Base class for all scraping sources.

    Each concrete source must implement:

    - list_ad_urls(search_url, max_pages)
    - fetch_ad_data(ad_url)

    `fetch_ad_data` must return a dict compatible with the `buildings` table
    (Table 1) using keys like:

        a_url
        a_title
        a_city
        a_postalCode
        a_price
        a_surfaceArea
        a_description
        a_images
        a_publicationDate
        a_dpe
        a_ges

    Other columns (llm_* and c_*) will be filled later by enrichment.
    """

    name: str

    def __init__(self, session: Optional[requests.Session] = None) -> None:
        self.session: requests.Session = session or requests.Session()

    @abstractmethod
    def list_ad_urls(self, search_url: str, max_pages: int = 1) -> List[str]:
        """Return a list of ad URLs for a given search URL."""
        raise NotImplementedError

    @abstractmethod
    def fetch_ad_data(self, ad_url: str) -> Dict[str, object]:
        """
        Fetch and parse a single ad page.

        Returns a dict suitable for insertion via db.repositories.insert_building().
        """
        raise NotImplementedError
