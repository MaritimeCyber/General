# Right area — 오른쪽 광고 열 (5개 가젯)

화면 오른쪽 광고 열을 칸마다 독립된 Blogger HTML/JavaScript 가젯으로 나눈 파일입니다.

| 파일 | 칸 | 크기 | 좁은 화면(모바일) `mobile` |
|---|---|---|---|
| `Right_Ad_1_300x250.html` | 1 (위) | 300 × 250 | `"top"` — 첫 블록 뒤 |
| `Right_Ad_2_300x500.html` | 2 | 300 × 500 | `"middle"` — 가운데 |
| `Right_Ad_3_300x250.html` | 3 | 300 × 250 | `"end"` — 마지막 블록 뒤 |
| `Right_Ad_4_300x250.html` | 4 | 300 × 250 | `false` — 숨김 |
| `Right_Ad_5_300x500.html` | 5 (아래) | 300 × 500 | `false` — 숨김 |

## 동작
- 다섯 가젯이 하나의 오른쪽 열을 함께 씁니다. 먼저 실행된 가젯이 열을 만들고, 각 가젯은 자기 칸만 넣습니다.
- 레이아웃에서 가젯 순서·위치와 상관없이 항상 1 → 2 → 3 → 4 → 5 순서로 쌓입니다.
- 일부 가젯만 설치해도 동작합니다 (예: 2번만 설치하면 300 × 500 한 칸만 표시).
- 넓은 화면: 본문 오른쪽 빈 공간에 180~252px 폭으로 표시되고 본문과 함께 스크롤됩니다.
- 좁은 화면: 각 칸의 `mobile` 값에 따라 본문 블록(글 목록의 각 글 / 위젯) 사이에 따로 들어갑니다 — `"top"`(첫 블록 뒤, 1번), `"middle"`(가운데, 2번), `"end"`(마지막 블록 뒤, 3번), `false`(숨김).
- 표시 페이지: `COMMON.showOn` — 기본값은 홈·포스트·정적 페이지·목록 전부.

## 설치
1. Blogger → 레이아웃 → 아무 영역 → **+ 가젯 추가** → **HTML/JavaScript**
2. 제목은 비우고 파일 하나의 내용 전체를 붙여 넣고 저장 → 다섯 파일 각각 반복
3. 기존 `Right_Banner` 가젯(세 칸이 한 가젯에 들어 있던 이전 버전)은 **삭제** — 함께 두면 광고 열이 두 개 생깁니다.

## 배너 등록
각 파일의 `SLOT.sponsors` 에 넣습니다. 비워 두면 "Advertise here" 광고 자리가 표시됩니다.

```js
sponsors: [
  { name: "Company Name", image: "https://.../banner-300x500.png",
    url: "https://www.company.com/?utm_source=shippauljobs&utm_medium=right_300x500_a",
    alt: "Company Name - maritime cyber security solutions" }
]
```

## 분석 (Google Analytics 4)
테마에 이미 설치된 GA4 태그(`gtag.js`, `G-BB27P8MFK7`)로 광고 노출·클릭 이벤트를 보냅니다. `gtag` 가 없으면 GTM `dataLayer` 로 보냅니다.

| 이벤트 | 언제 |
|---|---|
| `spj_ad_view` | 광고 칸이 화면에 절반 이상 보였을 때 (페이지당 칸마다 1번) |
| `spj_ad_click` | 광고 칸 안의 링크를 클릭했을 때 (가운데 버튼 클릭 포함) |

| 매개변수 | 값 |
|---|---|
| `ad_slot` | 칸 번호 1~5 |
| `ad_size` | `300x250`, `300x500` |
| `ad_type` | `sponsor`(배너) / `placeholder`("Advertise here") |
| `ad_name` | 배너의 `name` → `alt` → 이미지 파일명, 빈 칸은 `(advertise here)` |
| `ad_layout` | `rail`(넓은 화면 오른쪽 열) / `inline`(좁은 화면, 본문 사이) |
| `page_type` | `home` / `post` / `page` / `list` |
| `link_type` | 클릭만: `banner` / `advertise` / `contact` |
| `link_url` | 클릭만: 이동한 주소 |

GA4 보고서에서 매개변수별로 보려면 **관리 → 데이터 표시 → 맞춤 정의 → 맞춤 측정기준 만들기**에서 위 매개변수 이름을 이벤트 범위로 하나씩 등록하세요 (등록 후부터 수집, 반영까지 최대 24~48시간). 실시간 확인은 **보고서 → 실시간** 또는 **관리 → DebugView**.

## 유지보수
- 가젯 코드에는 영어(ASCII)만 사용합니다. Blogger 가 한글·특수문자를 `&#…;` 로 바꿔 저장하기 때문입니다.
- 다섯 파일의 공통 코드(`Shared right-column core`)는 동일해야 합니다. 공통 부분을 고칠 때는 다섯 파일 모두 같이 수정하세요.
