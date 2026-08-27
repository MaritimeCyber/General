#!/usr/bin/env python3
"""
ShipPaulJobs — Blogger Parent Label Classifier v2
---------------------------------------------------
변경사항:
  - MAX_PARENT_LABELS = 1  (포스트 당 1개 Parent Label만 추가)
  - 포스트 READ: Atom 피드 사용 (인증 불필요)
  - 라벨 WRITE: Blogger API v3 PATCH (OAuth2 필요)

사용법:
  1. GCP Console → Blogger API 활성화 → OAuth2 클라이언트 ID 생성
  2. credentials.json 을 이 스크립트와 같은 폴더에 저장
  3. pip install google-api-python-client google-auth-oauthlib
  4. python blogger_label_classifier.py

첫 실행 시 브라우저가 열려 Google 계정 인증을 요청합니다.
DRY_RUN = True 로 먼저 결과를 확인하세요.
"""

import os
import json
import urllib.request
import re

# ── 설정 ────────────────────────────────────────────────────────────────────────
BLOG_ID       = "8002758868633250458"
BLOG_URL      = "https://www.shippauljobs.com"
CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE    = "token.json"
DRY_RUN       = False   # True = 로그만 출력, 실제 PATCH 없음

# ── Parent Label 키워드 매핑 ─────────────────────────────────────────────────────
KEYWORD_MAP = [
    (
        ["IACS", "UR E26", "UR E27", "IMO", "Flag State",
         "Regulation", "Compliance", "Mandate", "USCG", "CIRCIA",
         "NIS2", "CRA", "SOLAS", "Flag"],
        "Rules and Compliance"
    ),
    (
        ["AICyberLab", "A.I", "LLM", "Claude", "GPT",
         "Machine Learning", " AI ", "AI-"],
        "AI and Automation"
    ),
    (
        ["Hack", "Hacked", "Threat", "Vulnerability", "Incident",
         "Malware", "Attack", "Exploit", "CVE", "Ransomware",
         "Spoofing", "Jamming", "ThreatIntelligence"],
        "Threats and Attacks"
    ),
    (
        ["OT Security", "ICS Security", "OT/IT", "IT/OT",
         "Zone", "Conduit", "Pentest", "Firewall", "VLAN",
         "Purdue", "NDR", "SIEM", "SOLUTION", "PAM", "MFA",
         "Jump Server", "ZCD", " OT ", " ICS "],
        "OT Security"
    ),
    (
        ["Ship", "Vessel", "MASS", "Navigation",
         "Bridge", "Ballast", "Cargo", "Propulsion",
         "Communication System", "CBS", "Smart Ship",
         "Alarm", "Power Management", "Fire Detection"],
        "Ship and Vessel"
    ),
    (
        ["Brief", "Market", "Vendor", "Industry",
         "Trend", "Spotlight", "Consultant", "Survey",
         "Port", "Smart Port"],
        "Industry and Market"
    ),
]

PARENT_LABELS  = {label for _, label in KEYWORD_MAP}
MAX_PARENT_LABELS = 1   # ← 포스트 당 1개만


# ── 분류 함수 ────────────────────────────────────────────────────────────────────
def classify(title: str, existing_labels: list) -> list:
    # 제목 앞뒤에 공백을 추가해 단어 경계 매칭 보조
    combined = (" " + title + " " + " ".join(existing_labels) + " ").lower()
    matched = []
    for keywords, parent_label in KEYWORD_MAP:
        for kw in keywords:
            if kw.lower() in combined:
                if parent_label not in matched:
                    matched.append(parent_label)
                break
    return matched[:MAX_PARENT_LABELS]


# ── Atom 피드로 포스트 읽기 (인증 불필요) ────────────────────────────────────────
def fetch_all_posts_atom() -> list:
    """Atom JSON 피드로 전체 포스트 읽기 — GCP 인증 불필요."""
    posts = []
    start_index = 1
    batch = 150   # Blogger Atom 최대

    while True:
        url = (f"{BLOG_URL}/feeds/posts/default"
               f"?alt=json&max-results={batch}&start-index={start_index}")
        try:
            with urllib.request.urlopen(url, timeout=15) as resp:
                data = json.loads(resp.read())
        except Exception as e:
            print(f"  [피드 오류] {e}")
            break

        entries = data.get("feed", {}).get("entry", [])
        if not entries:
            break

        for e in entries:
            id_full = e["id"]["$t"]
            id_match = re.search(r"post-(\d+)", id_full)
            post_id = id_match.group(1) if id_match else id_full
            title = e["title"]["$t"]
            labels = [c["term"] for c in e.get("category", [])]
            posts.append({"id": post_id, "title": title, "labels": labels})

        total_str = data["feed"].get("openSearch$totalResults", {}).get("$t", "0")
        total = int(total_str)
        start_index += len(entries)
        if start_index > total:
            break

    return posts


# ── Blogger API WRITE 서비스 ─────────────────────────────────────────────────────
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
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    return build("blogger", "v3", credentials=creds)


# ── 메인 ─────────────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("ShipPaulJobs — Blogger Parent Label Classifier v2")
    print(f"  MAX_PARENT_LABELS = {MAX_PARENT_LABELS}")
    print(f"  {'[DRY RUN — 실제 변경 없음]' if DRY_RUN else '[LIVE — Blogger 업데이트]'}")
    print("=" * 60)

    # 1) 포스트 읽기 (Atom 피드, 인증 불필요)
    print("\n📡 Atom 피드에서 포스트 로딩...")
    posts = fetch_all_posts_atom()
    print(f"📋 총 포스트 수: {len(posts)}\n")

    # 2) OAuth2 서비스 초기화 (WRITE 전용)
    if not DRY_RUN:
        service = get_service()

    updated = skipped = no_match = 0

    for post in posts:
        post_id  = post["id"]
        title    = post.get("title", "")
        existing = post.get("labels", [])

        # 이미 Parent Label 있으면 스킵
        has_parent = [l for l in existing if l in PARENT_LABELS]
        if has_parent:
            print(f"  [SKIP — 이미 있음: {has_parent[0]}] {title[:60]}")
            skipped += 1
            continue

        # 분류
        non_parent  = [l for l in existing if l not in PARENT_LABELS]
        new_parents = classify(title, existing)

        if not new_parents:
            print(f"  [NO MATCH] {title[:60]}")
            no_match += 1
            continue

        updated_labels = non_parent + new_parents

        print(f"  [UPDATE] {title[:60]}")
        print(f"           + {new_parents[0]}")

        if not DRY_RUN:
            service.posts().patch(
                blogId=BLOG_ID,
                postId=post_id,
                body={"labels": updated_labels},
            ).execute()

        updated += 1

    print("\n" + "=" * 60)
    print(f"✅ 완료  |  업데이트: {updated}  스킵: {skipped}  매핑없음: {no_match}")
    print("=" * 60)


if __name__ == "__main__":
    main()
