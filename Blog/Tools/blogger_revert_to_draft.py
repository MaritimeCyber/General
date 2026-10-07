#!/usr/bin/env python3
"""
ShipPaulJobs — Blogger Revert to Draft
---------------------------------------------------
AdSense 2차 감사(AdSense_Audit_Report_20261007.md) 부록 A-1의
AI 논문 리뷰·AI 기초 18편을 Draft(임시저장)로 되돌립니다.

  - 삭제가 아니라 Draft 전환입니다. 보완 후 Blogger에서 다시 게시하면 같은 URL로 돌아옵니다.
  - 전환 전에 각 글의 제목·URL·게시일·라벨·본문을 JSON으로 백업합니다.
  - 이미 Draft이거나 삭제된 글(404)은 건너뜁니다.
  - 기본은 DRY RUN (변경 없음). 실제 적용은 --apply 옵션.

사용법:
  1. Blog/Tools 의 credentials.json / token.json 을 그대로 사용합니다 (다른 Tools 스크립트와 동일).
  2. pip install google-auth google-auth-oauthlib requests
  3. python blogger_revert_to_draft.py           # 미리보기
  4. python blogger_revert_to_draft.py --apply   # 실제 Draft 전환
"""

import json
import os
import sys
import types
from datetime import datetime

BLOG_ID          = "8002758868633250458"
CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE       = "token.json"

# (URL 경로, 메모) — 부록 A-1 의 18편
POSTS_TO_DRAFT = [
    ("/2025/01/model-context-protocol-open-standard.html",   "#163 MCP"),
    ("/2025/01/autogen-enabling-next-gen-llm.html",          "#165 AutoGen"),
    ("/2024/05/crewai-role-based-ai-multi-agent.html",       "#176 CrewAI"),
    ("/2024/03/toolformer-language-models-can-teach.html",   "#177 Toolformer"),
    ("/2024/02/ai-sora.html",                                "#178 Sora"),
    ("/2023/11/nl2sql.html",                                 "#179 NL2SQL"),
    ("/2023/06/react-synergizing-reasoning-and-acting.html", "#180 ReAct"),
    ("/2021/05/neurips-2020-dynamic-allocation-of.html",     "#181 NeurIPS RL"),
    ("/2021/04/issn-2249-3905-natural-language.html",        "#182 NLP Review"),
    ("/2021/04/computer-vision-image-processing.html",       "#183 CV Roadmap"),
    ("/2021/02/bert-pre-training-of-deep-bidirectional.html", "#184 BERT"),
    ("/2021/02/bert-15.html",                                "#185 Math -> Chatbot"),
    ("/2021/02/1-step-3-ai.html",                            "#186 Market Keywords"),
    ("/2020/07/research-facerecognition.html",               "#187 Face Recognition"),
    ("/2020/07/deep-learning-deep-learning-preview.html",    "#188 Deep Learning Fundamentals"),
    ("/2024/08/auto-gpt-autonomous-gpt-4-experiment.html",   "Auto-GPT"),
    ("/2024/06/langgraph-building-stateful-multi-actor.html", "LangGraph"),
    ("/2024/06/generative-agents-interactive-simulacra.html", "Generative Agents"),
]


API_BASE = "https://blogger.googleapis.com/v3"


class HttpError(Exception):
    def __init__(self, response):
        super().__init__(f"{response.status_code} {response.text[:200]}")
        self.resp = types.SimpleNamespace(status=response.status_code)


class _Call:
    def __init__(self, session, method, url, **kwargs):
        self.session, self.method, self.url, self.kwargs = session, method, url, kwargs

    def execute(self):
        r = self.session.request(self.method, self.url, **self.kwargs)
        if not r.ok:
            raise HttpError(r)
        return r.json() if r.content else {}


class _Posts:
    def __init__(self, session):
        self.session = session

    def getByPath(self, blogId, path):
        return _Call(self.session, "GET", f"{API_BASE}/blogs/{blogId}/posts/bypath", params={"path": path})

    def patch(self, blogId, postId, body):
        return _Call(self.session, "PATCH", f"{API_BASE}/blogs/{blogId}/posts/{postId}", json=body)

    def revert(self, blogId, postId):
        return _Call(self.session, "POST", f"{API_BASE}/blogs/{blogId}/posts/{postId}/revert")


class BloggerService:
    """googleapiclient 없이 Blogger REST API 를 호출 (add_naver_verification.py 와 같은 AuthorizedSession 방식)."""
    def __init__(self, session):
        self.session = session

    def posts(self):
        return _Posts(self.session)


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
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request, AuthorizedSession

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

    return BloggerService(AuthorizedSession(creds))


def main():
    apply = "--apply" in sys.argv

    print("=" * 60)
    print("ShipPaulJobs — Blogger Revert to Draft")
    print(f"  대상: {len(POSTS_TO_DRAFT)}개")
    print(f"  {'[LIVE — Draft 전환]' if apply else '[DRY RUN — 실제 변경 없음, --apply 로 적용]'}")
    print("=" * 60)

    service = get_service()

    found = []
    missing = 0

    for path, memo in POSTS_TO_DRAFT:
        try:
            post = service.posts().getByPath(blogId=BLOG_ID, path=path).execute()
        except HttpError as e:
            print(f"\n  [SKIP — 공개 글 없음] {memo}  {path}  ({e.resp.status} — 이미 Draft/삭제)")
            missing += 1
            continue
        print(f"\n  [DRAFT] {memo}  {path}")
        print(f"          {post.get('title', '')}")
        found.append(post)

    reverted = 0
    if apply and found:
        backup = f"draft_backup_{datetime.now():%Y%m%d_%H%M%S}.json"
        with open(backup, "w", encoding="utf-8") as f:
            json.dump(
                [{k: p.get(k) for k in ("id", "url", "title", "published", "updated", "labels", "content")}
                 for p in found],
                f, ensure_ascii=False, indent=2,
            )
        print(f"\n💾 백업 저장: {backup}")

        for post in found:
            service.posts().revert(blogId=BLOG_ID, postId=post["id"]).execute()
            reverted += 1

    print("\n" + "=" * 60)
    if apply:
        print(f"✅ 완료  |  Draft 전환: {reverted}  건너뜀: {missing}")
    else:
        print(f"✅ 미리보기  |  Draft 전환 예정: {len(found)}  건너뜀: {missing}")
    print("=" * 60)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
