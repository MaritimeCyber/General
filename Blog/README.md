# ShipPaulJobs Blog — 폴더 구조

> Last updated: 2026-08-23

## 최상위 구조

```
Blog/
├── Main/           # 블로그 테마 XML + Main.html (Blogger 직접 적용)
├── Layout/         # UI 컴포넌트 (사이드바, 헤더)
│   ├── Header/     # 상단 헤더 위젯
│   └── SideBar/    # 사이드바 위젯 모음
├── Pages/          # Blogger 정적 페이지 + 서비스 페이지
│   ├── Menu/       # 메인 메뉴 네비게이션 페이지
│   └── AppService/ # 앱 서비스 (ComplianceBot 등)
├── POST/           # 블로그 포스트 (주제별 분류)
├── Authors/        # 저자별 HTML 템플릿
├── Backend/        # 인젝션 코드, 백엔드 위젯
└── Tools/          # Python 자동화 스크립트
```

---

## POST/ 주제별 폴더

| 폴더 | 내용 | 주요 저자 |
|------|------|-----------|
| `AI/` | AI 에이전트, ChatBot 시리즈 | Paul |
| `Books/` | ICS 시리즈 내비게이션, 시리즈 박스 | Lew |
| `Compliance/` | IACS 규정 준수 시리즈 | Paul, Blue Horizonist |
| `Compliance/IACS_E26/` | IACS UR E26 조항별 포스트 | Paul |
| `Compliance/IACS_E27/` | IACS UR E27 시리즈 | Blue Horizonist |
| `Compliance/OT_Cyber_Series/` | OT 사이버 시리즈 (5편) | Paul |
| `Compliance/Vessel_Operators_Series/` | 선박 운항자 시리즈 (4편) | Paul |
| `Cybersecurity/` | 선박 사이버 솔루션 (Firewall, IDS, SIEM 등) | SPJ |
| `Cybersecurity/Jump_Server/` | Jump Server 시리즈 (4편) | CaptainPaul |
| `Insight/` | 인사이트 & 트렌드 분석 | Paul |
| `Jobs/` | 해양 취업 정보 | Paul |
| `Leadership/` | 리더십 시리즈 Ch1~Ch7 | Paul |
| `News/` | 해사 뉴스 리뷰 | Paul |
| `Paper/` | 논문 리뷰 | Paul |
| `Pillar/` | Pillar 콘텐츠 (IACS UR E26, E27 종합 가이드) | Paul |
| `RND/` | R&D 관련 포스트 | Paul |
| `Ship_Systems/` | 선박 시스템 소개 (항법, 추진, 화재감지 등) | SPJ |
| `Type_Approval/` | 형식 승인 관련 포스트 | Iris, Richard, Sheep |

---

## Authors/ 저자별 템플릿

| 폴더 | 저자 |
|------|------|
| `Paul/` | Captain Paul (InSung Lee) — 블로그 운영자 |
| `Blue_Horizonist/` | Blue Horizonist — E27 기고자 |
| `Changmin/` | Changmin — OT Security 기고자 |
| `Yeon/` | Yeon — IACS/Compliance 기고자 |
| `Richard/` | Richard — Type Approval 기고자 |
| `Brandon/` | Brandon — Insight 기고자 |
| `Gaber_Esmail/` | Gaber Esmail — Survey/Insight 기고자 |
| `Shin/` | Shin — Insight 기고자 |
| `Lew/` | Lew — Books/ICS 시리즈 기고자 |
| `SPJ/` | ShipPaulJobs 공식 계정 |

---

## 파일명 규칙

```
형식: [Subject]_[AuthorName]_[N].html
예시: E26_4_2_1_Zones_Paul.html
      Jump_Server_CaptainPaul_1.html
      Alarm_Monitoring_System_SPJ_1.html
```

규칙:
- 단어 구분: 언더스코어(`_`) 사용 (공백 금지)
- 저자명: `_Paul` / `_SPJ` / `_BlueHorizonist` / `_Changmin` 등
- 시리즈 번호: `_1`, `_2`, `_3` 필수
- 대소문자: PascalCase 또는 UPPERCASE 일관 적용
- 템플릿 파일: `template_` 접두어 (`tempplate` 오타 사용 금지)

---

## Layout/ 위젯 목록

| 파일 | 용도 |
|------|------|
| `Header/Header.html` | 블로그 상단 헤더 |
| `Header/InjectionCode_Header.html` | 헤더 인젝션 코드 |
| `SideBar/Advertising_Guide.html` | 광고 가이드 위젯 |
| `SideBar/ClassApprovalCheck.html` | 선급 승인 조회 위젯 |
| `SideBar/Compliance_AI_Injection.html` | Compliance AI 위젯 |
| `SideBar/Download.html` | 다운로드 위젯 |
| `SideBar/Free_Maritime_Tools_Suite.html` | 무료 도구 모음 위젯 |
| `SideBar/Maritime_Cyber_Intelligence.html` | 사이버 인텔리전스 위젯 |
| `SideBar/VesselTracking.html` | 선박 추적 위젯 |
| `SideBar/Who_We_Are.html` | 소개 위젯 |
| `SideBar/shipjobsIcon.html` | 아이콘 위젯 |

---

## Pages/ 정적 & 서비스 페이지

### Pages/Menu/ — 메인 메뉴 네비게이션 페이지

Blogger 메인 메뉴에 연결되는 동적 페이지들:

| 파일 | 메뉴 |
|------|------|
| `Completed_Series.html` | Completed Series |
| `Explore_All_Posts.html` | Explore All Posts |
| `Marine_Solutions.html` | Marine Solutions |
| `Maritime_Compliance.html` | Compliance |
| `Maritime_Industry_Insights.html` | Insight |
| `Maritime_Weekly.html` | Maritime Weekly |
| `Publications.html` | Publications |
| `Ship_Systems.html` | Ship Systems |
| `Smart_Maritime_Jobs.html` | Smart Jobs |

### Pages/AppService/ — 앱 서비스 페이지

| 파일 | 설명 |
|------|------|
| `ComplianceBot` 등 | 규정 준수 체크봇 등 인터랙티브 서비스 |

---

## Tools/ 자동화 스크립트

| 파일 | 기능 |
|------|------|
| `add_internal_links.py` | 내부 링크 자동 추가 |
| `add_naver_verification.py` | 네이버 인증 태그 추가 |
| `append_field_notes.py` | Field Notes 추가 |
| `blogger_label_classifier.py` | 레이블 분류기 |
| `fix_alt_blogger.py` | ALT 텍스트 수정 |
| `fix_descriptions.py` | 메타 설명 수정 |
| `move_series_nav.py` | 시리즈 내비게이션 이동 |
| `update_all_posts.py` | 전체 포스트 일괄 업데이트 |
