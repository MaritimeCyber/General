#!/usr/bin/env python3
"""
ShipPaulJobs — Move Series Navigation to After Author Bio
----------------------------------------------------------
Some posts have the ⚓ Series Navigation block at the very top of the content.
This script moves it to immediately after the author bio section.

Target: posts where "Series Navigation" appears in the content
(primarily the After Mandate ①–⑥ series, but scans all 32 posts).
"""

import os

BLOG_URL         = "https://www.shippauljobs.com"
CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE       = "token.json"
DRY_RUN          = False

# Only posts where ⚓ Series Navigation is at the very top of the content
TARGET_POSTS = [
    "/2026/06/ur-e26-after-mandate-one-mandatory-rule.html",
    "/2026/07/ur-e26-after-mandate-owners-view-where.html",
    "/2026/07/ur-e26-after-mandate-through-eyes-of.html",
    "/2026/07/ur-e26-after-mandate-shipyards-view.html",
    "/2026/07/ur-e26-after-mandate-vendors-view.html",
    "/2026/07/ur-e26-after-mandate-consultants-view.html",
]


# ── HTML rearrangement ───────────────────────────────────────────────────────

def rearrange(html: str) -> tuple:
    """
    Moves the Series Navigation block to after the author bio block.
    Returns (new_html, changed: bool, message: str).
    """
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        return html, False, "BeautifulSoup not installed — run: pip install beautifulsoup4 --break-system-packages"

    soup = BeautifulSoup(html, "html.parser")

    # ── 1. Find Series Navigation block ──────────────────────────────────────
    # Look for any tag whose text contains "Series Navigation"
    nav_elem = None
    for tag in soup.find_all(True):
        if "Series Navigation" in (tag.get_text() or ""):
            # Check it's a reasonably small block (not the whole document)
            text_len = len(tag.get_text())
            if text_len < 2000:
                nav_elem = tag
                break

    if nav_elem is None:
        return html, False, "No 'Series Navigation' block found — skipping"

    # Walk up to the top-level ancestor (direct child of soup root)
    nav_top = nav_elem
    while nav_top.parent and nav_top.parent != soup:
        nav_top = nav_top.parent

    # ── 2. Find Author bio block ──────────────────────────────────────────────
    # Look for a tag containing a personal LinkedIn URL (linkedin.com/in/)
    author_elem = None
    for a_tag in soup.find_all("a", href=True):
        href = a_tag.get("href", "")
        if "linkedin.com/in/" in href:
            author_elem = a_tag
            break

    if author_elem is None:
        return html, False, "No author LinkedIn link found — skipping"

    # Walk up to the top-level ancestor
    author_top = author_elem
    while author_top.parent and author_top.parent != soup:
        author_top = author_top.parent

    # ── 3. Check current order ────────────────────────────────────────────────
    children = list(soup.children)
    try:
        nav_idx    = children.index(nav_top)
        author_idx = children.index(author_top)
    except ValueError:
        return html, False, "Could not locate blocks among top-level children"

    if nav_idx > author_idx:
        return html, False, "Series Navigation is already after author bio — skipping"

    # ── 4. Move: extract nav, insert after author ─────────────────────────────
    nav_top.extract()          # remove from current position
    author_top.insert_after(nav_top)  # place right after author bio

    return str(soup), True, f"Moved Series Navigation (was idx {nav_idx}) to after author bio (idx {author_idx})"


# ── Auth ─────────────────────────────────────────────────────────────────────

def get_session():
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request, AuthorizedSession

    SCOPES = ["https://www.googleapis.com/auth/blogger"]
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
    return AuthorizedSession(creds)


BASE = "https://blogger.googleapis.com/v3"


def get_blog_id(session) -> str:
    r = session.get(f"{BASE}/blogs/byurl", params={"url": BLOG_URL})
    r.raise_for_status()
    data = r.json()
    print(f"✅ Blog ID: {data['id']}  ({data['name']})")
    return data["id"]


def get_post_by_path(session, blog_id: str, path: str):
    r = session.get(
        f"{BASE}/blogs/{blog_id}/posts/bypath",
        params={"path": path, "fields": "id,title,content"}
    )
    if r.status_code == 200:
        return r.json()
    print(f"  ⚠️  getByPath failed: {r.status_code} {r.text[:100]}")
    return None


def patch_post(session, blog_id: str, post_id: str, body: dict):
    r = session.patch(f"{BASE}/blogs/{blog_id}/posts/{post_id}", json=body)
    r.raise_for_status()
    return r.json()


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("ShipPaulJobs — Move Series Navigation → After Author Bio")
    print(f"{'[DRY RUN]' if DRY_RUN else '[LIVE] actual update'}")
    print("=" * 60)

    session = get_session()
    blog_id = get_blog_id(session)

    moved = skipped = failed = 0

    for path in TARGET_POSTS:
        url = BLOG_URL + path
        print(f"\n🔗 {url}")

        post = get_post_by_path(session, blog_id, path)
        if not post:
            print("  ❌ fetch failed, skipping")
            failed += 1
            continue

        post_id = post["id"]
        title   = post.get("title", "?")
        content = post.get("content", "")

        print(f"  📄 [{post_id}] {title!r}")

        # Quick check — skip posts without Series Navigation
        if "Series Navigation" not in content:
            print("  ⏭  No Series Navigation in content — skipping")
            skipped += 1
            continue

        new_content, changed, msg = rearrange(content)
        print(f"  ℹ️  {msg}")

        if not changed:
            skipped += 1
            continue

        if DRY_RUN:
            print("  [DRY RUN] would patch post")
            moved += 1
            continue

        try:
            patch_post(session, blog_id, post_id, {"content": new_content})
            print("  ✅ Series Navigation moved successfully")
            moved += 1
        except Exception as e:
            print(f"  ❌ patch failed: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Done: {moved} moved, {skipped} skipped, {failed} failed")
    print("=" * 60)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
