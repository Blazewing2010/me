import json
import re
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from html import unescape
from pathlib import Path

import requests

FEED_URL = "https://pronounsandpolitics.substack.com/feed"
OUTPUT_FILE = Path("_data/substack.json")
MAX_POSTS = 12


def strip_html(text):
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", "", text)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def get_text(element, tag_names):
    for tag in tag_names:
        found = element.find(tag)
        if found is not None and found.text:
            return found.text.strip()
    return ""


def main():
    session = requests.Session()
    response = session.get(
        FEED_URL,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept": "application/rss+xml, application/xml, text/xml;q=0.9, */*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://pronounsandpolitics.substack.com/",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        },
        timeout=30,
    )
    response.raise_for_status()

    root = ET.fromstring(response.content)
    channel = root.find("channel")
    if channel is None:
        raise ValueError("Could not find RSS channel in Substack feed.")

    items = channel.findall("item")
    posts = []

    for item in items[:MAX_POSTS]:
        title = get_text(item, ["title"])
        link = get_text(item, ["link"])
        pub_date = get_text(item, ["pubDate"])
        description = get_text(
            item,
            ["description", "{http://purl.org/rss/1.0/modules/content/}encoded"],
        )

        parsed_date = ""
        if pub_date:
            try:
                parsed_date = parsedate_to_datetime(pub_date).date().isoformat()
            except Exception:
                parsed_date = pub_date

        excerpt = strip_html(description)
        if len(excerpt) > 280:
            excerpt = excerpt[:280].rsplit(" ", 1)[0] + "..."

        posts.append(
            {
                "title": title,
                "link": link,
                "date": parsed_date,
                "excerpt": excerpt,
            }
        )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(posts)} posts to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
