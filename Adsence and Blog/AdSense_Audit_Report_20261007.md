# AdSense 재심사 감사 보고서 (2차)
**사이트**: shippauljobs.com | **Publisher ID**: ca-pub-1136000774216453
**감사일**: 2026-10-07 | **판정**: 정책 위반 — 가치가 별로 없는 콘텐츠 (Low Value Content)
**근거 자료**: `all_192_posts.txt`(sitemap 기준 192개), `non_indexed_posts_analysis.txt`(GSC), `AdSense_Audit_Report_20260722.md`(1차 감사)

> 참고: 이번 감사 환경에서는 라이브 사이트(shippauljobs.com / blogspot) 접속이 네트워크 정책으로 차단되어, 저장소의 sitemap·GSC 추출 자료를 기준으로 분석했습니다. 아래 수치는 해당 시점 스냅샷 기준입니다.

---

## 0. 이번 거절 문구가 말하는 것

이번 통지는 1차(7월) 때와 문구가 다릅니다. 핵심 세 문장:

| 통지 문구 | 심사관이 실제로 보는 신호 | 이 사이트의 현재 상태 |
|---|---|---|
| "충분한 **고유 가치**를 제공" | 다른 곳에 없는 1차 경험·분석인가, 규정 요약/AI 생성 글인가 | 규정 해설·시리즈물 다수, 원문 재서술 비중 높음 |
| "웹에서 **꾸준히 운영**" | 일정한 발행 리듬, 오래 유지된 URL, 구조 정리 | 192개 중 **127개가 2026년**, 7월 한 달 46개 (버스트 발행) |
| "상업적 광고를 지원하는 수준의 **사용자 관심**" | 자연 검색 유입, 재방문, 색인 비율 | 색인 **~104/192 (54%)**, 5~8월 글 95개 중 ~88개 미색인 |

즉, **개별 글 단어 수 문제가 아니라 "사이트 전체 신호" 문제**입니다. 1차 감사에서 E26 소항목 25개를 정리했지만, 그 이후 오히려 대량 발행이 이어져 같은 판정이 반복된 것으로 판단됩니다.

---

## 1. 🔴 원인 분석 (심각도 순)

### 1-1. 제목 없는 포스트 28개 — 가장 직접적인 저품질 신호
sitemap 기준 `[제목 없음]` 으로 노출되는 포스트가 **28개 (전체의 14.6%)** 입니다. Blogger에서 제목 필드가 비어 있으면 `<title>`이 블로그 이름만 남고, 검색결과·AdSense 크롤러 모두 "제목 없는 페이지"로 인식합니다.

| URL | 조치 |
|---|---|
| /2026/07/chapter-3-do-not-kill-goose-that-lays.html | 제목 입력 |
| /2026/06/ship-ot-cybersecurity-iacs-e26e27.html | 제목 입력 |
| /2026/05/risk-management-prologue-ur-e26-and.html | 제목 입력 |
| /2026/05/maritime-cyber-security-jobs-complete.html | 제목 입력 |
| /2026/04/top-maritime-companies-hiring-in-2026.html | 제목 입력 (채용 리스트형이면 Draft) |
| /2026/04/ot-asset-management-for-ships.html | 제목 입력 |
| /2026/04/efficient-way-to-classify-system-types.html | 제목 입력 |
| /2026/03/ics-security-hapter-3-deep-dive-host.html | 제목 입력 (슬러그 오타 "hapter") |
| /2026/03/iacs-ur-e27-tasoc-supplier.html | 제목 입력 |
| /2026/03/iacs-ur-e26e27-audits-what.html | 제목 입력 |
| /2025/11/the-reality-of-cyber-regulations-facing.html | 제목 입력 |
| /2025/11/cyber-regulatory-landscape-and-industry.html | 제목 입력 |
| /2025/10/kormarin-2025-back-on-that-sea-again.html | 제목 입력 (전시회 참관기 = 1차 경험, 유지 가치 높음) |
| /2025/10/he-8-global-cybersecurity-institutions.html | 제목 입력 (슬러그 오타 "he-8") |
| /2025/10/blog-post.html | **슬러그 없음** → 내용 확인 후 Draft 또는 재작성 |
| /2025/05/understanding-imo-msc-fal1circ3rev3.html | 제목 입력 |
| /2025/03/the-relationship-between-cbs-definition.html | 제목 입력 |
| /2025/02/reconnecting-with-my-shipbuilding.html | 제목 입력 |
| /2025/02/global-maritime-leadership-ship.html | 제목 입력 |
| /2025/01/major-systems-installed-on-commercial.html | 제목 입력 |
| /2024/12/must-read-for-maritime-industry-review.html | 제목 입력 |
| /2024/12/imo-cybersecurity-regulations-and.html | 제목 입력 |
| /2024/10/impact-of-starlink-on-maritime.html | 제목 입력 |
| /2024/08/blog-post.html | **슬러그 없음** → Draft 권장 |
| /2024/08/auto-gpt-autonomous-gpt-4-experiment.html | 주제 이탈 → Draft 권장 |
| /2024/06/langgraph-building-stateful-multi-actor.html | 주제 이탈 → Draft 권장 |
| /2024/06/generative-agents-interactive-simulacra.html | 주제 이탈 → Draft 권장 |
| /2024/05/have-you-tried-journey-of-challenge-and.html | 내용 확인 후 결정 |

> sitemap의 `[제목 없음]` 은 추출 스크립트의 표기일 수 있으므로, **Blogger 관리자 → 글 목록에서 "(제목 없음)" 으로 표시되는지** 먼저 확인하세요. 실제로 비어 있다면 이것이 1순위 조치입니다.

### 1-2. 버스트 발행 = "Scaled content" 패턴
| 연도 | 포스트 수 |
|---|---|
| 2014–2021 | 12 |
| 2023 | 2 |
| 2024 | 13 |
| 2025 | 38 |
| **2026 (4~8월)** | **127** (4월 4 · 5월 16 · 6월 24 · **7월 46** · 8월 9) |

- 7월에만 하루 1.5개꼴. 동시에 AI 생성 커버 이미지(git 로그 "Add cover: …")와 AI 영상(Kling)이 대량 투입된 시기와 겹칩니다.
- Google은 짧은 기간 대량 발행 + 유사 구조(시리즈 · Chapter · Part)를 **"scaled content abuse"** 신호로 봅니다. 이것이 "꾸준히 운영" 문구에 대응하는 원인입니다.
- 8월 이후 발행이 9개로 급감 → "버스트 후 정체" 패턴은 오히려 "운영 지속성 부족"으로 읽힙니다.

### 1-3. 색인율 54% — Google 스스로 "가치 낮음"으로 판단 중
- 색인 ~104 / 192. 5~8월 글 95개 중 ~88개 미색인.
- "발견됨 – 현재 색인이 생성되지 않음"은 크롤링 지연이 아니라 **품질 판단 보류** 신호인 경우가 대부분입니다. 미색인 URL이 절반에 가까우면 AdSense 심사도 같은 판단을 내립니다.

### 1-4. 주제 분산 — 사이트 정체성 희석
사이트 정체성은 "조선해양 사이버 보안(IACS UR E26/E27)"인데, 다음 축들이 섞여 있습니다.

| 축 | 예시 | 문제 |
|---|---|---|
| 일반 AI 논문 리뷰 | BERT, ReAct, Toolformer, AutoGen, CrewAI, MCP, Sora, LangGraph, Auto-GPT | 제목에 "Maritime"을 덧붙인 일반 논문 요약 → 고유 가치 낮음, 수천 개 유사 글 존재 |
| 기업 AI 전략 | "2027 Revised Series" Part 1~5 (Org-wide consensus, Channel strategy, RAG, LLM ethics, Enterprise AI) | 해양과 무관한 일반 경영 글 |
| 커리어/협상/에세이 | Negotiation, Chicken or Egg, Smart Marine Consultant, Jobs | 일부는 1차 경험(좋음), 일부는 일반론 |
| 선박 시스템 일반 | Propulsion, Navigation, Communication, Cargo, Ballast, Alarm, Fire Detection (7월 집중) | 위키형 개요 글 → 기존 자료 대비 차별점 약함 |
| 2018–2021 R&D | Face recognition, Deep learning fundamentals, NLP review | 오래되고 주제 이탈 |

### 1-5. 시리즈 중복·카니발리제이션
같은 주제를 여러 시리즈가 반복 설명합니다: ZCD 3편 + Zone/VLAN + 물리 네트워크(E26 네트워크), "Chapter 1~9" 계열이 최소 2~3개 책에서 혼재, "UR E26, After the Mandate ①~⑥", "Type approval Part I/II", "AI Cyber Threats 1~3", "Maritime AI & Data 1~4", "Jump Server 1~3", "ICS Security Chapter 3/7/8".
→ Chapter 번호만 있는 제목("Chapter 7. Role of Shipyard and Supplier")은 단독으로 읽히지 않는 페이지로 평가됩니다.

### 1-6. 기타 구조 이슈
- **robots.txt 불일치**: 1차 보고서에는 `/2014/ ~ /2021/`, `/search/label/` 등 Disallow가 있다고 되어 있으나, 저장소 `robots.txt`에는 `/feeds`, `/search`만 있습니다. 실제 라이브 설정(Blogger → 설정 → 크롤러 및 색인 생성 → 맞춤 robots.txt)을 확인하세요.
  - 또한 **robots.txt Disallow는 저품질 글을 숨기지 못합니다.** 크롤러가 내용을 못 읽을 뿐 URL은 sitemap·내부링크로 계속 노출됩니다. 정리는 **Draft 전환 또는 삭제**로 해야 합니다.
- **ads.txt**: 정상 (`pub-1136000774216453 DIRECT` + Blogger host RESELLER).
- **제3자 문서 재배포 위험**: 저장소 `Download/` 폴더에 DNV·LR·ABS·RINA 규칙서, IEC 62443, "(구글 번역) UR-E26/E27" 등 저작권 문서가 있습니다. 블로그에서 이 파일들을 직접 링크·임베드하고 있다면 "복제 콘텐츠/저작권" 신호가 됩니다. 원문 공식 URL 링크로 대체하세요. (특히 IEC 62443은 유료 표준입니다.)

---

## 2. ✅ 조치 계획 (우선순위)

### 1단계 — 즉시 (1주 이내)
1. **제목 없는 28개 처리**: 유지할 글은 제목 입력, 슬러그 없는 `blog-post.html` 2개와 주제 이탈 AI 글 3개는 Draft.
2. **주제 이탈 글 Draft 전환** (약 30~40개 예상):
   - 일반 AI 논문 리뷰 전부 (BERT, ReAct, Toolformer, NL2SQL, Sora, AutoGen, CrewAI, MCP, LangGraph, Auto-GPT, Generative Agents, NeurIPS RL, NLP Review, CV Roadmap, Deep Learning Fundamentals, Face Recognition)
   - "2027 Revised Series" Part 1~5
   - 2014–2021 글 중 해양 사이버와 무관한 글
   - 판단 기준: **"이 글은 조선해양 사이버 보안 컨설턴트만 쓸 수 있는가?"** 아니면 Draft.
3. **Chapter 번호형 제목 수정**: "Chapter 7. Role of Shipyard and Supplier" → "Shipyard vs Supplier Responsibilities Under IACS UR E26/E27 (Ch.7)" 처럼 단독으로 의미가 통하게.
4. **중복 시리즈 병합**: 동일 주제는 대표 글 1개로 합치고 나머지는 Draft (Blogger는 301을 지원하지 않으므로, Draft 전환 후 대표 글로 내부 링크 정리).

목표: **공개 포스트 192 → 약 100~120개**, 남은 글 전부 제목·주제·깊이 기준 통과.

### 2단계 — 고유 가치 강화 (2~4주)
"고유 가치" 판정은 **1차 경험 증거**가 결정합니다. 이 사이트의 가장 큰 자산은 운영자의 실제 컨설팅 경험입니다. 핵심 글 15~20개(Pillar)에 다음을 추가하세요.

- 실제 프로젝트에서 나온 **익명화된 사례** (예: "FAT에서 E27 인증서가 있어도 실패한 3가지 경우")
- 직접 만든 **다이어그램·체크리스트·템플릿** (AI 생성 커버 이미지가 아니라, ZCD 예시도, 자산 인벤토리 샘플 등)
- 규정 원문 **조항 번호 인용 + 해석 차이**(선급별 KR/DNV/ABS 해석 비교 등 — 다른 사이트에 없는 정보)
- 작성자 바이라인 + 경력(About 페이지와 연결), **최종 검토일**
- 사이트 고유 도구(Maritime Cyber Rule Chart, E26 Zone Defense 게임 등)는 **설명 본문을 충분히** 붙여 "도구 + 해설" 페이지로 만들 것

### 3단계 — 운영 지속성 · 사용자 관심 (재심사 전 최소 4~8주)
1. **발행 리듬 정상화**: 주 1~2개, 일정한 요일. 대량 예약 발행 금지.
2. **GSC 색인율 개선**: Draft 정리 후 sitemap 재제출 → 핵심 글 URL 검사 → 색인 요청. **목표 색인율 80% 이상**.
3. **유입 확보**: LinkedIn·해양 커뮤니티·뉴스레터로 핵심 글 공유. 실제 방문자와 체류시간이 쌓여야 "사용자 관심" 신호가 생깁니다.
4. **내부 링크 허브**: 카테고리별 허브 페이지(예: "IACS UR E26 완전 가이드")에서 하위 글로 연결 → 구조적 유지관리 신호.

### 재심사 신청 시점
1차 감사(7/22) 직후 신청 → 재거절된 흐름을 반복하지 않도록, **정리 완료 후 최소 4주, 가능하면 6~8주** 운영 데이터를 쌓은 다음 신청하는 것을 권장합니다. 반복 거절은 다음 심사 대기 기간을 늘립니다.

---

## 3. 재심사 전 체크리스트

- [ ] Blogger 관리자에서 "(제목 없음)" 글 0개
- [ ] 슬러그 `blog-post.html` 형태 URL 0개
- [ ] 일반 AI 논문 리뷰 / 2027 Revised Series / 주제 이탈 글 Draft 완료
- [ ] Chapter·Part 번호만 있는 제목 0개
- [ ] 중복 시리즈 병합 완료, 공개 포스트 ~100~120개
- [ ] Pillar 글 15개 이상에 1차 경험 사례 · 자체 제작 도식 · 바이라인 · 검토일 추가
- [ ] 라이브 robots.txt 확인 (저품질 글은 robots가 아니라 Draft로 처리)
- [ ] 저작권 문서(선급 규칙서, IEC, 번역본) 직접 배포 링크 제거
- [ ] GSC sitemap 재제출, 색인율 80% 이상
- [ ] 정리 후 4주 이상 주 1~2회 일정 발행
- [ ] About / Privacy / Contact / Terms / Editorial Policy 접근 가능 (1차 감사 기준 이미 충족)
- [ ] AdSense → 사이트 → 문제 해결 체크 → 검토 요청

---

## 4. 1차 감사 대비 변화 요약

| 항목 | 1차 (7/22) | 2차 (10/7) |
|---|---|---|
| 진단 초점 | 개별 글 단어 수 (E26 소항목 25개) | **사이트 전체 신호** (발행 패턴 · 색인율 · 주제 분산 · 제목 누락) |
| 핵심 조치 | Draft 25개 → 즉시 재신청 | Draft 60~90개 + Pillar 강화 + **4~8주 운영 후** 재신청 |
| 새로 발견된 문제 | — | 제목 없는 글 28개, 7월 46개 버스트, 색인율 54%, AI 논문 리뷰 주제 이탈, 저작권 문서 배포 위험 |
