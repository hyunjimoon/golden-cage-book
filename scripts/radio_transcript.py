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
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/125.0 Safari/537.36"
)
ALLOWED_HOSTS = ("listennotes.com", "www.listennotes.com")


def fetch_html(url: str) -> str:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=30) as resp:  # nosec B310 - user-provided URL expected by tool
        charset = resp.headers.get_content_charset() or "utf-8"
        return resp.read().decode(charset, errors="replace")


def validate_source_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only http/https URLs are allowed")
    if not parsed.hostname:
        raise ValueError("URL hostname is required")
    hostname = parsed.hostname.lower()
    if hostname not in ALLOWED_HOSTS and not hostname.endswith(".listennotes.com"):
        raise ValueError("Only listennotes.com hosts are allowed")


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


def _decode_json_escapes(value: str) -> str:
    return (
        value.replace("\\\\", "\\")
        .replace("\\n", "\n")
        .replace("\\r", "\r")
        .replace("\\t", "\t")
        .replace('\\"', '"')
        .replace("\\/", "/")
    )


def _extract_json_value_strings(source: str, key: str) -> list[str]:
    values = []
    marker = f'"{key}"'
    start = 0
    while True:
        idx = source.find(marker, start)
        if idx == -1:
            break
        colon = source.find(":", idx + len(marker))
        quote = source.find('"', colon + 1) if colon != -1 else -1
        if colon == -1 or quote == -1:
            start = idx + len(marker)
            continue

        i = quote + 1
        escaped = False
        chars = []
        while i < len(source):
            ch = source[i]
            if escaped:
                chars.append("\\" + ch)
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                break
            else:
                chars.append(ch)
            i += 1

        if i < len(source) and source[i] == '"':
            values.append("".join(chars))
            start = i + 1
        else:
            start = idx + len(marker)
            continue
    return values


def extract_from_embedded_json(html: str) -> str | None:
    # Common "transcript":"..." pattern in embedded app state.
    matches = _extract_json_value_strings(html, "transcript")
    if not matches:
        return None

    cleaned = []
    for m in matches:
        decoded = _decode_json_escapes(m)
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
    # Keep Hangul syllables (가-힣) for readable slugs in Korean URLs.
    slug = re.sub(r"[^0-9A-Za-z가-힣._-]+", "-", slug).strip("-")
    return slug or "episode"


def write_markdown(output_path: Path, source_url: str, transcript: str) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

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
        validate_source_url(args.url)
    except ValueError as exc:
        print(f"Invalid source URL: {exc}")
        return 1

    try:
        html = fetch_html(args.url)
    except HTTPError as exc:
        print(f"Failed to fetch page from {args.url}: HTTP {exc.code}")
        return 1
    except URLError as exc:
        print(f"Failed to fetch page from {args.url}: {exc.reason}")
        return 1
    except TimeoutError:
        print(f"Failed to fetch page from {args.url}: request timeout")
        return 1
    except OSError as exc:
        print(f"Failed to fetch page from {args.url}: {exc}")
        return 1

    try:
        transcript = extract_transcript(html)
    except ValueError as exc:
        print(f"Failed to parse transcript from {args.url}: {exc}")
        return 1

    write_markdown(output, args.url, transcript)
    print(f"Saved transcript: {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
