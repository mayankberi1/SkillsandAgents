#!/usr/bin/env python3
"""Fetch RSS and Atom feed metadata as JSON using only the standard library."""

import argparse
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import json
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _child_text(element: ET.Element, name: str) -> str | None:
    for child in element:
        if _local_name(child.tag) == name:
            text = " ".join(child.itertext()).strip()
            return text or None
    return None


def _valid_http_url(value: str | None) -> bool:
    if not value:
        return False
    try:
        parsed = urlsplit(value.strip())
        return parsed.scheme.lower() in {"http", "https"} and bool(parsed.hostname)
    except ValueError:
        return False


def _parse_published(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError:
        try:
            parsed = parsedate_to_datetime(value.strip())
        except (TypeError, ValueError, OverflowError):
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _entry_link(entry: ET.Element) -> str | None:
    links = [child for child in entry if _local_name(child.tag) == "link"]
    # RSS uses element text; Atom article links are href attributes.
    for link in links:
        if link.attrib.get("rel", "alternate") != "alternate":
            continue
        value = link.attrib.get("href") or (link.text or "").strip()
        if _valid_http_url(value):
            return value.strip()
    return None


def _parse_feed(raw_data: bytes, source_url: str) -> list[dict]:
    root = ET.fromstring(raw_data)
    feed_element = next(
        (element for element in root.iter() if _local_name(element.tag) in {"channel", "feed"}),
        root,
    )
    feed_name = _child_text(feed_element, "title")
    entries = [child for child in root.iter() if _local_name(child.tag) in {"item", "entry"}]
    articles = []

    for entry in entries:
        published = _parse_published(
            _child_text(entry, "pubDate")
            or _child_text(entry, "published")
            or _child_text(entry, "updated")
        )
        summary = (
            _child_text(entry, "description")
            or _child_text(entry, "summary")
            or _child_text(entry, "content")
            or _child_text(entry, "encoded")
        )
        articles.append(
            {
                "title": _child_text(entry, "title"),
                "url": _entry_link(entry),
                "published": published.isoformat().replace("+00:00", "Z") if published else None,
                "source": source_url,
                "source_name": feed_name,
                "summary": summary,
            }
        )
    return articles


def _safe_error(url: str, message: str) -> dict:
    return {"url": url, "scope": "feed", "code": "fetch_failed", "message": message}


def _fetch_feed(url: str, timeout: float) -> bytes:
    request = Request(url, headers={"User-Agent": "news-collector/1.0"})
    with urlopen(request, timeout=timeout) as response:
        return response.read()


def collect_feeds(urls: list[str], timeout: float = 15.0) -> dict:
    articles = []
    errors = []
    for url in urls:
        if not _valid_http_url(url):
            errors.append(_safe_error(url, "Feed URL must be a valid HTTP(S) URL."))
            continue
        try:
            articles.extend(_parse_feed(_fetch_feed(url, timeout), url))
        except (HTTPError, URLError, TimeoutError, OSError):
            errors.append(_safe_error(url, "Feed could not be fetched."))
        except ET.ParseError:
            errors.append(_safe_error(url, "Feed could not be parsed as RSS or Atom."))
    return {"articles": articles, "errors": errors}


def _positive_timeout(value: str) -> float:
    try:
        timeout = float(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("timeout must be a positive number") from error
    if timeout <= 0 or not timeout < float("inf"):
        raise argparse.ArgumentTypeError("timeout must be a positive number")
    return timeout


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Read RSS/Atom feeds and return article metadata as JSON."
    )
    parser.add_argument(
        "--timeout",
        type=_positive_timeout,
        default=15.0,
        help="feed request timeout in seconds (default: 15)",
    )
    parser.add_argument("urls", nargs="+", help="HTTP(S) feed URLs")
    args = parser.parse_args(argv)
    invalid_urls = [url for url in args.urls if not _valid_http_url(url)]
    if invalid_urls:
        parser.error("feed URLs must use HTTP or HTTPS and include a hostname")
    json.dump(collect_feeds(args.urls, args.timeout), sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
