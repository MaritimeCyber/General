#!/usr/bin/env python3
"""
ShipPaulJobs — Blogger Alt Attribute Fix
-----------------------------------------
google-api-python-client 없이 requests + google-auth 만으로 구현.
"""

import re
import os
import json

# ── 설정 ────────────────────────────────────────────────────────────────────────
BLOG_URL         = "https://www.shippauljobs.com"
CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE       = "token.json"
DRY_RUN          = False

# ── 업데이트 대상 포스트 ──────────────────────────────────────────────────────────
UPDATE_TARGETS = [
    (
        "https://www.shippauljobs.com/2026/07/ship-ot-network-design-iacs-ur-e26-e27.html",
        [("blogger.googleusercontent.com", "Maritime OT Cyber Resilience: From Cable to Cyber")],
        True,
        "From Cable to Cyber Resilience  Designing Physical Networks for IACS UR E26/E27",
    ),
    (
        "https://www.shippauljobs.com/2026/07/zone-conduit-vlan-purdue-model-ship-iacs-ur-e26.html",
        [("blogger.googleusercontent.com", "Maritime OT Security: Zone Before VLAN")],
        True, None,
    ),
    (
        "https://www.shippauljobs.com/2026/07/ship-zcd-documentation-zone-conduit-diagram-iacs-ur-e26.html",
        [("blogger.googleusercontent.com", "Ship OT Network Security: From Networks to ZCD")],
        True, None,
    ),
    (
        "https://www.shippauljobs.com/2026/07/ship-zcd-failures-iacs-ur-e26-e27-seven-mistakes.html",
        [("blogger.googleusercontent.com", "Why Most Ship ZCDs Fail: Maritime OT Analysis")],
        True, None,
    ),
    (
        "https://www.shippauljobs.com/2026/07/ship-zcd-anatomy-building-blocks-iacs-ur-e26.html",
        [("blogger.googleusercontent.com", "Anatomy of a Ship ZCD: Maritime OT Cybersecurity")],
        True, None,
    ),
    (
        "https://www.shippauljobs.com/2026/03/ship-ot-monitoring-for-iacs-e26e27.html",
        [("blogger.googleusercontent.com", "Ship OT Monitoring for IACS E26/E27: Required Functions and Protocols")],
        True, None,
    ),
    (
        "https://www.shippauljobs.com/2026/03/automating-iacs-e26e27-annual-survey.html",
        [("blogger.googleusercontent.com", "Automating IACS E26/E27 Annual Survey: OT Monitoring Scope")],
        True, None,
    ),
    (
        "https://www.shippauljobs.com/2026/06/iacs-ur-e26e27-compliance-matrix.html",
        [("blogger.googleusercontent.com", "IACS E26/E27 Compliance Matrix: Maritime OT Cybersecurity Solutions")],
        True, None,
    ),
    (
        "https://www.shippauljobs.com/2026/07/imo-mass-code-enters-into-force-1-july.html",
        [("blogger.googleusercontent.com", "Autonomous Ships and International Cyber Rules: IMO MASS Code")],
        True, None,
    ),
    (
        "https://www.shippauljobs.com/2026/06/ship-ot-cybersecurity-iacs-e26e27.html",
        [("blogger.googleusercontent.com", "IACS E26/E27 Cybersecurity Solutions for Maritime OT")],
        True, None,
    ),
    (
        "https://www.shippauljobs.com/2026/06/ai-is-already-faster-than-your-patch.html",
        [("blogger.googleusercontent.com", "AI vs Maritime OT Patch Cycle: 48-Hour Threat Response")],
        True, None,
    ),
    (
        "https://www.shippauljobs.com/2026/07/iacs-ur-e26-compliance-series-17-cyber.html",
        [("", "Cyber Resilience System Integrator – Ship Cybersecurity Diagram")],
        True, None,
    ),
]


# ── 유틸 함수 ─────────────────────────────────────────────────────────────────
def add_alt_to_img(html: str, src_sub: str, alt_text: str) -> tuple:
    count = 0

    def replacer(m):
        nonlocal count
        tag = m.group(0)
        if "alt=" in tag.lower():
            return tag
        if src_sub and src_sub not in tag:
            return tag
        count += 1
        return re.sub(r"(<img\b)", f'\\1 alt="{alt_text}"', tag, count=1, flags=re.IGNORECASE)

    new_html = re.sub(r"<img[^>]*>", replacer, html, flags=re.IGNORECASE)

    # src_sub가 빈 문자열이면 <img> 태그도 처리
    if not src_sub:
        def replacer_empty(m):
            nonlocal count
            tag = m.group(0)
            if "alt=" in tag.lower():
                return tag
            count += 1
            return re.sub(r"(<img\b)", f'\\1 alt="{alt_text}"', tag, count=1, flags=re.IGNORECASE)
        new_html = re.sub(r"<img\s*>", replacer_empty, new_html, flags=re.IGNORECASE)

    return new_html, count


def get_session():
    """google-auth + requests 만으로 인증된 세션 반환"""
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


def get_post_by_url(session, blog_id: str, url: str):
    path = url.replace(BLOG_URL, "")
    r = session.get(
        f"{BASE}/blogs/{blog_id}/posts/bypath",
        params={"path": path, "fields": "id,title,content"}
    )
    if r.status_code == 200:
        return r.json()
    print(f"  ⚠️  getByPath 실패: {r.status_code} {r.text[:120]}")
    return None


def patch_post(session, blog_id: str, post_id: str, body: dict):
    r = session.patch(
        f"{BASE}/blogs/{blog_id}/posts/{post_id}",
        json=body
    )
    r.raise_for_status()
    return r.json()


def patch_page(session, blog_id: str, page_id: str, body: dict):
    r = session.patch(
        f"{BASE}/blogs/{blog_id}/pages/{page_id}",
        json=body
    )
    r.raise_for_status()
    return r.json()


def get_page_by_url(session, blog_id: str, url: str):
    r = session.get(
        f"{BASE}/blogs/{blog_id}/pages",
        params={"fields": "items(id,title,url,content)"}
    )
    if r.status_code != 200:
        print(f"  ⚠️  pages.list 실패: {r.status_code}")
        return None
    for page in r.json().get("items", []):
        if page.get("url", "").rstrip("/") == url.rstrip("/"):
            return page
    print(f"  ⚠️  Page not found for URL: {url}")
    return None


# ── 메인 ─────────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("ShipPaulJobs — Blogger Alt Attribute Fix (requests 버전)")
    print(f"{'[DRY RUN]' if DRY_RUN else '[LIVE] 실제 업데이트'}")
    print("=" * 60)

    session = get_session()
    blog_id = get_blog_id(session)

    total_fixed = 0
    total_skipped = 0

    for entry in UPDATE_TARGETS:
        post_url, img_fixes, is_post, *rest = entry
        new_title = rest[0] if rest else None

        print(f"\n🔗 {post_url}")

        item = (get_post_by_url(session, blog_id, post_url)
                if is_post else
                get_page_by_url(session, blog_id, post_url))

        if not item:
            print("  ❌ 조회 실패, 건너뜀")
            total_skipped += 1
            continue

        item_id   = item["id"]
        cur_title = item.get("title", "?")
        content   = item.get("content", "")

        print(f"  📄 [{item_id}] {cur_title!r}")

        new_content = content
        changed = 0
        for src_sub, alt_text in img_fixes:
            new_content, n = add_alt_to_img(new_content, src_sub, alt_text)
            if n:
                print(f"  ✏️  +alt: '{alt_text}' ({n}개)")
            changed += n

        title_changed = False
        patch_title = cur_title
        if new_title and cur_title.strip() != new_title.strip():
            patch_title = new_title
            title_changed = True
            print(f"  ✏️  제목 수정: {cur_title!r} → {new_title!r}")

        if changed == 0 and not title_changed:
            print("  ✅ 이미 최신 상태, 건너뜀")
            total_skipped += 1
            continue

        if DRY_RUN:
            print(f"  [DRY RUN] alt {changed}개 + 제목 {'수정' if title_changed else '유지'}")
            total_fixed += 1
            continue

        patch_body = {"content": new_content}
        if title_changed:
            patch_body["title"] = patch_title

        try:
            if is_post:
                patch_post(session, blog_id, item_id, patch_body)
            else:
                patch_page(session, blog_id, item_id, patch_body)
            print(f"  ✅ 업데이트 완료 (alt {changed}개{'+ 제목' if title_changed else ''})")
            total_fixed += 1
        except Exception as e:
            print(f"  ❌ 업데이트 실패: {e}")
            total_skipped += 1

    print("\n" + "=" * 60)
    print(f"완료: {total_fixed}개 업데이트, {total_skipped}개 건너뜀")
    print("=" * 60)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
