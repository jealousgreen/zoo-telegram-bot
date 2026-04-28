from __future__ import annotations

import json
import logging
from urllib.parse import urljoin

import aiohttp
from bs4 import BeautifulSoup

from bot.data.models import Animal

logger = logging.getLogger(__name__)

_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; MoscowZooTotemBot/1.0; +https://t.me/)"
}


def _absolute(base_url: str, maybe_url: str | None) -> str | None:
    if not maybe_url:
        return None
    maybe_url = maybe_url.strip()
    if maybe_url.startswith("//"):
        return "https:" + maybe_url
    return urljoin(base_url, maybe_url)


async def resolve_photo_url(animal: Animal) -> str | None:

    if animal.photo_url:
        return animal.photo_url

    try:
        timeout = aiohttp.ClientTimeout(total=8)
        async with aiohttp.ClientSession(timeout=timeout, headers=_HEADERS) as session:
            async with session.get(animal.species_url) as response:
                if response.status >= 400:
                    logger.warning("Cannot fetch %s: HTTP %s", animal.species_url, response.status)
                    return None
                html = await response.text()
    except Exception:
        logger.exception("Cannot fetch animal page: %s", animal.species_url)
        return None

    soup = BeautifulSoup(html, "html.parser")

    meta_selectors = [
        ("property", "og:image"),
        ("name", "twitter:image"),
        ("property", "vk:image"),
    ]
    for attr, value in meta_selectors:
        tag = soup.find("meta", attrs={attr: value})
        url = _absolute(animal.species_url, tag.get("content") if tag else None)
        if url:
            return url

    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        try:
            data = json.loads(script.string or "{}")
        except json.JSONDecodeError:
            continue
        candidates = data if isinstance(data, list) else [data]
        for item in candidates:
            if not isinstance(item, dict):
                continue
            image = item.get("image")
            if isinstance(image, str):
                return _absolute(animal.species_url, image)
            if isinstance(image, list) and image:
                return _absolute(animal.species_url, str(image[0]))
            if isinstance(image, dict):
                return _absolute(animal.species_url, image.get("url"))

    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src") or img.get("data-lazy-src")
        url = _absolute(animal.species_url, src)
        if url and not url.endswith(".svg"):
            return url

    return None
