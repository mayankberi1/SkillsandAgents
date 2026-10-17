from datetime import date, timedelta, timezone

import feedparser
from langchain.tools import tool
from concurrent.futures import ThreadPoolExecutor
from tools.fetch_text_from_url import fetch_text_from_url
from tools.text_summariser import summarise_texts
import socket
from datetime import datetime

# Get the current local date
today = date.today()

@tool
def rss_reader(feed_urls: list[str]) -> list[dict]:
    """Read an RSS or Atom feeds and return their contents as JSON.

    Args:
        :param after_date: The date to start reading feeds from. optional.
        :param feed_urls: list of RSS or Atom Urls (string) to read
        :returns: return dictionary.
    """
    socket.setdefaulttimeout(5.0)
    with ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(read_rss_feed, feed_urls, timeout=5)

    list_entries = []

    for feeds in results:
        for entry in feeds:
            list_entries.append(entry)

    return list_entries


def read_rss_feed(feed_url: str) -> list[dict]:
    news_articles = []
    try:
        feed = feedparser.parse(feed_url)

        print(f"Reading {feed_url}: {len(feed.entries)}")

        for entry in feed.entries:
            # print(entry)
            # only pick if pubdate is on or after after_date
            published = datetime(
                *entry.published_parsed[:6],
                tzinfo=timezone.utc,
            )

            cutoff = datetime.now(timezone.utc) - timedelta(days=1)

            if published >= cutoff:
                # print("Published within the last day")
                news_articles.append(
                    {
                        "source": feed_url,
                        "title": entry.get("title", ""),
                        "url": entry.get("link",""),
                        'tags': entry.get("tags",""),
                        'summary': entry.get("summary",""),
                        'links': entry.get("links",""),
                        'author': entry.get("author",""),
                        'published': published
                    }
                )

        with ThreadPoolExecutor(max_workers=25) as executor:
            article_texts = list(
                executor.map(
                    fetch_text_from_url,
                    (article["url"] for article in news_articles),
                )
            )

        # summaries = summarise_texts(article_texts)
        #
        # for article, summary in zip(news_articles, summaries):
        #     article["detailed_description"] = summary

        return news_articles

    except Exception as exc:
        return [{"error": f"Unable to read feed: {exc}"}]
