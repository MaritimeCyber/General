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

### 1-1. 제목 확인이 필요한 포스트 28개 — ⚠️ 실제 누락 여부 미확인
`all_192_posts.txt` 추출 결과에서 제목이 `[제목 없음]` 으로 표기된 포스트가 **28개** 입니다. 단, **이것이 실제로 제목이 비어 있다는 뜻인지는 확인되지 않았습니다.**

- Blogger는 **첫 게시 시점의 제목으로 URL 슬러그를 만듭니다.** 28개 중 26개는 `kormarin-2025-back-on-that-sea-again` 처럼 영문 슬러그가 있으므로, 게시 당시에는 제목이 있었습니다. → 대부분 **추출 스크립트가 제목을 못 가져온 표기 오류**일 가능성이 높습니다 (sitemap.xml 자체에는 제목이 없음).
- `/2025/10/blog-post.html`, `/2024/08/blog-post.html` 2개는 Blogger가 **한글 제목으로 게시된 글**에 자동으로 붙이는 슬러그입니다. 영문 사이트에서 한글 제목 글이 남아 있을 가능성이 높으므로 우선 확인 대상입니다.
- 만약 실제로 제목이 비어 있다면 `<title>`이 블로그 이름만 남아 저품질 신호가 되므로 1순위 조치입니다.

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
| /2025/10/blog-post.html | ✅ **Draft 전환 완료 (2026-10-07)** |
| /2025/05/understanding-imo-msc-fal1circ3rev3.html | 제목 입력 |
| /2025/03/the-relationship-between-cbs-definition.html | 제목 입력 |
| /2025/02/reconnecting-with-my-shipbuilding.html | 제목 입력 |
| /2025/02/global-maritime-leadership-ship.html | 제목 입력 |
| /2025/01/major-systems-installed-on-commercial.html | 제목 입력 |
| /2024/12/must-read-for-maritime-industry-review.html | 제목 입력 |
| /2024/12/imo-cybersecurity-regulations-and.html | 제목 입력 |
| /2024/10/impact-of-starlink-on-maritime.html | 제목 입력 |
| /2024/08/blog-post.html | ✅ **Draft 전환 완료 (2026-10-07)** |
| /2024/08/auto-gpt-autonomous-gpt-4-experiment.html | 주제 이탈 → Draft 권장 |
| /2024/06/langgraph-building-stateful-multi-actor.html | 주제 이탈 → Draft 권장 |
| /2024/06/generative-agents-interactive-simulacra.html | 주제 이탈 → Draft 권장 |
| /2024/05/have-you-tried-journey-of-challenge-and.html | 내용 확인 후 결정 |

> **확인 방법**: 위 URL을 브라우저로 열어 탭 제목이 "글 제목 | 블로그명" 인지, 블로그명만 나오는지 확인하거나, Blogger 관리자 글 목록에서 "(제목 없음)" 으로 표시되는지 확인하세요. 표의 "제목 입력" 조치는 실제로 비어 있을 때만 해당합니다.

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
1. **제목 확인 필요 28개 점검**: 실제로 비어 있는 글만 제목 입력. `blog-post.html` 2개(한글 제목 추정)는 ✅ Draft 완료 (10/7). auto-gpt, langgraph, generative-agents 3개는 부록 A-1 보완 계획(에이전트 프레임워크 비교 리뷰로 통합)을 따름.
2. **주제 이탈 글 정리** (전체 목록은 **부록 A**):
   - **AI 논문 리뷰 18개 → Draft가 아니라 보완** (운영자 결정, 10/7). 논문 리뷰는 Publications 페이지로 소개되는 사이트의 정식 카테고리이므로 유지하되, 부록 A-1의 "해양 적용 리뷰 템플릿"으로 보강. 해양 연결이 끝내 약한 글만 통합 또는 Draft.
   - **2027 Revised Series 5개 → 해양 조직 관점으로 보완**, 불가능한 편만 Draft (부록 A-2)
   - 2014–2021 글 중 해양 사이버와 무관한 글
   - 판단 기준: **"이 글은 조선해양 사이버 보안 컨설턴트만 쓸 수 있는가?"** 아니면 Draft.
3. **Chapter 번호형 제목 수정** (전체 목록·수정안은 **부록 B**): "Chapter 7. Role of Shipyard and Supplier" → "Shipyard vs Supplier Responsibilities Under IACS UR E26/E27 (Ch.7)" 처럼 단독으로 의미가 통하게.
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

- [ ] 제목 확인 필요 28개 점검 → 실제 "(제목 없음)" 글 0개
- [x] 슬러그 `blog-post.html` 형태 URL 0개 (2개 Draft 전환, 10/7)
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
| 핵심 조치 | Draft 25개 → 즉시 재신청 | 주제 이탈 글 정리(논문 리뷰는 보완·통합) + Pillar 강화 + **4~8주 운영 후** 재신청 |
| 새로 발견된 문제 | — | 제목 확인 필요 28개(대부분 추출 오류 추정), 7월 46개 버스트, 색인율 54%, AI 논문 리뷰 주제 이탈, 저작권 문서 배포 위험 |

---

## 부록 A. 주제 이탈 후보 목록 (41개)

판단 기준: "조선해양 사이버 보안 컨설턴트만 쓸 수 있는 글인가?" 번호는 `all_192_posts.txt` 순번입니다.

### A-1. AI 논문 리뷰·AI 기초 — **18편 전체 Draft 전환 → 보완 후 재게시** (10/7 운영자 결정)

> **실행**: `blogger_revert_to_draft.py` 로 18편을 한 번에 Draft로 되돌립니다 (전환 전 본문 JSON 백업 생성). 아래 템플릿으로 보완을 마친 글부터 Blogger에서 다시 게시하면 같은 URL로 복귀합니다.

논문 리뷰 자체는 문제가 아닙니다. AdSense·Google이 감점하는 것은 **"논문 요약"** 이고, 가점하는 것은 **"그 논문을 이 분야 전문가가 어떻게 읽었는가"** 입니다. 같은 논문의 요약은 웹에 수백 개 있으므로, 요약 비중을 줄이고 해양 사이버 보안 컨설턴트만 쓸 수 있는 부분을 늘리는 것이 보완의 핵심입니다.

#### 해양 적용 리뷰 템플릿 (모든 논문 리뷰 공통)
| 섹션 | 내용 | 권장 비중 |
|---|---|---|
| 1. 서지 정보 | 저자, 학회/저널, 연도, arXiv/DOI 링크 | — |
| 2. 핵심 요약 | 문제·방법·결과를 3~5문장으로. **길게 쓰지 않는다** | 15% 이하 |
| 3. 선박·항만 적용 시나리오 | 어떤 CBS/시스템(IAS, ECDIS, VSAT, NMS, SIEM 등)에 어떻게 쓰이는지 구체 시나리오 | 25% |
| 4. 해양 환경에서의 한계 | 저대역 위성통신, 오프라인 운항, OT 패치 주기, 선원 운영 역량, 형식승인 제약 등 | 20% |
| 5. 직접 해본 것 | 재현 코드, 실험, 샘플 데이터(익명화한 선박 로그 등), 결과 스크린샷·표 | 20% |
| 6. 규정 연계 | IACS UR E26/E27 조항, IEC 62443 FR/SR, IMO MSC-FAL.1/Circ.3 중 어디에 닿는가 | 10% |
| 7. 실무 체크리스트 / 결론 | 선주·조선소·공급사가 지금 할 일 3~5개 | 10% |
| 8. 리뷰어·검토일 | 작성자 바이라인, 최종 검토일 | — |

글 하단에 **Publications 페이지로 돌아가는 링크**를 넣고, Publications 페이지에서도 각 리뷰를 "해양 적용 포인트" 한 줄과 함께 소개하면 카테고리 구조 신호가 강해집니다.

#### 글별 보완 방향
| # | 글 | 해양 연결 강도 | 보완 방향 |
|---|---|---|---|
| 163 | MCP | 강 | 선박 AI 에이전트가 MCP로 NMS/SIEM 도구에 붙을 때의 권한 분리·원격접속 통제 → UR E26 원격접속·최소권한과 매핑 |
| 178 | Sora | 강 | VHF/화상회의 딥페이크로 선장 지시·회사 지시를 위조하는 사회공학 시나리오, 검증 절차(콜백, 코드워드) 제안 |
| 187 | Face Recognition (dlib/OpenCV) | 강 | ISPS Code 선박·항만 출입통제 적용, 오인식률 실험 결과, 생체정보 개인정보(GDPR) 이슈 |
| 179 | NL2SQL | 강 | 선박 NMS/SIEM 로그를 자연어로 질의하는 데모, 잘못된 쿼리·권한 상승 위험 |
| 184 | BERT | 중 | 선박 시스템 로그 분류 실험(샘플 데이터·정확도 표), 오프라인 선상 추론 가능성 |
| 177 | Toolformer | 중 | 해양 CTI(위협 인텔리전스) 수집 자동화 시나리오 — #180 ReAct와 **1편으로 통합** 권장 |
| 180 | ReAct | 중 | 사고 대응 플레이북 자동화 시나리오 — #177과 통합 |
| 165, 176, — | AutoGen · CrewAI · LangGraph · Auto-GPT · Generative Agents (5편) | 중 | **"Multi-Agent Frameworks for a Maritime SOC — 5개 프레임워크 비교 리뷰" 1~2편으로 통합**. 같은 기준(권한 통제, 오프라인 동작, 감사 로그)으로 비교한 표가 핵심 가치 |
| 181 | NeurIPS RL Memory Allocation | 약 | 선상 엣지 장비의 메모리 제약과 연결 가능하면 보완, 아니면 통합/Draft |
| 182, 183, 188, 185, 186 | NLP Review · CV Roadmap · Deep Learning Fundamentals · Math→Chatbot · Market Keywords | 약 | 일반 튜토리얼 성격. **"Maritime AI Foundations" 1편으로 통합** 후 개별 글 Draft 권장 |

> 결과적으로 18개 → **보완 유지 약 8~10편 + 통합 글 2~3편** 이 됩니다. 글 수가 줄어도 편당 깊이가 올라가는 쪽이 심사에 유리합니다.

#### 재심사 일정과의 관계
18편을 모두 보완하는 것은 시간이 걸립니다. **보완을 시작하지 못한 글은 보완할 때까지 잠시 Draft로 두었다가, 보완 후 다시 공개**하는 방법도 있습니다 (Blogger에서 Draft → 재게시해도 URL은 유지됩니다). 보완 순서는 해양 연결이 "강"인 글부터 권장합니다.

**현재 목록:**

| # | 연월 | 제목 |
|---|---|---|
| 163 | 2025/01 | [PAPER] Model Context Protocol (MCP) — Open Standard Specification |
| 165 | 2025/01 | [AI Cyber Lab] AutoGen Paper Review |
| 176 | 2024/05 | [PAPER] CrewAI — Role-based AI Multi-Agent Framework |
| 177 | 2024/03 | [AI Cyber Lab] Toolformer Paper Review |
| 178 | 2024/02 | [AI Cyber Lab] OpenAI Sora & Maritime Cybersecurity |
| 179 | 2023/11 | [AI Cyber Lab] NL2SQL × Maritime Cybersecurity |
| 180 | 2023/06 | [AI Cyber Lab] ReAct Paper Review |
| 181 | 2021/05 | [Paper] Dynamic Allocation in Reinforcement Learning: NeurIPS 2020 |
| 182 | 2021/04 | [Paper] Natural Language Processing: A Review |
| 183 | 2021/04 | Computer Vision R&D Roadmap: CNN, GAN, and 3D Reconstruction |
| 184 | 2021/02 | [AI Cyber Lab] BERT Paper Review |
| 185 | 2021/02 | From Mathematical Foundations to AI Chatbot Development |
| 186 | 2021/02 | The Shift in Market Keywords and the Role of AI |
| 187 | 2020/07 | [R&D] Open-Source Face Recognition with dlib & OpenCV |
| 188 | 2020/07 | Deep Learning Fundamentals — Neural Networks, CNN, RNN, LSTM & Transformers |
| — | 2024/08 | /auto-gpt-autonomous-gpt-4-experiment.html |
| — | 2024/06 | /langgraph-building-stateful-multi-actor.html |
| — | 2024/06 | /generative-agents-interactive-simulacra.html |

### A-2. 기업 AI 경영 시리즈 — **해양 조직 관점으로 보완, 불가능한 편만 Draft (5개)**
현재는 해양·사이버와 직접 관련 없는 일반 경영/AI 도입론입니다. 이 시리즈는 논문 리뷰가 아니므로 A-1과 기준이 다릅니다. 유지하려면 **"선사·조선소가 AI를 도입할 때"** 로 관점을 바꿔야 합니다.

- Part 1 (Org-Wide Consensus): 조선소 설계·생산·품질 부서 간 AI 도입 합의 사례로 재구성
- Part 2 (Channel Strategy): 선박-육상 간 커뮤니케이션 채널(선원·운항관리·공급사)에 AI 에이전트를 붙일 때
- Part 3 (RAG): 선급 규칙·IACS UR·매뉴얼 RAG 구축 경험 — **가장 보완 가치 높음**
- Part 4 (LLM Ethics): 자율운항(MASS Code)·선상 AI 의사결정 책임 문제
- Part 5 (Enterprise AI): 해운사 AI 거버넌스와 사이버 보안(UR E26 범위 밖 IT 시스템)
- 공통: Part 1 제목의 "(this article)" 삭제

| # | 제목 |
|---|---|
| 8 | Building Org-Wide Consensus in the LLM Era (this article) [2027 Revised Series · Part 1] |
| 4 | Channel Strategy in the AI Agent Era [Part 2] |
| 9 | RAG and AI Agents — Activating Intelligent Service [Part 3] |
| 2 | LLM Architecture & AI Ethics [Part 4] |
| 6 | Enterprise AI in the Agent Era [Part 5 — Finale] |

### A-3. 조직·리더십 에세이 시리즈 — **검토 후 Draft 또는 별도 정리 (7개)**
개인 경험이 담긴 글이라 E-E-A-T에 도움이 될 수 있지만, 사이트 주제와는 떨어져 있고 제목도 번호형입니다. 유지한다면 해양 업계 경험으로 다시 연결해 제목을 바꾸고, 아니면 Draft.

| # | 제목 |
|---|---|
| 144 | Chapter 1. Is Yi Sun-sin Essential to an Organization? |
| 143 | Chapter 2. In the end, it was myself who led me. |
| — | /2026/07/chapter-3-do-not-kill-goose-that-lays.html |
| 142 | Chapter 4. Why do I clash with my boss every time? |
| 127 | Chapter 5. Reflecting on my past career and the taboos of organizational life. |
| 124 | Chapter 6. The Villain Effect — A Story of How Organizations Lose Themselves |
| 94 | Chapter 7. Negotiation: The Game Is Different at Every Level |

### A-4. 개인·회사 소식, 인사말 — **검토: 1개 About/Journey 글로 통합 권장 (7개)**
짧은 공지·감사글은 단독 페이지로는 가치가 낮습니다. 경력 스토리는 About 페이지나 "My Journey" 글 하나로 통합하세요.

| # | 제목 |
|---|---|
| 161 | A New Chapter: From Curiosity to Action |
| — | /2025/02/reconnecting-with-my-shipbuilding.html |
| 145 | The First Step Toward the World's First Cyber Ship – With Sincere Thanks for the Cybersecurity Policy Briefing |
| 138 | ⚓ A Letter of Gratitude and Commitment – 2025 |
| 131 | Evergreen Collaboration Begins: A Significant Step Toward Global Growth |
| 130 | Returning to the Shipyard: Where My Past, Present, and Future Converge |
| — | /2024/05/have-you-tried-journey-of-challenge-and.html |

### A-5. 오래된 레거시 글 — **검토 (4개)**
| # | 제목 | 의견 |
|---|---|---|
| 192 | (2014) SK Telecom × DSME Smart Ship Partnership | 스마트십 역사 자료로 보강 시 유지 가능 |
| 191 | (2018) DSME · Naver · Intel Smart Ship 4.0 MOU | 위와 동일 |
| 190 | (2019) The vision behind ShipPaulJobs | About 페이지로 통합 |
| 189 | (2020) DID System Autonomous Operation | 주제 이탈 → Draft |

### A-6. 별도 주의 — 사실 확인 필요
아래 글은 주제 이탈은 아니지만, **사실 여부가 불확실하면 "신뢰할 수 있는 정보" 기준에서 감점**됩니다. 출처 링크가 본문에 있는지 확인하세요.
- #36 "OpenAI's Model Escaped Its Sandbox and Breached Hugging Face"
- #60/95/79 "AI Cyber Threats (1~3/3): Understanding Claude Mythos …"
- #5 "Floating Data Centers", #53 "AI Shipyard Has Officially Begun" — 해양 연관성은 있으나 근거 자료 보강 필요

---

## 부록 B. 제목 수정 목록

### B-1. 번호만으로는 내용을 알 수 없는 제목 → 수정안

> **일괄 적용**: B-1(#83 제외)과 B-2의 20개는 `blogger_title_updater.py` 로 한 번에 바꿀 수 있습니다. 제목만 바뀌고 URL은 유지됩니다. 먼저 `python blogger_title_updater.py` 로 미리보기를 확인한 뒤 `--apply` 로 적용하세요. #83은 본문 주제를 확인한 뒤 직접 제목을 정해야 합니다.
E26/E27 엔지니어링 시리즈(Chapter 1~9)는 핵심 콘텐츠이므로 **유지하되 제목만 단독으로 읽히게** 바꿉니다. 시리즈 표기는 뒤로 보냅니다.

| # | 현재 제목 | 수정안 |
|---|---|---|
| 77 | Chapter 1. Digitalization of Modern Ships | How Ship Digitalization Created the Cyber Risk Behind IACS UR E26 (Ch.1) |
| 76 | Chapter 2. Increasing OT System Interdependency | Why Shipboard OT Interdependency Turns One Failure into Many (Ch.2) |
| 75 | Chapter 3. Why Cybersecurity Became a System Engineering Issue | Ship Cybersecurity Is a System Engineering Problem, Not an IT Add-On (Ch.3) |
| 74 | Chapter 4: Understanding Why IACS Introduced E26 and E27 | Why IACS Introduced UR E26 and E27: The Engineering Gap They Close (Ch.4) |
| 11 | Chapter 5. From Functional Design to Explainable Design | From Functional to Explainable Design: What UR E26 Reviewers Expect (Ch.5) |
| 50 | Chapter 6. Required Engineering Evidence | What Engineering Evidence UR E26/E27 Approval Actually Requires (Ch.6) |
| 55 | Chapter 7. Role of Shipyard and Supplier | Shipyard vs. Supplier Responsibilities Under IACS UR E26/E27 (Ch.7) |
| 49 | Chapter 8. How Engineering Information Flows Through a Project | How Cyber Engineering Information Flows from Supplier to Class in a Newbuild (Ch.8) |
| 7 | Chapter 9 From Compliance Documentation to Sustainable Cybersecurity Engineering | Beyond E26 Paperwork: Building Sustainable Ship Cybersecurity Engineering (Ch.9) |
| 46 | Article 1 : The Cyber Resilience System Integrator and the Six Core Ship-Level Deliverables | The Cyber Resilience System Integrator: Six Ship-Level Deliverables Under UR E26 |
| 83 | Which Comes First — the Chicken or the Egg? (Part 1) | 본문 주제를 제목에 명시 (예: "E26 vs E27: Which Comes First in a Newbuild Project?") |

### B-2. 시리즈 표기는 있으나 주제가 앞에 와야 하는 제목
| # | 현재 | 수정안 |
|---|---|---|
| 85 | Part 1. Why Modern Ships Need Jump Servers (Maritime Jump Server Series) | Why Modern Ships Need Jump Servers — Maritime Jump Server Series (1/3) |
| 67 | Part 2. Designing Secure Remote Access for Ships | Designing Secure Remote Access for Ships — Maritime Jump Server Series (2/3) |
| 34 | Part 3. How to Evaluate a Maritime Jump Server Solution | How to Evaluate a Maritime Jump Server Solution — Jump Server Series (3/3) |
| 111 | ICS Security Chapter 1 The Nature of Industrial Control Systems … | The Nature of ICS/OT and Its Security Paradigm — ICS Security Ch.1 |
| 110 | ICS Security Chapter 2 CS Network Architecture Fundamentals | ICS Network Architecture Fundamentals — ICS Security Ch.2 (오타 "CS" 수정) |
| 109 | ICS Security Chapter 4 Threat Modeling Fundamentals … | ICS Threat Modeling: Attack Chains & EWS Pivot Analysis — ICS Security Ch.4 |
| 108 | ICS Security Chapter 5 Host Security … | ICS Host Security After Preventive Controls — ICS Security Ch.5 |
| 100 | ICS Securit Chapter 6 Documentation Fundamentals … | ICS Security Documentation Fundamentals — ICS Security Ch.6 (오타 "Securit" 수정) |
| 93 | ICS Security Chapter 7 Security Testing Fundamentals … | ICS Security Testing Fundamentals — ICS Security Ch.7 |
| 92 | ICS Security Chapter 8 · OT Security Architecture & Deployment Fundamentals | OT Security Architecture & Deployment — ICS Security Ch.8 |

### B-3. 오타·편집 흔적 (즉시 수정)
| # | 문제 | 수정 |
|---|---|---|
| 8 | 제목에 "(this article)" 이 남아 있음 | 삭제 (A-2 Draft 대상이면 생략) |
| 100 | "ICS Securit" | "ICS Security" |
| 110 | "CS Network" | "ICS Network" |
| 41 | "Binding. : Effective …" 구두점 중복 | "Italy Makes Maritime Cyber Compliance Binding from 1 Nov 2026 — What Circular 177/2025 Requires" |
| 3 | 문장형 제목 + 마침표 | "Rushing CSDD During Construction Breaks SCARP After Vessel Delivery" |
| 27, 134, 136, 168 | 공백 2칸 ("Cable to Cyber Resilience  Designing", "Poor  Documentation", "Why  Compliance", "E27]  Compliance") | 공백 1칸 |
| — | 슬러그 `ics-security-hapter-3`, `he-8-global-…` | Blogger는 게시 후 슬러그 변경 시 URL이 바뀌므로 **제목만** 수정 |
