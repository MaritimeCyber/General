#!/usr/bin/env python3
"""
ShipPaulJobs — Blogger Parent Label Classifier
-----------------------------------------------
PHASE 1 경량 모드: 제목 + 기존 라벨만으로 Parent Label 분류 후 PATCH

사용법:
  1. credentials.json 을 이 스크립트와 같은 폴더에 저장
  2. pip install google-api-python-client google-auth-oauthlib
  3. python blogger_label_classifier.py

첫 실행 시 브라우저가 열려 Google 계정 인증을 요청합니다.
"""

import json
import os

# ── 설정 ────────────────────────────────────────────────────────────────────────
BLOG_URL = "https://www.shippauljobs.com"          # 블로그 URL (Blog ID 자동 탐색)
CREDENTIALS_FILE = "credentials.json"               # GCP OAuth 클라이언트 JSON
TOKEN_FILE = "token.json"                           # 인증 토큰 캐시 (자동 생성)
DRY_RUN = False                                     # True = 실제 PATCH 없이 로그만 출력

# ── Parent Label 키워드 매핑 ─────────────────────────────────────────────────────
KEYWORD_MAP = [
    (
        ["IACS", "UR E26", "UR E27", "IMO", "Flag State",
         "Regulation", "Compliance", "Mandate"],
        "Regulatory Intelligence"
    ),
    (
        ["AI", "LLM", "Claude", "GPT", "Automation",
         "Machine Learning", "Pentest AI"],
        "AI Intelligence"
    ),
    (
        ["Hack", "Threat", "Vulnerability", "Incident",
         "Malware", "Attack", "Exploit", "CVE"],
        "Threat Intelligence"
    ),
    (
        ["OT", "ICS", "Zone", "Conduit", "Network",
         "Architecture", "Pentest", "Firewall", "VLAN",
         "Purdue", "Switch", "NDR", "SIEM", "IDS"],
        "Cyber Operations"
    ),
    (
        ["Smart Ship", "Vessel", "MASS", "Navigation",
         "Bridge", "Ballast", "Cargo", "Propulsion",
         "Communication System", "Ship System"],
        "Vessel Intelligence"
    ),
    (
        ["Brief", "Market", "Vendor", "Industry",
         "Trend", "Spotlight", "Consultant"],
        "Market Intelligence"
    ),
]

PARENT_LABELS = {label for _, label in KEYWORD_MAP}
MAX_PARENT_LABELS = 2   # 애매한 경우 최대 2개까지 허용


# ── 분류 함수 ────────────────────────────────────────────────────────────────────
def classify(title: str, existing_labels: list[str]) -> list[str]:
    """제목과 기존 라벨을 합쳐 키워드 매칭으로 Parent Label 반환 (최대 2개)."""
    combined = (title + " " + " ".join(existing_labels)).lower()
    matched = []
    for keywords, parent_label in KEYWORD_MAP:
        for kw in keywords:
            if kw.lower() in combined:
                if parent_label not in matched:
                    matched.append(parent_label)
                break
    return matched[:MAX_PARENT_LABELS]


# ── Blogger API 유틸 ─────────────────────────────────────────────────────────────
def get_service():
    from googleapiclient.discovery import build
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request

    SCOPES = ["https://www.googleapis.com/auth/blogger"]
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    return build("blogger", "v3", credentials=creds)


def get_blog_id(service) -> str:
    """블로그 URL로 Blog ID 자동 탐색."""
    resp = service.blogs().getByUrl(url=BLOG_URL).execute()
    blog_id = resp["id"]
    print(f"✅ Blog ID: {blog_id}  ({resp['name']})")
    return blog_id


def fetch_all_posts(service, blog_id: str) -> list[dict]:
    """전체 포스트 제목 + 라벨만 페치 (본문 제외)."""
    posts = []
    page_token = None
    while True:
        resp = (
            service.posts()
            .list(
                blogId=blog_id,
                fields="nextPageToken,items(id,title,labels)",
                maxResults=500,
                status=["live", "draft"],
                pageToken=page_token,
            )
            .execute()
        )
        batch = resp.get("items", [])
        posts.extend(batch)
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return posts


# ── 메인 ─────────────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("ShipPaulJobs — Blogger Parent Label Classifier")
    print(f"{'[DRY RUN] 실제 PATCH 없음' if DRY_RUN else '[LIVE] 실제 라벨 수정'}")
    print("=" * 60)

    service = get_service()
    blog_id = get_blog_id(service)
    posts = fetch_all_posts(service, blog_id)
    print(f"\n📋 총 포스트 수: {len(posts)}\n")

    updated = 0
    skipped = 0
    no_match = 0

    for post in posts:
        post_id = post["id"]
        title = post.get("title", "")
        existing = post.get("labels", [])

        # 기존 Parent Label 제거 후 새로 계산
        non_parent = [l for l in existing if l not in PARENT_LABELS]
        new_parents = classify(title, existing)

        if not new_parents:
            print(f"  [NO MATCH] {title}")
            no_match += 1
            continue

        updated_labels = non_parent + new_parents

        if set(updated_labels) == set(existing):
            print(f"  [NO CHANGE] {title}  →  {existing}")
            skipped += 1
            continue

        # 변경 사항 출력
        print(f"  [UPDATE] {title}")
        print(f"           Before: {existing}")
        print(f"           After:  {updated_labels}")

        if not DRY_RUN:
            service.posts().patch(
                blogId=blog_id,
                postId=post_id,
                body={"labels": updated_labels},
            ).execute()

        updated += 1

    print("\n" + "=" * 60)
    print(f"✅ 완료  |  업데이트: {updated}  스킵: {skipped}  매핑없음: {no_match}")
    print("=" * 60)


if __name__ == "__main__":
    main()
