#!/usr/bin/env python3
"""
upload_pillar_banners.py
------------------------
1. target_posts.json의 61개 포스트에 Pillar 01 배너 추가
2. efficient-way-to-classify-system-types 포스트에 내부 링크 5개 추가

Run:
  cd ~/VSCode_Project/MaritimeCyber/General/Blog/Tools
  ~/anaconda3/bin/python3 upload_pillar_banners.py
"""

import json, time, sys

BLOG_ID        = "8002758868633250458"
TOKEN_FILE     = "token.json"
CREDENTIALS_FILE = "credentials.json"
BASE           = "https://blogger.googleapis.com/v3"
DRY_RUN        = False   # True → API 호출 없이 미리보기만

# ── Pillar 01 배너 ────────────────────────────────────────────────────────────
P01_URL   = "https://www.shippauljobs.com/2026/08/iacs-ur-e26-complete-guide-to-cyber.html"
P01_CHECK = "iacs-ur-e26-complete-guide-to-cyber"

BANNER = (
    '<div style="background:linear-gradient(135deg,#0a2342,#154f7a);border-radius:12px;'
    'padding:20px 24px;margin:20px 0 16px;font-family:Inter,sans-serif;">'
    '<div style="font-size:10px;font-weight:800;color:#7effd8;letter-spacing:1.5px;'
    'text-transform:uppercase;margin-bottom:10px;">📖 IACS UR E26 Complete Guide</div>'
    f'<a href="{P01_URL}" style="text-decoration:none;">'
    '<div style="color:white;font-size:14px;font-weight:700;line-height:1.5;margin-bottom:6px;">'
    'IACS UR E26 — Cyber Resilience of Ships: The Complete Guide</div>'
    '<div style="color:rgba(255,255,255,0.72);font-size:12px;line-height:1.65;">'
    'ZCD · CBS Classification · SCARP · Audit Procedures · E27 Interface — 모든 것을 한 페이지에서.</div>'
    '<div style="display:inline-block;margin-top:10px;background:rgba(126,255,216,0.15);'
    'color:#7effd8;font-size:11px;font-weight:700;padding:4px 14px;border-radius:20px;'
    'border:1px solid rgba(126,255,216,0.3);">전체 가이드 읽기 →</div>'
    '</a></div>'
)

# 저자 카드 앵커 (우선순위 순)
ANCHORS = [
    "<!--══ AUTHOR CARD ══-->",
    "<!-- AUTHOR CARD -->",
    "<!-- AUTHOR CTA -->",
    '<div style="align-items: flex-start; border-top: 2px solid rgb(226, 234, 243);',
    '<div style="background:#fff;border:1px solid #d1e0ee;border-radius:14px;padding:22px 24px;display:flex;align-items:center;gap:18px;font-family:Inter,sans-serif;">',
]

# ── 내부 링크 (classify-system-types 포스트) ──────────────────────────────────
CLASSIFY_POST_ID    = "6140389425780492839"
INTERNAL_LINKS_CHECK = "iacs-ur-e26-complete-guide-to-cyber"
INTERNAL_LINKS_BOX  = (
    '<div style="background:#f0f4f8;border-left:4px solid #1a73e8;padding:16px 20px;'
    'margin:32px 0;border-radius:0 8px 8px 0;">'
    '<p style="margin:0 0 12px;font-weight:700;color:#1a73e8;">📌 Related Reading</p>'
    '<ul style="margin:0;padding-left:20px;line-height:1.8;">'
    '<li><a href="https://www.shippauljobs.com/2026/08/iacs-ur-e26-complete-guide-to-cyber.html" '
    'style="color:#1a73e8;">IACS UR E26: Complete Guide to Cyber Security Compliance</a></li>'
    '<li><a href="https://www.shippauljobs.com/2026/08/iacs-ur-e26-vs-e27-complete-comparison.html" '
    'style="color:#1a73e8;">IACS UR E26 vs E27: Complete Comparison</a></li>'
    '<li><a href="https://www.shippauljobs.com/2026/07/ship-zcd-documentation-zone-conduit-diagram-iacs-ur-e26.html" '
    'style="color:#1a73e8;">Ship ZCD Documentation: Zone &amp; Conduit Diagram for IACS UR E26</a></li>'
    '<li><a href="https://www.shippauljobs.com/2026/07/if-it-is-out-of-scope-your-e26.html" '
    'style="color:#1a73e8;">If It Is Out of Scope, Your E26 Compliance Is at Risk</a></li>'
    '<li><a href="https://www.shippauljobs.com/2026/07/e26-zone-defense-learn-iacs-ur-e26-as.html" '
    'style="color:#1a73e8;">E26 Zone Defense: Learn IACS UR E26 as a Zone-Based Framework</a></li>'
    '</ul></div>'
)

# ── API helpers ───────────────────────────────────────────────────────────────
def get_session():
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request, AuthorizedSession
    SCOPES = ["https://www.googleapis.com/auth/blogger"]
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds.valid and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
    return AuthorizedSession(creds)

def get_content(session, post_id):
    r = session.get(f"{BASE}/blogs/{BLOG_ID}/posts/{post_id}",
                    params={"fields": "content"})
    r.raise_for_status()
    return r.json().get("content", "")

def patch_content(session, post_id, content):
    r = session.patch(f"{BASE}/blogs/{BLOG_ID}/posts/{post_id}",
                      json={"content": content})
    r.raise_for_status()
    return r.status_code

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    session = get_session()

    # 1) Pillar 01 배너 — 61개 타겟 포스트
    with open("target_posts.json") as f:
        targets = json.load(f)  # URL → PostID

    ok = skip = warn = fail = 0

    for url, post_id in targets.items():
        slug = url.rstrip("/").split("/")[-1][:55]
        try:
            content = get_content(session, post_id)

            if P01_CHECK in content:
                print(f"[SKIP] {slug}")
                skip += 1
                continue

            # 앵커 탐색 (마지막 occurrence)
            anchor_idx = -1
            for anchor in ANCHORS:
                idx = content.rfind(anchor)
                if idx >= 0:
                    anchor_idx = idx
                    break

            if anchor_idx < 0:
                # 폴백: content 끝에 추가
                new_content = content + "\n" + BANNER
                print(f"[APND] 앵커 없어 끝에 추가: {slug}")
                warn += 1
            else:
                new_content = content[:anchor_idx] + BANNER + "\n" + content[anchor_idx:]

            if not DRY_RUN:
                patch_content(session, post_id, new_content)
                time.sleep(0.4)

            if anchor_idx >= 0:
                print(f"[OK]   {slug}")
            ok += 1

        except Exception as e:
            print(f"[ERR]  {slug}: {e}")
            fail += 1

    print(f"\n[Pillar 배너] OK={ok}  SKIP={skip}  WARN={warn}  FAIL={fail}")

    # 2) 내부 링크 — classify-system-types
    print("\n--- classify-system-types 내부 링크 ---")
    try:
        content = get_content(session, CLASSIFY_POST_ID)
        if INTERNAL_LINKS_CHECK in content:
            print("[SKIP] 내부 링크 이미 존재")
        else:
            new_content = content + "\n" + INTERNAL_LINKS_BOX
            if not DRY_RUN:
                patch_content(session, CLASSIFY_POST_ID, new_content)
            print("[OK]   내부 링크 5개 추가 완료")
    except Exception as e:
        print(f"[ERR]  classify post: {e}")

    print("\n모두 완료.")

if __name__ == "__main__":
    main()
