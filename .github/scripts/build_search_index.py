#!/usr/bin/env python3
"""Builds Asset/data/search-index.json for the ShipJobs bot (ComplianceBot.html).

Indexes the text of every published blog post, plus document titles from the
folders listed in .github/search-sources.json. Unpublished files in the repository
are never read. The file is kept when the blog looks unreachable, and rewritten
only when its contents change.
"""
import html
import json
import pathlib
import re
import sys
import time
import urllib.request

FEED = "https://www.shippauljobs.com/feeds/posts/default?alt=json&max-results=150&start-index=%d"
OUT = pathlib.Path("Asset/data/search-index.json")
SOURCES = pathlib.Path(".github/search-sources.json")
MIN_POSTS = 100
CHUNK_CHARS = 700
MAX_POST_CHARS = 15000
DOC_TYPES = {".pdf", ".docx", ".doc", ".pptx", ".xlsx"}


def fetch_posts():
    posts, start = [], 1
    while True:
        req = urllib.request.Request(FEED % start, headers={"User-Agent": "ShipPaulJobs search index builder"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            entries = json.load(resp)["feed"].get("entry", [])
        if not entries:
            return posts
        posts.extend(entries)
        start += len(entries)
        time.sleep(1)


def to_text(markup):
    markup = re.sub(r"(?is)<(style|script)\b.*?</\1>|<!--.*?-->", " ", markup)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", markup))).strip()


def chunks(text):
    out, cur = [], ""
    for part in re.split(r"(?<=[.!?。])\s+", text[:MAX_POST_CHARS]):
        if cur and len(cur) + len(part) > CHUNK_CHARS:
            out.append(cur)
            cur = ""
        cur = (cur + " " + part).strip()
    if cur:
        out.append(cur)
    return [c[:CHUNK_CHARS * 2] for c in out]


def catalog():
    config = json.loads(SOURCES.read_text(encoding="utf-8"))
    rows = []
    for entry in config["catalog"]:
        for path in sorted(pathlib.Path(entry["folder"]).rglob("*")):
            if path.suffix.lower() not in DOC_TYPES or any(x in str(path) for x in entry["exclude"]):
                continue
            rows.append({"t": re.sub(r"[_]+", " ", path.stem).strip(), "u": entry["link"], "s": entry["source"]})
    return rows


def main():
    entries = fetch_posts()
    if len(entries) < MIN_POSTS:
        print("Only %d posts fetched; keeping the existing index." % len(entries), file=sys.stderr)
        return 1
    posts = []
    for e in entries:
        link = next((l["href"] for l in e.get("link", []) if l.get("rel") == "alternate"), "")
        if not link:
            continue
        posts.append({
            "t": html.unescape(e["title"]["$t"]).strip(),
            "u": link,
            "d": e["published"]["$t"][:10],
            "l": [c["term"] for c in e.get("category", [])],
            "c": chunks(to_text(e.get("content", {}).get("$t", ""))),
        })
    posts.sort(key=lambda p: p["d"], reverse=True)
    docs = catalog()
    if OUT.exists():
        old = json.loads(OUT.read_text(encoding="utf-8"))
        if old.get("posts") == posts and old.get("docs") == docs:
            print("No change.")
            return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    OUT.write_text(json.dumps({"updated": stamp, "posts": posts, "docs": docs}, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    print("%d posts, %d chunks, %d documents" % (len(posts), sum(len(p["c"]) for p in posts), len(docs)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
