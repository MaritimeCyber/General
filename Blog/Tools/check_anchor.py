#!/usr/bin/env python3
"""포스트 하나의 content 끝부분 확인 — 앵커 패턴 탐색용"""
import json

TOKEN_FILE = "token.json"
BLOG_ID    = "8002758868633250458"
BASE       = "https://blogger.googleapis.com/v3"

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

with open("target_posts.json") as f:
    targets = json.load(f)

session = get_session()

# 첫 번째 포스트만 확인
url, post_id = next(iter(targets.items()))
r = session.get(f"{BASE}/blogs/{BLOG_ID}/posts/{post_id}", params={"fields":"content"})
content = r.json().get("content","")
print(f"URL: {url}")
print(f"Content length: {len(content)}")
print("\n=== LAST 2000 chars ===")
print(content[-2000:])
