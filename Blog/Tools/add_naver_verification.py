#!/usr/bin/env python3
import os, json

BLOG_ID = "8002758868633250458"
TOKEN_FILE = os.path.expanduser("~/VSCode_Project/MaritimeCyber/General/Blog/Tools/token.json")
NEW_TAG = '<meta name="naver-site-verification" content="30546e575410e001d4a18c2ea086e100aee42e67" />'
INSERT_AFTER = "content='472da63a757063775c60582bd3235f2887abb75c' name='naver-site-verification'/>"

def get_session():
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request, AuthorizedSession
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, ["https://www.googleapis.com/auth/blogger"])
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
    return AuthorizedSession(creds)

def main():
    session = get_session()
    BASE = "https://blogger.googleapis.com/v3"

    # Get current template
    r = session.get(f"{BASE}/blogs/{BLOG_ID}/templates/default")
    r.raise_for_status()
    template = r.json()
    html = template.get("markup", "")
    print(f"템플릿 길이: {len(html)}")

    if '30546e575410e001d4a18c2ea086e100aee42e67' in html:
        print("✅ 이미 태그 있음, 종료")
        return

    if INSERT_AFTER not in html:
        print(f"⚠️ 기준 태그 없음: {INSERT_AFTER[:50]}")
        return

    new_html = html.replace(INSERT_AFTER, INSERT_AFTER + "\n    " + NEW_TAG)
    print(f"태그 추가 완료, 저장 중...")

    r2 = session.patch(f"{BASE}/blogs/{BLOG_ID}/templates/default", json={"markup": new_html})
    r2.raise_for_status()
    print("✅ 테마 업데이트 완료!")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
