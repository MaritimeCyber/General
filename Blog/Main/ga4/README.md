# GA4 설정 — 콘텐츠·광고 측정 (속성 p451826577, 측정 ID G-BB27P8MFK7)

## 1. 테마에 적용 (Blogger → 테마 → HTML 편집)
`Blog/Main/Main.html` 에는 이미 반영되어 있습니다. 라이브 테마에는 아래 두 곳만 바꿉니다. **작업 전 테마 백업 필수.**

1. **`<head>` 의 GA 코드 교체**
   `<!-- Google tag (gtag.js) -->` 부터 `gtag('config', 'G-BB27P8MFK7', ...)` 가 있는 `</script>` 까지를
   [`GA4_head_snippet.html`](GA4_head_snippet.html) 내용으로 바꿉니다.
2. **글 저자·라벨 데이터 추가**
   `<b:includable id='postMetadataJSON' var='post'>` 안의 JSON-LD `</script>` 바로 다음 줄에
   [`GA4_post_meta_snippet.html`](GA4_post_meta_snippet.html) 의 `<script class='spj-ga-post' ...>` 한 줄을 넣습니다.

저장 시 오류가 나면 저장하지 말고 오류 메시지를 알려 주세요.

### 이중 집계 방지
- Blogger → 설정 → **Google 애널리틱스 측정 ID** 칸은 **비워 둡니다.** (테마에 직접 넣은 코드만 사용)
- 확인: 블로그를 열고 GA → 보고서 → 실시간에서 `page_view` 가 페이지당 1번만 올라가는지 봅니다.

## 2. 보내는 데이터
### page_view (모든 페이지, 1번)
| 매개변수 | 예 | 비고 |
|---|---|---|
| `page_type` | home / post / page / label / search / archive | |
| `post_author` | Julius Shin | 글·정적 페이지 |
| `post_labels` | IACS UR E26, Cyber Security | 글, 최대 100자 |
| `primary_label` | IACS UR E26 | 글의 첫 라벨 / 라벨 목록 페이지 |
| `publish_month` | 2026-09 | 글 URL 기준 |
| `content_group` | IACS UR E26 | GA4 기본 측정기준 "콘텐츠 그룹" — 등록 불필요 |

### 광고 이벤트 (`Blog/Main/right area/Right_Ad_All.html`)
| 이벤트 | 조건 |
|---|---|
| `spj_ad_view` | 광고 칸 면적 50% 이상이 **1초 이상** 화면에 보임 (IAB 기준, 칸마다 페이지당 1번) |
| `spj_ad_click` | 광고 칸 안 링크 클릭 |

매개변수: `ad_slot`, `ad_size`, `ad_type`(sponsor/placeholder), `ad_name`, `ad_layout`(rail/inline), `page_type`, 클릭 시 `link_type`(banner/advertise/contact), `link_url`.

## 3. GA 관리 화면에서 등록 (한 번만)
**관리 → 데이터 표시 → 맞춤 정의 → 맞춤 측정기준 만들기**, 범위는 모두 **이벤트**.

| 측정기준 이름 | 이벤트 매개변수 |
|---|---|
| Page type | `page_type` |
| Post author | `post_author` |
| Post labels | `post_labels` |
| Primary label | `primary_label` |
| Publish month | `publish_month` |
| Ad slot | `ad_slot` |
| Ad size | `ad_size` |
| Ad type | `ad_type` |
| Ad name | `ad_name` |
| Ad layout | `ad_layout` |
| Ad link type | `link_type` |

- 등록 **이후** 수집된 데이터부터 보고서에 나타납니다 (24~48시간 소요).
- **관리 → 데이터 표시 → 이벤트**에서 `spj_ad_click` 을 **주요 이벤트(Key event)** 로 표시하면 획득 보고서에서 광고 클릭 전환을 볼 수 있습니다.

## 4. 보고서 만들기 (탐색 → 자유 형식)
| 보고서 | 측정기준(행) | 측정항목 | 필터 |
|---|---|---|---|
| 주제별 성과 | 콘텐츠 그룹 | 조회수, 활성 사용자, 평균 참여 시간 | page_type = post |
| 저자별 성과 | Post author | 조회수, 사용자, 참여율 | page_type = post |
| 국가 × 주제 | 국가, 콘텐츠 그룹 | 활성 사용자 | |
| 발행월별 글 성과 | Publish month | 조회수, 사용자 | (7월 대량 발행 글 효과 확인) |
| **광고 칸 리포트 (광고주용)** | Ad slot, Ad name, 이벤트 이름 | 이벤트 수 | 이벤트 이름 = spj_ad_view 또는 spj_ad_click |

광고 칸 리포트에서 **클릭률(CTR) = spj_ad_click ÷ spj_ad_view** 입니다. 주간 리포트로 광고주에게 제공하면 됩니다.
