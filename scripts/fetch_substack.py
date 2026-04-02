import json
import re
from email.utils import parsedate_to_datetime
from html import unescape
from pathlib import Path
from urllib.parse import quote

import requests

FEED_URL = "https://pronounsandpolitics.substack.com/feed"
RSS2JSON_URL = f"https://api.rss2json.com/v1/api.json?rss_url={quote(FEED_URL, safe='')}"
OUTPUT_FILE = Path("_data/substack.json")
MAX_POSTS = 12


def strip_html(text):
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", "", text)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def main():
    response = requests.get(RSS2JSON_URL, timeout=30)
    response.raise_for_status()
    data = response.json()

    items = data.get("items", [])
    posts = []

    for item in items[:MAX_POSTS]:
        title = item.get("title", "").strip()
        link = item.get("link", "").strip()
        pub_date = item.get("pubDate", "").strip()
        description = item.get("description", "").strip()

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
