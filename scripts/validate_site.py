#!/usr/bin/env python3
"""Fast, dependency-free integrity checks for the static site."""

from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
SITE_URL = "https://pokharastudioinn.com.np/"

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


def load_constant(source: str, name: str):
    marker = f"const {name} = "
    start = source.index(marker) + len(marker)
    end = source.index(";", start)
    return json.loads(source[start:end])


def fail(message: str) -> None:
    raise AssertionError(message)


def validate_image(path_or_url: str, listing_id: str | None = None) -> None:
    if path_or_url.startswith(("https://", "http://")):
        parsed = urlparse(path_or_url)
        if parsed.scheme != "https" or parsed.hostname != "a0.muscache.com":
            fail(f"untrusted remote image URL: {path_or_url}")
        
        low = path_or_url.lower()
        for kw in FORBIDDEN_IMAGE_KEYWORDS:
            if kw in low:
                fail(f"forbidden platform/avatar asset detected in images: {path_or_url}")
        
        if listing_id:
            hosting_match = re.search(r"/hosting-(\d+)/", low)
            if hosting_match and hosting_match.group(1) != str(listing_id):
                fail(f"{listing_id} contains remote image belonging to another listing: {path_or_url}")
        return

    path = ROOT / path_or_url
    if not path.is_file():
        fail(f"missing local image: {path_or_url}")
    signature = path.read_bytes()[:12]
    suffix = path.suffix.lower()
    if suffix in {".jpg", ".jpeg"} and not signature.startswith(b"\xff\xd8\xff"):
        fail(f"JPEG extension/content mismatch: {path_or_url}")
    if suffix == ".png" and signature[:8] != b"\x89PNG\r\n\x1a\n":
        fail(f"PNG extension/content mismatch: {path_or_url}")


def main() -> int:
    data_source = (ROOT / "js" / "data.js").read_text(encoding="utf-8")
    html_source = (ROOT / "index.html").read_text(encoding="utf-8")
    robots_source = (ROOT / "robots.txt").read_text(encoding="utf-8")
    apartments = load_constant(data_source, "APARTMENTS_DATA")
    slides = load_constant(data_source, "HERO_SLIDES")
    reviews = load_constant(data_source, "REVIEWS_DATA")

    if len(apartments) != 9:
        fail(f"expected 9 apartments, found {len(apartments)}")
    ids = [str(item.get("id", "")) for item in apartments]
    duplicates = [item for item, count in Counter(ids).items() if count > 1]
    if duplicates:
        fail(f"duplicate apartment IDs: {duplicates}")

    required = {"id", "url", "name", "tagline", "description", "rating", "reviews", "images"}
    for apartment in apartments:
        missing = required - apartment.keys()
        if missing:
            fail(f"{apartment.get('id', 'unknown')} missing fields: {sorted(missing)}")
        if len(apartment["images"]) < 3:
            fail(f"{apartment['id']} has fewer than 3 photos")
        if not apartment["url"].startswith("https://www.airbnb.com/rooms/"):
            fail(f"invalid listing URL for {apartment['id']}")
        for image in apartment["images"]:
            validate_image(image, str(apartment["id"]))

    known_ids = set(ids)
    for slide in slides:
        if str(slide.get("apt_id")) not in known_ids:
            fail(f"hero references unknown apartment: {slide.get('apt_id')}")
        validate_image(slide["image"], str(slide.get("apt_id")))

    if not reviews:
        fail("reviews data is empty")

    document_ids = re.findall(r'\bid="([^"]+)"', html_source)
    duplicate_document_ids = [item for item, count in Counter(document_ids).items() if count > 1]
    if duplicate_document_ids:
        fail(f"duplicate HTML IDs: {duplicate_document_ids}")
    if len(re.findall(r"<h1\b", html_source, flags=re.IGNORECASE)) != 1:
        fail("index.html must contain exactly one h1")
    if f'<link rel="canonical" href="{SITE_URL}">' not in html_source:
        fail("canonical URL is missing or does not use the production domain")
    if f"Sitemap: {SITE_URL}sitemap.xml" not in robots_source:
        fail("robots.txt sitemap URL does not match the production domain")

    sitemap = ET.parse(ROOT / "sitemap.xml")
    locations = [element.text for element in sitemap.findall("{*}url/{*}loc")]
    if locations != [SITE_URL]:
        fail(f"unexpected sitemap URLs: {locations}")

    structured_blocks = re.findall(
        r'<script type="application/ld\+json">\s*(.*?)\s*</script>',
        html_source,
        flags=re.DOTALL,
    )
    for block in structured_blocks:
        json.loads(block)

    print(
        f"Validated {len(apartments)} apartments, "
        f"{sum(len(item['images']) for item in apartments)} photos, "
        f"{len(slides)} hero slides, and {len(reviews)} reviews."
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, json.JSONDecodeError, ValueError) as exc:
        print(f"VALIDATION FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
