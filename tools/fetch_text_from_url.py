import asyncio
import urllib.error
import urllib.request
from langchain.tools import tool
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

@tool
def fetch_text_from_urls(urls: list[str]) -> list[str]:
    """Fetch documents from a list of URLs (strings).
    :param urls: list of urls
    :return: list of document strings
    """
    #fetch_text_from_url in parallel for all the urls
    return _fetch_text_from_urls(urls)

def _fetch_text_from_urls(urls: list[str]) -> list[str]:
    """Fetch the document from a URL.
    """
    #fetch_text_from_url in parallel for all the urls
    with ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(fetch_text_from_url, urls)

    return list(results)


def fetch_text_from_url(url: str) -> str:
    """
    Fetch the document text from a URL.
    :param url: url string
    :return:  document string from the url
    """
    print(f"Fetching text from {url}")
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; quickstart-research/1.0)"},
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            raw = resp.read()
    except urllib.error.URLError as e:
        return f"Fetch failed: {e}"
    html = raw.decode("utf-8", errors="replace")
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator=" ")

    return text
