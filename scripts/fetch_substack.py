import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from html import unescape
from pathlib import Path

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
    with urllib.request.urlopen(FEED_URL) as response:
        xml_data = response.read()

    root = ET.fromstring(xml_data)
    channel = root.find("channel")

    posts = []

    if channel is None:
        raise ValueError("Could not find RSS channel in Substack feed.")

    for item in channel.findall("item")[:MAX_POSTS]:
        title = get_text(item, ["title"])
        link = get_text(item, ["link"])
        pub_date = get_text(item, ["pubDate"])
        description = get_text(item, ["description", "{http://purl.org/rss/1.0/modules/content/}encoded"])

        parsed_date = ""
        if pub_date:
            try:
                parsed_date = parsedate_to_datetime(pub_date).date().isoformat()
            except Exception:
                parsed_date = pub_date

        excerpt = strip_html(description)
        excerpt = excerpt[:280].rsplit(" ", 1)[0] + "..." if len(excerpt) > 280 else excerpt

        posts.append({
            "title": title,
            "link": link,
            "date": parsed_date,
            "excerpt": excerpt
        })

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
