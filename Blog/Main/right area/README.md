# Right area — 오른쪽 광고 열 (통합 가젯 1개)

2026-10-09부터 오른쪽 광고 열은 **가젯 1개(`Right_Ad_All.html`)**로 운영합니다.
Blogger 레이아웃의 사이드바(하단) 맨 위 HTML/JavaScript 가젯 **HTML2**가 이 파일입니다.

## 광고 관리 = `SLOTS` 목록만 수정
레이아웃 → HTML2 가젯 편집 → `SLOTS` 안에서 해당 칸만 고치고 저장합니다.

| 항목 | 의미 |
|---|---|
| `order` | 칸 순서 (1 = 맨 위) |
| `show` | `false` 면 그 칸을 아예 표시 안 함 (예전의 "위젯 표시 안 함"과 같음) |
| `start` / `end` | `"YYYY-MM-DD"` (한국 시간). 기간 밖이면 자동으로 숨김. 비워 두면 제한 없음 |
| `size` / `ratio` | `"300 × 250"` + `"6 / 5"`, `"300 × 500"` + `"3 / 5"` |
| `mobile` | 좁은 화면 위치: `"top"` / `"middle"` / `"end"` / `false`(숨김) |
| `sponsors` | 비우면 "Advertise here" 칸, 채우면 배너 (여러 개면 무작위 순환) |

```js
{ order: 1, show: true, start: "2026-10-01", end: "2026-10-28",
  size: "300 × 250", ratio: "6 / 5", mobile: "top",
  sponsors: [
    { name: "Company Name", image: "https://.../banner-300x250.png",
      url: "https://www.company.com/?utm_source=shippauljobs&utm_medium=right_300x250",
      alt: "Company Name - maritime cyber security solutions" }
  ] },
```
- 6번째 칸이 필요하면 블록 하나를 복사해 `order: 6`으로 추가합니다.
- **가젯 코드에는 영어(ASCII)만** 사용합니다. Blogger가 한글·특수문자를 `&#…;`로 바꿔 저장합니다 (`×`, `·`는 `×`, `·`로 표기).
- 저장 전 실수하면 5개 칸이 모두 안 보일 수 있으니, 저장 후 블로그를 새로고침해 확인합니다.

## 동작
- 넓은 화면: 본문 오른쪽 빈 공간에 180~252px 폭으로 표시되고 본문과 함께 스크롤됩니다.
- 좁은 화면: 각 칸의 `mobile` 값에 따라 본문 블록 사이에 들어갑니다.
- 표시 페이지: `COMMON.showOn` — 기본값은 홈·포스트·정적 페이지·목록 전부.
- "contact us" 링크: `/p/contact.html` (예전 가젯의 `/p/contact-shippauljobs.html`은 404였음).

## 분석 (Google Analytics 4)
테마의 GA4 태그(`gtag.js`, `G-BB27P8MFK7`)로 이벤트를 보냅니다 (통합 가젯부터 실제 적용 — 예전 Blogger 가젯에는 추적 코드가 반영돼 있지 않았음).

| 이벤트 | 언제 |
|---|---|
| `spj_ad_view` | 광고 칸이 화면에 절반 이상 보였을 때 (페이지당 칸마다 1번) |
| `spj_ad_click` | 광고 칸 안의 링크를 클릭했을 때 |

매개변수: `ad_slot`, `ad_size`, `ad_type`(sponsor/placeholder), `ad_name`, `ad_layout`(rail/inline), `page_type`, 클릭 시 `link_type`, `link_url`.
GA4 보고서에서 보려면 **관리 → 맞춤 정의 → 맞춤 측정기준**에 위 매개변수를 이벤트 범위로 등록하세요.

## 예전 가젯 (legacy/)
`legacy/Right_Ad_1~5` 는 칸마다 따로 쓰던 이전 방식입니다. Blogger 레이아웃에는 HTML3·HTML1·HTML5·HTML6·HTML7로 **숨김 상태로 남아 있으며**, 문제가 생기면 다시 "이 위젯 표시"를 켜고 HTML2를 숨기면 즉시 되돌릴 수 있습니다. 통합 가젯이 안정적으로 확인되면 레이아웃에서 삭제해도 됩니다.
