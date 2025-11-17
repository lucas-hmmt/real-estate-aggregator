from __future__ import annotations

"""
Source registry.

Provides a helper to get a scraper instance by source name (e.g. "SeLoger").
"""

from typing import Optional, Type

from .base_source import BaseSource
from .seloger_source import SeLogerSource

# Registry of available sources.
# Add more sources (e.g., BieniciSource) to this dict later.
SOURCE_REGISTRY: dict[str, Type[BaseSource]] = {
    "SeLoger": SeLogerSource,
    # "Bienici": BieniciSource,  # to be added when implemented
}


def get_source_by_name(name: str) -> Optional[BaseSource]:
    """
    Return a new scraper instance for the given source name, or None if
    the source is not implemented yet.
    """
    cls = SOURCE_REGISTRY.get(name)
    if not cls:
        return None
    return cls()
