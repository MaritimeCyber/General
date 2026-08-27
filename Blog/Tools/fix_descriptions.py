#!/usr/bin/env python3
import os

BLOG_ID = "8002758868633250458"
TOKEN_FILE = os.path.expanduser("~/VSCode_Project/MaritimeCyber/General/Blog/Tools/token.json")
BASE = "https://blogger.googleapis.com/v3"

TARGETS = [
    (
        "/2025/03/real-time-security-monitoring-system.html",
        "Learn how to build a real-time cyber security monitoring system for ships using SIEM and IDS. Covers onboard sensor integration, alert logic, and IACS UR E26/E27 compliance requirements."
    ),
    (
        "/2021/02/1-step-3-ai.html",
        "Explores how maritime market keywords are evolving and how AI reshapes search intent, content strategy, and competitive positioning for ship operators and OT vendors."
    ),
]

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

    for path, description in TARGETS:
        print(f"\n🔗 {path}")
        r = session.get(f"{BASE}/blogs/{BLOG_ID}/posts/bypath",
                        params={"path": path, "fields": "id,title,content"})
        if r.status_code != 200:
            print(f"  ❌ 조회 실패: {r.status_code}")
            continue

        post = r.json()
        post_id = post["id"]
        title = post["title"]
        content = post.get("content", "")
        print(f"  📄 [{post_id}] {title!r}")

        # Check if post-specific description already in content
        if f'name="description" content="{description[:30]}' in content:
            print("  ✅ 이미 있음")
            continue

        # Patch with customMetaData (Blogger search description field)
        r2 = session.patch(
            f"{BASE}/blogs/{BLOG_ID}/posts/{post_id}",
            json={"customMetaData": f'{{"searchDescription":"{description}"}}'}
        )
        if r2.status_code == 200:
            print(f"  ✅ description 업데이트 완료")
        else:
            print(f"  ⚠️  customMetaData 실패 ({r2.status_code}), content 방식 시도...")
            # Fallback: prepend meta tag to content
            meta = f'<meta name="description" content="{description}"/>\n'
            if '<meta name="description"' not in content:
                new_content = meta + content
                r3 = session.patch(f"{BASE}/blogs/{BLOG_ID}/posts/{post_id}",
                                   json={"content": new_content})
                if r3.status_code == 200:
                    print(f"  ✅ content에 meta tag 추가 완료")
                else:
                    print(f"  ❌ 실패: {r3.status_code} {r3.text[:100]}")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
