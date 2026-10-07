#!/usr/bin/env python3
"""
ShipPaulJobs — Blogger Title Updater
---------------------------------------------------
AdSense 2차 감사(AdSense_Audit_Report_20261007.md) 부록 B-1/B-2의
"번호만 있는 제목" 수정안을 Blogger에 일괄 적용합니다.

  - 제목(title)만 변경합니다. URL(슬러그)·본문·라벨·게시일은 그대로 유지됩니다.
  - 현재 제목이 예상한 기존 제목과 다르면 건너뜁니다 (이미 수동 수정했거나 대상이 바뀐 경우).
  - 기본은 DRY RUN (변경 없음). 실제 적용은 --apply 옵션.

사용법:
  1. Blog/Tools 의 credentials.json / token.json 을 그대로 사용합니다 (다른 Tools 스크립트와 동일).
  2. pip install google-api-python-client google-auth-oauthlib
  3. python blogger_title_updater.py           # 미리보기
  4. python blogger_title_updater.py --apply   # 실제 적용
"""

import json
import os
import sys
from datetime import datetime

BLOG_ID          = "8002758868633250458"
CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE       = "token.json"

# (URL 경로, 기존 제목, 새 제목)
TITLE_UPDATES = [
    # ── B-1. E26/E27 엔지니어링 시리즈 Chapter 1~9 ─────────────────────────────
    ("/2026/06/chapter-1-digitalization-of-modern-ships.html",
     "Chapter 1. Digitalization of Modern Ships",
     "How Ship Digitalization Created the Cyber Risk Behind IACS UR E26 (Ch.1)"),
    ("/2026/06/chapter-2-increasing-ot-system.html",
     "Chapter 2. Increasing OT System Interdependency",
     "Why Shipboard OT Interdependency Turns One Failure into Many (Ch.2)"),
    ("/2026/06/chapter-3-why-cybersecurity-became.html",
     "Chapter 3. Why Cybersecurity Became a System Engineering Issue",
     "Ship Cybersecurity Is a System Engineering Problem, Not an IT Add-On (Ch.3)"),
    ("/2026/06/chapter-4-understanding-why-iacs.html",
     "Chapter 4: Understanding Why IACS Introduced E26 and E27",
     "Why IACS Introduced UR E26 and E27: The Engineering Gap They Close (Ch.4)"),
    ("/2026/07/why-maritime-cybersecurity-became.html",
     "Chapter 5. From Functional Design to Explainable Design",
     "From Functional to Explainable Design: What UR E26 Reviewers Expect (Ch.5)"),
    ("/2026/07/chapter-6-required-engineering-evidence.html",
     "Chapter 6. Required Engineering Evidence",
     "What Engineering Evidence UR E26/E27 Approval Actually Requires (Ch.6)"),
    ("/2026/07/Chapter7.RoleofShipyardandSupplier.html",
     "Chapter 7. Role of Shipyard and Supplier",
     "Shipyard vs. Supplier Responsibilities Under IACS UR E26/E27 (Ch.7)"),
    ("/2026/07/chapter-8-how-engineering-information.html",
     "Chapter 8. How Engineering Information Flows Through a Project",
     "How Cyber Engineering Information Flows from Supplier to Class in a Newbuild (Ch.8)"),
    ("/2026/08/chapter-9-from-compliance-documentation.html",
     "Chapter 9 From Compliance Documentation to Sustainable Cybersecurity Engineering",
     "Beyond E26 Paperwork: Building Sustainable Ship Cybersecurity Engineering (Ch.9)"),
    ("/2026/07/iacs-ur-e26-compliance-series-17-cyber.html",
     "Article 1 : The Cyber Resilience System Integrator and the Six Core Ship-Level Deliverables",
     "The Cyber Resilience System Integrator: Six Ship-Level Deliverables Under UR E26"),

    # ── B-2. Jump Server 시리즈 ───────────────────────────────────────────────
    ("/2026/05/part-1-why-modern-ships-need-jump.html",
     "Part 1. Why Modern Ships Need Jump Servers (Maritime Jump Server Series)",
     "Why Modern Ships Need Jump Servers — Maritime Jump Server Series (1/3)"),
    ("/2026/06/part-2-designing-secure-remote-access.html",
     "Part 2. Designing Secure Remote Access for Ships",
     "Designing Secure Remote Access for Ships — Maritime Jump Server Series (2/3)"),
    ("/2026/07/part-3-how-to-evaluate-maritime-jump.html",
     "Part 3. How to Evaluate a Maritime Jump Server Solution",
     "How to Evaluate a Maritime Jump Server Solution — Jump Server Series (3/3)"),

    # ── B-2. ICS Security 시리즈 ──────────────────────────────────────────────
    ("/2026/03/ics-security-chapter-1-nature-of.html",
     "ICS Security Chapter 1 The Nature of Industrial Control Systems (ICS/OT) and the Security Paradigm",
     "The Nature of ICS/OT and Its Security Paradigm — ICS Security Ch.1"),
    ("/2026/03/ics-security-chapter-2-cs-network.html",
     "ICS Security Chapter 2 CS Network Architecture Fundamentals",
     "ICS Network Architecture Fundamentals — ICS Security Ch.2"),
    ("/2026/03/ics-security-chapter-4-threat-modeling.html",
     "ICS Security Chapter 4 Threat Modeling Fundamentals — Attack Chain Structure & EWS Pivot Analysis",
     "ICS Threat Modeling: Attack Chains & EWS Pivot Analysis — ICS Security Ch.4"),
    ("/2026/03/ics-security-chapter-5-host-security.html",
     "ICS Security Chapter 5 Host Security — Visibility Required After Preventive Controls",
     "ICS Host Security After Preventive Controls — ICS Security Ch.5"),
    ("/2026/04/ics-securit-chapter-6-documentation.html",
     "ICS Securit Chapter 6 Documentation Fundamentals — Structuring Security into Verifiable Form",
     "ICS Security Documentation Fundamentals — ICS Security Ch.6"),
    ("/2026/05/ics-security-chapter-7-security-testing.html",
     "ICS Security Chapter 7 Security Testing Fundamentals — Verifying That Security Actually Works",
     "ICS Security Testing Fundamentals — ICS Security Ch.7"),
    ("/2026/05/ics-security-chapter-8-ot-security.html",
     "ICS Security Chapter 8 · OT Security Architecture & Deployment Fundamentals",
     "OT Security Architecture & Deployment — ICS Security Ch.8"),
]


def norm(s: str) -> str:
    """공백 차이(두 칸 공백, 앞뒤 공백)는 같은 제목으로 취급."""
    return " ".join(s.split())


def load_token_info(path: str) -> dict:
    """token.json 을 읽되, expiry 가 숫자(epoch 초)로 저장된 경우 google-auth 형식 문자열로 변환."""
    from datetime import timezone
    with open(path, encoding="utf-8") as f:
        info = json.load(f)
    expiry = info.get("expiry")
    if isinstance(expiry, (int, float)):
        if expiry > 1e12:  # 밀리초 단위
            expiry /= 1000
        info["expiry"] = datetime.fromtimestamp(expiry, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return info


def get_service():
    from googleapiclient.discovery import build
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request

    SCOPES = ["https://www.googleapis.com/auth/blogger"]
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_info(load_token_info(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    return build("blogger", "v3", credentials=creds)


def main():
    apply = "--apply" in sys.argv

    print("=" * 60)
    print("ShipPaulJobs — Blogger Title Updater")
    print(f"  대상: {len(TITLE_UPDATES)}개")
    print(f"  {'[LIVE — Blogger 제목 변경]' if apply else '[DRY RUN — 실제 변경 없음, --apply 로 적용]'}")
    print("=" * 60)

    from googleapiclient.errors import HttpError
    service = get_service()

    updated = already = mismatch = missing = 0

    for path, old_title, new_title in TITLE_UPDATES:
        try:
            post = service.posts().getByPath(blogId=BLOG_ID, path=path).execute()
        except HttpError as e:
            print(f"\n  [NOT FOUND] {path}  ({e.resp.status} — Draft 전환/삭제 여부 확인)")
            missing += 1
            continue

        current = post.get("title", "")

        if norm(current) == norm(new_title):
            print(f"\n  [SKIP — 이미 변경됨] {path}")
            already += 1
            continue

        if norm(current) != norm(old_title):
            print(f"\n  [SKIP — 현재 제목이 예상과 다름] {path}")
            print(f"           현재: {current}")
            print(f"           예상: {old_title}")
            mismatch += 1
            continue

        print(f"\n  [UPDATE] {path}")
        print(f"           - {current}")
        print(f"           + {new_title}")

        if apply:
            service.posts().patch(
                blogId=BLOG_ID,
                postId=post["id"],
                body={"title": new_title},
            ).execute()

        updated += 1

    print("\n" + "=" * 60)
    verb = "변경" if apply else "변경 예정"
    print(f"✅ 완료  |  {verb}: {updated}  이미 변경: {already}  "
          f"제목 불일치: {mismatch}  찾을 수 없음: {missing}")
    print("=" * 60)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
