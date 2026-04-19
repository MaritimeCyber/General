# Blog — Maritime 4.0 Blog Assets

This directory contains HTML widgets, gadgets, and article templates used in the
[Maritime 4.0: Innovation Driven by AI, Data, and Cyber Security](https://shippauljobs.blogspot.com/) blog.

## Structure

```
Blog/
├── Backend/                                                # Live widgets hosted on GitHub
│   ├── Hello_GuestInfo.html                               # Hello Guest widget (main logic)
│   ├── InjectionCode_Hello.html                           # Blogger gadget: fetches & injects Hello Guest
│   ├── ShipOrderTrends.html                               # [Live Feed] Ship order news (RSS aggregator)
│   ├── MaritimeCyberNews.html                             # [Live Feed] Maritime cyber threat intel
│   ├── InjectionCode_MaritimeCyberIntelligence.html       # Blogger gadget: injects MaritimeCyberNews
│   └── MaritimeJobsFeed.html                              # [Live Feed] Maritime AI/Data/Cyber jobs feed
├── Main/                                                   # Blog theme & layout widgets
│   ├── Main.html                                          # Full Blogger theme XML backup (live theme)
│   ├── theme-8002758868633250458.xml                      # Theme backup file
│   ├── Top/
│   │   ├── Header.html                                    # Blog header widget
│   │   └── InjectionCode_Header.html                      # Blogger gadget: fetches & injects Header
│   └── SideBar/
│       ├── Find Us on GitHub.html                         # GitHub repository link widget
│       ├── Maritime Cyber ​​Intelligence.html              # Blog intro widget
│       ├── Who We Are.html                                # Team introduction widget
│       ├── shipjobsIcon.html                              # Blog icon/logo widget
│       ├── InjectionCode_Temp.html                        # Generic injection code template
│       └── tempplate_Who_am_I.html                        # Author intro article template
└── POST/                                                   # Blog article templates by category
    ├── Books/
    │   ├── tempplate_lew1.html
    │   ├── tempplate_lew2.html
    │   └── tempplate_lew3.html
    ├── Compliances/
    │   ├── CPMPLIANCE_lew.html
    │   └── README.md
    ├── Crew/
    │   └── theCrew.html
    ├── InsightTrend/
    │   ├── tempplate_Blue Horizonist.html
    │   ├── tempplate_Ethan_Insight.html
    │   ├── tempplate_Ethan_Life_story,.html
    │   └── tempplate_Yeon_1.html
    ├── Paper/
    │   ├── review/
    │   │   └── PAPER tempplate_insung1.html
    │   └── README.md
    └── RND/
        └── tempplate_Ethan_RnD.html
```

## Widget Architecture

### Backend Widgets (`Backend/`)

Backend widgets follow a two-file pattern:

| File | Role |
|------|------|
| `*.html` (e.g. `Hello_GuestInfo.html`) | Full widget logic — HTML + CSS + JS. Hosted as a raw GitHub file. |
| `InjectionCode_*.html` | Blogger gadget pasted into Layout. Fetches the raw file via `fetch()` and injects it into the DOM, re-executing `<script>` tags manually (required because `innerHTML` blocks script execution). |

#### Live Feed Widgets

| Widget | Service URL | Theme |
|--------|-------------|-------|
| **ShipOrderTrends** | [Ship Order Trends](https://www.shippauljobs.com/2026/04/ship-order-trends-provided-by-shipjobs.html) | Teal `#1a9e82` |
| **MaritimeCyberNews** | [Maritime Cyber Threat Intel](https://www.shippauljobs.com/2026/04/live-feed-maritime-cyber-threat-intel.html) | Red `#ef4444` |
| **MaritimeJobsFeed** | [Maritime Jobs Feed](https://www.shippauljobs.com/2026/04/live-feed-maritime-jobs-feed-ai-data.html) | Amber `#f59e0b` |

All Live Feed widgets share the same architecture:
- RSS aggregation via `rss2json` ∥ `allorigins` parallel race pattern
- 30-minute `localStorage` cache
- Period filter (1W / 1M / 3M / 6M / All) — default **6M**
- Category tabs with keyword-based filtering
- shipjobs2.png logo + `<h1>` title flex layout in gradient header

#### Other Backend Widgets

**Hello_GuestInfo** (`Backend/Hello_GuestInfo.html`)
- Greets visitors in their native language (19 languages supported)
- Displays IP geo-info: country flag, ISP, local time, currency, dial code, network type
- Shows device info (OS, browser, resolution) and referrer source
- Renders a full OSI 7-layer / PDU stack view using client-side detection
- Uses `ipapi.co` API with 30-minute `localStorage` cache

### Blog Theme & Layout Widgets (`Main/`)

| File | Description |
|------|-------------|
| `Main.html` | Full Blogger theme XML backup — the current live theme for shippauljobs.blogspot.com |
| `theme-8002758868633250458.xml` | Alternative theme backup format |
| `Top/Header.html` | Blog header widget |
| `SideBar/*.html` | Sidebar widgets (GitHub link, team intro, logo icon, Maritime Cyber Intelligence) |

### Article Templates (`POST/`)

Templates follow the **Maritime 4.0 Design System** — full inline styles only (no `<style>` block; Blogger strips CSS blocks).

| Directory | Description |
|-----------|-------------|
| `Books/` | Book review templates by Lew (lew1–lew3) |
| `Compliances/` | Cyber compliance article templates |
| `Crew/` | Team introduction article |
| `InsightTrend/` | Insight & trend analysis (Ethan, Yeon, Blue Horizonist) |
| `Paper/` | Research paper summary templates |
| `RND/` | R&D / applied research articles (Edge AI, Jetson Nano, etc.) |

**Two style variants:**
- 💡 **Insight** → `POST/InsightTrend/tempplate_Ethan_Insight.html`
- 🔬 **R&D** → `POST/RND/tempplate_Ethan_RnD.html`

## Usage

### Backend widgets (`Backend/`)
1. The `InjectionCode_*.html` gadget is pasted into Blogger → **Layout → Add a Gadget → HTML/JavaScript**.
2. It fetches the corresponding `*.html` from the GitHub raw URL at runtime.
3. No manual copy-paste needed for the main widget file — push to GitHub and it updates live.

### Layout / Sidebar widgets (`Main/`)
1. Open the target `.html` file.
2. Copy the full content.
3. In Blogger, navigate to **Layout → Add a Gadget → HTML/JavaScript**.
4. Paste and save.

### Article templates (`POST/`)
1. Open the template `.html` file.
2. Copy the content and paste into the Blogger post editor in **HTML view**.
3. Fill in the article-specific fields and publish.

> Back to [Repository Root](../README.md)
