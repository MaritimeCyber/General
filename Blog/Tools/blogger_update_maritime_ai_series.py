#!/usr/bin/env python3
"""
ShipPaulJobs — Maritime Enterprise AI Series Updater
---------------------------------------------------
"2027 Revised Series" 5편을 해양 조직 관점으로 보완한 로컬 HTML
(Blog/POST/AI/ChatBot/ChatBot_N_2027.html)을 Blogger에 반영합니다.

  - 제목과 본문을 함께 교체합니다. URL(슬러그)은 그대로 유지됩니다.
  - 라이브 글에 다른 Tools 스크립트가 덧붙인 블록(관련 글, Field Note)은 보존해서 뒤에 다시 붙입니다.
  - 교체 전 라이브 제목·본문을 JSON으로 백업합니다.
  - 기본은 DRY RUN (변경 없음). 실제 적용은 --apply 옵션.

사용법 (Blog/Tools 폴더):
  python blogger_update_maritime_ai_series.py           # 미리보기
  python blogger_update_maritime_ai_series.py --apply   # 실제 반영
"""

import json
import os
import re
import sys
from datetime import datetime

from blogger_title_updater import BLOG_ID, HttpError, get_service

SRC_DIR = os.path.join("..", "POST", "AI", "ChatBot")

# (URL 경로, 로컬 파일, 새 제목)
SERIES_POSTS = [
    ("/2026/08/building-org-wide-consensus-in-llm-era.html", "ChatBot_1_2027.html",
     "Building AI Consensus in Shipping Companies and Shipyards — Who Must Be in the Room, from the Bridge to the Boardroom (Maritime Enterprise AI 1/5)"),
    ("/2026/08/from-messenger-to-autonomous-agent.html", "ChatBot_2_2027.html",
     "AI Channels for Ship and Shore — From Office Copilots to Shipboard Agents over Satellite Links (Maritime Enterprise AI 2/5)"),
    ("/2026/08/activating-intelligent-service.html", "ChatBot_3_2027.html",
     "RAG and AI Agents for Class Rules, SMS Manuals and Ship Data — Design Choices for Maritime Organizations (Maritime Enterprise AI 3/5)"),
    ("/2026/08/llm-architecture-ai-ethics-2027-revised.html", "ChatBot_4_2027.html",
     "LLM Failure Modes and AI Regulation in Maritime — Hallucination, Prompt Injection, the EU AI Act and the ISM Code (Maritime Enterprise AI 4/5)"),
    ("/2026/08/enterprise-ai-in-agent-era-2027-revised.html", "ChatBot_5_2027.html",
     "Choosing Enterprise AI as a Shipowner or Shipyard — A Ten-Question Decision Framework (Maritime Enterprise AI 5/5)"),
]

# 다른 Tools 스크립트가 라이브 글 끝에 붙이는 블록 (add_internal_links.py, update_all_posts.py)
PRESERVE_IDS = ["related-articles-section", "field-note-section"]


def extract_div_by_id(html: str, div_id: str):
    """id 가 div_id 인 <div> 블록 전체(중첩 div 포함)를 반환. 없으면 None."""
    m = re.search(rf'<div\b[^>]*\bid="{re.escape(div_id)}"[^>]*>', html)
    if not m:
        return None
    depth, pos = 0, m.start()
    for tag in re.finditer(r"<(/?)div\b[^>]*>", html[pos:], flags=re.I):
        depth += -1 if tag.group(1) else 1
        if depth == 0:
            return html[pos:pos + tag.end()]
    return None


def main():
    apply = "--apply" in sys.argv

    print("=" * 60)
    print("ShipPaulJobs — Maritime Enterprise AI Series Updater")
    print(f"  대상: {len(SERIES_POSTS)}개")
    print(f"  {'[LIVE — 제목·본문 교체]' if apply else '[DRY RUN — 실제 변경 없음, --apply 로 적용]'}")
    print("=" * 60)

    service = get_service()
    plans, missing = [], 0

    for path, filename, new_title in SERIES_POSTS:
        local = open(os.path.join(SRC_DIR, filename), encoding="utf-8").read()
        try:
            post = service.posts().getByPath(blogId=BLOG_ID, path=path).execute()
        except HttpError as e:
            print(f"\n  [SKIP — 공개 글 없음] {path}  ({e.resp.status} — Draft/삭제 여부 확인)")
            missing += 1
            continue

        live = post.get("content", "")
        kept = [blk for blk in (extract_div_by_id(live, i) for i in PRESERVE_IDS) if blk and blk not in local]
        new_content = local.rstrip() + "\n" + "\n".join(kept) if kept else local

        print(f"\n  [UPDATE] {path}")
        print(f"           - {post.get('title', '')}")
        print(f"           + {new_title}")
        kept_ids = [i for i in PRESERVE_IDS if any('id="%s"' % i in b for b in kept)]
        note = f"  (보존 블록: {', '.join(kept_ids)})" if kept_ids else ""
        print(f"           본문: {len(live):,} → {len(new_content):,} chars{note}")
        plans.append((post, new_title, new_content))

    if apply and plans:
        backup = f"series_backup_{datetime.now():%Y%m%d_%H%M%S}.json"
        with open(backup, "w", encoding="utf-8") as f:
            json.dump([{k: p.get(k) for k in ("id", "url", "title", "content")} for p, _, _ in plans],
                      f, ensure_ascii=False, indent=2)
        print(f"\n💾 백업 저장: {backup}")
        for post, new_title, new_content in plans:
            service.posts().patch(blogId=BLOG_ID, postId=post["id"],
                                  body={"title": new_title, "content": new_content}).execute()

    print("\n" + "=" * 60)
    verb = "반영" if apply else "반영 예정"
    print(f"✅ 완료  |  {verb}: {len(plans)}  건너뜀: {missing}")
    print("=" * 60)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
