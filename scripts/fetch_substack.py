import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from html import unescape
from pathlib import Path
from urllib.error import HTTPError

FEED_URL = "https://YOURSUBSTACKNAME.substack.com/feed"
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
    req = urllib.request.Request(
        FEED_URL,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/rss+xml, application/xml, text/xml;q=0.9, */*;q=0.8",
        },
    )

    try:
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
    except HTTPError as e:
        raise RuntimeError(f"Could not fetch feed {FEED_URL}: HTTP {e.code}") from e

    root = ET.fromstring(xml_data)
    channel = root.find("channel")

    if channel is None:
        raise ValueError("Could not find RSS channel in Substack feed.")

    items = channel.findall("item")
    print(f"Found {len(items)} feed items")

    posts = []

    for item in items[:MAX_POSTS]:
        title = get_text(item, ["title"])
        link = get_text(item, ["link"])
        pub_date = get_text(item, ["pubDate"])
        description = get_text(
            item,
            ["description", "{http://purl.org/rss/1.0/modules/content/}encoded"]
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

        posts.append({
            "title": title,
            "link": link,
            "date": parsed_date,
            "excerpt": excerpt
        })

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(posts)} posts to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
