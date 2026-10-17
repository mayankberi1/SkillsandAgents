import feedparser
from datetime import date, timedelta, timezone
from concurrent.futures import ThreadPoolExecutor
from tools.fetch_text_from_url import fetch_text_from_url
from datetime import datetime

# Get the current local date
today = date.today()

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