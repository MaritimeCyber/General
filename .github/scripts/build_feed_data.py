#!/usr/bin/env python3
"""Builds the JSON files read by the blog's live feed widgets (Asset/data/).

Browsers cannot read these RSS feeds directly (CORS) and the free RSS relays are
unreliable, so this runs on a schedule and the widgets read the saved files.
A file is kept when nothing could be fetched, and rewritten only when its items
change.
"""
import email.utils
import html
import json
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

OUT_DIR = pathlib.Path("Asset/data")
MAX_AGE_DAYS = 180
MAX_ITEMS = 300
EN = "hl=en-US&gl=US&ceid=US:en"
KR = "hl=ko&gl=KR&ceid=KR:ko"


def gnews(query, lang=EN):
    return (
        "https://news.google.com/rss/search?q=%s&%s" % (urllib.parse.quote_plus(query), lang),
        "Google News KR" if lang == KR else "Google News",
    )


# Google News matches loosely, so each feed keeps only titles clearly on its subject.
FEEDS = {
    "jobs-feed.json": {
        "sources": [
            gnews("maritime jobs hiring"),
            gnews("maritime cybersecurity hiring"),
            gnews("shipping company appoints chief digital officer"),
            gnews("maritime data engineer AI hiring"),
            gnews("shipping compliance officer appointed"),
            gnews("marine engineer naval architect recruitment"),
            gnews("해운 채용", KR),
            gnews("조선 해운 채용", KR),
        ],
        "relevant": re.compile(
            r"\b(maritime|shipping|shipowners?|ships?|vessels?|marine|naval|seafarers?|shipyards?|shipbuild\w*|offshore|tankers?|ports?|carriers?)\b"
            r"|해운|해양|조선|항만|선박|항로|선원|해사|해기사",
            re.I,
        ),
    },
    "ship-orders.json": {
        "sources": [
            gnews("ship newbuilding order shipbuilding"),
            gnews("newbuilding order shipyard"),
            gnews("shipyard wins order vessels"),
            gnews("tanker newbuilding order"),
            gnews("containership newbuilding order"),
            gnews("LNG carrier newbuilding order"),
            gnews("bulk carrier newbuilding order"),
            gnews("car carrier PCTC newbuilding order"),
            ("https://gcaptain.com/feed/", "gCaptain"),
        ],
        "relevant": re.compile(r"\b(newbuild\w*|new-?build\w*|shipbuild\w*|shipyards?|orders?|ordered|orderbook)\b", re.I),
    },
}


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (ShipPaulJobs feed builder)"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return ET.fromstring(resp.read())


def clean(text):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", html.unescape(text or "")))).strip()


def build(name, feed):
    now, items, seen, ok = time.time(), [], set(), 0
    for url, source in feed["sources"]:
        try:
            root = fetch(url)
        except Exception as err:
            print("FAILED %s: %s" % (url, err), file=sys.stderr)
            continue
        ok += 1
        for node in root.iter("item"):
            title = clean(node.findtext("title"))
            pub = node.findtext("pubDate") or ""
            key = title.lower()[:80]
            if not title or key in seen or not feed["relevant"].search(title):
                continue
            try:
                stamp = email.utils.parsedate_to_datetime(pub).timestamp()
            except (TypeError, ValueError):
                continue
            if now - stamp > MAX_AGE_DAYS * 86400:
                continue
            seen.add(key)
            items.append((stamp, {
                "title": title,
                "link": (node.findtext("link") or "").strip(),
                "pubDate": pub,
                "description": clean(node.findtext("description"))[:160],
                "_src": source,
            }))
        time.sleep(1)
    print("%s: %d/%d sources ok, %d items" % (name, ok, len(feed["sources"]), len(items)))
    if not items:
        print("%s: nothing fetched; keeping the existing file." % name, file=sys.stderr)
        return False
    items.sort(key=lambda pair: pair[0], reverse=True)
    rows = [row for _, row in items[:MAX_ITEMS]]
    out = OUT_DIR / name
    if out.exists() and json.loads(out.read_text(encoding="utf-8")).get("items") == rows:
        print("%s: no change." % name)
        return True
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    updated = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now))
    out.write_text(json.dumps({"updated": updated, "items": rows}, ensure_ascii=False, indent=0) + "\n", encoding="utf-8")
    return True


def main():
    results = [build(name, feed) for name, feed in FEEDS.items()]
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
