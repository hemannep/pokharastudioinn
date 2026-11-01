#!/usr/bin/env python3
"""Safely refresh listing-scoped photo URLs from public Airbnb pages."""

from __future__ import annotations

import html
import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "js" / "data.js"
INDEX_FILE = ROOT / "index.html"
SITEMAP_FILE = ROOT / "sitemap.xml"
MIN_VALID_PHOTOS = 5
MAX_VALID_PHOTOS = 80
MAX_RESPONSE_BYTES = 12 * 1024 * 1024

FORBIDDEN_IMAGE_KEYWORDS = (
    "platform",
    "platformassets",
    "airbnbplatformassets",
    "/user/",
    "favicon",
    "icon",
    "logo",
    "badge",
    "search-bar-icons",
    "review-ai-synthesis",
    "userprofile",
)

PHOTO_PATTERN = re.compile(
    r"https://a0\.muscache\.com/im/pictures/[^\"'<>\s?]+",
    re.IGNORECASE,
)


def is_clean_listing_photo(url: str, listing_id: str) -> bool:
    """Check that the URL is a genuine apartment photo and not a platform icon or user avatar."""
    low = url.lower()
    if any(keyword in low for keyword in FORBIDDEN_IMAGE_KEYWORDS):
        return False
    hosting_match = re.search(r"/hosting-(\d+)/", low)
    if hosting_match and hosting_match.group(1) != str(listing_id):
        return False
    return True


def fetch_listing(url: str, attempts: int = 3) -> str:
    """Fetch a bounded HTML response, retrying transient network failures."""
    last_error: Exception | None = None
    for attempt in range(attempts):
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/131.0 Safari/537.36"
                ),
                "Accept": "text/html,application/xhtml+xml",
                "Accept-Language": "en-US,en;q=0.9",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                final_host = urllib.parse.urlparse(response.geturl()).hostname or ""
                content_type = response.headers.get_content_type()
                if not (final_host == "airbnb.com" or final_host.endswith(".airbnb.com")):
                    raise ValueError(f"unexpected redirect host: {final_host}")
                if content_type not in {"text/html", "application/xhtml+xml"}:
                    raise ValueError(f"unexpected content type: {content_type}")
                body = response.read(MAX_RESPONSE_BYTES + 1)
                if len(body) > MAX_RESPONSE_BYTES:
                    raise ValueError("Airbnb response exceeded safety limit")
                return body.decode("utf-8", errors="replace")
        except (urllib.error.URLError, TimeoutError, ValueError) as exc:
            last_error = exc
            if attempt + 1 < attempts:
                time.sleep(2**attempt)

    raise RuntimeError(f"listing fetch failed after {attempts} attempts: {last_error}")


def extract_photos(page: str, listing_id: str) -> list[str]:
    """Extract authentic listing photos from Airbnb, strictly excluding platform assets and user avatars."""
    decoded = html.unescape(page).replace("\\u002F", "/").replace("\\/", "/")
    photos: list[str] = []
    seen: set[str] = set()

    def add_photo(raw_url: str) -> None:
        base = raw_url.split("?")[0].rstrip("\\")
        if base not in seen and is_clean_listing_photo(base, listing_id):
            seen.add(base)
            photos.append(f"{base}?im_w=1200")

    # 1. Parse official PhotoTourModalSection / mediaItems from script data
    script_matches = re.findall(r"<script\b[^>]*>(.*?)</script>", decoded, re.DOTALL)
    for s in script_matches:
        if "PhotoTourModalSection" in s or "mediaItems" in s:
            trimmed = s.strip()
            try:
                if trimmed.startswith("{") and trimmed.endswith("}"):
                    obj = json.loads(trimmed)
                else:
                    m = re.search(r"(\{.*\})", trimmed, re.DOTALL)
                    obj = json.loads(m.group(1)) if m else None

                if obj:
                    def walk(node: object) -> None:
                        if isinstance(node, dict):
                            if node.get("__typename") == "PhotoTourModalSection" or "mediaItems" in node:
                                items = node.get("mediaItems")
                                if isinstance(items, list):
                                    for item in items:
                                        if isinstance(item, dict) and "baseUrl" in item:
                                            add_photo(str(item["baseUrl"]))
                            for v in node.values():
                                walk(v)
                        elif isinstance(node, list):
                            for v in node:
                                walk(v)

                    walk(obj)
            except Exception:
                pass
        if len(photos) >= MIN_VALID_PHOTOS:
            break

    # 2. Check JSON-LD metadata for listing photos
    for s in script_matches:
        if "schema.org" in s and "image" in s:
            try:
                obj = json.loads(s.strip())
                imgs = obj.get("image", [])
                if isinstance(imgs, list):
                    for img in imgs:
                        if isinstance(img, str) and "muscache" in img:
                            add_photo(img)
            except Exception:
                pass

    # 3. Add any direct listing-specific hosting photos
    listing_token = f"/Hosting-{listing_id}/".lower()
    for match in PHOTO_PATTERN.finditer(decoded):
        candidate = match.group(0).rstrip("\\")
        if listing_token in candidate.lower():
            add_photo(candidate)

    return photos[:MAX_VALID_PHOTOS]


def load_constant(source: str, name: str):
    marker = f"const {name} = "
    start = source.index(marker) + len(marker)
    end = source.index(";", start)
    return json.loads(source[start:end])


def replace_constant(source: str, name: str, value) -> str:
    marker = f"const {name} = "
    start = source.index(marker) + len(marker)
    end = source.index(";", start)
    serialized = json.dumps(value, indent=2, ensure_ascii=False)
    return source[:start] + serialized + source[end:]


def write_atomic(path: Path, content: str) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content, encoding="utf-8")
    os.replace(temporary, path)


def main() -> int:
    source = DATA_FILE.read_text(encoding="utf-8")
    apartments = load_constant(source, "APARTMENTS_DATA")
    hero_slides = load_constant(source, "HERO_SLIDES")
    changed = 0
    failures = 0

    for apartment in apartments:
        listing_id = str(apartment["id"])
        try:
            photos = extract_photos(fetch_listing(apartment["url"]), listing_id)
        except Exception as exc:  # Existing galleries are preserved on every failure path.
            failures += 1
            print(f"SKIP {listing_id}: {exc}")
            continue

        current_count = len(apartment.get("images", []))
        minimum_expected = MIN_VALID_PHOTOS
        if not minimum_expected <= len(photos) <= MAX_VALID_PHOTOS:
            failures += 1
            print(
                f"SKIP {listing_id}: untrusted gallery size "
                f"{len(photos)} (expected at least {minimum_expected})"
            )
            continue

        if apartment.get("images") != photos:
            apartment["images"] = photos
            changed += 1
            print(f"UPDATE {listing_id}: {len(photos)} verified photos")
        else:
            print(f"OK {listing_id}: unchanged")

        time.sleep(1)

    if failures > len(apartments) // 2:
        print(f"ABORT: {failures} of {len(apartments)} listings failed validation")
        return 1

    if changed:
        first_images = {str(item["id"]): item["images"][0] for item in apartments if item["images"]}
        for slide in hero_slides:
            if str(slide.get("apt_id")) in first_images:
                slide["image"] = first_images[str(slide["apt_id"])]

        updated = replace_constant(source, "HERO_SLIDES", hero_slides)
        updated = replace_constant(updated, "APARTMENTS_DATA", apartments)
        write_atomic(DATA_FILE, updated)

        # A content-derived version makes browsers/CDNs request the refreshed
        # gallery immediately while keeping long-lived caching safe.
        data_version = hashlib.sha256(updated.encode("utf-8")).hexdigest()[:12]

        first_hero_image = hero_slides[0]["image"]
        index_source = INDEX_FILE.read_text(encoding="utf-8")
        index_updated, replacements = re.subn(
            r'(<link rel="preload" as="image" href=")[^"]+(" fetchpriority="high">)',
            rf"\g<1>{first_hero_image}\g<2>",
            index_source,
            count=1,
        )
        if replacements != 1:
            raise RuntimeError("hero preload marker was not found in index.html")
        index_updated, replacements = re.subn(
            r'<script src="js/data\.js(?:\?v=[^"]+)?"></script>',
            f'<script src="js/data.js?v={data_version}"></script>',
            index_updated,
            count=1,
        )
        if replacements != 1:
            raise RuntimeError("data script marker was not found in index.html")
        write_atomic(INDEX_FILE, index_updated)

        sitemap_source = SITEMAP_FILE.read_text(encoding="utf-8")
        sitemap_updated, replacements = re.subn(
            r"<lastmod>\d{4}-\d{2}-\d{2}</lastmod>",
            f"<lastmod>{date.today().isoformat()}</lastmod>",
            sitemap_source,
            count=1,
        )
        if replacements != 1:
            raise RuntimeError("lastmod marker was not found in sitemap.xml")
        write_atomic(SITEMAP_FILE, sitemap_updated)

    print(f"Finished: {changed} listing(s) updated, {failures} skipped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
