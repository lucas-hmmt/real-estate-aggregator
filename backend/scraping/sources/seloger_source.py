# -*- coding: utf-8 -*-
from __future__ import annotations

"""
SeLoger scraper (source implementation for the scraping engine).

Provides:

- list_ad_urls(search_url, max_pages)
- fetch_ad_data(ad_url) -> dict with `a_` fields for Table 1

Based on your working script, adapted to our project structure and DB schema.
"""

import json
import re
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Optional
from urllib.parse import urlparse, parse_qs

import requests
from bs4 import BeautifulSoup

from .base_source import BaseSource

# -------------------- configuration --------------------

REQUEST_DELAY_SEC = 0.3  # be nice
MAX_PAGES_DEFAULT = 50

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Cache-Control": "no-cache",
}

# -------------------- utils --------------------


def _get_html(url: str, session: Optional[requests.Session] = None) -> str:
    """Fetch HTML from web or local file:// URL."""
    parsed = urlparse(url)
    if parsed.scheme == "file":
        return Path(parsed.path).read_text(encoding="utf-8", errors="ignore")
    sess = session or requests.Session()
    resp = sess.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    return resp.text


def _unique(seq: Iterable[str]) -> List[str]:
    seen = set()
    out: List[str] = []
    for s in seq:
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out


def _extract_city_from_title(
    title: Optional[str], fallback: Optional[str] = None
) -> Optional[str]:
    if not title:
        return fallback
    m = re.search(r"\((\d{5})\)", title)
    if not m:
        return fallback
    prefix = title[: m.start()].strip()
    if "," in prefix:
        prefix = prefix.split(",")[-1].strip()
    prefix = re.sub(r"\s{2,}", " ", prefix)
    parts = re.split(r"\s+", prefix)
    if len(parts) >= 1:
        return parts[-1]
    return fallback


def _price_to_plain_number(value: Optional[str]) -> Optional[str]:
    """
    Convert a raw price value to a plain number string without separators or currency.
    Returns e.g. "599000" or None.
    """
    if value is None:
        return None
    digits = re.sub(r"[^\d]", "", str(value))
    return digits if digits else None


def _price_from_text(text: Optional[str]) -> Optional[str]:
    """
    Fallback extractor: find a price pattern like '1 350 000 €' in text and normalize to '1350000'.
    """
    if not text:
        return None
    m = re.search(r"(\d[\d\s]{3,})\s*€", text.replace("\xa0", " "))
    if not m:
        return None
    return _price_to_plain_number(m.group(1))


def _extract_from_head_meta(soup: BeautifulSoup, name: str) -> Optional[str]:
    tag = soup.find("meta", attrs={"name": name})
    if tag and tag.get("content"):
        return tag["content"]
    return None


def _extract_canonical_url(soup: BeautifulSoup) -> Optional[str]:
    tag = soup.find("link", rel="canonical")
    if tag and tag.get("href"):
        return tag["href"]
    return None


def _extract_id_from_canonical(url: Optional[str]) -> Optional[str]:
    if not url:
        return None
    m = re.search(r"/(\d+)/detail\.htm", url)
    return m.group(1) if m else None


def _extract_city_from_legacy_tracking(html: str) -> Optional[str]:
    m = re.search(r'"av_city"\s*:\s*"([^"]+)"', html)
    if m:
        return m.group(1).strip()
    return None


def _extract_description_from_dom(soup: BeautifulSoup) -> Optional[str]:
    title_el = soup.find("h2", id="description")
    if not title_el:
        title_el = soup.find(
            attrs={"data-testid": re.compile(r"cdp-main-description-title", re.I)}
        )
    if not title_el:
        return None

    headline = title_el.get_text(strip=True)
    body_text = ""
    nxt = title_el.find_next_sibling()
    hop = 0
    while nxt is not None and hop < 8 and (not body_text or len(body_text) < 50):
        txt = nxt.get_text("\n", strip=True)
        if len(txt) > 50:
            body_text = txt
            break
        nxt = nxt.find_next_sibling()
        hop += 1

    if headline and body_text:
        return (headline + "\n" + body_text).strip()
    return None


def _extract_description_from_embedded_json(html: str) -> Optional[str]:
    m_jsonparse = re.search(
        r'__UFRN_FETCHER__\"]=JSON\.parse\("(?P<payload>.+?)"\);',
        html,
        re.DOTALL,
    )
    text = None
    headline = None
    if m_jsonparse:
        try:
            payload_str = m_jsonparse.group("payload")
            decoded = json.loads(payload_str)

            def walk(obj):
                nonlocal text, headline
                if isinstance(obj, dict):
                    if "body" in obj and isinstance(obj["body"], dict):
                        b = obj["body"]
                        if (
                            "texts" in b
                            and isinstance(b["texts"], list)
                            and b["texts"]
                        ):
                            if isinstance(b["texts"][0], dict) and "text" in b["texts"][0]:
                                text = b["texts"][0]["text"]
                                headline = b.get("headline")
                                return True
                    for v in obj.values():
                        if walk(v):
                            return True
                elif isinstance(obj, list):
                    for v in obj:
                        if walk(v):
                            return True
                return False

            walk(decoded)
        except Exception:
            pass

    if text is None:
        m = re.search(
            r'"body"\s*:\s*\{[^{}]*"headline"\s*:\s*"(?P<head>.*?)"[^{}]*"texts"\s*:\s*\[\s*\{\s*"text"\s*:\s*"(?P<txt>.*?)"\s*\}\s*\]',
            html,
            re.DOTALL,
        )
        if m:
            headline = m.group("head")
            text = m.group("txt")

    if text:
        try:
            text = json.loads(f'"{text}"')
        except Exception:
            text = text.replace("\\n", "\n").replace("\\r", "").replace("\\t", "\t")
        if headline:
            try:
                headline = json.loads(f'"{headline}"')
            except Exception:
                pass
            return f"{headline}\n{text}".strip()
        return text.strip()

    m = re.search(r'property="og:description"\s+content="([^"]+)"', html)
    if m:
        return m.group(1).strip()
    return None


def _normalize_url(u: str) -> str:
    return u.replace("&amp;", "&").rstrip("\\")


def _is_gallery_photo(u: str) -> bool:
    """Keep only gallery photos; exclude logos/icons/etc."""
    try:
        p = urlparse(u)
        host = p.netloc.lower()
        path = p.path.lower()
        qs = parse_qs(p.query)
    except Exception:
        return False

    if not host.endswith("seloger.com"):
        return False

    if not (path.endswith(".jpg") or path.endswith(".jpeg")):
        return False

    if any(k in path for k in ("logo", "agence", "brand", "icon", "marker", "avatar")):
        return False

    if ("w" in qs and "h" in qs) or ("ci_seal" in qs):
        return True

    return False


def _extract_image_urls(soup: BeautifulSoup, raw_html: str) -> List[str]:
    urls: List[str] = []

    # 1) <source srcset>
    for source in soup.find_all("source"):
        srcset = source.get("srcset")
        if srcset:
            for part in srcset.split(","):
                url = part.strip().split(" ")[0]
                if url:
                    urls.append(url)

    # 2) <img src>
    for img in soup.find_all("img"):
        src = img.get("src")
        if src:
            urls.append(src)

    # 3) Regex for jpg/png/jpeg
    for m in re.finditer(
        r'https?://[^\s"\']+?\.(?:jpg|png|jpeg)(?:\?[^\s"\']*)?',
        raw_html,
        flags=re.IGNORECASE,
    ):
        urls.append(m.group(0))

    norm: List[str] = []
    seen = set()
    for u in urls:
        u2 = _normalize_url(u)
        if u2 not in seen:
            seen.add(u2)
            norm.append(u2)

    gallery = [u for u in norm if _is_gallery_photo(u)]
    return gallery


# -------------------- core models --------------------


@dataclass
class Ad:
    Id: Optional[str]
    Url: Optional[str]
    title: Optional[str]
    city: Optional[str]
    postalCode: Optional[str]
    price: Optional[str]  # plain digits only, e.g. "1350000"
    surfaceArea: Optional[str]
    description: Optional[str]
    Images: Optional[str]


# -------------------- step 1: collect ad URLs --------------------

AD_HREF_RE = re.compile(r"https://www\.seloger\.com/\d+/detail\.htm")


def get_listing_urls(
    search_url: str,
    max_pages: int = 1,
    session: Optional[requests.Session] = None,
) -> List[str]:
    sess = session or requests.Session()
    all_urls: List[str] = []
    prev_count = 0

    for page in range(1, max_pages + 1):
        url = search_url
        if page > 1:
            sep = "&" if "?" in search_url else "?"
            if "page=" in search_url:
                url = re.sub(r"([?&])page=\d+", rf"\1page={page}", search_url)
            else:
                url = f"{search_url}{sep}page={page}"

        html = _get_html(url, session=sess)
        soup = BeautifulSoup(html, "html.parser")

        anchors = soup.select(
            "a[data-testid='card-mfe-covering-link-testid'], a.css-1a6drk4"
        )
        for a in anchors:
            href = (a.get("href") or "").strip()
            if AD_HREF_RE.fullmatch(href):
                all_urls.append(href)

        for m in AD_HREF_RE.finditer(html):
            all_urls.append(m.group(0))

        all_urls = _unique(all_urls)

        if page > 1 and url != search_url and len(all_urls) == prev_count:
            break

        prev_count = len(all_urls)
        time.sleep(REQUEST_DELAY_SEC)

    return all_urls


# -------------------- step 2: parse ad page --------------------


def parse_ad(
    ad_url: str,
    html: Optional[str] = None,
    session: Optional[requests.Session] = None,
) -> Ad:
    sess = session or requests.Session()
    raw_html = html if html is not None else _get_html(ad_url, session=sess)
    soup = BeautifulSoup(raw_html, "html.parser")

    canonical = _extract_canonical_url(soup) or ad_url
    ad_id_raw = _extract_id_from_canonical(canonical) or _extract_from_head_meta(
        soup, "ad:idtiers"
    )

    # Prefix with "seloger_"
    ad_id = (
        f"seloger_{ad_id_raw}"
        if ad_id_raw and not str(ad_id_raw).startswith("seloger_")
        else ad_id_raw
    )

    postal = _extract_from_head_meta(soup, "ad:cp")
    price_meta = _extract_from_head_meta(soup, "ad:prix")

    price = _price_to_plain_number(price_meta) or _price_from_text(raw_html)
    surface_num = _extract_from_head_meta(soup, "ad:surface")

    # Title
    title = None
    og_title = soup.find("meta", attrs={"property": "og:title"})
    if og_title and og_title.get("content"):
        title = og_title["content"].strip()
    if not title and soup.title:
        title = (soup.title.string or "").strip()

    # City
    city = _extract_city_from_legacy_tracking(raw_html) or _extract_city_from_title(
        title
    )

    # Description
    description = _extract_description_from_dom(soup) or _extract_description_from_embedded_json(
        raw_html
    )

    # Images (gallery only)
    images = _extract_image_urls(soup, raw_html)

    # Note: for this project we store comma-separated URLs in a_images
    images_str = ",".join(images) if images else None

    return Ad(
        Id=ad_id,
        Url=canonical,
        title=title,
        city=city,
        postalCode=postal,
        price=price,
        surfaceArea=surface_num,
        description=description,
        Images=images_str,
    )


# -------------------- SeLogerSource class --------------------


class SeLogerSource(BaseSource):
    """
    Source implementation for "SeLoger".

    - Uses the functions above to:
        * list ad URLs for a search page
        * parse each ad page into our DB fields
    """

    name = "SeLoger"

    def __init__(self, session: Optional[requests.Session] = None) -> None:
        super().__init__(session=session)

    def list_ad_urls(self, search_url: str, max_pages: int = MAX_PAGES_DEFAULT) -> List[str]:
        return get_listing_urls(
            search_url=search_url,
            max_pages=max_pages,
            session=self.session,
        )

    def fetch_ad_data(self, ad_url: str) -> dict:
        """
        Fetch and parse a single ad page, and map to our buildings schema.

        Returns:
            dict ready for insertion via db.repositories.insert_building()
        """
        ad = parse_ad(ad_url, session=self.session)
        time.sleep(REQUEST_DELAY_SEC)

        # Convert price and surface to numeric types when possible
        price_int = int(ad.price) if ad.price and ad.price.isdigit() else None
        surface_float = (
            float(ad.surfaceArea) if ad.surfaceArea not in (None, "") else None
        )

        # Publication date: date of scraping (MM-DD-YYYY)
        publication_date = datetime.now().strftime("%m-%d-%Y")

        building = {
            "a_url": ad.Url,
            "a_title": ad.title,
            "a_city": ad.city,
            "a_postalCode": ad.postalCode,
            "a_price": price_int,
            "a_surfaceArea": surface_float,
            "a_description": ad.description,
            "a_images": ad.Images,
            "a_publicationDate": publication_date,
            "a_dpe": "",  # empty for now
            "a_ges": "",  # empty for now
            # llm_* and c_* fields will be filled later by enrichment
        }

        return building
