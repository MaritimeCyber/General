#!/usr/bin/env python3
"""Builds Asset/data/jobs-feed.json for the Maritime Jobs Feed widget.

Browsers cannot read Google News RSS directly (CORS) and the free RSS relays are
unreliable, so this runs on a schedule and the widget reads the saved file.
Keeps the old file when nothing could be fetched, and rewrites it only when the
items change.
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

OUT = pathlib.Path("Asset/data/jobs-feed.json")
MAX_AGE_DAYS = 180
MAX_ITEMS = 300
EN = "hl=en-US&gl=US&ceid=US:en"
KR = "hl=ko&gl=KR&ceid=KR:ko"
QUERIES = [
    ("maritime jobs hiring", EN),
    ("maritime cybersecurity hiring", EN),
    ("shipping company appoints chief digital officer", EN),
    ("maritime data engineer AI hiring", EN),
    ("shipping compliance officer appointed", EN),
    ("marine engineer naval architect recruitment", EN),
    ("해운 채용", KR),
    ("조선 해운 채용", KR),
]
# Google News matches loosely, so keep only titles that are clearly about the sector.
RELEVANT = re.compile(
    r"\b(maritime|shipping|shipowners?|ships?|vessels?|marine|naval|seafarers?|shipyards?|shipbuild\w*|offshore|tankers?|ports?|carriers?)\b"
    r"|해운|해양|조선|항만|선박|항로|선원|해사|해기사",
    re.I,
)


def fetch(query, lang):
    url = "https://news.google.com/rss/search?q=%s&%s" % (urllib.parse.quote_plus(query), lang)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (ShipPaulJobs feed builder)"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return ET.fromstring(resp.read())


def clean(text):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", text or ""))).strip()


def main():
    now, items, seen, ok = time.time(), [], set(), 0
    for query, lang in QUERIES:
        try:
            root = fetch(query, lang)
        except Exception as err:
            print("FAILED %s: %s" % (query, err), file=sys.stderr)
            continue
        ok += 1
        for node in root.iter("item"):
            title = clean(node.findtext("title"))
            pub = node.findtext("pubDate") or ""
            key = title.lower()[:80]
            if not title or key in seen or not RELEVANT.search(title):
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
                "_src": "Google News KR" if lang == KR else "Google News",
            }))
        time.sleep(1)
    print("%d/%d queries ok, %d items" % (ok, len(QUERIES), len(items)))
    if not items:
        print("Nothing fetched; keeping the existing file.", file=sys.stderr)
        return 1
    items.sort(key=lambda pair: pair[0], reverse=True)
    rows = [row for _, row in items[:MAX_ITEMS]]
    if OUT.exists() and json.loads(OUT.read_text(encoding="utf-8")).get("items") == rows:
        print("No change.")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now))
    OUT.write_text(json.dumps({"updated": stamp, "items": rows}, ensure_ascii=False, indent=0) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
