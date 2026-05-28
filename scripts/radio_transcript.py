#!/usr/bin/env python3
"""
Podcast transcript automation.

Fetches an episode page HTML, extracts transcript-like text,
and stores a cited markdown file in the repository.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from typing import Any, Generator
from urllib.parse import urlparse
from urllib.request import Request, urlopen


USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/125.0 Safari/537.36"
)


def fetch_html(url: str) -> str:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=30) as resp:  # nosec B310 - user-provided URL expected by tool
        charset = resp.headers.get_content_charset() or "utf-8"
        return resp.read().decode(charset, errors="replace")


def _json_walk(node: Any) -> Generator[dict, None, None]:
    """Recursively walk nested JSON and yield dictionary nodes."""
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from _json_walk(value)
    elif isinstance(node, list):
        for item in node:
            yield from _json_walk(item)


def _clean_text(text: str) -> str:
    text = unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\r\n?", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
    return text.strip()


def extract_from_jsonld(html: str) -> str | None:
    blocks = re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    candidates = []
    for block in blocks:
        raw = block.strip()
        if not raw:
            continue
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue

        for node in _json_walk(data):
            value = node.get("transcript")
            if isinstance(value, str) and len(value.strip()) > 40:
                candidates.append(value)

    if not candidates:
        return None
    return max(candidates, key=len)


def extract_from_embedded_json(html: str) -> str | None:
    # Common "transcript":"..." pattern in embedded app state.
    matches = re.findall(r'"transcript"\s*:\s*"((?:\\.|[^"\\])*)"', html)
    if not matches:
        return None

    cleaned = []
    for m in matches:
        try:
            decoded = json.loads(f"\"{m}\"")
        except json.JSONDecodeError:
            decoded = m
        if len(decoded.strip()) > 40:
            cleaned.append(decoded)

    if not cleaned:
        return None
    return max(cleaned, key=len)


def extract_from_dom_text(html: str) -> str | None:
    # Fallback for visible transcript blocks.
    patterns = [
        r'(<[^>]+class=["\'][^"\']*transcript[^"\']*["\'][^>]*>.*?</[^>]+>)',
        r'(<p[^>]*>\s*\[[0-9:]+\].*?</p>)',
    ]
    chunks = []
    for pattern in patterns:
        chunks.extend(re.findall(pattern, html, flags=re.IGNORECASE | re.DOTALL))

    if not chunks:
        return None

    text = "\n".join(_clean_text(c) for c in chunks)
    return text if len(text.strip()) > 40 else None


def extract_transcript(html: str) -> str:
    for extractor in (extract_from_jsonld, extract_from_embedded_json, extract_from_dom_text):
        value = extractor(html)
        if value:
            cleaned = _clean_text(value)
            if cleaned:
                return cleaned
    raise ValueError("Transcript not found in source page")


def slug_from_url(url: str) -> str:
    path = urlparse(url).path.rstrip("/")
    slug = path.split("/")[-1] if path else "episode"
    # Keep Korean characters for readable slugs from Korean podcast URLs.
    slug = re.sub(r"[^0-9A-Za-z가-힣._-]+", "-", slug).strip("-")
    return slug or "episode"


def write_markdown(output_path: Path, source_url: str, transcript: str) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")

    content = [
        "# 라디오 트랜스크립트",
        "",
        f"- source: {source_url}",
        f"- fetched_at_utc: {now}",
        "- generated_by: scripts/radio_transcript.py",
        "",
        "## Transcript",
        "",
        transcript,
        "",
    ]
    output_path.write_text("\n".join(content), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract transcript from podcast episode URL")
    parser.add_argument("url", help="Podcast episode URL")
    parser.add_argument(
        "--output",
        help="Output markdown path (default: docs/transcripts/<slug>.md)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow overwriting existing output file",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.output:
        output = Path(args.output)
    else:
        output = Path("docs/transcripts") / f"{slug_from_url(args.url)}.md"

    if output.exists() and not args.overwrite:
        print(f"Output already exists: {output}. Use --overwrite to replace.")
        return 2

    try:
        html = fetch_html(args.url)
    except Exception as exc:  # pylint: disable=broad-except
        print(f"Failed to fetch page from {args.url}: {exc}")
        return 1

    try:
        transcript = extract_transcript(html)
    except Exception as exc:  # pylint: disable=broad-except
        print(f"Failed to parse transcript from {args.url}: {exc}")
        return 1

    write_markdown(output, args.url, transcript)
    print(f"Saved transcript: {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
